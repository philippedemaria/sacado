from django.shortcuts import render, redirect
from account.models import  Student, Teacher, User,Resultknowledge, Resultskill, Resultlastskill
from account.forms import StudentForm, TeacherForm, UserForm
from django.contrib.auth.forms import  AuthenticationForm
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import  permission_required,user_passes_test
from sendmail.forms import  EmailForm
from group.forms import GroupForm 
from group.models import Group , Sharing_group
from school.models import Stage
from qcm.models import  Parcours , Studentanswer, Exercise, Relationship,Resultexercise, Resultggbskill, Supportfile,Remediation, Constraint, Course, Demand, Mastering, Masteringcustom, Masteringcustom_done, Mastering_done, Writtenanswerbystudent , Customexercise, Customanswerbystudent, Comment, Correctionknowledgecustomexercise , Correctionskillcustomexercise , Remediationcustom, Annotation, Customannotation
from qcm.forms import ParcoursForm , ExerciseForm, RemediationForm, UpdateParcoursForm , UpdateSupportfileForm, SupportfileKForm, RelationshipForm, SupportfileForm, AttachForm ,   CustomexerciseNPForm, CustomexerciseForm ,CourseForm , DemandForm , CommentForm, MasteringForm, MasteringcustomForm , MasteringDoneForm , MasteringcustomDoneForm, WrittenanswerbystudentForm,CustomanswerbystudentForm , WAnswerAudioForm, CustomAnswerAudioForm , RemediationcustomForm
from socle.models import  Theme, Knowledge , Level , Skill
from django.http import JsonResponse 
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import uuid
import time
import math
import json
import random
from datetime import datetime , timedelta
from django.db.models import Q
from django.core.mail import send_mail

from group.decorators import user_is_group_teacher 
from qcm.decorators import user_is_parcours_teacher, user_can_modify_this_course, student_can_show_this_course , user_is_relationship_teacher, user_is_customexercice_teacher 
from account.decorators import user_can_create, user_is_superuser
##############bibliothèques pour les impressions pdf  #########################
import os
from django.utils import formats, timezone
from io import BytesIO, StringIO
from django.http import  HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape , letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image , PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import yellow, red, black, white, blue
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT
from cgi import escape
cm = 2.54
import os
import re
import pytz
import csv
import html
from general_fonctions import *


def new_content_type(s):
    names = ['Pages', 'Questionnaires', 'Activités', 'Tâches',  'Fichiers', 'Urls externes', 'Discussions' , 'Notes',  'Acquis', 'Participants', 'Suivis' ]                
    slugs = ['page', 'test',  'activity', 'task', 'file', 'url', 'discussion', 'mark', 'acquis', 'user', 'suivi' ]   
    verbose_names = ['Toutes les pages', 'Tous les questionnaires', 'Toutes les activités', 'Toutes les tâches',  'Tous les fichiers', 'Toutes les urls externes', 'Toutes les discussions', 'Notes', 'Acquis', 'Tous les participants', 'Les suivis des activités' ] 

    for i in range(len(names)) :
        verbose_button = verbose_names[i]
        slug = slugs[i]
        name = names[i]
        image = "img/"+slugs[i]+".png"
        Content_type.objects.create(name = name, image = image , slug = slug ,verbose_button = verbose_button, display = 1 ,section = s)


def get_time(s,e):
    start_time = s.split(",")[0]
    end_time = e.split(".")[0]
    full_time = int(end_time) - int(start_time)
    return  full_time




def advises(request):
    teacher = Teacher.objects.get(user_id = request.user.id)
    return render(request, 'advises.html', {'teacher': teacher})


def convert_seconds_in_time(secondes):
    if secondes < 60:
        return "{}s".format(secondes)
    elif secondes < 3600:
        minutes = secondes // 60
        sec = secondes % 60
        if sec < 10:
            sec = f'0{sec}'
        return "{}:{}".format(minutes, sec)
    else:
        hours = secondes // 3600
        minutes = (secondes % 3600) // 60
        sec = (secondes % 3600) % 60
        if sec < 10:
            sec = f'0{sec}'
        if minutes < 10:
            minutes = f'0{minutes}'
        return "{}:{}:{}".format(hours, minutes, sec)


def send_to_teachers(level) : # envoie d'une notification au enseignant du niveau coché lorsqu'un exercice est posté
    rcv = []
    teachers = Teacher.objects.filter(levels=level)
    for t in teachers :
        if t.exercise_post :
            if t.user.email : 
                rcv.append(t.user.email)

    msg = "Un nouvel exercice vient d'être publié sur SacAdo sur le niveau "+str(level)
    try :
        send_mail("Nouvel exercice SacAdo",  msg , "info@sacado.xyz" , rcv)
    except :
        pass



def students_from_p_or_g(request,parcours) :
    """
    Si un groupe est en session, renvoie la liste des élèves du groupe et du parcours
    Sinon les élèves du parcours
    Classés par ordre alphabétique
    """
    try :
        group_id = request.session["group_id"]
        group = Group.objects.get(id = group_id) 
        students_group = group.students.all()
        students_parcours = parcours.students.order_by("user__last_name")
        students = [student for student in students_parcours if student   in students_group] # Intersection des listes
    except :
        students = list(parcours.students.order_by("user__last_name"))
    return students




def get_complement(request, teacher, parcours_or_group):

    data = {}

    try :
        group_id = request.session.get("group_id",None)
        if group_id :
            group = Group.objects.get(pk = group_id)
        else :
            group = None   

        if Sharing_group.objects.filter(group_id= group_id , teacher = teacher).exists() :
            sh_group = Sharing_group.objects.get(group_id=group_id, teacher = teacher)
            role = sh_group.role
            access = True
        else :
            role = False
            access = False
    except :
        group_id = None
        role = False
        group = None
        access = False

    if parcours_or_group.teacher == teacher:
        role = True

    data["group_id"] = group_id
    data["group"] = group
    data["role"] = role
    data["access"] = access

    return data



def get_stage(user):

    try :
        if user.school :
            school = user.school
            stage = Stage.objects.get(school = school)
        else : 
            stage = { "low" : 50 ,  "medium" : 70 ,  "up" : 85  }
    except :
        stage = { "low" : 50 ,  "medium" : 70 ,  "up" : 85  }  
    return stage


#######################################################################################################################################################################
#######################################################################################################################################################################
#################   parcours par defaut
#######################################################################################################################################################################
#######################################################################################################################################################################
def associate_parcours(request,id):
    teacher = Teacher.objects.get(user_id = request.user.id)
    group = Group.objects.get(pk = id)
    theme_theme_ids = request.POST.getlist("themes")
    for theme_id in theme_theme_ids :
        theme = Theme.objects.get(pk = int(theme_id))
        parcours, created = Parcours.objects.get_or_create(title=theme.name, color=group.color, author=teacher, teacher=teacher, level=group.level,  is_favorite = 1,  is_share = 0, linked = 1)
        exercises = Exercise.objects.filter(level= group.level,theme = theme, supportfile__is_title=0)
        parcours.students.set(group.students.all())
        i  = 0
        for e in exercises:
            relationship, created = Relationship.objects.get_or_create(parcours = parcours, exercise=e, order = i)
            relationship.students.set(group.students.all())
            if created :
                relationship.skills.set(e.supportfile.skills.all()) 
            i+=1

    if len(parcours.students.all())>0 :
        return redirect("list_parcours_group" , group.id )
    else :
        return redirect("index") 




@csrf_exempt
def ajax_parcours_default(request):
    data = {}
    level_id =  request.POST.get("level_selected_id")    
    level =  Level.objects.get(pk = level_id)
    context = {  'level': level,   }
    data['html'] = render_to_string('qcm/parcours_default_popup.html', context)
 
    return JsonResponse(data)

 

def get_parcours_default(request):
    teacher = Teacher.objects.get(user_id = request.user.id)
    level_id = request.POST.get("level_selected_id")
    theme_ids = request.POST.getlist("themes")
    n = 0
    for theme_id in theme_ids :
        theme = Theme.objects.get(pk = int(theme_id))
        parcours, created = Parcours.objects.get_or_create(title=theme.name, color="#5d4391", author=teacher, teacher=teacher, level_id=level_id,  is_favorite = 1,  is_share = 0, linked = 0)
        exercises = Exercise.objects.filter(level_id=level_id,theme = theme, supportfile__is_title=0)
        i  = 0
        for e in exercises:
            relationship, created = Relationship.objects.get_or_create(parcours = parcours, exercise=e, order = i)
            if created :
                relationship.skills.set(e.supportfile.skills.all()) 
            i+=1
        n +=1
    if n > 1 :
        messages.info(request, "Les parcours sont créés avec succès. Penser à leur attribuer des élèves et les à publier.")
    else :
        messages.info(request, "Le parcours est créé avec succès. Penser à lui attribuer des élèves et le à publier.")
    return redirect("index") 

#######################################################################################################################################################################
#######################################################################################################################################################################
#################   parcours
#######################################################################################################################################################################
#######################################################################################################################################################################

@csrf_exempt
def ajax_chargethemes(request):
    ids_level =  request.POST.get("id_level")
    id_subject =  request.POST.get("id_subject")

    data = {}
    level =  Level.objects.get(pk = ids_level)

    thms = level.themes.values_list('id', 'name').filter(subject_id=id_subject)
    data['themes'] = list(thms)
 
    return JsonResponse(data)


@csrf_exempt  # PublieDépublie un exercice depuis organize_parcours
def ajax_populate(request):  

    exercise_id = int(request.POST.get("exercise_id"))
    parcours_id = int(request.POST.get("parcours_id"))
    parcours = Parcours.objects.get(pk = parcours_id)
    exercise = Exercise.objects.get(pk = exercise_id)
    statut = request.POST.get("statut") 
    data = {}    

    teacher = Teacher.objects.get(user= request.user)    

    if parcours.teacher == teacher :
        if statut=="true" or statut == "True":

            r = Relationship.objects.get(parcours=parcours, exercise = exercise)  
            students = parcours.students.all()
            for student in students :
                r.students.remove(student)

            r.delete()         
            statut = 0
            data["statut"] = "False"
            data["class"] = "btn btn-danger"
            data["noclass"] = "btn btn-success"
            data["html"] = "<i class='fa fa-times'></i>"
            data["no_store"] = False

        else:
            statut = 1
            if Relationship.objects.filter(parcours_id=parcours_id , exercise__supportfile = exercise.supportfile ).count() == 0 :
                relation = Relationship.objects.create(parcours_id=parcours_id, exercise_id = exercise_id, order = 100, situation = exercise.supportfile.situation , duration = exercise.supportfile.duration) 
                relation.skills.set(exercise.supportfile.skills.all())
                students = parcours.students.all()
                relation.students.set(students)
                data["statut"] = "True"
                data["class"] = "btn btn-success"
                data["noclass"] = "btn btn-danger"
                data["html"] = "<i class='fa fa-check-circle fa-2x'></i>"
                data["no_store"] = False
            else :
                data["statut"] = "False"
                data["class"] = "btn btn-danger"
                data["noclass"] = "btn btn-success"
                data["html"] = "<i class='fa fa-times'></i>"
                data["no_store"] = True

    return JsonResponse(data) 





#@user_is_parcours_teacher
def peuplate_parcours(request,id):
    teacher = Teacher.objects.get(user_id = request.user.id)
    levels =  teacher.levels.all() 
    parcours = Parcours.objects.get(id=id)

    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id']
    access = data['access']

    if not authorizing_access(teacher,parcours, access ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    form = UpdateParcoursForm(request.POST or None , instance=parcours, teacher = teacher  )
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("order")
    """ affiche le parcours existant avant la modif en ajax""" 
    exercises = parcours.exercises.filter(supportfile__is_title=0).order_by("theme")
    """ fin """
    themes_tab = []
    for level in levels :
        for theme in level.themes.all():
            if not theme in themes_tab:
                themes_tab.append(theme)
    
    if request.method == 'POST' :
        level = request.POST.get("level") 
        # modifie les exercices sélectionnés
        exercises_all = parcours.exercises.filter(supportfile__is_title=0,level=level)
        exercises_posted_ids = request.POST.getlist('exercises')

        new_list = []
        for e_id in exercises_posted_ids :
            try : 
                exercise  = Exercise.objects.get(id=e_id)
                new_list.append(exercise)
            except :
                pass


        intersection_list = [value for value in exercises_all if value not in new_list]

        for exercise in intersection_list :
            try :
                rel = Relationship.objects.get(parcours = parcours , exercise = exercise).delete() # efface les existants sur le niveau sélectionné
            except :
                pass
        i = 0 # réattribue les exercices choisis

        for exercise in exercises_posted_ids :
            try :
                if Relationship.objects.filter(parcours = nf , exercise__supportfile = exercise.supportfile ).count() == 0 :
                    r = Relationship.objects.create(parcours = nf , exercise = exercise , order =  i, situation = exercise.supportfile.situation , duration = exercise.supportfile.duration )  
                    r.skills.set(exercise.supportfile.skills.all()) 
                    i+=1
                else :
                    pass
            except :
                pass


        # fin ---- modifie les exercices sélectionnés
    context = {'form': form, 'parcours': parcours, 'communications':[], 'group' : group , 'role' : role , 'teacher': teacher, 'exercises': exercises , 'levels': levels , 'themes' : themes_tab , 'user': request.user , 'group_id' : group_id , 'relationships' :relationships  }

    return render(request, 'qcm/form_peuplate_parcours.html', context)


 
def peuplate_parcours_evaluation(request,id):
    teacher = Teacher.objects.get(user_id = request.user.id)
    levels =  teacher.levels.all() 
 
    parcours = Parcours.objects.get(id=id)


    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id']
    access = data['access']

    if not authorizing_access(teacher,parcours, access ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')



    form = UpdateParcoursForm(request.POST or None , instance=parcours, teacher = teacher  )
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("order")
    """ affiche le parcours existant avant la modif en ajax""" 
    exercises = parcours.exercises.filter(supportfile__is_title=0).order_by("theme")
    """ fin """
    themes_tab = []
    for level in levels :
        for theme in level.themes.all():
            if not theme in themes_tab:
                themes_tab.append(theme)
    
    if request.method == 'POST' :
        level = request.POST.get("level") 
        # modifie les exercices sélectionnés
        exercises_all = parcours.exercises.filter(supportfile__is_title=0,level=level)
        exercises_posted_ids = request.POST.getlist('exercises')

        new_list = []
        for e_id in exercises_posted_ids :
            try : 
                exercise  = Exercise.objects.get(id=e_id)
                new_list.append(exercise)
            except :
                pass


        intersection_list = [value for value in exercises_all if value not in new_list]

        for exercise in intersection_list :
            try :
                rel = Relationship.objects.get(parcours = parcours , exercise = exercise).delete() # efface les existants sur le niveau sélectionné
            except :
                pass
        i = 0 # réattribue les exercices choisis

        for exercise in exercises_posted_ids :
            try :
                if Relationship.objects.filter(parcours = nf , exercise__supportfile = exercise.supportfile ).count() == 0 :
                    r = Relationship.objects.create(parcours = nf , exercise = exercise , order =  i, situation = exercise.supportfile.situation , duration = exercise.supportfile.duration )  
                    r.skills.set(exercise.supportfile.skills.all()) 
                    i+=1
                else :
                    pass
            except :
                pass
 

 

        # fin ---- modifie les exercices sélectionnés
    context = {'form': form, 'parcours': parcours, 'communications':[], 'group' : group , 'role' : role , 'teacher': teacher, 'exercises': exercises , 'levels': levels , 'themes' : themes_tab , 'user': request.user , 'group_id' : group_id , 'relationships' :relationships  }

    return render(request, 'qcm/form_peuplate_parcours.html', context)





#@user_is_parcours_teacher
def individualise_parcours(request,id):
    teacher = Teacher.objects.get(user_id = request.user.id)
    parcours = Parcours.objects.get(pk = id)
    relationships = Relationship.objects.filter(parcours = parcours).order_by("order")
    students = parcours.students.all().order_by("user__last_name")

    customexercises = Customexercise.objects.filter(parcourses = parcours).order_by("ranking")  

    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id']
    access = data['access']

    if not authorizing_access(teacher,parcours, access ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')
 

    context = {'relationships': relationships, 'parcours': parcours,     'communications':[],     'students': students,  'form': None,  
                    'teacher': teacher, 'customexercises' : customexercises ,
                  'exercises': None , 
                  'levels': None , 
                  'themes' : None ,
                   'user': request.user , 
                   'group_id' : group_id , 'group' : group , 'role' : role }

    return render(request, 'qcm/form_individualise_parcours.html', context )





@csrf_exempt # PublieDépublie un exercice depuis organize_parcours
def ajax_individualise(request):  

    exercise_id = int(request.POST.get("exercise_id"))
    parcours_id = int(request.POST.get("parcours_id"))
    student_id = int(request.POST.get("student_id"))
    data = {}
    teacher = Teacher.objects.get(user= request.user)
    parcours = Parcours.objects.get(pk = parcours_id)
    statut = request.POST.get("statut") 

    if not authorizing_access(teacher,parcours , True ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    custom = int(request.POST.get("custom") )

    if custom :
        customexercise = Customexercise.objects.get(pk = exercise_id )

        if student_id == 0 : 
             
            if statut=="true" or statut == "True" :
                try :
                    som = 0
                    for s in parcours.students.all() :
                        if Customanswerbystudent.objects.filter(student = s , customexercise = customexercise).count() == 0 :
                            customexercise.students.remove(s)
                            som +=1
                except :
                    pass

                statut = 0
                data["statut"] = "False"
                data["class"] = "btn btn-danger"
                data["noclass"] = "btn btn-success"
                if som == 0 :
                    data["alert"] = True
                else :
                    data["alert"] = False 
            else : 
                try :
                    customexercise.students.set(parcours.students.all())
                except :
                    pass
                statut = 1    
                data["statut"] = "True"
                data["class"] = "btn btn-success"
                data["noclass"] = "btn btn-danger"
                data["alert"] = False   
        else :
            student = Student.objects.get(pk = student_id) 
            if statut=="true" or statut == "True":
                try :
                    if Customanswerbystudent.objects.filter(student = student , customexercise = customexercise).count() == 0 :
                        customexercise.students.remove(student)
                        data["alert"] = False
                    else :
                        data["alert"] = True                        
                except :
                    pass
                statut = 0
                data["statut"] = "False"
                data["class"] = "btn btn-danger"
                data["noclass"] = "btn btn-success" 
            else:
                statut = 1
                try :
                    customexercise.students.add(student) 
                except :
                    pass
                data["statut"] = "True"
                data["class"] = "btn btn-success"
                data["noclass"] = "btn btn-danger"
                data["alert"] = False   
    else :

        exercise = Exercise.objects.get(pk = exercise_id)
        relationship = Relationship.objects.get(parcours=parcours,exercise=exercise) 

        if student_id == 0 :  
            if statut=="true" or statut == "True" :
                somme = 0
                try :
                    for s in parcours.students.all() :
                        if Studentanswer.objects.filter(student = s , exercise = exercise, parcours = relationship.parcours).count() == 0 :
                            relationship.students.remove(s)
                            somme +=1
                except :
                    pass
                statut = 0
                data["statut"] = "False"
                data["class"] = "btn btn-danger"
                data["noclass"] = "btn btn-success"
                if somme == 0 :
                    data["alert"] = True
                else :
                    data["alert"] = False

            else : 
                relationship.students.set(parcours.students.all())
                statut = 1    
                data["statut"] = "True"
                data["class"] = "btn btn-success"
                data["noclass"] = "btn btn-danger"
                data["alert"] = False
        else :
            student = Student.objects.get(pk = student_id)  

            if statut=="true" or statut == "True":

                if Studentanswer.objects.filter(student = student , exercise = exercise, parcours = relationship.parcours).count() == 0 :
                    relationship.students.remove(student)
                    statut = 0
                    data["statut"] = "False"
                    data["class"] = "btn btn-danger"
                    data["noclass"] = "btn btn-success"
                    data["alert"] = False
                else :
                    data["statut"] = "True"
                    data["class"] = "btn btn-success"
                    data["noclass"] = "btn btn-danger"
                    data["alert"] = True
            else:
                statut = 1
                relationship.students.add(student) 
                data["statut"] = "True"
                data["class"] = "btn btn-success"
                data["noclass"] = "btn btn-danger"
                data["alert"] = False

    return JsonResponse(data) 



def list_parcours(request):

    teacher = Teacher.objects.get(user_id = request.user.id)
    today = time_zone_user(teacher.user)
    parcourses = Parcours.objects.filter(teacher = teacher,is_evaluation=0,is_archive=0).order_by("-is_favorite")  
    nb_archive =  Parcours.objects.filter(teacher = teacher,is_evaluation=0,is_archive=1).count()  
    try :
        del request.session["group_id"]
    except:
        pass  

    return render(request, 'qcm/list_parcours.html', { 'parcourses' : parcourses , 'communications' : [] , 'relationships' : [],  'parcours' : None , 'group' : None , 'today' : today ,  'teacher' : teacher , 'nb_archive' : nb_archive })



def list_archives(request):

    teacher = Teacher.objects.get(user_id = request.user.id)
    parcourses = Parcours.objects.filter(teacher = teacher,is_evaluation=0,is_archive=1).order_by("level")  
    today = time_zone_user(teacher.user)
    try :
        del request.session["group_id"]
    except:
        pass   

    return render(request, 'qcm/list_archives.html', { 'parcourses' : parcourses , 'parcours' : None , 'teacher' : teacher ,  'communications' : [] , 'relationships' : [], 'today' : today , })




def list_evaluations(request):
    teacher = Teacher.objects.get(user_id = request.user.id)
    today = time_zone_user(teacher.user)
    parcourses = Parcours.objects.filter(teacher = teacher,is_evaluation=1,is_archive=0).order_by("-is_favorite")     
    nb_archive = Parcours.objects.filter(teacher = teacher,is_evaluation=1,is_archive=1).count()  
    try :
        del request.session["group_id"]
    except:
        pass  

    return render(request, 'qcm/list_evaluations.html', { 'parcourses' : parcourses, 'parcours' : None ,  'teacher' : teacher ,  'communications' : [] , 'relationships' : []   ,  'today' : today , 'nb_archive' : nb_archive })




def list_evaluations_archives(request):
    teacher = Teacher.objects.get(user_id = request.user.id)
    parcourses = Parcours.objects.filter(teacher = teacher,is_evaluation=1,is_archive=1).order_by("level")    
    today = time_zone_user(teacher.user)
    try :
        del request.session["group_id"]
    except:
        pass  

    return render(request, 'qcm/list_evaluations_archives.html', { 'parcourses' : parcourses, 'parcours' : None , 'teacher' : teacher , 'communications' : [] ,  'today' : today , 'relationships' : []   })




##@user_is_group_teacher
def list_parcours_group(request,id):

    teacher = Teacher.objects.get(user_id = request.user.id)
    today = time_zone_user(teacher.user)
    group = Group.objects.get(pk = id) 

    request.session["group_id"] = group.id

    try :
        sharing_group = Sharing_group.objects.get(group = group, teacher=teacher)
        sharing = True
    except :
        sharing = False


    if not authorizing_access(teacher,group, sharing ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')


    group_tab = []
    data = {}
    parcours_tab = []
    students = group.students.all()

    for student in students :
        if sharing :
            pcs = Parcours.objects.filter(students= student, is_favorite=1).order_by("is_evaluation", "ranking")
        else :
            pcs = Parcours.objects.filter(Q(teacher=teacher)|Q(author=teacher), students= student, is_favorite=1).order_by("is_evaluation", "ranking")
        if len(parcours_tab) == teacher.teacher_parcours.count() :
            break  
        else :    
            for parcours in pcs : 
                if parcours not in parcours_tab :
                    parcours_tab.append(parcours)
                if len(parcours_tab) == teacher.teacher_parcours.count() :
                    break 
    return render(request, 'qcm/list_parcours_group.html', {'parcours_tab': parcours_tab , 'group': group,  'parcours' : None , 'communications' : [] , 'relationships' : [] , 'role' : role , 'today' : today })



def all_parcourses(request):
    teacher = Teacher.objects.get(user_id = request.user.id)
    parcourses = Parcours.objects.exclude(exercises=None ).exclude(teacher=teacher).exclude(teacher__user__school= None).order_by("author").prefetch_related('exercises__knowledge__theme').select_related('author')

    if request.user.school != None :
        inside = True
    else :
        inside = False

    return render(request, 'qcm/all_parcourses.html', {'parcourses': parcourses , 'inside' : inside , 'communications' : [] , 'parcours' : None , 'relationships' : []})



 
def create_parcours(request):

    teacher = Teacher.objects.get(user = request.user)
    levels =  teacher.levels.all()    
    form = ParcoursForm(request.POST or None, request.FILES or None, teacher = teacher)
 
    themes_tab = []
    for level in levels :
        for theme in level.themes.all():
            if not theme in themes_tab:
                themes_tab.append(theme)


    groups = Group.objects.filter(teacher=teacher).prefetch_related('students').order_by("level")
    share_groups = Sharing_group.objects.filter(teacher  = teacher,role=1).order_by("group__level")

    if len(share_groups)>0 :
        sharing = True
    else :
        sharing = False


    if form.is_valid():
        nf = form.save(commit=False)
        nf.author = teacher
        nf.teacher = teacher
        nf.is_evaluation = 0 
        nf.save()
        nf.students.set(form.cleaned_data.get('students'))

        sg_students =  request.POST.getlist('students_sg')

        for s_id in sg_students :
            student = Student.objects.get(user_id = s_id)
            nf.students.add(s)


        i = 0
        for exercise in form.cleaned_data.get('exercises'):
            exercise = Exercise.objects.get(pk=exercise.id)
            relationship = Relationship.objects.create(parcours=nf, exercise=exercise, order=i,
                                                       duration=exercise.supportfile.duration,
                                                       situation=exercise.supportfile.situation)
            relationship.students.set(form.cleaned_data.get('students'))
            relationship.skills.set(exercise.supportfile.skills.all()) 
            i += 1

        if request.POST.get("save_and_choose") :
            return redirect('peuplate_parcours', nf.id)
        else:
            return redirect('parcours')
    else:
        print(form.errors)



    try :
        if 'group_id' in request.session :
            if request.session.get["group_id"] :
                group_id = request.session["group_id"]
                group = Group.objects.get(pk = group_id) 
        else :
            group_id = None
            group = None
            request.session["group_id"]  = None            

    except :
        group_id = None
        group = None
        request.session["group_id"]  = None


    context = {'form': form,   'teacher': teacher,  'groups': groups,  'levels': levels, 'idg': 0,   'themes' : themes_tab, 'group_id': group_id , 'parcours': None,  'relationships': [], 'share_groups' : share_groups , 
               'exercises': [], 'levels': levels, 'themes': themes_tab, 'students_checked': 0 , 'communications' : [],  'group': group , 'role' : True }


    return render(request, 'qcm/form_parcours.html', context)


  
def update_parcours(request, id, idg=0 ):
    teacher = Teacher.objects.get(user_id=request.user.id)
    levels = teacher.levels.all()
 
    parcours = Parcours.objects.get(id=id)
    form = UpdateParcoursForm(request.POST or None, request.FILES or None, instance=parcours, teacher=teacher)

    """ affiche le parcours existant avant la modif en ajax"""
    exercises = parcours.exercises.filter(supportfile__is_title=0).order_by("theme")
    """ fin """
    themes_tab = []
    for level in levels:
        for theme in level.themes.all():
            if not theme in themes_tab:
                themes_tab.append(theme)

    groups = Group.objects.filter(teacher=teacher).prefetch_related('students').order_by("level")
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("order")


    share_groups = Sharing_group.objects.filter(teacher  = teacher,role=1).order_by("group__level")
    if len(share_groups)>0 :
        sharing = True
    else :
        sharing = False

    if not authorizing_access(teacher, parcours, sharing ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    if request.method == "POST":
        if form.is_valid():
            nf = form.save(commit=False)
            nf.author = teacher
            nf.teacher = teacher
            nf.is_evaluation = 0 
            nf.save()
            nf.students.set(form.cleaned_data.get('students'))

            sg_students =  request.POST.getlist('students_sg')
            for s_id in sg_students :
                student = Student.objects.get(user_id = s_id)
                nf.students.add(student)

            try:
                for exercise in parcours.exercises.all():
                    relationship = Relationship.objects.get(parcours=nf, exercise=exercise)
                    relationship.students.set(form.cleaned_data.get('students'))
            except:
                pass

            if request.POST.get("save_and_choose") :
                return redirect('peuplate_parcours', nf.id)
            elif idg == 99999999999:
                return redirect('index')
            elif idg == 0:
                return redirect('parcours')
            else:
                return redirect('list_parcours_group', idg)
        else :
            print(form.errors)
 
    if idg > 0 and idg < 99999999999 :
        group_id = idg
        request.session["group_id"] = idg
        group = Group.objects.get(pk = group_id) 
        if Sharing_group.objects.filter(group_id=group_id, teacher = teacher).exists() :
            sh_group = Sharing_group.objects.get(group_id=group_id, teacher = teacher)
            role = sh_group.role 
    else :
        group_id = None
        group = None
        request.session["group_id"] = None
        role = False

    if parcours.teacher == teacher :
        role = True



    students_checked = parcours.students.count()  # nombre d'étudiant dans le parcours

    context = {'form': form, 'parcours': parcours, 'groups': groups, 'idg': idg, 'teacher': teacher, 'group_id': group_id ,  'group': group ,  'relationsips': relationships, 'share_groups': share_groups, 'relationships' :  [] ,
               'exercises': exercises, 'levels': levels, 'themes': themes_tab, 'students_checked': students_checked, 'communications' : [], 'role' : role }

    return render(request, 'qcm/form_parcours.html', context)



#@user_is_parcours_teacher 
def archive_parcours(request, id, idg=0):


    parcours = Parcours.objects.filter(id=id).update(is_archive=1,is_favorite=0,is_publish=0)
    teacher = Teacher.objects.get(user = request.user) 

    if not authorizing_access(teacher, parcours, False ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')


    if idg == 99999999999:
        return redirect('index')
    elif idg == 0 :
        return redirect('parcours')
    else :
        return redirect('list_parcours_group', idg)



#@user_is_parcours_teacher 
def unarchive_parcours(request, id, idg=0):


    parcours = Parcours.objects.filter(id=id).update(is_archive=0,is_favorite=0,is_publish=0)

    teacher = Teacher.objects.get(user = request.user)

    if not authorizing_access(teacher, parcours, False ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    if idg == 99999999999:
        return redirect('index')
    elif idg == 0 :
        return redirect('parcours')
    else :
        return redirect('list_parcours_group', idg)
 


#@user_is_parcours_teacher 
def delete_parcours(request, id, idg=0):
    parcours = Parcours.objects.get(id=id)
    parcours.students.clear()
    parcours.parcours_relationship.all()


    teacher = Teacher.objects.get(user = request.user)

    if not authorizing_access(teacher, parcours, False ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

 
    for r in parcours.parcours_relationship.all() :
        r.students.clear()
        r.skills.clear()
        r.delete()

    for c in parcours.course.all() :
        c.students.clear()
        c.creators.clear()
        c.delete()

    studentanswers = Studentanswer.objects.filter(parcours = parcours)
    for s in studentanswers :
        s.delete()
 
    parcours.delete()

    if idg == 99999999999:
        return redirect('index')
    elif idg == 0 :
        return redirect('parcours')
    else :
        return redirect('list_parcours_group', idg)



def show_parcours(request, id):
    parcours = Parcours.objects.get(id=id)
    user = User.objects.get(pk=request.user.id)
    teacher = Teacher.objects.get(user=user)

    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id'] 
    access = data['access'] 
 
    if not authorizing_access(teacher, parcours, access ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')


    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("order")
    nb_exo_only, nb_exo_visible,nb_exo_only_c, nb_exo_visible_c = [] , []  , [], []
    i , j = 0, 0
    for r in relationships:

        if not r.exercise.supportfile.is_title and not r.exercise.supportfile.is_subtitle:
            i += 1
        nb_exo_only.append(i)
        if not r.exercise.supportfile.is_title and not r.exercise.supportfile.is_subtitle and r.is_publish != 0:
            j += 1
        nb_exo_visible.append(j)

 
    customexercises = Customexercise.objects.filter(parcourses=parcours).order_by("ranking")

    for ce in customexercises:
        i += 1
        nb_exo_only_c.append(i)
        if ce.is_publish :
            j += 1
        nb_exo_visible_c.append(j)



    students_p_or_g = students_from_p_or_g(request,parcours)

    nb_students_p_or_g = len(students_p_or_g)

    skills = Skill.objects.all()
    nb_custom_exercises = customexercises.count()
    nb_exercises = parcours.exercises.filter(supportfile__is_title=0).count() + nb_custom_exercises
    context = {'relationships': relationships, 'parcours': parcours, 'teacher': teacher, 'skills': skills, 'communications' : [] , 'customexercises' : customexercises ,
               'students_from_p_or_g': students_p_or_g, 'nb_exercises': nb_exercises, 'nb_exo_visible': nb_exo_visible,  'nb_exo_visible_c': nb_exo_visible_c, 'nb_students_p_or_g' : nb_students_p_or_g , 
               'nb_exo_only': nb_exo_only, 'nb_exo_only_c': nb_exo_only_c, 'group_id': group_id, 'group': group, 'role' : role }

    return render(request, 'qcm/show_parcours.html', context)





def show_parcours_student(request, id):
    parcours = Parcours.objects.get(id=id)
    user = request.user
    student = Student.objects.get(user = user)

    if not authorizing_access_student(student, parcours):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    relationships = Relationship.objects.filter(parcours=parcours, students=student, is_publish=1 ).order_by("order")
    customexercises = Customexercise.objects.filter(parcourses = parcours, students=student, is_publish=1 ).order_by("ranking") 
 

    nb_exo_only,nb_exo_only_c = [] , [] 
    i=0

    for r in relationships :
        if not r.exercise.supportfile.is_title and not r.exercise.supportfile.is_subtitle:
            i+=1
        nb_exo_only.append(i)

    for ce in customexercises:
        i += 1
        nb_exo_only_c.append(i)

    today = time_zone_user(user)
    stage = get_stage(user)



    courses = parcours.course.filter(Q(is_publish=1)|Q(publish_start__lte=today,publish_end__gte=today)).order_by("ranking")

    nb_exercises = Relationship.objects.filter(parcours=parcours, students=student, is_publish=1 ).count() + Customexercise.objects.filter(parcourses = parcours, students=student, is_publish=1 ).count()


    context = {'relationships': relationships, 'customexercises': customexercises, 'stage' : stage , 'today' : today , 'courses':courses ,  'parcours': parcours, 'student': student, 'nb_exercises': nb_exercises,'nb_exo_only': nb_exo_only, 'nb_exo_only_c' : nb_exo_only_c ,  'today': today ,   }
 
    return render(request, 'qcm/show_parcours_student.html', context)





def show_parcours_visual(request, id):
    parcours = Parcours.objects.get(id=id)
 
    relationships = Relationship.objects.filter(parcours=parcours,  is_publish=1 ).order_by("order")
    nb_exo_only = [] 
    i=0
    for r in relationships :
        if r.exercise.supportfile.is_title or r.exercise.supportfile.is_subtitle:
            i=0
        else :
            i+=1
        nb_exo_only.append(i)
    nb_exercises = parcours.exercises.filter(supportfile__is_title=0).count()
    context = {'relationships': relationships,  'parcours': parcours,   'nb_exo_only': nb_exo_only, 'nb_exercises': nb_exercises,  'communications' : [] ,  }
 
    return render(request, 'qcm/show_parcours_visual.html', context)





#@user_is_parcours_teacher 
def result_parcours(request, id):

    parcours = Parcours.objects.get(id=id)
    students = students_from_p_or_g(request,parcours) # liste des élèves d'un parcours donné 
    teacher = Teacher.objects.get(user = request.user)

    try :
        group_id = request.session["group_id"]
        if Sharing_group.objects.filter(group_id=group_id, teacher = parcours.teacher).exists() :
            sh_group = Sharing_group.objects.get(group_id=group_id, teacher = parcours.teacher)
            role = sh_group.role
        else :
            role = False
    except :
        group_id = None
        role = False

    if parcours.teacher == teacher :
        role = True

    if not authorizing_access(teacher, parcours,role):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')


    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise').order_by("order")
    themes_tab, historic = [],  []
    for relationship in relationships:
        theme = {}
        # on devrait mettre la condition dans la requète 
        # mais le relationships ci-dessus doit être envoyé dans le template
        # alors on enlève les titres du supportfile
        if not relationship.exercise.supportfile.is_title :
            thm = relationship.exercise.theme
            if not thm  in historic :
                historic.append(thm)
                theme["id"] = thm.id
                theme["name"]= thm.name
                themes_tab.append(theme)

    customexercises = parcours.parcours_customexercises.all() 

    form = EmailForm(request.POST or None )

    stage = get_stage(teacher.user)

    context = {  'customexercises': customexercises, 'relationships': relationships, 'parcours': parcours, 'students': students, 'themes': themes_tab, 'form': form,  'group_id' : group_id  , 'stage' : stage, 'communications' : [] , 'role' : role }

    return render(request, 'qcm/result_parcours.html', context )



 ########## Sans doute plus utilisée ???? 
#@user_is_parcours_teacher 
def result_parcours_theme(request, id, idt):

    teacher = Teacher.objects.get(user=request.user)

    parcours = Parcours.objects.get(id=id)
    students = students_from_p_or_g(request,parcours)

    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id'] 
    access = data['access'] 

    customexercises = parcours.parcours_customexercises.all() 
 
    if not authorizing_access(teacher, parcours,access):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    theme = Theme.objects.get(id=idt)
    exercises = Exercise.objects.filter(knowledge__theme = theme, supportfile__is_title=0).order_by("id")
    relationships = Relationship.objects.filter(parcours= parcours,exercise__in=exercises ).order_by("order")
    themes_tab, historic = [],  []
    for relationship in relationships:
        theme = {}
        thm = relationship.exercise.theme
        if not thm  in historic :
            historic.append(thm)
            theme["id"] = thm.id
            theme["name"]= thm.name
            themes_tab.append(theme)

    stage = get_stage(teacher.user)
    form = EmailForm(request.POST or None)

    context = {  'relationships': relationships, 'customexercises': customexercises,'parcours': parcours, 'students': students,  'themes': themes_tab,'form': form, 'group_id' : group_id , 'stage' : stage, 'communications' : [], 'role' : role  }

    return render(request, 'qcm/result_parcours.html', context )
 



 
#@user_is_parcours_teacher 
def result_parcours_knowledge(request, id):

    teacher = Teacher.objects.get(user=request.user)
    parcours = Parcours.objects.get(id=id)
    students = students_from_p_or_g(request,parcours)

    form = EmailForm(request.POST or None)
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("order")

    knowledges = []
         
    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id'] 
    access = data['access'] 


    if not authorizing_access(teacher, parcours,access):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    knowledge_ids = parcours.exercises.values_list("knowledge",flat=True).order_by("knowledge").distinct()

    customexercises = parcours.parcours_customexercises.all()
    for ce in  customexercises :
        for knowledge in ce.knowledges.all() :
            knowledges.append(knowledge)

    for k_id in knowledge_ids :
        kn = Knowledge.objects.get(pk = k_id)
        if  kn not in knowledges :
            knowledges.append(kn)

    stage = get_stage(teacher.user)
    context = {  'relationships': relationships,  'students': students, 'parcours': parcours,  'form': form, 'exercise_knowledges' : knowledges, 'group_id' : group_id, 'stage' : stage , 'communications' : [] , 'role' : role  }

    return render(request, 'qcm/result_parcours_knowledge.html', context )



#@user_is_parcours_teacher 
def stat_parcours(request, id):

    teacher = Teacher.objects.get(user = request.user)
    parcours = Parcours.objects.get(id=id)
    exercises = parcours.exercises.all()
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("order")
    parcours_duration = parcours.duration #durée prévue pour le téléchargement
    for e in exercises :
        r = Relationship.objects.get(exercise = e, parcours = parcours)
        parcours_duration += r.duration


    form = EmailForm(request.POST or None )
    stats = []
 

    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id'] 
    access = data['access']
    if not authorizing_access(teacher, parcours,access):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    customexercises = parcours.parcours_customexercises.order_by("ranking")
    students = students_from_p_or_g(request,parcours) 

    for s in students :
        student = {}
        student["name"] = s
        studentanswers = Studentanswer.objects.filter(student=s,  exercise__in= exercises, parcours=parcours).order_by("date")

        studentanswer_tab , student_tab  = [], []
        for studentanswer in studentanswers :
            if studentanswer.exercise not in studentanswer_tab :
                studentanswer_tab.append(studentanswer.exercise)
                student_tab.append(studentanswer)
        student["nb_exo"] = len(studentanswer_tab)
        duration, score, total_numexo, good_answer = 0, 0, 0, 0
        tab, tab_date = [], []
        student["legal_duration"] = parcours.duration

        for studentanswer in  student_tab : 
            duration += int(studentanswer.secondes)
            score += int(studentanswer.point)
            total_numexo += int(studentanswer.numexo)
            good_answer += int(studentanswer.numexo*studentanswer.point/100)
            tab.append(studentanswer.point)
            tab_date.append(studentanswer.date)
            tab_date.sort()
        try :
            if len(student_tab)>1 :
                average_score = int(score/len(student_tab))
                student["duration"] = convert_seconds_in_time(duration)
                student["average_score"] = int(average_score)
                student["good_answer"] = int(good_answer)
                student["total_numexo"] = int(total_numexo)
                student["last_connexion"] = studentanswer.date
                student["score"] = int(score)
                student["score_tab"] = tab
                if duration > parcours_duration : 
                    student["test_duration"] = True
                else :
                    student["test_duration"] = False 
                tab.sort()
                if len(tab)%2 == 0 :
                    med = (tab[(len(tab)-1)//2]+tab[(len(tab)-1)//2+1])/2 ### len(tab)-1 , ce -1 est causÃ© par le rang 0 du tableau
                else:
                    med = tab[(len(tab)-1)//2+1]
                student["median"] = int(med)
                student["percent"] = math.ceil(int(good_answer)/int(total_numexo) * 100 )   
            else :
                average_score = int(score)
                student["duration"] = convert_seconds_in_time(duration)
                student["average_score"] = int(score)
                student["last_connexion"]  = studentanswer.date
                if duration > parcours_duration : 
                    student["test_duration"] = True
                else :
                    student["test_duration"] = False 
                student["median"] = int(score)
                student["score"] = int(score)
                student["score_tab"] = tab
                student["good_answer"] = int(good_answer)
                student["total_numexo"] = int(total_numexo)
                student["percent"] = math.ceil(int(good_answer)/int(total_numexo) * 100)        
        except :
            student["duration"] = ""
            student["average_score"] = ""
            student["last_connexion"] =  ""
            student["median"] = ""
            student["score"] = ""
            student["score_tab"] = []
            student["test_duration"] = False
            student["good_answer"] = ""
            student["total_numexo"] = ""
            student["percent"] = ""

 
        total_c, details_c  = 0 , ""
        for ce in customexercises :
            if ce.is_mark :
                cen = ce.customexercise_custom_answer.get(student=student, parcours = parcours) 
                total_c = total_c + cen.point
                details_c = details_c + "-" +str(cen.point)  

        student["total_note"] = total_c
        student["details_note"] = details_c

             


        total_knowledge, total_skill, detail_skill, detail_knowledge = 0,0, "",""
        for ce in customexercises :
            for skill in  ce.skills.all() :
                scs = ce.customexercise_correctionskill.get(skill = skill,student=student, parcours = parcours)
                try :
                    total_skill += scs.point
                    detail_skill += detail_skill + "-" +str(scs.point) 
                except :
                    total_skill = ""
            student["total_skill"] = total_skill
            student["detail_skill"] = detail_skill

            for knowledge in  ce.knowledges.all() :
                sck = ce.customexercise_correctionknowledge.get(knowledge = knowledge,student=student, parcours = parcours)
                try :
                    total_knowledge += sck.point
                    detail_knowledge += detail_knowledge + "-" +str(sck.point) 
                except :
                    total_knowledge = total_knowledge
            student["total_knowledge"] = total_knowledge
            student["detail_knowledge"] = detail_knowledge  


        stats.append(student)

    context = {  'parcours': parcours, 'form': form, 'stats':stats , 'group_id': group_id , 'group': group , 'relationships' : relationships , 'communications' : [] , 'role' : role  }

    return render(request, 'qcm/stat_parcours.html', context )




#@user_is_parcours_teacher 
def stat_evaluation(request, id):

    teacher = Teacher.objects.get(user = request.user)
    parcours = Parcours.objects.get(id=id)
    exercises = parcours.exercises.all()
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("order")
    parcours_duration = parcours.duration #durée prévue pour le téléchargement
    for e in exercises :
        r = Relationship.objects.get(exercise = e, parcours = parcours)
        parcours_duration += r.duration

    customexercises = parcours.parcours_customexercises.order_by("ranking")

    form = EmailForm(request.POST or None )
    stats = []
 
    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id'] 
    access = data['access']
    if not authorizing_access(teacher, parcours,access):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    students = students_from_p_or_g(request,parcours) 

    for s in students :
        student = {}
        student["name"] = s
        studentanswers = Studentanswer.objects.filter(student=s,  exercise__in= exercises, parcours=parcours).order_by("date")

        studentanswer_tab , student_tab  = [], []
        for studentanswer in studentanswers :
            if studentanswer.exercise not in studentanswer_tab :
                studentanswer_tab.append(studentanswer.exercise)
                student_tab.append(studentanswer)
        student["nb_exo"] = len(studentanswer_tab)
        duration, score, total_numexo, good_answer = 0, 0, 0, 0
        tab, tab_date = [], []
        student["legal_duration"] = parcours.duration

        for studentanswer in  student_tab : 
            duration += int(studentanswer.secondes)
            score += int(studentanswer.point)
            total_numexo += int(studentanswer.numexo)
            good_answer += int(studentanswer.numexo*studentanswer.point/100)
            tab.append(studentanswer.point)
            tab_date.append(studentanswer.date)
            tab_date.sort()
        try :
            if len(student_tab)>1 :
                average_score = int(score/len(student_tab))
                student["duration"] = convert_seconds_in_time(duration)
                student["average_score"] = int(average_score)
                student["good_answer"] = int(good_answer)
                student["total_numexo"] = int(total_numexo)
                student["last_connexion"] = studentanswer.date
                student["score"] = int(score)
                student["score_tab"] = tab
                if duration > parcours_duration : 
                    student["test_duration"] = True
                else :
                    student["test_duration"] = False 
                tab.sort()
                if len(tab)%2 == 0 :
                    med = (tab[(len(tab)-1)//2]+tab[(len(tab)-1)//2+1])/2 ### len(tab)-1 , ce -1 est causÃ© par le rang 0 du tableau
                else:
                    med = tab[(len(tab)-1)//2+1]
                student["median"] = int(med)
                student["percent"] = math.ceil(int(good_answer)/int(total_numexo) * 100 )   
            else :
                average_score = int(score)
                student["duration"] = convert_seconds_in_time(duration)
                student["average_score"] = int(score)
                student["last_connexion"]  = studentanswer.date
                if duration > parcours_duration : 
                    student["test_duration"] = True
                else :
                    student["test_duration"] = False 
                student["median"] = int(score)
                student["score"] = int(score)
                student["score_tab"] = tab
                student["good_answer"] = int(good_answer)
                student["total_numexo"] = int(total_numexo)
                student["percent"] = math.ceil(int(good_answer)/int(total_numexo) * 100)             
        except :
            student["duration"] = ""
            student["average_score"] = ""
            student["last_connexion"] =  ""
            student["median"] = ""
            student["score"] = ""
            student["score_tab"] = []
            student["test_duration"] = False
            student["good_answer"] = ""
            student["total_numexo"] = ""
            student["percent"] = ""
        
 
        total_c, details_c  = 0 , ""
        for ce in customexercises :
            if ce.is_mark :
                cen = ce.customexercise_custom_answer.get(student=student, parcours = parcours) 
                total_c = total_c + cen.point
                details_c = details_c + "-" +str(cen.point)  

        student["total_note"] = total_c
        student["details_note"] = details_c

        

        total_knowledge, total_skill, detail_skill, detail_knowledge = 0,0, "",""
        for ce in customexercises :
            for skill in  ce.skills.all() :
                scs = ce.customexercise_correctionskill.get(skill = skill,student=student, parcours = parcours)
                try :
                    total_skill += scs.point
                    detail_skill += detail_skill + "-" +str(scs.point) 
                except :
                    total_skill = ""
            student["total_skill"] = total_skill
            student["detail_skill"] = detail_skill

            for knowledge in  ce.knowledges.all() :
                sck = ce.customexercise_correctionknowledge.get(knowledge = knowledge,student=student, parcours = parcours)
                try :
                    total_knowledge += sck.point
                    detail_knowledge += detail_knowledge + "-" +str(sck.point) 
                except :
                    total_knowledge = total_knowledge
            student["total_knowledge"] = total_knowledge
            student["detail_knowledge"] = detail_knowledge  

        stats.append(student)

    context = {  'parcours': parcours, 'form': form, 'stats':stats , 'group_id': group_id , 'group': group , 'relationships' : relationships , 'communications' : [] , 'role' : role  }

    return render(request, 'qcm/stat_parcours.html', context )









def add_exercice_in_a_parcours(request):

    e= request.POST.get('exercise')
    exercise = Exercise.objects.get(id=int(e))

    exercises_parcours = request.POST.get('exercises_parcours') 
    p_tab_ids = []
    for p in exercises_parcours.split("-"):
        if p != "" :
            p_tab_ids.append(int(p))

    for p_id in p_tab_ids :
        parcours = Parcours.objects.get(pk=p_id)
        try :
            rel = Relationship.objects.get(parcours = parcours , exercise = exercise).delete() 
        except :
            pass    

    ps= request.POST.getlist('parcours') 
    orders = request.POST.getlist('orders') 
    i=0
    for p in ps :
        parcours = Parcours.objects.get(id=int(p))
        try:
            r = int(orders[i])
        except :
            r = 0

        relation = Relationship.objects.create(parcours = parcours , exercise = exercise , order=  r, is_publish= 1 , start= None , date_limit= None, duration= exercise.supportfile.duration, situation= exercise.supportfile.situation ) 
        relation.skills.set(exercise.supportfile.skills.all())   
        i +=1

    return redirect('exercises')

 
 
def clone_parcours(request, id):

    teacher = Teacher.objects.get(user_id = request.user.id)
    parcours = Parcours.objects.get(pk=id)
    relationships = Relationship.objects.filter(parcours = parcours)   
    parcours.pk = None
    parcours.teacher = teacher 
    parcours.code = str(uuid.uuid4())[:8]  
    parcours.save()

    for relationship in relationships :
        relationship.pk = None
        relationship.parcours = parcours
        relationship.save() 

    messages.success(request, "Le parcours est cloné avec succès. Bonne utilisation.")

    if parcours.is_evaluation :
        return redirect('evaluations')
    else :
        return redirect('parcours')
 


def ajax_parcours_get_exercise_custom(request):

    teacher = Teacher.objects.get(user_id = request.user.id) 
    exercise_id =  int(request.POST.get("exercise_id"))
    customexercise = Customexercise.objects.get(pk=exercise_id)
    parcourses =  teacher.teacher_parcours.all()    

    context = {  'customexercise': customexercise , 'parcourses': parcourses , 'teacher' : teacher  }
    data = {}
    data['html'] = render_to_string('qcm/ajax_parcours_get_exercise_custom.html', context)
 
    return JsonResponse(data)
 
 
def parcours_clone_exercise_custom(request):

    teacher = Teacher.objects.get(user_id = request.user.id)
    exercise_id =  int(request.POST.get("exercise_id"))
    customexercise = Customexercise.objects.get(pk=exercise_id)

    checkbox_value = request.POST.get("checkbox_value")
    customexercise.pk = None
    customexercise.teacher = teacher
    customexercise.code = str(uuid.uuid4())[:8]  
    customexercise.save()

    if checkbox_value != "" :
        checkbox_ids = checkbox_value.split("-")
        for checkbox_id in checkbox_ids :
            try :
                parcours = Parcours.objects.get(pk = checkbox_id)
                customexercise.parcourses.add(parcours)
            except :
                pass 

    data = {}  
    return JsonResponse(data)


  

def exercise_custom_show_shared(request):
    
    user = request.user
    if user.is_teacher:  # teacher
        teacher = Teacher.objects.get(user=user) 
        customexercises = Customexercise.objects.filter(is_share = 1).exclude(teacher = teacher)
        return render(request, 'qcm/list_custom_exercises.html', {  'teacher': teacher , 'customexercises':customexercises, 'parcours': None, 'relationships' : [] ,  'communications': [] , })
    else :
        return redirect('index')   


 
def ajax_exercise_error(request):

    message = request.POST.get("message")  
    exercise_id = request.POST.get("exercise_id")
    exercise = Exercise.objects.get(id = int(exercise_id))
    if request.user :
        usr = request.user.email
    else :
        usr = "info@sacado.xyz"

    msg = "L'exercice dont l'id est -- "+exercise_id+" --  décrit ci-dessous : \n Savoir faire visé : "+exercise.knowledge.name+ " \n Niveau : "+exercise.level.name+  "  \n Thème : "+exercise.theme.name +" comporte un problème. \n  S'il est identifié par l'utilisateur, voici la description :  \n" + message   

    send_mail("Avertissement SacAdo Exercice "+exercise_id,  msg , request.user.email , ["brunoserres33@gmail.com", "philippe.demaria83@gmail.com", str(exercise.supportfile.author.user.email)])
    data = {}
    data["htmlg"]= "Envoi réussi, merci."
    return JsonResponse(data) 


#@user_is_parcours_teacher
def parcours_tasks_and_publishes(request, id):

    today = time_zone_user(request.user)
    parcours = Parcours.objects.get(id=id)
    teacher = Teacher.objects.get(user=request.user)

    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id'] 
    access = data['access']
    if not authorizing_access(teacher, parcours,access):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    form = AttachForm(request.POST or None, request.FILES or None)

    relationships = Relationship.objects.filter(parcours=parcours).order_by("exercise__theme")
    context = {'relationships': relationships,  'parcours': parcours, 'teacher': teacher  , 'today' : today , 'group' : group , 'group_id' : group_id , 'communications' : [] , 'form' : form , 'role' : role , }
    return render(request, 'qcm/parcours_tasks_and_publishes.html', context)
 

 

 

#@user_is_parcours_teacher
def result_parcours_exercise_students(request,id):
    teacher = Teacher.objects.get(user_id = request.user.id)
    parcours = Parcours.objects.get(pk = id)
    try :
        group_id = request.session.get("group_id")
        group = Group.objects.get(pk = group_id)
    except :
        group_id = None
        group = None

    if not authorizing_access(teacher, parcours,True):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    relationships = Relationship.objects.filter(parcours = parcours, is_publish = 1) 
    customexercises = parcours.parcours_customexercises.filter( is_publish = 1).order_by("ranking")
    stage = get_stage(teacher.user)

    return render(request, 'qcm/result_parcours_exercise_students.html', {'customexercises': customexercises , 'stage':stage ,   'relationships': relationships ,  'parcours': parcours , 'group_id': group_id ,  'group' : group ,  })






@csrf_exempt # PublieDépublie un exercice depuis organize_parcours
def ajax_is_favorite(request):  

    parcours_id = int(request.POST.get("parcours_id",None))
    statut = int(request.POST.get("statut"))
    data = {}
    if statut :
        Parcours.objects.filter(pk = parcours_id).update(is_favorite = 0)
        data["statut"] = ""
        data["fav"] = 0
    else :
        Parcours.objects.filter(pk = parcours_id).update(is_favorite = 1)  
        data["statut"] = "<i class='fa fa-star fa-stack-1x' style='font-size: 12px; color:#FFF' ></i>"
        data["fav"] = 1
    return JsonResponse(data) 




@csrf_exempt # PublieDépublie un exercice depuis organize_parcours
def ajax_course_sorter(request):  
    try :
        course_ids = request.POST.get("valeurs")
        course_tab = course_ids.split("-") 
        parcours_id = int(request.POST.get("parcours_id"))

        for i in range(len(course_tab)-1):
            Course.objects.filter(parcours_id = parcours_id , pk = course_tab[i]).update(ranking = i)
    except :
        pass

    data = {}
    return JsonResponse(data) 

@csrf_exempt # PublieDépublie un exercice depuis organize_parcours
def ajax_parcours_sorter(request):  

    try :
        course_ids = request.POST.get("valeurs")
        course_tab = course_ids.split("-") 
     

        for i in range(len(course_tab)-1):
            Parcours.objects.filter( pk = course_tab[i]).update(ranking = i)
    except :
        pass
    data = {}
    return JsonResponse(data) 

 

@csrf_exempt
def ajax_sort_exercise(request):  
    try :
        exercise_ids = request.POST.get("valeurs")
        exercise_tab = exercise_ids.split("-") 

        parcours = request.POST.get("parcours")

        custom = request.POST.get("custom")
        if not custom :
            for i in range(len(exercise_tab)-1):
                try :
                    Relationship.objects.filter(parcours = parcours , exercise_id = exercise_tab[i]).update(order = i)
                except :
                    pass
        else :
            for i in range(len(exercise_tab)-1):
                try :
                    Customexercise.objects.filter(pk = exercise_tab[i]).update(ranking = i)
                except :
                    pass
 

    except :
        pass
    data = {}
    return JsonResponse(data) 



@csrf_exempt # PublieDépublie un exercice depuis organize_parcours
def ajax_publish(request):  

    statut = request.POST.get("statut")
    custom = request.POST.get("custom")

    data = {}
 
    if statut=="true" or statut == "True":
        statut = 0
        data["statut"] = "false"
        data["publish"] = "Dépublié"
        data["class"] = "legend-btn-danger"
        data["noclass"] = "legend-btn-success"
        data["removeclass"] = "btn-success"

    else:
        statut = 1
        data["statut"] = "true"
        data["publish"] = "Publié"
        data["class"] = "legend-btn-success"
        data["noclass"] = "legend-btn-danger"
        data["removeclass"] = "btn-danger"

    if custom == "0" :
        relationship_id = request.POST.get("relationship_id")        
        Relationship.objects.filter(pk = int(relationship_id)).update(is_publish = statut)
    else :
        customexercise_id = request.POST.get("relationship_id")        
        Customexercise.objects.filter(pk = int(customexercise_id)).update(is_publish = statut)    
    return JsonResponse(data) 


@csrf_exempt   # PublieDépublie un parcours depuis form_group et show_group
def ajax_publish_parcours(request):  

    parcours_id = request.POST.get("parcours_id")
    statut = request.POST.get("statut")
    data = {}
    if statut=="true" or statut == "True":
        statut = 0
        data["statut"] = "false"
        if request.POST.get("from") == "1" :
            data["publish"] = "Parcours non publié"
        elif request.POST.get("from") == "2" :
            data["publish"] = "Non publié"
        else :
            data["publish"] = "Dépublier"
        data["style"] = "#dd4b39"
        data["class"] = "legend-btn-danger"
        data["noclass"] = "legend-btn-success"
        data["label"] = "Non publié"
    else:
        statut = 1
        data["statut"] = "true"
        if request.POST.get("from") == "1" :
            data["publish"] = "Parcours publié"
        elif request.POST.get("from") == "2" :
            data["publish"] = "Publié" 
        else :
            data["publish"] = "Dépublier"
        data["style"] = "#00a65a"
        data["class"] = "legend-btn-success"
        data["noclass"] = "legend-btn-danger"
        data["label"] = "Publié"
        parcours = Parcours.objects.get(pk = int(parcours_id) )

    Parcours.objects.filter(pk = int(parcours_id)).update(is_publish = statut)
 
    return JsonResponse(data) 


@csrf_exempt
def ajax_dates(request):  # On soncerve relationship_id par commodité mais c'est relationship_id et non customexercise_id dans tout le script
    data = {}
    relationship_id = request.POST.get("relationship_id")
    typ = int(request.POST.get("type"))
    duration =  request.POST.get("duration") 
    custom =  request.POST.get("custom") 
    try :
        if typ == 0 : # Date de publication
            date = request.POST.get("dateur") 
            if date :
                if custom == "0" :
                    Relationship.objects.filter(pk = int(relationship_id)).update(start = date)
                else :
                    Customexercise.objects.filter(pk = int(relationship_id)).update(start = date)
                data["class"] = "btn-success"
                data["noclass"] = "btn-default"
            else :
                if custom == "0" :
                    Relationship.objects.filter(pk = int(relationship_id)).update(start = None)
                else :
                    Customexercise.objects.filter(pk = int(relationship_id)).update(start = None)
                data["class"] = "btn-default"
                data["noclass"] = "btn-success"
            data["dateur"] = date 

        elif typ == 1 :  # Date de rendu de tache
            date = request.POST.get("dateur") 
            if date :
                if custom == "0" : 
                    Relationship.objects.filter(pk = int(relationship_id)).update(date_limit = date)

                    r = Relationship.objects.get(pk = int(relationship_id))
                    data["class"] = "btn-success"
                    data["noclass"] = "btn-default"
                    msg = "Pour le "+str(date)+": \n Faire l'exercice : https://sacado.xyz/qcm/show_this_exercise/"+str(r.exercise.id)+" : " +str(r.exercise)+" \n. Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte."
                    data["dateur"] = date 
                    students = r.students.all()
                    rec = []
                else :
                    Customexercise.objects.filter(pk = int(relationship_id)).update(date_limit = date)
                    ce = Customexercise.objects.get(pk = int(relationship_id))
                    data["class"] = "btn-success"
                    data["noclass"] = "btn-default"
                    msg = "Pour le "+str(date)+": \n Faire l'exercice : https://sacado.xyz/qcm/show_this_exercise/"+str(ce.id)+"\n. Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte."
                    data["dateur"] = date 
                    students = ce.students.all()
                    rec = []


                for s in students :
                    if s.task_post : 
                        if  s.user.email :                  
                            rec.append(s.user.email)

                send_mail("SacAdo Tâche à effectuer avant le "+str(date),  msg , "info@sacado.xyz" , rec ) 
                send_mail("SacAdo Tâche à effectuer avant le "+str(date),  msg , "info@sacado.xyz" , [r.parcours.teacher.user.email] )   

            else :
                if custom == "0" : 
                    Relationship.objects.filter(pk = int(relationship_id)).update(date_limit = None)

                    r = Relationship.objects.get(pk = int(relationship_id))
                    data["class"] = "btn-default"
                    data["noclass"] = "btn-success"
                    msg = "L'exercice https://sacado.xyz/qcm/show_this_exercise/"+str(r.exercise.id)+" : "+str(r.exercise)+" n'est plus une tâche \n. Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte."
                    date = "Tâche ?"  
                    data["dateur"] = date 
                    students = r.students.all()
                else :
                    Customexercise.objects.filter(pk = int(relationship_id)).update(date_limit = None)
                    ce = Customexercise.objects.get(pk = int(relationship_id))
                    data["class"] = "btn-success"
                    data["noclass"] = "btn-default"
                    msg = "L'exercice https://sacado.xyz/qcm/show_this_exercise/"+str(ce.id)+" : n'est plus une tâche \n Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte."
                    data["dateur"] = date 
                    students = ce.students.all()
          
                rec = []
                for s in students :
                    if s.task_post : 
                        if  s.user.email :                  
                            rec.append(s.user.email)
                send_mail("SacAdo. Annulation de tâche à effectuer",  msg , "info@sacado.xyz" , rec ) 
                send_mail("SacAdo. Annulation de tâche à effectuer",  msg , "info@sacado.xyz" , [r.parcours.teacher.user.email] ) 

        else :
            if custom == "0" :
                Relationship.objects.filter(pk = int(relationship_id)).update(start = date)
                r = Relationship.objects.get(pk = int(relationship_id))
                msg = "Pour le "+str(date)+": \n Faire l'exercice : https://sacado.xyz/qcm/show_this_exercise/"+str(r.exercise.id)+" : " +str(r.exercise)+" \n. Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte."
                students = r.students.all()
            else :
                Customexercise.objects.filter(pk = int(relationship_id)).update(start = date)
                Customexercise.objects.filter(pk = int(relationship_id)).update(date_limit = None)
                ce = Customexercise.objects.get(pk = int(relationship_id))
                msg = "Pour le "+str(date)+": \n Faire l'exercice : https://sacado.xyz/qcm/show_this_exercise/"+str(ce.id)+"\n Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte."
                students = ce.students.all()

            data["class"] = "btn-success"
            data["noclass"] = "btn-default"
 
            rec = []
            for s in students :
                if s.task_post : 
                    if  s.user.email :                  
                        rec.append(s.user.email)

            send_mail("SacAdo Tâche à effectuer avant le "+str(date),  msg , "info@sacado.xyz" , rec ) 
            send_mail("SacAdo Tâche à effectuer avant le "+str(date),  msg , "info@sacado.xyz" , [r.parcours.teacher.user.email] ) 

            data["dateur"] = date  

    except :
        try :
            duration =  request.POST.get("duration") 
            if custom == "0" :
                Relationship.objects.filter(pk = int(relationship_id)).update(duration = duration)
            else :
                Customexercise.objects.filter(pk = int(relationship_id)).update(duration = duration)
            data["clock"] = "<i class='fa fa-clock-o'></i> "+str(duration)+"  min."          
            try :
                situation =  request.POST.get("situation")
                rel = Relationship.objects.get(pk = int(relationship_id))

                if rel.exercise.supportfile.is_ggbfile :
                    Relationship.objects.filter(pk = int(relationship_id)).update(situation = situation)
                    data["save"] = "<i class='fa fa-save'></i> "+str(situation)
                    data["situation"] = "<i class='fa fa-save'></i> "+str(situation)
                    data["annonce"] = ""
                    data["annoncement"]   = False

                else :
                    Relationship.objects.filter(pk = int(relationship_id)).update(instruction = situation)  
                    data["save"] = False
                    data["duration"] = ""
                    data["annonce"] = situation
                    data["annoncement"]   = True
            except : 
                pass

        except :
            try :
                situation =  request.POST.get("situation") 
                rel = Relationship.objects.get(pk = int(relationship_id))
                if rel.exercise.supportfile.is_ggbfile :
                    Relationship.objects.filter(pk = int(relationship_id)).update(situation = situation)
                    data["save"] = "<i class='fa fa-save'></i> "+str(situation) 
                    data["annonce"] = "" 
                    data["annoncement"]   = False                                 
                else :
                    Relationship.objects.filter(pk = int(relationship_id)).update(instruction = situation)   
                    data["save"] = False
                    data["annonce"] = situation
                    data["annoncement"]   = True
                try :
                    duration =  request.POST.get("duration") 
                    if custom == "0" :
                        Relationship.objects.filter(pk = int(relationship_id)).update(duration = duration)
                    else :
                        Customexercise.objects.filter(pk = int(relationship_id)).update(duration = duration)
                    data["clock"] = "<i class='fa fa-clock-o'></i> "+str(duration)+"  min."                            
                    data["duration"] = duration
                except : 
                    pass
            except :
                pass

    return JsonResponse(data) 



@csrf_exempt
def ajax_skills(request):  
    data = {}
    relationship_id = request.POST.get("relationship_id")
    skill_id =  int(request.POST.get("skill_id") )
    relationship  = Relationship.objects.get(pk = relationship_id )
    skill = Skill.objects.get(pk = skill_id ) 

    if Relationship.objects.filter(pk = relationship_id, skills = skill).count()>0 :
        relationship.skills.remove(skill)    
    else :
        relationship.skills.add(skill)   

    return JsonResponse(data) 



def aggregate_parcours(request):

    code = request.POST.get("parcours")
    student = Student.objects.get(user=request.user)

    if Parcours.objects.exclude(students = student).filter(code = code).exists()  :
        parcours = Parcours.objects.get(code = code)
        parcours.students.add(student)

    return redirect("index") 


def ajax_parcoursinfo(request):

    code =  request.POST.get("code")
    data = {}    
    try : 
        nb_group = Parcours.objects.filter(code = code).count()
 
        if  nb_group == 1 :

            data['htmlg'] = "<br><i class='fa fa-check text-success'></i>" 
 
        else :
            data['htmlg'] = "<br><i class='fa fa-times text-danger'></i> Parcours inconnu."
 
    except :
            data['htmlg'] = "<br><i class='fa fa-times text-danger'></i> Parcours inconnu."
 

 
    return JsonResponse(data)




def ajax_detail_parcours(request):

    custom =  int(request.POST.get("custom"))    
    parcours_id =  int(request.POST.get("parcours_id"))
    exercise_id =  int(request.POST.get("exercise_id"))
    num_exo =  int(request.POST.get("num_exo"))    
    parcours = Parcours.objects.get(id = parcours_id)

    students = students_from_p_or_g(request,parcours)

    try :
        relationship = Relationship.objects.get(exercise_id = exercise_id, parcours_id=parcours_id )
    except :
        relationship = None
    
    data = {}
    if custom == 0 :
        exercise = Exercise.objects.get(id = exercise_id) 
        stats = []
        for s in students :
            student = {}
            student["name"] = s 

            studentanswers = Studentanswer.objects.filter(student=s,exercise=exercise)
            duration, score = 0, 0
            tab, tab_date = [], []
            for studentanswer in  studentanswers : 
                duration += int(studentanswer.secondes)
                score += int(studentanswer.point)
                tab.append(studentanswer.point)
                tab_date.append(studentanswer.date)
            tab_date.sort()
            try :
                if len(studentanswers)>1 :
                    average_score = int(score/len(studentanswers))
                    student["duration"] = convert_seconds_in_time(duration)
                    student["average_score"] = int(average_score)
                    student["heure_max"] = tab_date[len(tab_date)-1]
                    student["heure_min"] = tab_date[0]
                    tab.sort()
                    if len(tab)%2 == 0 :
                        med = (tab[(len(tab)-1)//2]+tab[(len(tab)-1)//2+1])/2 ### len(tab)-1 , ce -1 est causÃ© par le rang 0 du tableau
                    else:
                        med = tab[(len(tab)-1)//2+1]
                    student["median"] = int(med)
                    student["nb"] = int(len(tab))                
                else :
                    average_score = int(score)
                    student["duration"] = convert_seconds_in_time(duration)
                    student["average_score"] = int(score)
                    student["heure_max"] = tab_date[0]
                    student["heure_min"] = tab_date[0]
                    student["median"] = int(score)
                    student["nb"] = 0  
            except :
                student["duration"] = ""
                student["average_score"] = ""
                student["heure_max"] = ""
                student["heure_min"] = ""
                student["median"] = ""
                student["nb"] = 0  
            stats.append(student)

        context = {  'parcours': parcours,  'exercise':exercise ,'stats':stats ,  'num_exo':num_exo, 'relationship':relationship, 'communications' : [] , }

        data['html'] = render_to_string('qcm/ajax_detail_parcours.html', context)

    else :
        parcours = Parcours.objects.get(pk = parcours_id )
        customexercise = Customexercise.objects.get(id = exercise_id, parcourses = parcours) 
        students = customexercise.students.order_by("user__last_name") 
        duration, score = 0, 0
        tab = []
        cas =  Customanswerbystudent.objects.filter(parcours=parcours, customexercise = customexercise)
        for ca in cas  : 
            try :
                score += int(ca.point)
                tab.append(ca.point)
            except:
                pass
        tab.sort()

        try :
            if len(tab)%2 == 0 :
                med = (tab[(len(tab)-1)//2]+tab[(len(tab)-1)//2+1])/2 ### len(tab)-1 , ce -1 est cause par le rang 0 du tableau
            else:
                med = tab[(len(tab)-1)//2+1]
        except :
            med = 0     
 
        try :
            average = int(score / len(cas))
        except :
            average = "" 


        context = {  'parcours': parcours,  'customexercise':customexercise ,'average':average , 'students' : students , 'relationship':[], 'num_exo' : num_exo, 'communications' : [] , 'median' : med , 'communications' : [] , }

        data['html'] = render_to_string('qcm/ajax_detail_parcours_customexercise.html', context)


    return JsonResponse(data)




def delete_relationship(request,idr):

    relation = Relationship.objects.get(pk = idr) 
    if relation.parcours.teacher.user == request.user  :
        relation.delete()

    return redirect("show_parcours" , relation.parcours.id ) 
    

def delete_relationship_by_individualise(request,idr, id):

    relation = Relationship.objects.get(pk = idr) 
    if relation.parcours.teacher.user == request.user  :
        relation.delete()

    return redirect("individualise_parcours" , relation.parcours.id   ) 



def remove_students_from_parcours(request):

    parcours_id = request.POST.get("parcours_id")
    parcours = Parcours.objects.get(pk = parcours_id)
    students_id = request.POST.getlist("students")
    for student_id in students_id:
        student = Student.objects.get(user = student_id)
        relationships = Relationship.objects.filter(parcours = parcours, students = student)
        for r in relationships :
            r.students.remove(student)
        parcours.students.remove(student)
 
    return redirect("parcours" ) 




#######################################################################################################################################################################
#######################################################################################################################################################################
#################   Exercise
#######################################################################################################################################################################
#######################################################################################################################################################################

def all_datas(user, status,level):
    teacher = Teacher.objects.get(user=user)
    datas = []
    levels_tab,knowledges_tab, exercises_tab    =   [],  [],  []


    levels_dict = {}
    levels_dict["name"]=level 

    themes = level.themes.all().order_by("id")
    themes_tab =   []
    for theme in themes :
        themes_dict =  {}                
        themes_dict["name"]=theme.name 
        knowlegdes = Knowledge.objects.filter(theme=theme,level=level).order_by("theme")
        knowledges_tab  =  []
        for knowledge in knowlegdes :
            knowledges_dict  =   {}  
            knowledges_dict["name"]=knowledge 
            exercises = Exercise.objects.filter(knowledge=knowledge,supportfile__is_title=0).select_related('supportfile').order_by("theme")
            exercises_tab    =   []
            for exercise in exercises :
                exercises_tab.append(exercise)
            knowledges_dict["exercises"]=exercises_tab
            knowledges_tab.append(knowledges_dict)
        themes_dict["knowledges"]=knowledges_tab
        themes_tab.append(themes_dict)
    levels_dict["themes"]=themes_tab

    return levels_dict

def all_levels(user, status):
    teacher = Teacher.objects.get(user=user)
    datas = []
    levels_tab,knowledges_tab, exercises_tab    =   [],  [],  []

    if status == 0 : 
        levels = teacher.levels.all()
    elif status == 1 : 
        levels = Level.objects.all().order_by("id")

    for level in levels :
        levels_dict = {}
        levels_dict["name"]=level 

        themes = level.themes.all().order_by("id")
        themes_tab =   []
        for theme in themes :
            themes_dict =  {}                
            themes_dict["name"]=theme.name 
            knowlegdes = Knowledge.objects.filter(theme=theme,level=level).order_by("theme")
            knowledges_tab  =  []
            for knowledge in knowlegdes :
                knowledges_dict  =   {}  
                knowledges_dict["name"]=knowledge 
                exercises = Exercise.objects.filter(knowledge=knowledge,supportfile__is_title=0).order_by("theme")
                exercises_tab    =   []
                for exercise in exercises :
                    exercises_tab.append(exercise)
                knowledges_dict["exercises"]=exercises_tab
                knowledges_tab.append(knowledges_dict)
            themes_dict["knowledges"]=knowledges_tab
            themes_tab.append(themes_dict)
        levels_dict["themes"]=themes_tab
        datas.append(levels_dict)
    return datas



def list_exercises(request):
    
    user = request.user
    if user.is_teacher:  # teacher
        teacher = Teacher.objects.get(user=user)
        datas = all_levels(user, 0)
        customexercises = teacher.teacher_customexercises.all()
        return render(request, 'qcm/list_exercises.html', {'datas': datas, 'teacher': teacher , 'customexercises':customexercises, 'parcours': None, 'relationships' : [] ,  'communications': [] , })
    
    elif user.is_student: # student
        student = Student.objects.get(user=user)
        parcourses = student.students_to_parcours.all()

        nb_exercises = Relationship.objects.filter(parcours__in=parcourses,is_publish=1,exercise__supportfile__is_title=0).count()
        relationships = Relationship.objects.filter(parcours__in=parcourses,is_publish=1,exercise__supportfile__is_title=0).order_by("exercise__theme")

        return render(request, 'qcm/student_list_exercises.html',
                      {'relationships': relationships, 'nb_exercises': nb_exercises ,     })

    else: # non utilisé
        parent = Parent.objects.get(user=user)
        students = parent.students.all()
        parcourses = []
        for student in students :
            for parcours in student.students_to_parcours.all() :
                if parcours not in parcourses :
                    parcourses.append(parcours)  

        nb_exercises = Relationship.objects.filter(parcours__in=parcourses,is_publish=1,exercise__supportfile__is_title=0).count()
        relationships = Relationship.objects.filter(parcours__in=parcourses,is_publish=1,exercise__supportfile__is_title=0).order_by("exercise__theme")

        return render(request, 'qcm/student_list_exercises.html',
                      {'relationships': relationships, 'nb_exercises': nb_exercises ,     })





@user_passes_test(user_is_superuser)
def admin_list_associations(request,id):
    level = Level.objects.get(pk = id)
    user = request.user

    teacher = Teacher.objects.get(user=user)
    data = all_datas(user, 1,level)

    return render(request, 'qcm/list_associations.html', {'data': data, 'teacher': teacher , 'parcours': None, 'relationships' : [] , 'communications' : []   })
 


@user_passes_test(user_is_superuser)
def gestion_supportfiles(request):
  
    lvls = []
    q_levels = Level.objects.all()
    for level in q_levels :
        query_lk = level.knowledges.all()

        nbk = query_lk.count() # nombre de savoir faire listés sur le niveau
        nbe = level.exercises.filter(supportfile__is_title=0).count() # nombre d'exercices sur le niveau
        m = level.exercises.filter(knowledge__in = query_lk).count()
        nb = nbk - m
        lvls.append({ 'name' : level.name , 'nbknowlegde': nbk , 'exotot' : nbe , 'notexo' : nb }) 

    return render(request, 'qcm/gestion_supportfiles.html', {'lvls': lvls, 'parcours': None, 'relationships' : [] , 'communications' : [] })




@user_passes_test(user_is_superuser)
def ajax_update_association(request):
    data = {} 
    code = request.POST.get('code')
    exercise_id = int(request.POST.get('exercise_id'))
    action = request.POST.get('action')


    if action == "create" :
        supportfile = Supportfile.objects.get(code=code)
        try :
            knowledge = Knowledge.objects.get(pk=exercise_id)
            exercise = Exercise.objects.create(knowledge= knowledge, level= knowledge.level,theme= knowledge.theme,supportfile_id= supportfile.id)
            data['error'] = ""
        except :
            data['error'] = "Code incorrect"
        data['html'] = render_to_string('qcm/ajax_create_association.html', {  'exercise' : exercise ,  })

    elif action == "update" : 
        try :
            supportfile = Supportfile.objects.get(code=code)
            exercise_id = int(request.POST.get('exercise_id'))
            exercise = Exercise.objects.get(pk=exercise_id)

            Exercise.objects.filter(pk=exercise_id).update(supportfile= supportfile)
            data['error'] = ""
        except :
            data['error'] = "Code incorrect"
        data['html'] = render_to_string('qcm/ajax_association.html', {  'exercise' : exercise ,  })

    elif action == "delete" :
        exercise = Exercise.objects.get(pk=exercise_id) 
        exercise.delete()
    return JsonResponse(data)





@user_passes_test(user_is_superuser)
def admin_list_supportfiles(request,id):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    if user.is_superuser:  # admin and more

        teacher = Teacher.objects.get(user=user)
        datas = []

        level = Level.objects.get(pk=id)
        levels_dict = {}
        levels_dict["name"] = level

        themes = level.themes.filter(subject__in=teacher.subjects.all()).order_by("id")
        themes_tab = []
        for theme in themes:
            themes_dict = {}
            themes_dict["name"] = theme.name
            knowlegdes = Knowledge.objects.filter(theme=theme, level=level).order_by("theme")
            knowledges_tab = []
            for knowledge in knowlegdes:
                supportfiles = knowledge.supportfiles.filter(is_title=0).order_by("theme")
                exercises = Exercise.objects.filter(knowledge=knowledge, level=level, theme=theme,supportfile__in=supportfiles).order_by("theme")

                knowledges_tab.append(
                    {
                        "name": knowledge,
                        "exercises": exercises,
                        "supportfiles": supportfiles,
                    }
                )

            themes_dict["knowledges"] = knowledges_tab
            themes_tab.append(themes_dict)
        levels_dict["themes"] = themes_tab
 



    return render(request, 'qcm/list_supportfiles.html', {'levels_dict': levels_dict, 'teacher':teacher , 'level':level , 'relationships' : [] , 'communications' : [] , 'parcours' :  None })


 


def parcours_exercises(request,id):
    user = request.user
    parcours = Parcours.objects.get(pk=id)
    student = Student.objects.get(user=user)

    if not authorizing_access_student(student, parcours):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    relationships = Relationship.objects.filter(parcours=parcours,is_publish=1).order_by("exercise__theme")

    return render(request, 'qcm/student_list_exercises.html', {'parcours': parcours  , 'relationships': relationships, })




def exercises_level(request, id):
    exercises = Exercise.objects.filter(level_id=id,supportfile__is_title=0).order_by("theme")
    level = Level.objects.get(pk=id)
    themes =  level.themes.all()
    form = AuthenticationForm() 
    u_form = UserForm()
    t_form = TeacherForm()
    s_form = StudentForm()
    return render(request, 'list_exercises.html', {'exercises': exercises, 'level':level , 'themes':themes , 'form':form , 'u_form':u_form , 's_form': s_form , 't_form': t_form , 'levels' : [] })






@user_passes_test(user_is_superuser)
def create_supportfile(request):

    code = str(uuid.uuid4())[:8]
    teacher = Teacher.objects.get(user_id = request.user.id)
    form = SupportfileForm(request.POST or None,request.FILES or None,teacher = teaher)
    if request.user.is_superuser :
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.code = code
            nf.author = teacher
            send_to_teachers(nf.level)        
            nf.save()
            # le supprot GGB est placé comme exercice par défaut.
            Exercise.objects.create(supportfile = nf, knowledge = nf.knowledge, level = nf.level, theme = nf.theme )


            return redirect('admin_supportfiles' , nf.level.id )

    context = {'form': form,   'teacher': teacher, 'knowledge': None,  'knowledges': [], 'relationships': [],  'supportfiles': [],   'levels': [], 'parcours': None, 'supportfile': None, 'communications' : [] ,  }

    return render(request, 'qcm/form_supportfile.html', context)



@user_passes_test(user_is_superuser)
def create_supportfile_knowledge(request,id):

    code = str(uuid.uuid4())[:8]
    knowledge = Knowledge.objects.get(id = id)
    teacher = Teacher.objects.get(user_id = request.user.id)
    form = SupportfileKForm(request.POST or None,request.FILES or None, knowledge = knowledge )
    levels = Level.objects.all()
    supportfiles = Supportfile.objects.filter(is_title=0).order_by("level")
    knowledges = Knowledge.objects.all().order_by("level")

    if request.user.is_superuser : 
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.code = code
            nf.author = teacher
            nf.knowledge = knowledge
            #send_to_teachers(nf.level)    
            nf.save()
            # le support GGB est placé comme exercice par défaut.
            Exercise.objects.create(supportfile = nf, knowledge = nf.knowledge, level = nf.level, theme = nf.theme )
            return redirect('admin_supportfiles' , nf.level.id )
        else :
            print(form.errors)


    context = {'form': form,   'teacher': teacher,  'knowledges': knowledges, 'relationships': [],  'knowledge': knowledge,  'supportfile': None,  'supportfiles': supportfiles,   'levels': levels , 'parcours': None, 'communications' : [] ,  }

    return render(request, 'qcm/form_supportfile.html', context)



@user_passes_test(user_is_superuser)
def update_supportfile(request, id, redirection=0):

    teacher = Teacher.objects.get(user_id = request.user.id)
    if request.user.is_superuser:
        supportfile = Supportfile.objects.get(id=id)
        knowledge = supportfile.knowledge
        supportfile_form = UpdateSupportfileForm(request.POST or None, request.FILES or None, instance=supportfile, knowledge = knowledge)
        levels = Level.objects.all()
        supportfiles = Supportfile.objects.filter(is_title=0).order_by("level")
        knowledges = Knowledge.objects.all().order_by("level")

        if request.method == "POST":
            if supportfile_form.is_valid():
                nf = supportfile_form.save(commit=False)
                nf.code = supportfile.code
                nf.save()
                supportfile_form.save_m2m()
                messages.success(request, "L'exercice a été modifié avec succès !")

                return redirect('admin_supportfiles', supportfile.level.id)

        context = {'form': supportfile_form, 'teacher': teacher, 'supportfile': supportfile, 'knowledges': knowledges, 'relationships': [] ,
                   'supportfiles': supportfiles, 'levels': levels, 'parcours': None, 'communications' : [] , 'knowledge' : knowledge ,   }

        return render(request, 'qcm/form_supportfile.html', context)

 



@user_passes_test(user_is_superuser)
def delete_supportfile(request, id):
    if request.user.is_superuser:
        supportfile = Supportfile.objects.get(id=id)
        if Relationship.objects.filter(exercise__supportfile=supportfile).count() == 0:
            supportfile.delete()
            messages.success(request, "Le support GGB a été supprimé avec succès !")
        else:
            messages.error(request, " Des parcours utilisent ce support GGB. Il n'est pas possible de le supprimer.")

    return redirect('admin_supportfiles', supportfile.level.id)



@user_passes_test(user_is_superuser)
def show_this_supportfile(request, id):

    if request.user.is_teacher:
        teacher = Teacher.objects.get(user=request.user)
        parcours = Parcours.objects.filter(teacher=teacher)
    else :
        parcours = None

    supportfile = Supportfile.objects.get(id=id)
    request.session['level_id'] = supportfile.level.id
    start_time = time.time()
    context = {'supportfile': supportfile, 'start_time': start_time, 'communications' : [] ,  'parcours': parcours}

    return render(request, 'qcm/show_supportfile.html', context)




@user_passes_test(user_is_superuser)
def create_exercise(request, supportfile_id):
 
    knowledges = Knowledge.objects.all().order_by("level").select_related('level')
    supportfile = Supportfile.objects.get(id=supportfile_id)

    if request.user.is_superuser:
        if request.method == "POST":
            knowledges_id = request.POST.getlist("choice_knowledges")
            knowledges_id_tab = []
            for k_id in knowledges_id:
                knowledges_id_tab.append(int(k_id))

            # les exercices déjà référencés sur le même support par leur knowledge
            exercises = Exercise.objects.filter(supportfile=supportfile)
            exercises_Kno_tab = []
            for exercise in exercises:
                if exercise.knowledge.id not in exercises_Kno_tab:
                    exercises_Kno_tab.append(int(exercise.knowledge.id))

            delete_list = [value for value in exercises_Kno_tab if value not in knowledges_id_tab]

            for knowledge_id in knowledges_id_tab:
                knowledge = Knowledge.objects.get(pk=knowledge_id)
                exercise, result = Exercise.objects.get_or_create(supportfile=supportfile, knowledge=knowledge,
                                                                  level=knowledge.level, theme=knowledge.theme)

            for kn_id in delete_list:
                knowledge = Knowledge.objects.get(pk=kn_id)
                exercise = Exercise.objects.get(supportfile=supportfile, knowledge=knowledge)

                if Relationship.objects.filter(exercise=exercise).count() == 0:
                    exercise.delete()  # efface les existants sur le niveau sélectionné

            return redirect('admin_supportfiles' , supportfile.level.id )

    context = {  'knowledges': knowledges, 'supportfile': supportfile , 'parcours': None, 'communications' : [] , 'communications' : [] , 'relationships' : []  }

    return render(request, 'qcm/form_exercise.html', context)




def show_exercise(request, id):
    exercise = Exercise.objects.get(id=id)

    request.session['level_id'] = exercise.level.id
    form = AuthenticationForm() 
    u_form = UserForm()
    t_form = TeacherForm()
    s_form = StudentForm()

    context = {'exercise': exercise,   'form': form , 'u_form' : u_form , 's_form' : s_form , 't_form' : t_form , 'levels' : [],   'communications' : [] , 'relationships' : []  }
 
    if exercise.supportfile.is_ggbfile :
        wForm = None
        url = "show_exercise.html" 
    elif exercise.supportfile.is_python :
        url = "basthon/index_shower.html"
        wForm = None
    else :
        url = "qcm/show_teacher_writing.html" 

    return render(request, url , context)




def show_this_exercise(request, id):

    if request.user.is_authenticated:
        today = time_zone_user(request.user)
        if request.user.is_teacher:
            teacher = Teacher.objects.get(user=request.user)
            parcours = Parcours.objects.filter(teacher=teacher)
        elif request.user.is_student :
            student = Student.objects.get(user=request.user)
            parcours = None
        else :
            student = None
            parcours = None
    else :
        student = None
        parcours = None        
        today = timezone.now()

    start_time = time.time()

    exercise = Exercise.objects.get(pk = id)

    if exercise.supportfile.is_ggbfile :
        wForm = None
        url = "qcm/show_exercise.html" 
    elif exercise.supportfile.is_python :
        url = "basthon/index_teacher.html"
        wForm = None
    else :
        wForm = WrittenanswerbystudentForm(request.POST or None, request.FILES or None )
        url = "qcm/show_teacher_writing.html" 


    context = {'exercise': exercise, 'start_time': start_time, 'parcours': parcours , 'communications' : [] , 'relationships' : [] , 'today' : today , 'wForm' : wForm }

    return render(request, url, context)



def execute_exercise(request, idp,ide):

    parcours = Parcours.objects.get(id= idp)
    exercise = Exercise.objects.get(id= ide)
    relation = Relationship.objects.get(parcours=parcours, exercise=exercise)
    request.session['level_id'] = exercise.level.id
    start_time =  time.time()
    today = time_zone_user(request.user)
    timer = today.time()

    context = {'exercise': exercise,  'start_time' : start_time,  'parcours' : parcours,  'relation' : relation , 'timer' : timer ,'today' : today , 'communications' : [] , 'relationships' : [] }
    return render(request, 'qcm/show_relation.html', context)





def store_the_score_relation_ajax(request):

    time_begin = request.POST.get("start_time",None)

    if time_begin :
        this_time = request.POST.get("start_time").split(",")[0]
        end_time  =  str(time.time()).split(".")[0]
        timer =  int(end_time) - int(this_time)
    else : 
        timer = 0

    numexo = int(request.POST.get("numexo"))-1    
    relation_id = int(request.POST.get("relation_id"))


    relation = Relationship.objects.get(pk = relation_id)
    data = {}
    print(request.user)
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        score = round(float(request.POST.get("score")),2)*100
        if score > 100 :
            score = 100
 
        if int(relation.situation) <= int(numexo+1):
            Studentanswer.objects.create(exercise  = relation.exercise , parcours  = relation.parcours ,  student  = student , numexo= numexo,  point= score, secondes = timer)
            result, createded = Resultexercise.objects.get_or_create(exercise  = relation.exercise , student  = student , defaults = { "point" : score , })
            if not createded :
                Resultexercise.objects.filter(exercise  = relation.exercise , student  = student).update(point= score)
 
            # Moyenne des scores obtenus par savoir faire enregistré dans Resultknowledge
            knowledge = relation.exercise.knowledge
            scored = 0
            studentanswers = Studentanswer.objects.filter(student = student,exercise__knowledge = knowledge) 
            for studentanswer in studentanswers:
                scored +=  studentanswer.point 
            try :
                scored = scored/len(studentanswers)
            except :
                scored = 0
            result, created = Resultknowledge.objects.get_or_create(knowledge  = relation.exercise.knowledge , student  = student , defaults = { "point" : scored , })
            if not created :
                Resultknowledge.objects.filter(knowledge  = relation.exercise.knowledge , student  = student).update(point= scored)
            

            # Moyenne des scores obtenus par compétences enregistrées dans Resultskill
            skills = relation.skills.all()
            for skill in skills :
                Resultskill.objects.create(student = student, skill = skill, point = score) 
                resultskills = Resultskill.objects.filter(student = student, skill = skill).order_by("-id")[0:10]
                sco = 0
                for resultskill in resultskills :
                    sco += resultskill.point
                    try :
                        sco_avg = sco/len(resultskills)
                    except :
                        sco_avg = 0
                result, creat = Resultlastskill.objects.get_or_create(student = student, skill = skill, defaults = { "point" : sco_avg , })
                if not creat :
                    Resultlastskill.objects.filter(student = student, skill = skill).update(point = sco_avg) 
                
                result, creater = Resultggbskill.objects.get_or_create(student = student, skill = skill, relationship = relation, defaults = { "point" : score , })
                if not creater :
                    Resultggbskill.objects.filter(student = student, skill = skill, relationship = relation).update(point = sco_avg) 


            try :
                if relation.exercise.supportfile.annoncement != "" :
                    name_title = relation.exercise.supportfile.annoncement
                else :
                    name_title = relation.exercise.knowledge.name
                msg = "Exercice : "+str(unescape_html(cleanhtml(name_title)))+"\n Fait par : "+str(student.user)+"\n Nombre de situations : "+str(numexo)+"\n Score : "+str(score)+"%"+"\n Temps : "+str(convert_seconds_in_time(timer))
                rec = []
                for g in student.students_to_group.filter(teacher = relation.parcours.teacher):
                    if not g.teacher.user.email in rec : 
                        rec.append(g.teacher.user.email)
 
                if g.teacher.notification :
                    send_mail("SacAdo Exercice posté",  msg , "info@sacado.xyz" , rec )

            except:
                pass
        try :
            nb_done = 0
            for exercise in relation.parcours.exercises.all() :
                if Studentanswer.objects.filter(exercise  = exercise , parcours  = relation.parcours ,  student  = student).count()>0 :
                    nb_done +=1

            if nb_done == relation.parcours.exercises.count() :
                redirect('index')
        except:
            pass

    return redirect('show_parcours_student' , relation.parcours.id )


def ajax_theme_exercice(request):
    level_id = request.POST.get('level_id', None)

    if level_id.isdigit():
        level = Level.objects.get(id=level_id)
        themes = level.themes.all()
        data = {'themes': serializers.serialize('json', themes)}
    else:
        data = {}

    return JsonResponse(data)


def ajax_level_exercise(request):

    teacher = Teacher.objects.get(user= request.user)
    data = {} 
    level_ids = request.POST.getlist('level_id')
    theme_ids = request.POST.getlist('theme_id')

    parcours_id = request.POST.get('parcours_id', None)
 

    if  parcours_id :
        parcours = Parcours.objects.get(id = int(parcours_id))
        ajax = True

    else :
        parcours = None
        ajax = False
        parcours_id = None

    datas = []
    levels_dict = {}
    levels_tab,knowledges_tab, exercises_tab    =   [],  [],  []

    for level_id in level_ids :
        level = Level.objects.get(pk=level_id)
        levels_dict = {}
        levels_dict["name"]=level 
 
        try :
            if theme_ids[0] != "" :
                themes = Theme.objects.filter(id__in=theme_ids).order_by("id")
            else :
                themes = level.themes.all().order_by("id")
        except :
            themes = level.themes.all().order_by("id")

        themes_tab =   []
        for theme in themes :
            themes_dict =  {}                
            themes_dict["name"]=theme
            knowlegdes = Knowledge.objects.filter(theme=theme,level=level).order_by("theme")
            knowledges_tab  =  []
            for knowledge in knowlegdes :
                knowledges_dict  =   {}  
                knowledges_dict["name"]=knowledge 
                exercises = Exercise.objects.filter(knowledge=knowledge,supportfile__is_title=0).order_by("theme")
                exercises_tab    =   []
                for exercise in exercises :
                    exercises_tab.append(exercise)
                knowledges_dict["exercises"]=exercises_tab
                knowledges_tab.append(knowledges_dict)
            themes_dict["knowledges"]=knowledges_tab
            themes_tab.append(themes_dict)
        levels_dict["themes"]=themes_tab
        datas.append(levels_dict)

    data['html'] = render_to_string('qcm/ajax_list_exercises.html', { 'datas': datas , "parcours" : parcours, "ajax" : ajax, "teacher" : teacher , "request" : request , 'parcours_id' : parcours_id })
 
    return JsonResponse(data)



def ajax_knowledge_exercise(request):
    theme_id = request.POST.get('theme_id', None)
    level_id = request.POST.get('level_id', None)
    data = {}
 
    knowledges = Knowledge.objects.filter(theme_id=theme_id,level_id=level_id )
    data = {'knowledges': serializers.serialize('json', knowledges)}


    return JsonResponse(data)

 
@csrf_exempt
def ajax_create_title_parcours(request):
    ''' Création d'une section ou d'une sous-section dans un parcours '''
    teacher = Teacher.objects.get(user=request.user)

    parcours_id = int(request.POST.get('parcours_id', 0))

    code = str(uuid.uuid4())[:8]
    data = {}

    form = AttachForm(request.POST, request.FILES)

    if form.is_valid():
        
        supportfile = form.save(commit=False)
        supportfile.knowledge_id = 1
        supportfile.author = teacher
        supportfile.code=code
        supportfile.level_id=1
        supportfile.theme_id=1
        supportfile.is_title=1
        supportfile.save()

        exe = Exercise.objects.create(knowledge_id=1, level_id=1, theme_id=1, supportfile=supportfile)
        relation = Relationship.objects.create(exercise=exe, parcours_id=parcours_id, order=0)

        parcours = Parcours.objects.get(pk = parcours_id)
        for student in parcours.students.all():
            relation.students.add(student)



        if supportfile.attach_file != "" :
            attachment = "<a href='#' target='_blank'>"+ supportfile.annoncement +"</a>"
        else :
            attachment = supportfile.annoncement


        data["html"] = f'''<div class="panel-body separation_dashed" style="line-height: 30px;  border-top-right-radius:5px; border-top-left-radius:5px; background-color : #F2F1F0;id='new_title{exe.id}'">
        <a href='#' style='cursor:move;' class='move_inside'>
            <i class="fas fa-grip-vertical fa-xs" style="color:MediumSeaGreen;vertical-align: text-top;padding-right:5px;"></i>
        </a>
        <input type='hidden' class='div_exercise_id' value='{exe.id}' name='input_exercise_id' />
            <h3>{attachment}
                <a href='#' data-exercise_id='{exe.id}' data-parcours_id='{parcours_id}' class='pull-right erase_title'>
                    <i class='fa fa-times text-danger'></i>
                </a>
            </h3>
        </div>'''

    return JsonResponse(data)



def ajax_erase_title(request):

    exercise_id = int(request.POST.get('exercise_id', None))
    parcours_id = int(request.POST.get('parcours_id', None))    
 
    data = {}

    Relationship.objects.get(exercise_id=exercise_id, parcours_id=parcours_id ).delete()
    Exercise.objects.get(pk = exercise_id ).delete()
 
    return JsonResponse(data)




def relation_is_done(request, id ): #id  = id_content
    relationship = Relationship.objects.get(pk=id)
    return redirect('show_parcours_student' , relationship.parcours.id )


def content_is_done(request, id ): #id  = id_content
    return redirect('exercises' )



# def ajax_search_exercise(request):

#     code =  request.POST.get("search") 
#     knowledges = Knowledge.objects.filter(name__contains= code)
#     exercises = Exercise.objects.filter(Q(knowledge__in = knowledges)|Q(supportfile__annoncement__contains= code)|Q(supportfile__code__contains= code)).filter(supportfile__is_title=0)
#     data = {}
#     html = render_to_string('qcm/search_exercises.html',{ 'exercises' : exercises  })
 
#     data['html'] = html       

#     return JsonResponse(data)



def ajax_search_exercise(request):

    code =  request.POST.get("search") 
    knowledges = Knowledge.objects.filter(name__contains= code)

    if request.user.user_type == 2 :
        teacher = Teacher.objects.get(user_id = request.user.id)
        parcours = parcours.teacher_parcours.all()

    elif request.user.user_type == 0 :
        student = Student.objects.get(user_id = request.user.id)
        parcours = student.students_to_parcours.all()
    else :
        parcours = None 
  

    relationships = Relationship.objects.filter(Q(exercise__knowledge__in = knowledges)|Q(exercise__supportfile__annoncement__contains= code)|Q(exercise__supportfile__code__contains= code)).filter(exercise__supportfile__is_title=0, parcours__in = parcours)
    data = {}
    html = render_to_string('qcm/search_exercises.html',{ 'relationships' : relationships  })
 
    data['html'] = html       

    return JsonResponse(data)



def create_evaluation(request):

    if not request.user.is_authenticated :
        redirect('index')

    teacher = Teacher.objects.get(user_id = request.user.id)
    levels =  teacher.levels.all()    
    form = ParcoursForm(request.POST or None, request.FILES or None, teacher = teacher)

    themes_tab = []
    for level in levels :
        for theme in level.themes.all():
            if not theme in themes_tab:
                themes_tab.append(theme)

    share_groups = Sharing_group.objects.filter(teacher  = teacher,role=1).order_by("group__level")
    groups = Group.objects.filter(teacher  = teacher).order_by("level")

    if form.is_valid():
        nf = form.save(commit=False)
        nf.author = teacher
        nf.teacher = teacher
        nf.is_evaluation = 1    
        nf.save()
        nf.students.set(form.cleaned_data.get('students'))
        i = 0
        for exercise in form.cleaned_data.get('exercises'):
            exercise = Exercise.objects.get(pk=exercise.id)
            relationship = Relationship.objects.create(parcours=nf, exercise=exercise, order=i, 
                                                       duration=exercise.supportfile.duration,
                                                       situation=exercise.supportfile.situation)
            relationship.students.set(form.cleaned_data.get('students'))
            relationship.skills.set(exercise.supportfile.skills.all()) 
            i += 1

        if request.POST.get("save_and_choose") :
            return redirect('peuplate_parcours', nf.id)
        else :
            return redirect('evaluations')   
    else:
        print(form.errors)


    try :
        if 'group_id' in request.session :
            if request.session.get["group_id"] :
                group_id = request.session["group_id"]
                group = Group.objects.get(pk = group_id) 
        else :
            group_id = None
            group = None
            request.session["group_id"]  = None            

    except :
        group_id = None
        group = None
        request.session["group_id"]  = None


    context = {'form': form, 'teacher': teacher, 'parcours': None, 'groups': groups, 'idg': 0,  'group_id': group_id ,  'relationships': [], 'communications' : [], 'share_groups' : share_groups , 
               'exercises': [], 'levels': levels, 'themes': themes_tab, 'students_checked': 0 , 'role':True}

    return render(request, 'qcm/form_evaluation.html', context)


#@user_is_parcours_teacher 
def update_evaluation(request, id, idg=0 ):
    teacher = Teacher.objects.get(user_id=request.user.id)
    levels = teacher.levels.all()

    parcours = Parcours.objects.get(id=id)

    if not authorizing_access(teacher, parcours,True):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    form = UpdateParcoursForm(request.POST or None, request.FILES or None, instance=parcours, teacher=teacher)

    """ affiche le parcours existant avant la modif en ajax"""
    exercises = parcours.exercises.filter(supportfile__is_title=0).order_by("theme")
    """ fin """
    themes_tab = []
    for level in levels:
        for theme in level.themes.all():
            if not theme in themes_tab:
                themes_tab.append(theme)

    groups = Group.objects.filter(teacher=teacher).prefetch_related('students').order_by("level")
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("order")
    share_groups = Sharing_group.objects.filter(teacher  = teacher,role=1).order_by("group__level")
    if request.method == "POST":
        if form.is_valid():
            nf = form.save(commit=False)
            nf.author = teacher
            nf.teacher = teacher
            nf.is_evaluation = 1 
            nf.save()
            nf.students.set(form.cleaned_data.get('students'))
            try:
                for exercise in parcours.exercises.all():
                    relationship = Relationship.objects.get(parcours=nf, exercise=exercise)
                    relationship.students.set(form.cleaned_data.get('students'))
            except:
                pass

            if request.POST.get("save_and_choose") :
                return redirect('peuplate_parcours', nf.id)
            elif idg == 99999999999:
                return redirect('index')
            elif idg == 0:
                return redirect('evaluations')
            else:
                return redirect('list_parcours_group', idg)

 
    if idg > 0 and idg < 99999999999 :
        group_id = idg
        request.session["group_id"] = idg
        group = Group.objects.get(pk = group_id) 
 
    else :
        group_id = None
        group = None
        request.session["group_id"] = None

    data = get_complement(request, teacher, parcours)
    role = data['role']


    students_checked = parcours.students.count()  # nombre d'étudiant dans le parcours

    context = {'form': form, 'parcours': parcours, 'groups': groups, 'idg': idg, 'teacher': teacher, 'group_id': group_id ,  'relationships': relationships, 'communications' : [], 'role': role,  'share_groups' : share_groups , 
               'exercises': exercises, 'levels': levels, 'themes': themes_tab, 'students_checked': students_checked}

    return render(request, 'qcm/form_evaluation.html', context)



 


def delete_evaluation(request,id):

    parcours = Parcours.objects.get(pk=id)
    teacher = Teacher.objects.get(user=request.user)

    if not authorizing_access(teacher, parcours,True):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    if parcours.teacher == teacher :
        parcours.exercices.clear() 
        parcours.delete() 
    return redirect('index')



#@user_is_parcours_teacher 
def show_evaluation(request, id):

    parcours = Parcours.objects.get(id=id)
    teacher =  parcours.teacher 

    if not authorizing_access(teacher, parcours,True):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("order")
    nb_exo_only, nb_exo_visible = [], []
    i ,j = 0, 0
    for r in relationships:
        if r.exercise.supportfile.is_title or r.exercise.supportfile.is_subtitle:
            i = 0
        else:
            i += 1
        nb_exo_only.append(i)
        if r.exercise.supportfile.is_title or r.exercise.supportfile.is_subtitle or r.is_publish == 0:
            j = 0
        else:
            j += 1
        nb_exo_visible.append(j)


    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id']  

    customexercises = Customexercise.objects.filter(teacher=teacher).order_by("ranking")

 

    nb_exo_only_c, nb_exo_visible_c = [] , []
    for ce in customexercises:
        i += 1
        nb_exo_only_c.append(i)
        if ce.is_publish :
            j += 1
        nb_exo_visible_c.append(j)


    students_p_or_g = students_from_p_or_g(request,parcours)

    nb_students_p_or_g = len(students_p_or_g)

    skills = Skill.objects.all()

    nb_exercises = parcours.exercises.filter(supportfile__is_title=0).count()
    context = {'relationships': relationships, 'parcours': parcours, 'teacher': teacher, 'skills': skills, 'communications' : [] ,  'customexercises': customexercises, 
                'nb_exo_only_c': nb_exo_only_c,'nb_exo_visible_c': nb_exo_visible_c,
               'students_from_p_or_g': students_p_or_g, 'nb_exercises': nb_exercises, 'nb_exo_visible': nb_exo_visible, 'nb_students_p_or_g' : nb_students_p_or_g , 
               'nb_exo_only': nb_exo_only, 'group_id': group_id, 'group': group, 'role' : role }

    return render(request, 'qcm/show_parcours.html', context)


 
#####################################################################################################################################
#####################################################################################################################################
######   Correction des exercices
#####################################################################################################################################
#####################################################################################################################################



def correction_exercise(request,id,idp,ids=0):

    teacher = Teacher.objects.get(user=request.user)
    stage = get_stage(teacher.user)
    formComment = CommentForm(request.POST or None )

    comments = Comment.objects.filter(teacher = teacher)

    if ids > 0 :
        student = Student.objects.get(pk=ids)
    else : 
        student = None

    nb = 0
    if idp == 0 :
        relationship = Relationship.objects.get(pk=id)

        if student :
            if Writtenanswerbystudent.objects.filter(relationship = relationship , student = student).exists():
                w_a = Writtenanswerbystudent.objects.get(relationship = relationship , student = student)
                annotations = Annotation.objects.filter(writtenanswerbystudent = w_a)
                nb = annotations.count()
            else :
                w_a = False
                annotations = [] 
        else :
            w_a = False 
            annotations = [] 

        context = {'relationship': relationship,  'teacher': teacher, 'stage' : stage , 'comments' : comments   , 'formComment' : formComment , 'custom':0, 'nb':nb, 'w_a':w_a, 'annotations':annotations,  'communications' : [] ,  'parcours' : relationship.parcours , 'parcours_id': relationship.parcours.id, 'group' : None , 'student' : student }
 
        return render(request, 'qcm/correction_exercise.html', context)
    else :
        customexercise = Customexercise.objects.get(pk=id)
        parcours = Parcours.objects.get(pk = idp)
 
        if student :
            if Customanswerbystudent.objects.filter(customexercise = customexercise ,  parcours = parcours , student_id = student).exists():
                c_e = Customanswerbystudent.objects.get(customexercise = customexercise ,  parcours = parcours , student_id = student)
                customannotations = Customannotation.objects.filter(customanswerbystudent = c_e)
                nb = customannotations.count()
            else :
                c_e = False 
                customannotations = []
        else :
            c_e = False 
            customannotations = []
        context = {'customexercise': customexercise,  'teacher': teacher, 'stage' : stage , 'comments' : comments   , 'formComment' : formComment , 'nb':nb,'c_e':c_e, 'customannotations':customannotations,  'custom':1,  'communications' : [], 'parcours' : parcours, 'group' : None , 'parcours_id': parcours.id, 'student' : student }
 
        return render(request, 'qcm/correction_custom_exercise.html', context)




@csrf_exempt  
def ajax_save_annotation(request):

    data = {}

    custom =  int(request.POST.get("custom"))
    answer_id =  request.POST.get("answer_id") 
    attr_id = request.POST.get("attr_id") 
    style = request.POST.get("style") 
    classe = request.POST.get("classe") 
    studentcontent = request.POST.get("studentcontent") 

    if custom :
        annotation, created = Customannotation.objects.get_or_create(customanswerbystudent_id = answer_id,attr_id = attr_id , defaults = {  'classe' : classe, 'style' : style , 'content' : studentcontent} )
        if not created :
            Customannotation.objects.filter(customanswerbystudent_id = answer_id, attr_id = attr_id).update(content = studentcontent, style = style)
    else :
        annotation, created = Annotation.objects.get_or_create(writtenanswerbystudent_id = answer_id,attr_id = attr_id , defaults = {  'classe' : classe, 'style' : style , 'content' : studentcontent} )
        if not created :
            Annotation.objects.filter(writtenanswerbystudent_id = answer_id, attr_id = attr_id).update(content = studentcontent, style = style)

    return JsonResponse(data)  



@csrf_exempt  
def ajax_remove_annotation(request):
    """
    Suppression d'une appréciation par un enseignant
    """

    data = {}
    custom =  int(request.POST.get("custom"))
    attr_id = request.POST.get("attr_id") 
    teacher = Teacher.objects.get(user = request.user)
    try :
        if custom :
            Customannotation.objects.get(customanswerbystudent__customexercise__teacher= teacher,  attr_id = attr_id ).delete()
        else :  
            Annotation.objects.get(writtenanswerbystudent__relationship__parcours__teacher = teacher, attr_id = attr_id).delete()
    except :
        pass

    return JsonResponse(data)  


####Sélection des élèves par AJAX --- N'est pas utilisé ---A supprimer éventuellement avec son url 
def ajax_choose_student(request): # Ouvre la page de la réponse des élèves à un exercice non auto-corrigé

    relationship_id =  int(request.POST.get("relationship_id")) 
    student_id =  int(request.POST.get("student_id"))
    student = Student.objects.get(pk = student_id)   
    data = {}
    custom = int(request.POST.get("custom"))

 
    comments = Comment.objects.filter(teacher = teacher)
 
    if request.POST.get("custom") == "0" :

        relationship = Relationship.objects.get(pk = int(relationship_id))
        teacher = relationship.parcours.teacher
        if Writtenanswerbystudent.objects.filter(relationship = relationship , student = student).exists():
            w_a = Writtenanswerbystudent.objects.get(relationship = relationship , student = student)
        else :
            w_a = False 
     
        context = { 'relationship' : relationship , 'student': student ,   'w_a' : w_a,   'teacher' : teacher, 'comments' : comments      }

        html = render_to_string('qcm/ajax_correction_exercise.html', context )   

    else :

        customexercise = Customexercise.objects.get(pk = relationship_id)
        parcours_id =  int(request.POST.get("parcours_id"))
        parcours = Parcours.objects.get(pk = parcours_id)
        teacher = customexercise.teacher
        if Customanswerbystudent.objects.filter(customexercise = customexercise ,  parcours = parcours , student = student).exists():
            c_e = Customanswerbystudent.objects.get(customexercise = customexercise ,   parcours = parcours , student = student )
        else :
            c_e = False 

        context = { 'customexercise' : customexercise , 'student': student ,   'c_e' : c_e , 'parcours_id' :  parcours_id,   'teacher' : teacher , 'comments' : comments  }

        html = render_to_string('qcm/ajax_correction_exercise_custom.html', context )
     
    data['html'] = html       

    return JsonResponse(data)







def ajax_exercise_evaluate(request): # Evaluer un exercice non auto-corrigé


    student_id =  int(request.POST.get("student_id"))
    value =  int(request.POST.get("value"))
    typ =  int(request.POST.get("typ")) 
    data = {}

    student = Student.objects.get(user_id = student_id)  

    stage = get_stage(student.user) 
    tab_label = ["","text-danger","text-warning","text-success","text-primary"]
    tab_value = [-1, stage.low-1,stage.medium-1,stage.up-1,100]       

    if typ == 0 : 

        knowledge_id = request.POST.get("knowledge_id",None)       
        skill_id = request.POST.get("skill_id",None)

        relationship_id =  int(request.POST.get("relationship_id"))   
        relationship = Relationship.objects.get(pk = relationship_id)
        if tab_value[value] > -1 :

            if knowledge_id :
                studentanswer, creator = Studentanswer.objects.get_or_create(parcours = relationship.parcours, exercise = relationship.exercise, student = student , defaults={"point" : tab_value[value] , 'secondes' : 0} )
                if not creator :
                    Studentanswer.objects.filter(parcours  = relationship.parcours, exercise = relationship.exercise , student  = student).update(point= tab_value[value])
                # Moyenne des scores obtenus par savoir faire enregistré dans Resultknowledge
                knowledge = relationship.exercise.knowledge
                scored = 0
                studentanswers = Studentanswer.objects.filter(student = student,exercise__knowledge = knowledge) 
                for studentanswer in studentanswers:
                    scored +=  studentanswer.point 
                try :
                    scored = scored/len(studentanswers)
                except :
                    scored = 0
                result, created = Resultknowledge.objects.get_or_create(knowledge  = relationship.exercise.knowledge , student  = student , defaults = { "point" : scored , })
                if not created :
                    Resultknowledge.objects.filter(knowledge  = relationship.exercise.knowledge , student  = student).update(point= scored)
                
                resultat, crtd = Writtenanswerbystudent.objects.get_or_create(relationship  = relationship  , student  = student , defaults = { "is_corrected" : True , })
                if not crtd :
                    Writtenanswerbystudent.objects.filter(relationship  = relationship  , student  = student).update(is_corrected = True)


            if skill_id :
            # Moyenne des scores obtenus par compétences enregistrées dans Resultskill
                skill = Skill.objects.get(pk = skill_id )
                Resultskill.objects.create(student = student, skill = skill, point = tab_value[value]) 
                resultskills = Resultskill.objects.filter(student = student, skill = skill).order_by("-id")[0:10]
                sco = 0
                for resultskill in resultskills :
                    sco += resultskill.point
                    try :
                        sco_avg = sco/len(resultskills)
                    except :
                        sco_avg = 0
                result, creat = Resultlastskill.objects.get_or_create(student = student, skill = skill, defaults = { "point" : sco_avg , })
                if not creat :
                    Resultlastskill.objects.filter(student = student, skill = skill).update(point = sco_avg) 

                result, creater = Resultggbskill.objects.get_or_create(student = student, skill = skill, relationship = relationship, defaults = { "point" : tab_value[value] , })
                if not creater :
                    Resultggbskill.objects.filter(student = student, skill = skill, relationship = relationship).update(point = tab_value[value]) 

            data['eval'] = "<i class = 'fa fa-check text-success pull-right'></i>"       
        else :
            data['eval'] = ""
  
    else :
       
        customexercise_id =  int(request.POST.get("customexercise_id"))  
 
        parcours_id =  int(request.POST.get("parcours_id")) 
        knowledge_id = request.POST.get("knowledge_id",None)       
        skill_id = request.POST.get("skill_id",None)

        this_custom = Customanswerbystudent.objects.filter(parcours_id = parcours_id , customexercise_id = customexercise_id, student = student)
        this_custom.update(is_corrected= 1)

        if tab_value[value] > -1 :

            if skill_id : 
                result, created = Correctionskillcustomexercise.objects.get_or_create(parcours_id = parcours_id , customexercise_id = customexercise_id, student  = student , skill_id = skill_id   , defaults = { "point" : tab_value[value]  })
                if not created :
                    Correctionskillcustomexercise.objects.filter(parcours_id = parcours_id , customexercise_id = customexercise_id, student  = student, skill_id = skill_id ).update(point= tab_value[value] )

            if knowledge_id : 
                result, created = Correctionknowledgecustomexercise.objects.get_or_create(parcours_id = parcours_id , customexercise_id = customexercise_id, student  = student , knowledge_id = knowledge_id  ,  defaults = {  "point" : tab_value[value]  })
                if not created :
                    Correctionknowledgecustomexercise.objects.filter(parcours_id = parcours_id , customexercise_id = customexercise_id, student  = student , knowledge_id = knowledge_id ).update(point= tab_value[value] )

            data['eval'] = "<i class = 'fa fa-check text-success pull-right'></i>"       
        else :
            data['eval'] = ""

    return JsonResponse(data)  




def ajax_mark_evaluate(request): # Evaluer un exercice custom par note

    student_id =  int(request.POST.get("student_id"))
    customexercise_id =  int(request.POST.get("customexercise_id"))  
    parcours_id =  int(request.POST.get("parcours_id")) 
    mark =  request.POST.get("mark")
    data = {}
    this_custom = Customanswerbystudent.objects.filter(parcours_id = parcours_id , customexercise_id = customexercise_id, student_id = student_id)
    this_custom.update(is_corrected= 1)
    this_custom.update(point= mark)

    data['eval'] = "<i class = 'fa fa-check text-success pull-right'></i>"             

    return JsonResponse(data)  





def ajax_comment_all_exercise(request): # Ajouter un commentaire à un exercice non auto-corrigé

    student_id =  int(request.POST.get("student_id"))
    comment =  cleanhtml(unescape_html(request.POST.get("comment")))

    exercise_id =  int(request.POST.get("exercise_id"))  

    student = Student.objects.get(user_id = student_id)  

    if int(request.POST.get("typ")) == 0 :
        relationship = Relationship.objects.get(pk = exercise_id)
        Writtenanswerbystudent.objects.filter(relationship = relationship, student = student).update(comment = comment )
        Writtenanswerbystudent.objects.filter(relationship = relationship, student = student).update(is_corrected = 1 )
    else  :
        parcours_id =  int(request.POST.get("parcours_id"))     
        ce = Customexercise.objects.get(pk = exercise_id)
        Customanswerbystudent.objects.filter(customexercise = ce, student = student, parcours_id = parcours_id).update(comment = comment )
        Customanswerbystudent.objects.filter(customexercise = ce, student = student, parcours_id = parcours_id).update(is_corrected = 1 )

    data = {}
    data['eval'] = "<i class = 'fa fa-check text-success pull-right'></i>"          
    return JsonResponse(data)  




@csrf_exempt
def ajax_audio_comment_all_exercise(request): # Ajouter un commentaire à un exercice non auto-corrigé


    data = {}
    student_id =  int(request.POST.get("id_student"))
    audio_text = request.FILES.get("id_mediation")
    student = Student.objects.get(user_id = student_id)

    id_relationship =  int(request.POST.get("id_relationship"))  

    if int(request.POST.get("custom")) == 0 :
        relationship = Relationship.objects.get(pk = id_relationship)

        if Writtenanswerbystudent.objects.filter(student = student , relationship = relationship).exists() :
            w_a = Writtenanswerbystudent.objects.get(student = student , relationship = relationship) # On récupère la Writtenanswerbystudent
            form = WAnswerAudioForm(request.POST or None, request.FILES or None,instance = w_a )
        else :
            form = WAnswerAudioForm(request.POST or None, request.FILES or None )

        if form.is_valid() :
            nf =  form.save(commit = False)
            nf.audio = audio_text
            nf.relationship = relationship
            nf.student = student
            nf.is_corrected = True                     
            nf.save()

    else  :

        parcours_id =  int(request.POST.get("id_parcours"))  
        parcours = Parcours.objects.get(pk = parcours_id)
        customexercise = Customexercise.objects.get(pk = id_relationship)
        
        if Customanswerbystudent.objects.filter(customexercise  = customexercise, student = student , parcours = parcours).exists() :
            c_e = Customanswerbystudent.objects.get(customexercise  = customexercise, student = student , parcours = parcours) # On récupère la Customanswerbystudent
            form = CustomAnswerAudioForm(request.POST or None, request.FILES or None,instance = c_e )
        else :
            form = CustomAnswerAudioForm(request.POST or None, request.FILES or None )

        if form.is_valid() :
            nf =  form.save(commit = False)
            nf.audio = audio_text
            nf.customexercise = customexercise
            nf.student = student
            nf.parcours = parcours
            nf.is_corrected = True    
            nf.save()

    data = {}
    data['eval'] = "<i class = 'fa fa-check text-success pull-right'></i>"          
    return JsonResponse(data)  




@csrf_exempt  
def audio_remediation(request):

    data = {}
    idr =  int(request.POST.get("id_relationship"))
    relationship = Relationship.objects.get(pk=idr) 
    form = RemediationForm(request.POST or None, request.FILES or None )

    if form.is_valid():
        nf =  form.save(commit = False)
        nf.mediation = request.FILES.get("id_mediation")
        nf.relationship = relationship
        nf.audio = True
        nf.save()
    else:
        print(form.errors)

    return JsonResponse(data)  



 
###################################################################
######   Création des commentaires de correction
###################################################################
@csrf_exempt  
def ajax_create_or_update_appreciation(request):

    data = {}
    comment_id = request.POST.get("comment_id",None)
    comment = request.POST.get("comment",None)
    teacher = Teacher.objects.get(user = request.user)

    # Choix du formulaire à compléter
    if comment_id :
        appreciation = Comment.objects.get(pk = int(comment_id) )
        formComment = CommentForm(request.POST or None, instance = appreciation ) # Formulaire existant
    else :
        formComment = CommentForm(request.POST or None ) # Formulaire nouvelle appréciation
 
    if formComment.is_valid(): # Analyse du formulaire
        nf =  formComment.save(commit = False)
        nf.teacher = teacher
        nf.save() # Enregistrement

    if comment_id :
        data["comment_id"] = nf.pk
        data["comment"] = nf.comment
    else :
        nb = Comment.objects.filter(teacher= teacher).count() + 1
        data["html"] = "<button id='comment"+str(nb)+"' data-nb="+str(nb)+" data-text=\""+str(nf.comment)+"\" class='btn btn-default comment'>"+str(nf.comment)+"</button>"

    return JsonResponse(data)  





@csrf_exempt  
def ajax_remove_my_appreciation(request):

    data = {}
    comment_id = request.POST.get("comment_id")
    appreciation = Comment.objects.get(pk = int(comment_id) )
    appreciation.delete()

    return JsonResponse(data)  


#####################################################################################################################################
#####################################################################################################################################
######   Fin des outils de correction
#####################################################################################################################################
#####################################################################################################################################


 
def parcours_create_custom_exercise(request,id,typ): #Création d'un exercice non autocorrigé dans un parcours

    parcours = Parcours.objects.get(pk=id)
    teacher = Teacher.objects.get(user= request.user)
    stage = get_stage(teacher.user)


    if not authorizing_access(teacher, parcours,True):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    ceForm = CustomexerciseForm(request.POST or None, request.FILES or None , teacher = teacher , parcours = parcours) 


    if request.method == "POST" :
        if ceForm.is_valid() :
            nf = ceForm.save(commit=False)
            nf.teacher = teacher
            nf.save()
            ceForm.save_m2m()
            nf.parcourses.add(parcours)            
        else :
            print(ceForm.errors)
        return redirect('show_parcours', parcours.id )
 
    context = {'parcours': parcours,  'teacher': teacher, 'stage' : stage ,  'communications' : [] , 'form' : ceForm , 'customexercise' : False }

    return render(request, 'qcm/form_exercise_custom.html', context)


 
def parcours_update_custom_exercise(request,idcc,id): # Modification d'un exercice non autocorrigé dans un parcours

    custom = Customexercise.objects.get(pk=idcc)

    teacher = Teacher.objects.get(user= request.user)
    stage = get_stage(teacher.user)

    if id == 0 :

        if not authorizing_access(teacher, custom ,True):
            messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
            return redirect('index')

        ceForm = CustomexerciseNPForm(request.POST or None, request.FILES or None , teacher = teacher ,  custom = custom, instance = custom ) 

        if request.method == "POST" :
            if ceForm.is_valid() :
                nf = ceForm.save(commit=False)
                nf.teacher = teacher
                nf.save()
                ceForm.save_m2m()
            else :
                print(ceForm.errors)
            return redirect('exercises' )
     
        context = {  'teacher': teacher, 'stage' : stage ,  'communications' : [] , 'form' : ceForm , 'customexercise' : custom ,'parcours': None, }

    else :
 
        parcours = Parcours.objects.get(pk=id)
        if not authorizing_access(teacher, parcours,True):
            messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
            return redirect('index')

        ceForm = CustomexerciseForm(request.POST or None, request.FILES or None , teacher = teacher , parcours = parcours, instance = custom ) 

        if request.method == "POST" :
            if ceForm.is_valid() :
                nf = ceForm.save(commit=False)
                nf.teacher = teacher
                nf.save()
                ceForm.save_m2m()
                nf.parcourses.add(parcours)
            else :
                print(ceForm.errors)
            return redirect('show_parcours', parcours.id )
     
        context = {'parcours': parcours,  'teacher': teacher, 'stage' : stage ,  'communications' : [] , 'form' : ceForm , 'customexercise' : custom }

    return render(request, 'qcm/form_exercise_custom.html', context)


 

#@user_is_parcours_teacher 
def parcours_delete_custom_exercise(request,idcc,id): # Suppression d'un exercice non autocorrigé dans un parcours

    teacher = Teacher.objects.get(user=request.user)
    custom = Customexercise.objects.get(pk=idcc)
    teacher = Teacher.objects.get(user= request.user)

    if not authorizing_access(teacher, custom,True):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    if id == 0 :   
        custom.delete() 
        return redirect('exercises')
    else :
        parcours = Parcours.objects.get(pk=id)
        custom.parcourses.remove(parcours)
        custom.delete() 
        return redirect('show_parcours', parcours.id )



def write_exercise(request,id): # Coté élève
 
    student = Student.objects.get(user = request.user)  
    relationship = Relationship.objects.get(pk = id)


    if not authorizing_access_student(student, relationship):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    today = time_zone_user(student.user)
    if Writtenanswerbystudent.objects.filter(student = student, relationship = relationship ).exists() : 
        w = Writtenanswerbystudent.objects.get(student = student, relationship = relationship )
        wForm = WrittenanswerbystudentForm(request.POST or None, request.FILES or None, instance = w )    
    else :
        wForm = WrittenanswerbystudentForm(request.POST or None, request.FILES or None ) 

    if request.method == "POST":

        if wForm.is_valid():
            w_f = wForm.save(commit=False)
            w_f.relationship = relationship
            w_f.student = student         
            w_f.save()

            ### Envoi de mail à l'enseignant
            msg = "Exercice posté par : "+str(student.user) 
            if relationship.parcours.teacher.notification :
                send_mail("SACADO Exercice posté",  msg , "info@sacado.xyz" , [relationship.parcours.teacher.user.email] )

            return redirect('show_parcours_student' , relationship.parcours.id )


    context = {'relationship': relationship, 'communications' : [] , 'parcours' : relationship.parcours ,  'form' : wForm, 'today' : today  }

    if relationship.exercise.supportfile.is_python :
        url = "basthon/index.html" 
    else :
        url = "qcm/form_writing.html" 

    return render(request, url , context)






def write_custom_exercise(request,id,idp): # Coté élève - exercice non autocorrigé
 
    student = Student.objects.get(user = request.user)  
    customexercise = Customexercise.objects.get(pk = id)
    parcours = Parcours.objects.get(pk = idp)
    today = time_zone_user(student.user)

    if not authorizing_access_student(student, parcours):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    if Customanswerbystudent.objects.filter(student = student, customexercise = customexercise ).exists() : 
        ce = Customanswerbystudent.objects.get(student = student, customexercise = customexercise )
        cForm = CustomanswerbystudentForm(request.POST or None, request.FILES or None, instance = ce )    
    else :
        cForm = CustomanswerbystudentForm(request.POST or None, request.FILES or None ) 

    if request.method == "POST":

        if cForm.is_valid():
            w_f = cForm.save(commit=False)
            w_f.customexercise = customexercise
            w_f.parcours_id = idp
            w_f.student = student
            w_f.save()

            ### Envoi de mail à l'enseignant
            msg = "Exercice posté par : "+str(student.user) 
            if customexercise.teacher.notification :
                send_mail("SACADO Exercice posté",  msg , "info@sacado.xyz" , [customexercise.teacher.user.email] )

            return redirect('show_parcours_student' , idp )


    context = {'customexercise': customexercise, 'communications' : [] , 'form' : cForm , 'parcours' : parcours ,'student' : student, 'today' : today }

    if customexercise.is_python :
        url = "basthon/index_custom.html" 
    else :
        url = "qcm/form_writing_custom.html" 

    return render(request, url , context)


#######################################################################################################################################################################
############### VUE ENSEIGNANT
#######################################################################################################################################################################

def show_write_exercise(request,id): # vue pour le prof de l'exercice non autocorrigé par le prof

    relationship = Relationship.objects.get(pk = id)
    parcours = relationship.parcours
    today = timezone.now()

    wForm = WrittenanswerbystudentForm(request.POST or None, request.FILES or None )

    context = { 'relationship' : relationship, 'communications' : [] ,  'parcours' : parcours , 'today' : today ,  'form' : wForm,  'student' : None, }

    if relationship.exercise.supportfile.is_python :
        url = "basthon/index.html" 
    else :
        url = "qcm/form_writing.html" 

    return render(request, url , context)


def show_custom_exercise(request,id,idp): # vue pour le prof de l'exercice non autocorrigé par le prof

    customexercise = Customexercise.objects.get(pk = id)
    parcours = Parcours.objects.get(pk = idp)
    today = timezone.now()

    context = { 'customexercise' : customexercise, 'communications' : [] ,  'parcours' : parcours , 'today' : today , 'student' : None, }

    if customexercise.is_python :
        url = "basthon/index_custom.html" 
    else :
        url = "qcm/form_writing_custom.html" 

    return render(request, url , context)

#######################################################################################################################################################################
#######################################################################################################################################################################
#################   Task
#######################################################################################################################################################################
#######################################################################################################################################################################

  
def detail_task_parcours(request,id,s):

  
    parcours = Parcours.objects.get(pk=id) 
    teacher = parcours.teacher

    today = time_zone_user(teacher.user)
    date_today = today.date() 

    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id'] 
    access = data['access']
    if not authorizing_access(teacher, parcours,access):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')
    if s == 0 : # groupe

        relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours =parcours,exercise__supportfile__is_title=0).exclude(date_limit=None).order_by("-date_limit")  
        context = {'relationships': relationships, 'parcours': parcours , 'today':today ,  'communications' : [] ,  'date_today':date_today ,  'group_id' : group_id ,  'role' : role ,  }
 
        return render(request, 'qcm/list_tasks.html', context)
    else : # exercice

        exercise = Exercise.objects.get(pk=s)
        students = students_from_p_or_g(request,parcours) 
        details_tab = []
        for s in students :
            details = {}
            details["student"]=s.user
            try : 
                studentanswer = Studentanswer.objects.filter(exercise= exercise, student = s).last()
                details["point"]= studentanswer.point
                details["numexo"]=  studentanswer.numexo
                details["date"]= studentanswer.date 
                details["secondes"]= convert_seconds_in_time(int(studentanswer.secondes))
            except :
                details["point"]= ""
                details["numexo"]=  ""
                details["date"]= ""
                details["secondes"]= ""
            details_tab.append(details)

        relationship = Relationship.objects.get( parcours =parcours,exercise= exercise)
         
        context = {'details_tab': details_tab, 'parcours': parcours ,   'exercise' : exercise , 'relationship': relationship,  'date_today' : date_today, 'communications' : [] ,  'group_id' : group_id , 'role' : role }

        return render(request, 'qcm/task.html', context)


 
def detail_task(request,id,s):

    parcours = Parcours.objects.get(pk=id) 
    teacher = Teacher.objects.get(user= request.user)

    today = time_zone_user(teacher.user) 

    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id'] 
    access = data['access']
    
    if not authorizing_access(teacher, parcours,access):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    if s == 0 : # groupe
 
        relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours =parcours,exercise__supportfile__is_title=0).exclude(date_limit=None).order_by("-date_limit")  
        context = {'relationships': relationships, 'parcours': parcours , 'today':today ,   'communications' : [],  'role' : role ,  'group_id' : group_id }
        return render(request, 'qcm/list_tasks.html', context)
    else : # exercice

        exercise = Exercise.objects.get(pk=s)
        students = students_from_p_or_g(request,parcours) 
        details_tab = []
        for s in students :
            details = {}
            details["student"]=s.user
            try : 
                studentanswer = Studentanswer.objects.filter(exercise= exercise, student = s).last()
                details["point"]= studentanswer.point
                details["numexo"]=  studentanswer.numexo
                details["date"]= studentanswer.date 
                details["secondes"]= convert_seconds_in_time(int(studentanswer.secondes))
            except :
                details["point"]= ""                      
                details["numexo"]=  ""
                details["date"]= ""
                details["secondes"]= ""
            details_tab.append(details)

        relationship = Relationship.objects.get( parcours =parcours,exercise= exercise)


        context = {'details_tab': details_tab, 'parcours': parcours ,   'exercise' : exercise , 'relationship': relationship,  'today' : today ,  'communications' : [],  'role' : role ,  'group_id' : group_id}

        return render(request, 'qcm/task.html', context)



def all_my_tasks(request):
    today = time_zone_user(request.user) 
    teacher = Teacher.objects.get(user = request.user) 
    parcourses = Parcours.objects.filter(is_publish=  1,teacher=teacher ) 
    relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__teacher=teacher, date_limit__gte=today,exercise__supportfile__is_title=0).order_by("parcours") 
    context = {'relationships': relationships, 'parcourses': parcourses, 'parcours': None,  'communications' : [] , 'relationships' : [] , 'group_id' : None  , 'role' : False , }
    return render(request, 'qcm/all_tasks.html', context)



def these_all_my_tasks(request):
    today = time_zone_user(request.user) 
    teacher = Teacher.objects.get(user = request.user) 
    parcourses = Parcours.objects.filter(is_publish=  1,teacher=teacher ) 
    relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__teacher=teacher, exercise__supportfile__is_title=0).exclude(date_limit=None).order_by("parcours") 
    context = {'relationships': relationships, 'parcourses': parcourses, 'parcours': None,  'communications' : [] ,  'relationships' : [] ,'group_id' : None  , 'role' : False , } 
    return render(request, 'qcm/all_tasks.html', context)



 

def group_tasks(request,id):


    group = Group.objects.get(pk = id)
    teacher = Teacher.objects.get(user= request.user)
    today = time_zone_user(teacher.user) 

    nb_parcours_teacher = teacher.teacher_parcours.count() # nombre de parcours pour un prof
    students = group.students.prefetch_related("students_to_parcours")
    parcourses_tab = []
    for student in students :
        parcourses = student.students_to_parcours.all()
        for p in parcourses :
            if len(parcourses_tab) >= nb_parcours_teacher :
                break
            else :
                parcourses_tab.append(p)

    data = get_complement(request, teacher, group)
    role = data["role"]
    group_id = data["group_id"]

    relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__in=parcourses_tab, date_limit__gte=today,exercise__supportfile__is_title=0).order_by("parcours") 
    context = { 'relationships': relationships , 'group' : group , 'parcours' : None , 'communications' : [] , 'relationships' : [] , 'group_id' : group.id , 'role' : role , }

    return render(request, 'qcm/group_task.html', context)


def group_tasks_all(request,id):

    group = Group.objects.get(pk = id)
    teacher = Teacher.objects.get(user= request.user)
    today = time_zone_user(teacher.user) 
    nb_parcours_teacher = teacher.teacher_parcours.count() # nombre de parcours pour un prof

    students = group.students.prefetch_related("students_to_parcours")
    parcourses_tab = []
    for student in students :
        parcourses = student.students_to_parcours.all()
        for p in parcourses :
            if len(parcourses_tab) >= nb_parcours_teacher :
                break
            else :
                parcourses_tab.append(p)


    data = get_complement(request, teacher, group)
    role = data["role"]
    group_id = data["group_id"]

    relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today),  parcours__in=parcourses_tab, exercise__supportfile__is_title=0).exclude(date_limit=None).order_by("parcours") 
    context = { 'relationships': relationships ,    'group' : group , 'parcours' : None , 'relationships' : [] , 'communications' : [] ,  'group_id' : group.id , 'role' : role ,  }
    
    return render(request, 'qcm/group_task.html', context )




#######################################################################################################################################################################
#######################################################################################################################################################################
#################   Remédiation
#######################################################################################################################################################################
#######################################################################################################################################################################
@csrf_exempt 
@user_passes_test(user_is_superuser)
def create_remediation(request,idr): # Pour la partie superadmin

    relationship = Relationship.objects.get(pk=idr) 
    form = RemediationForm(request.POST or None,request.FILES or None, teacher = relationship.parcours.teacher)

    if form.is_valid():
        nf =  form.save(commit = False)
        nf.relationship = relationship
        nf.save()
        nf.exercises.add(exercise)
        form.save_m2m()
        return redirect('admin_exercises')

    context = {'form': form,  'exercise' : exercise}

    return render(request, 'qcm/form_remediation.html', context)

 
@csrf_exempt 
@user_passes_test(user_is_superuser)
def update_remediation(request,idr, id): # Pour la partie superadmin

    remediation = Remediation.objects.get(id=id)
    teacher = Teacher.objects.get(user = request.user)
    exercise = Exercise.objects.get(pk=ide) 
    form = RemediationUpdateForm(request.POST or None, request.FILES or None, instance=remediation, teacher = teacher  )
 
    if form.is_valid():
        nf.save()
        return redirect('exercises')

    context = {'form': form,  'exercise' : exercise}

    return render(request, 'qcm/form_remediation.html', context )


@csrf_exempt 
@user_passes_test(user_is_superuser)
def delete_remediation(request, id): # Pour la partie superadmin
    remediation = Remediation.objects.get(id=id)
    remediation.delete()

    return redirect('exercises')



@csrf_exempt 
def show_remediation(request, id):

    remediation = Remediation.objects.get(id=id)

    if remediation.video != "" :
        video_url = remediation.video
    else : 
        try : 
            video_url = None         
            ext = remediation.mediation[-3:]
            if ext == "ggb" : 
                ggb_file = True
            else :
                ggb_file = False
        except :
            video_url = None        
            ggb_file = False

    context = {'remediation': remediation, 'video_url': video_url, 'ggb_file': ggb_file   }
    
    return render(request, 'qcm/show_remediation.html', context)



@csrf_exempt 
def ajax_remediation(request):

    parcours_id =  request.POST.get("parcours_id",None) 

    if parcours_id :
        parcours_id =  int(request.POST.get("parcours_id"))
        customexercise_id =  int(request.POST.get("customexercise_id"))
        customexercise = Customexercise.objects.get( id = customexercise_id)

        form = RemediationcustomForm(request.POST or None,request.FILES or None, teacher = customexercise.teacher)
        data = {}

        remediations = Remediationcustom.objects.filter(customexercise = customexercise)

        context = {'form': form,  'customexercise' : customexercise ,  'remediations' : remediations , 'relationship' : None , 'parcours_id' : parcours_id   } 

    else :
        
        relationship_id =  int(request.POST.get("relationship_id"))
        relationship = Relationship.objects.get( id = relationship_id)

        form = RemediationForm(request.POST or None,request.FILES or None, teacher = relationship.parcours.teacher)
        data = {}

        remediations = Remediation.objects.filter(relationship = relationship)

        context = {'form': form,  'relationship' : relationship ,  'remediations' : remediations, 'customexercise' : None , 'parcours_id' : relationship.parcours.id   } 
    
    html = render_to_string('qcm/ajax_remediation.html',context)
    data['html'] = html       

    return JsonResponse(data)





@csrf_exempt  
def json_create_remediation(request,idr,idp,typ):

    if typ == 0 :
        relationship = Relationship.objects.get(pk=idr) 
        form = RemediationForm(request.POST or None, request.FILES or None , teacher = relationship.parcours.teacher)
     
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.relationship = relationship
            nf.save()  
            form.save_m2m()

    else :
        customexercise = Customexercise.objects.get(pk=idr) 
        form = RemediationcustomForm(request.POST or None, request.FILES or None, teacher = customexercise.teacher)
     
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.customexercise = customexercise
            nf.save()  
            form.save_m2m()

    return redirect( 'show_parcours', idp )
    



@csrf_exempt  
def json_delete_remediation(request, id,typ):

    if typ == 0 :
        remediation = Remediation.objects.get(id=id)
    else :
        remediation = Remediationcustom.objects.get(id=id)
    remediation.delete()

    return redirect( 'show_parcours', remediation.relationship.parcours.id )

 

@csrf_exempt  
def audio_remediation(request):

    data = {}
    idr =  int(request.POST.get("id_relationship"))
    is_custom = request.POST.get("is_custom")
    if int(is_custom) == 0 : # 0 pour les exos GGB
        relationship = Relationship.objects.get(pk=idr) 
        form = RemediationForm(request.POST or None, request.FILES or None , teacher = relationship.parcours.teacher)
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.mediation = request.FILES.get("id_mediation")
            nf.relationship = relationship
            nf.audio = True
            nf.save()  
            form.save_m2m()
        else:
            print(form.errors)

    else :
        customexercise = Customexercise.objects.get( id = idr)
        form = RemediationcustomForm(request.POST or None,request.FILES or None, teacher = customexercise.teacher)
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.mediation = request.FILES.get("id_mediation")
            nf.customexercise = customexercise
            nf.audio = True
            nf.save()  
            form.save_m2m()
        else:
            print(form.errors)


    return JsonResponse(data)  




@csrf_exempt 
def ajax_remediation_viewer(request): # student_view

    remediation_id =  int(request.POST.get("remediation_id"))
    if request.POST.get("is_custom") == "0" :
        remediation = Remediation.objects.get( id = remediation_id)
    else :
        remediation = Remediationcustom.objects.get( id = remediation_id)    


    data = {}
    context = { 'remediation' : remediation ,   } 
    html = render_to_string('qcm/ajax_remediation_viewer.html',context)
    data['html'] = html       

    return JsonResponse(data)


#######################################################################################################################################################################
#######################################################################################################################################################################
#################   constraint
#######################################################################################################################################################################
#######################################################################################################################################################################



@csrf_exempt  
def ajax_infoExo(request):
    code = request.POST.get("codeExo")
    data={}
    if Relationship.objects.filter(exercise__supportfile__code = code ).exists() or code == "all" :
        html = "<i class='fa fa-check text-success'></i>"
        test = 1
    else :
        html = "ERREUR"
        test = 0

    data["html"] = html 
    data["test"] = test
    return JsonResponse(data)


@csrf_exempt  
def ajax_create_constraint(request):

    relationship_id = int(request.POST.get("relationship_id"))

    this_relationship = Relationship.objects.get(pk = relationship_id)
    code = request.POST.get("codeExo") 
    score = request.POST.get("scoreMin")

    data = {}
    if code == "all" : # si tous les exercices précédents sont cochés
        parcours_id = int(request.POST.get("parcours_id"))
        
        relationships = Relationship.objects.filter(parcours_id = parcours_id, order__lt= this_relationship.order)
        for relationship in relationships :
            Constraint.objects.get_or_create(code = relationship.exercise.supportfile.code, relationship = this_relationship, defaults={"scoremin" : score , } )
        data["html"] = "<div id='constraint_saving0'><i class='fa fa-minus-circle'></i> Tous les exercices à "+score+"% <a href='#'  class='pull-right delete_constraint' data-relationship_id='"+str(relationship_id)+"' data-is_all=1 ><i class='fa fa-trash'></i> </a></div>"
        data["all"] = 1
    else :
        constraint, created = Constraint.objects.get_or_create(code = code, relationship = this_relationship, defaults={"scoremin" : score , } )
        data["html"] = "<div id='constraint_saving'"+str(constraint.id)+"><i class='fa fa-minus-circle'></i> Exercice "+code+" à "+score+"% <a href='#'  class='pull-right delete_constraint' data-constraint_id='"+str(constraint.id)+"' data-relationship_id='"+str(relationship_id)+"' data-is_all=0 ><i class='fa fa-trash'></i> </a></div>"
        data["all"] = 0
 
    return JsonResponse(data)
 

@csrf_exempt  
def ajax_delete_constraint(request):

    data={}
    is_all  = int(request.POST.get("is_all"))
    relationship_id = int(request.POST.get("relationship_id")) 
    if is_all == 1 :
        constraints = Constraint.objects.filter(relationship_id = relationship_id)
        for c in constraints :
            c.delete()
        data["html"] = 0
        data["nbre"] = 0
    else :
        constraint_id = int(request.POST.get("constraint_id"))     
        constraint = Constraint.objects.get(id = constraint_id )
        code = constraint.code
        data["html"] = code
        constraint.delete()
        nbre = Constraint.objects.filter(relationship_id = relationship_id).count() 
        data["nbre"] = nbre
    return JsonResponse(data)

 







#######################################################################################################################################################################
#######################################################################################################################################################################
#################   exports PRONOTE ou autre
#######################################################################################################################################################################
#######################################################################################################################################################################


 
def export_note_custom(request,id,idp):

    customexercise = Customexercise.objects.get(pk=id)
    parcours = Parcours.objects.get(pk=idp)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=Notes_exercice_{}_{}.csv'.format(customexercise.id,parcours.id)
    writer = csv.writer(response)
    fieldnames = ("Eleves", "Notes")
    writer.writerow(fieldnames)
    for student in parcours.students.order_by("user__last_name") :
        full_name = str(student.user.last_name).lower() +" "+ str(student.user.first_name).lower() 
        try :
            studentanswer = Customanswerbystudent.objects.get(student=student, customexercise=customexercise,  parcours=parcours) 
            score = int(studentanswer.point)
        except :
            score = "Abs"
        writer.writerow( (full_name , score) )
    return response

 
def export_note(request,idg,idp):

    group = Group.objects.get(pk=idg)
    parcours = Parcours.objects.get(pk=idp)
    value = int(request.POST.get("on_mark")) 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=Notes_{}_{}.csv'.format(group.name,parcours.id)
    writer = csv.writer(response)
    fieldnames = ("Eleves", "Notes")
    writer.writerow(fieldnames)
    for student in group.students.order_by("user__last_name") :
        full_name = str(student.user.last_name).lower() +" "+ str(student.user.first_name).lower() 
        try :
            studentanswer = Studentanswer.objects.filter(student=student, parcours=parcours).last() 
            if value :
                score = int(studentanswer.point * value/100)
            else :
                score = int(studentanswer.point) 
        except :
            score = "Abs"
        writer.writerow( (full_name , score) )
    return response


 
def export_knowledge(request,idp):

    parcours = Parcours.objects.get(pk=idp)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' + 'filename=Savoir_faire_{}.csv'.format(parcours.title)
    writer = csv.writer(response)
    fieldnames = ("Elèves", "Savoir faire", "Scores")
    writer.writerow(fieldnames)
    kns = []
    exercises = parcours.exercises.filter(supportfile__is_title=0)
    for e in exercises :
        if e.knowledge not in kns :
            kns.append(e.knowledge)

    for student in parcours.students.all() :
        full_name = str(student.user.last_name) +" "+ str(student.user.first_name)  
        try :
            resultknowledges = Resultknowledge.objects.filter(student=student, knowledge__in=kns).last() 
            for r in resultknowledges : 
                writer.writerow ({"Eleves": full_name, "Savoir faire": r.knowledge.name , "Scores": r.point  })
        except :
            pass
    return response

 
def export_skill(request,idp):

    parcours = Parcours.objects.get(pk=idp)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' + 'filename=Competences_{}.csv'.format(parcours.title)
    writer = csv.writer(response)
    fieldnames = ("Elèves", "Compétences", "Scores")
    writer.writerow(fieldnames)
    sks = []
    exercises = parcours.exercises.filter(supportfile__is_title=0)
    for e in exercises :
        for s in e.supportfile.skills.all() :
            if s not in sks :
                sks.append(s)

    for student in parcours.students.all() :
        full_name = str(student.user.last_name) +" "+ str(student.user.first_name)  
        try :
            resultlastskills = Resultlastskill.objects.filter(student=student, skills_in=sks).last() 
            for r in resultlastskills : 
                writer.writerow ({"Eleves": full_name, "Compétences": r.skill.name , "Scores": r.point  })
        except :
            pass
    return response
 
#######################################################################################################################################################################
#######################################################################################################################################################################
##################    Course     
#######################################################################################################################################################################
#######################################################################################################################################################################



def list_courses(request):

    teacher = Teacher.objects.get(user_id = request.user.id)
    courses = Course.objects.filter(teacher = teacher)

    return render(request, 'qcm/course/list_course.html', {'courses': courses,  })



#@user_is_parcours_teacher
def create_course(request, idc , id ):
    """
    idc : course_id et id = parcours_id pour correspondre avec le decorateur
    """
    parcours = Parcours.objects.get(pk =  id)
    teacher = Teacher.objects.get(user= request.user)


    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id'] 
    access = data['access']
    
    if not authorizing_access(teacher, parcours,access):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    form = CourseForm(request.POST or None , parcours = parcours )
    relationships = Relationship.objects.filter(parcours = parcours,exercise__supportfile__is_title=0).order_by("order")
    if request.method == "POST" :
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.parcours = parcours
            nf.teacher = teacher
            nf.save()
            try :
                return redirect('show_course' , 0 , id)
            except :
                return redirect('index')
        else:
            print(form.errors)




    context = {'form': form,   'teacher': teacher, 'parcours': parcours , 'relationships': relationships , 'course': None , 'communications' : [], 'group' : group, 'group_id' : group_id , 'role' : role }

    return render(request, 'qcm/course/form_course.html', context)



#@user_can_modify_this_course
def update_course(request, idc, id  ):
    """
    idc : course_id et id = parcours_id pour correspondre avec le decorateur
    """
    parcours = Parcours.objects.get(pk =  id)
    teacher = Teacher.objects.get(user= request.user)
    course = Course.objects.get(id=idc)
    course_form = CourseForm(request.POST or None, instance=course , parcours = parcours )
    relationships = Relationship.objects.filter(parcours = parcours,exercise__supportfile__is_title=0).order_by("order")
    if request.user.user_type == 2 :
        teacher = parcours.teacher
    else :
        teacher = None

    if request.method == "POST" :
        if course_form.is_valid():
            course_form.save()
            if request.user.user_type == 0 :
                student = Student.objects.get(user = request.user )
                course.students.add(student)

            messages.success(request, 'Le cours a été modifié avec succès !')
            try :
                return redirect('show_course' , 0 , id)
            except :
                return redirect('index')
        else :
            print(course_form.errors)

    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id'] 


    context = {'form': course_form,  'course': course, 'teacher': teacher , 'parcours': parcours  , 'relationships': relationships , 'communications' : [] , 'group' : group, 'group_id' : group_id , 'role' : role }

    return render(request, 'qcm/course/form_course.html', context )



def delete_course(request, idc , id  ):
    """
    idc : course_id et id = parcours_id pour correspondre avec le decorateur
    """

    parcours = Parcours.objects.get(pk =  id)
    teacher = Teacher.objects.get(user= request.user)

    course = Course.objects.get(id=idc)


    if not authorizing_access(teacher, parcours,True):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    course.delete()
    try :
        return redirect('list_parcours_group' , request.session.get("group_id"))
    except :
        return redirect('index')  



#@user_is_parcours_teacher
def show_course(request, idc , id ):
    """
    idc : course_id et id = parcours_id pour correspondre avec le decorateur
    """
    parcours = Parcours.objects.get(pk =  id)
    courses = parcours.course.all().order_by("ranking") 
    teacher = Teacher.objects.get(user= request.user)
    

    data = get_complement(request, teacher, parcours)
    role = data['role']
    group = data['group']
    group_id = data['group_id'] 
    access = data['access']
    
    if not authorizing_access(teacher, parcours,access):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    user = User.objects.get(pk = request.user.id)
    teacher = Teacher.objects.get(user = user)
    context = {  'courses': courses, 'teacher': teacher , 'parcours': parcours , 'group_id' : None, 'communications' : [] , 'relationships' : [] , 'group' : group ,  'group_id' : group_id , 'role' : role }
    return render(request, 'qcm/course/show_course.html', context)

 


 
def ajax_parcours_shower_course(request):
    course_id =  int(request.POST.get("course_id"))
    course = Course.objects.get(pk=course_id)

    data = {}
    data['annoncement'] = course.annoncement
    data['title'] = course.title
    return JsonResponse(data)



def ajax_parcours_get_course(request):
    teacher = Teacher.objects.get(user_id = request.user.id) 
    course_id =  int(request.POST.get("course_id"))
    course = Course.objects.get(pk=course_id)
    parcourses =  teacher.teacher_parcours.all()    

    context = {  'course': course , 'parcourses': parcourses , 'teacher' : teacher  }
    data = {}
    data['html'] = render_to_string('qcm/course/ajax_parcours_get_course.html', context)
 
    return JsonResponse(data)
 

 
def ajax_parcours_clone_course(request):

    teacher = Teacher.objects.get(user_id = request.user.id)
    course_id =  int(request.POST.get("course_id"))
    course = Course.objects.get(pk=course_id)

    checkbox_value = request.POST.get("checkbox_value")

    if checkbox_value != "" :
        checkbox_ids = checkbox_value.split("-")
        for checkbox_id in checkbox_ids :
            try :
                course.pk = None
                course.teacher = teacher
                course.parcours_id = int(checkbox_id)
                course.save()
            except :
                pass 

    data = {}  
    return JsonResponse(data)




def course_custom_show_shared(request):
    
    user = request.user
    if user.is_teacher:  # teacher
        teacher = Teacher.objects.get(user=user) 
        courses = Course.objects.filter(is_share = 1).exclude(teacher = teacher)
        return render(request, 'qcm/course/list_courses.html', {  'teacher': teacher , 'courses':courses, 'parcours': None, 'relationships' : [] ,  'communications': [] , })
    else :
        return redirect('index')   


@student_can_show_this_course
def show_course_student(request, idc , id ):
    """
    idc : course_id et id = parcours_id pour correspondre avec le decorateur
    """
    this_user = request.user
    parcours = Parcours.objects.get(pk =  id)
    today = time_zone_user(this_user)
    courses = parcours.course.filter(Q(is_publish=1)|Q(publish_start__lte=today),Q(is_publish=1)|Q(publish_end__gte=today)).order_by("ranking")  
 

    context = {  'courses': courses, 'parcours': parcours , 'group_id' : None, 'communications' : []}
    return render(request, 'qcm/course/show_course_student.html', context)
 


#######################################################################################################################################################################
#######################################################################################################################################################################
##################    Demand     
#######################################################################################################################################################################
#######################################################################################################################################################################



def list_demands(request):

    demands = Demand.objects.order_by("done")

    return render(request, 'qcm/demand/show_demand.html', {'demands': demands,  })




def create_demand(request):
    teacher = Teacher.objects.get(user_id = request.user.id)
    form = DemandForm(request.POST or None  )
    if request.method == "POST" :
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.teacher = teacher
            nf.save()
            messages.success(request, 'La demande a été envoyée avec succès !')
            rec = ['brunoserres33@gmal.com', 'philippe.demaria83@gmal.com', ]
            send_mail("SacAdo Demande d'exercice",  "Demande d'exercice.... voir dans Demande d'exercices sur https://sacado.xyz" , "info@sacado.xyz" , rec )

            sender = [teacher.user.email,]
            send_mail("SacAdo Demande d'exercice",  "Votre demande d'exercice est en cours de traitement." , "info@sacado.xyz" , sender )


            return redirect('index')

        else:
            print(form.errors)

    context = {'form': form,   'teacher': teacher, 'parcours': None , 'relationships': None , 'course': None , }

    return render(request, 'qcm/demand/form_demand.html', context)




def update_demand(request, id):
 
    demand = Demand.objects.get(id=id)
    demand_form = DemandForm(request.POST or None, instance=demand, )
    teacher = Teacher.objects.get(user= request.user)

    if request.method == "POST" :
        if demand_form.is_valid():
            nf =  form.save(commit = False)
            nf.teacher = teacher
            nf.save()
 

            messages.success(request, 'La demande a été modifiée avec succès !')
            return redirect('index')
        else :
            print(demand_form.errors)

    context = {'form': demand_form,  'demand': demand, 'teacher': teacher , 'parcours': None  , 'relationships': relationships , }

    return render(request, 'qcm/demand/form_demand.html', context )




def delete_demand(request, id  ):
    """
    idc : demand_id et id = parcours_id pour correspondre avec le decorateur
    """
    demand = Demand.objects.get(id=idc)
    demand.delete()
    return redirect('index')  




def show_demand(request, id ):
    """
    idc : demand_id et id = parcours_id pour correspondre avec le decorateur
    """
    demand = Demand.objects.get(pk =  id)

    user = User.objects.get(pk = request.user.id)
    teacher = Teacher.objects.get(user = user)
    context = {  'demands': demands, 'teacher': teacher , 'parcours': None , 'group_id' : None, 'communications' : []}
    return render(request, 'qcm/demand/show_demand.html', context)

 
@csrf_exempt
def ajax_chargeknowledges(request):
    id_theme =  request.POST.get("id_theme")
    theme = Theme.objects.get(id=id_theme)
 
    data = {}
    ks = Knowledge.objects.values_list('id', 'name').filter(theme=theme)
    data['knowledges'] = list(ks)
 
    return JsonResponse(data)


@csrf_exempt
def ajax_demand_done(request) :

    code = request.POST.get("code") #id de l'e
    id =  request.POST.get("id")

    Demand.objects.filter(id=id).update(done=1)
    Demand.objects.filter(id=id).update(code=code)

    demand = Demand.objects.get(id=id)

    rec = [demand.teacher.user.email]

    send_mail("SacAdo Demande d'exercice",  "Bonjour " + str(demand.teacher.user.get_full_name())+ ", \n\n Votre exercice est créé. \n\n Pour tester votre exercice, https://sacado.xyz/qcm/show_exercise/"+str(code)  +"\n\n Bonne utilisation de sacado." , "info@sacado.xyz" , rec )
    data={}
    return JsonResponse(data)




@csrf_exempt 
def ajax_course_viewer(request):  

    relation_id =  request.POST.get("relation_id",None)
    data = {}
    if relation_id : 
        relationship = Relationship.objects.get( id = int(relation_id))
        courses = Course.objects.filter(relationships = relationship).order_by("ranking")

        if request.user.user_type == 2 :
            is_teacher = True
        else : 
            is_teacher = False 
        context = { 'courses' : courses , 'parcours' : relationship.parcours , 'is_teacher' : is_teacher }
        html = render_to_string('qcm/course/course_viewer.html',context)
        data['html'] = html       

    return JsonResponse(data)




#######################################################################################################################################################################
#######################################################################################################################################################################
##################    Mastering     
#######################################################################################################################################################################
#######################################################################################################################################################################

def create_mastering(request,id):
    relationship = Relationship.objects.get(pk = id)
    stage = Stage.objects.get(school= relationship.parcours.teacher.user.school)
    form = MasteringForm(request.POST or None, request.FILES or None, relationship = relationship )

    masterings_q = Mastering.objects.filter(relationship = relationship , scale = 4).order_by("ranking")
    masterings_t = Mastering.objects.filter(relationship = relationship , scale = 3).order_by("ranking")
    masterings_d = Mastering.objects.filter(relationship = relationship , scale = 2).order_by("ranking")
    masterings_u = Mastering.objects.filter(relationship = relationship , scale = 1).order_by("ranking")
    teacher = Teacher.objects.get(user= request.user)



    if not authorizing_access(teacher, relationship.parcours,role):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')


    if request.method == "POST" :
        if form.is_valid():
            nf = form.save(commit = False)
            nf.scale = int(request.POST.get("scale"))
            nf.save()
            form.save_m2m()
        else:
            print(form.errors)

    context = {'form': form,   'relationship': relationship , 'parcours': relationship.parcours , 'relationships': [] ,  'communications' : [] ,  'course': None , 'stage' : stage , 'teacher' : teacher ,  'group': None,
                'masterings_q' : masterings_q, 'masterings_t' : masterings_t, 'masterings_d' : masterings_d, 'masterings_u' : masterings_u}

    return render(request, 'qcm/mastering/form_mastering.html', context)




#@user_is_relationship_teacher 
def parcours_mastering_delete(request,id,idm):

    m = Mastering.objects.get(pk = idm)

    if not authorizing_access(teacher,  m.relationship.parcours,True):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')


    m.delete()
    return redirect('create_mastering', id )






@csrf_exempt # PublieDépublie un exercice depuis organize_parcours
def ajax_sort_mastering(request):

    try :
        relationship_id = request.POST.get("relationship_id")
        mastering_ids = request.POST.get("valeurs")
        mastering_tab = mastering_ids.split("-") 
     
        for i in range(len(mastering_tab)-1):
            Mastering.objects.filter(relationship_id = relationship_id , pk = mastering_tab[i]).update(ranking = i)
    except :
        pass

    data = {}
    return JsonResponse(data) 




@csrf_exempt  # PublieDépublie un exercice depuis organize_parcours
def ajax_populate_mastering(request): 
    # Cette fonction est appelé pour les exercices ou pour les customexercices. Du coup pour éviter une erreur, si la relationship n'existe pas on ne fait rien, juste le css

    scale = int(request.POST.get("scale"))
    exercise_id = int(request.POST.get("exercise_id"))
    rs = request.POST.get("relationship_id",None) # Permet de garder le jeu du css
    if rs :
        relationship_id = int(rs)
        relationship = Relationship.objects.get(pk = relationship_id) 
    exercise = Exercise.objects.get(pk = exercise_id)
    statut = request.POST.get("statut") 
    data = {}    

    if statut=="true" or statut == "True":
        if rs :
            m = Mastering.objects.get(relationship=relationship, exercise = exercise)  
            m.delete()         
        statut = 0
        data["statut"] = "False"
        data["class"] = "btn btn-danger"
        data["noclass"] = "btn btn-success"
        data["html"] = "<i class='fa fa-times'></i>"
        data["no_store"] = False

    else:
        statut = 1
        if rs :
            if Mastering.objects.filter(relationship=relationship, exercise = exercise).count() == 0 :
                mastering = Mastering.objects.create(relationship=relationship, exercise = exercise, scale= scale, ranking=0)  
                data["statut"] = "True"
                data["no_store"] = False

            else :
                data["statut"] = "False"
                data["no_store"] = True
           
        else :
            data["statut"] = "True"
            data["no_store"] = False

    return JsonResponse(data) 



def mastering_student_show(request,id):

    relationship = Relationship.objects.get(pk = id)
    teacher = relationship.parcours.teacher
    stage = Stage.objects.get(school= teacher.user.school)

    student = Student.objects.get(user= request.user)
    studentanswer = Studentanswer.objects.filter(student=student, exercise = relationship.exercise, parcours = relationship.parcours).last()

    if studentanswer : 
        score = studentanswer.point
        if score > stage.up :
            masterings = Mastering.objects.filter(scale = 4, relationship = relationship)
        elif score > stage.medium :
            masterings = Mastering.objects.filter(scale = 3, relationship = relationship)
        elif score > stage.low :
            masterings = Mastering.objects.filter(scale = 2, relationship = relationship)
        else :
            masterings = Mastering.objects.filter(scale = 1, relationship = relationship)
    else :
        score = False
        masterings = []
    context = { 'relationship': relationship , 'masterings': masterings , 'parcours': None , 'relationships': [] ,  'communications' : [] ,  'score': score , 'group': None, 'course': None , 'stage' : stage , 'student' : student }

    return render(request, 'qcm/mastering/mastering_student_show.html', context)




@csrf_exempt  
def ajax_mastering_modal_show(request):

    mastering_id =  int(request.POST.get("mastering_id"))
    mastering = Mastering.objects.get( id = mastering_id)

    data = {}
    data['nocss'] = "modal-exo"
    data['css'] = "modal-md"
    data['duration'] = "<i class='fa fa-clock'></i> "+ str(mastering.duration)+" min."
    data['consigne'] = "<strong>Consigne : </strong>"+ str(mastering.consigne)
   
    form = None
    if mastering.writing  :
        resp = 0
        data['nocss'] = "modal-md"
        data['css'] = "modal-exo"
        student = Student.objects.get(user = request.user)
        mdone = Mastering_done.objects.filter( mastering = mastering , student = student)
        if mdone.count() == 1 :
            md = Mastering_done.objects.get( mastering = mastering , student = student)
            form = MasteringcustomDoneForm(instance = md )
        else :
            form = MasteringcustomDoneForm(request.POST or None )
    elif mastering.video != "" :
        resp = 1
    elif mastering.exercise :
        resp = 2
        data['duration'] = "<i class='fa fa-clock'></i> "+ str(mastering.exercise.supportfile.duration)+" min." 
        data['consigne'] = "Exercice"
        data['nocss'] = "modal-md"
        data['css'] = "modal-exo"
    elif len(mastering.courses.all()) > 0 :
        resp = 3
        data['css'] = "modal-exo"
        data['nocss'] = "modal-md"
    elif mastering.mediation != "" :
        resp = 4
        data['nocss'] = "modal-md"
        data['css'] = "modal-exo"

    context = { 'mastering' : mastering , 'resp' : resp , 'form' : form }

    html = render_to_string('qcm/mastering/modal_box.html',context)
    data['html'] = html       

    return JsonResponse(data)





def mastering_done(request):

    mastering = Mastering.objects.get(pk = request.POST.get("mastering"))
    student = Student.objects.get(user=request.user)

    mdone = Mastering_done.objects.filter( mastering = mastering , student = student)

    if mdone.count() == 0 : 
        form = MasteringDoneForm(request.POST or None )
    else :
        md = Mastering_done.objects.get( mastering = mastering , student = student)
        form = MasteringDoneForm(request.POST or None , instance = md )
    if form.is_valid() :
        nf = form.save(commit = False)
        nf.student =  student
        nf.mastering =  mastering
        nf.save()

    return redirect('mastering_student_show', mastering.relationship.id)








#######################################################################################################################################################################
#######################################################################################################################################################################
##################    Mastering Custom    
#######################################################################################################################################################################
#######################################################################################################################################################################

def create_mastering_custom(request,id,idp):
    customexercise = Customexercise.objects.get(pk = id)
    stage = Stage.objects.get(school= request.user.school)
    form = MasteringcustomForm(request.POST or None, request.FILES or None, customexercise = customexercise )

    parcours = Parcours.objects.get(pk= idp)

    masterings_q = Masteringcustom.objects.filter(customexercise = customexercise , scale = 4).order_by("ranking")
    masterings_t = Masteringcustom.objects.filter(customexercise = customexercise , scale = 3).order_by("ranking")
    masterings_d = Masteringcustom.objects.filter(customexercise = customexercise , scale = 2).order_by("ranking")
    masterings_u = Masteringcustom.objects.filter(customexercise = customexercise , scale = 1).order_by("ranking")
    teacher = Teacher.objects.get(user_id = request.user.id)
    if request.method == "POST" :
        exercise_id = request.POST.get("exercises",None)
        if form.is_valid():
            nf = form.save(commit = False)
            nf.scale = int(request.POST.get("scale"))
            nf.exercise_id = exercise_id            
            nf.save()
            form.save_m2m()
        else:
            print(form.errors)

    context = {'form': form,   'customexercise': customexercise , 'parcours': parcours , 'relationships': [] ,  'communications' : [] ,  'course': None , 'stage' : stage , 'teacher' : teacher ,  'group': None,
                'masterings_q' : masterings_q, 'masterings_t' : masterings_t, 'masterings_d' : masterings_d, 'masterings_u' : masterings_u}

    return render(request, 'qcm/mastering/form_mastering_custom.html', context)


#@user_is_customexercice_teacher 
def parcours_mastering_custom_delete(request,id,idm,idp):

    m = Masteringcustom.objects.get(pk = idm)
    m.delete()
    return redirect('create_mastering_custom', id ,idp )

@csrf_exempt # PublieDépublie un exercice depuis organize_parcours
def ajax_sort_mastering_custom(request):

    try :
        relationship_id = request.POST.get("relationship_id")
        mastering_ids = request.POST.get("valeurs")
        mastering_tab = mastering_ids.split("-") 
     
        for i in range(len(mastering_tab)-1):
            Mastering.objects.filter(relationship_id = relationship_id , pk = mastering_tab[i]).update(ranking = i)
    except :
        pass

    data = {}
    return JsonResponse(data) 
 

def mastering_custom_student_show(request,id):

    customexercise = Customexercise.objects.get(pk = id)
    stage = Stage.objects.get(school= customexercise.teacher.user.school)

    student = Student.objects.get(user = request.user)
    studentanswer = Customanswerbystudent.objects.filter(student=student, customexercise = customexercise, parcours__in= customexercise.parcourses.all()).last()

    skill_answer = Correctionskillcustomexercise.objects.filter(student=student, customexercise = customexercise, parcours__in= customexercise.parcourses.all()).last()
    

    knowledge_answer = Correctionknowledgecustomexercise.objects.filter(student=student, customexercise = customexercise, parcours__in= customexercise.parcourses.all()).last()


    if skill_answer or studentanswer or knowledge_answer : 
        score = skill_answer.point
        if score > stage.up :
            masterings = Masteringcustom.objects.filter(scale = 4, customexercise = customexercise)
        elif score > stage.medium :
            masterings = Masteringcustom.objects.filter(scale = 3, customexercise = customexercise)
        elif score > stage.low :
            masterings = Masteringcustom.objects.filter(scale = 2, customexercise = customexercise)
        else :
            masterings = Masteringcustom.objects.filter(scale = 1, customexercise = customexercise)
    else :
        score = False
        masterings = []

    context = { 'customexercise': customexercise , 'masterings': masterings , 'parcours': None , 'relationships': [] ,  'communications' : [] ,  'score': score , 'group': None, 'course': None , 'stage' : stage , 'student' : student }

    return render(request, 'qcm/mastering/mastering_custom_student_show.html', context)


@csrf_exempt  
def ajax_mastering_custom_modal_show(request):

    mastering_id =  int(request.POST.get("mastering_id"))
    mastering = Masteringcustom.objects.get( id = mastering_id)

    data = {}
    data['nocss'] = "modal-exo"
    data['css'] = "modal-md"
    data['duration'] = "<i class='fa fa-clock'></i> "+ str(mastering.duration)+" min."
    data['consigne'] = "<strong>Consigne : </strong>"+ str(mastering.consigne)
   
    form = None
    if mastering.writing  :
        resp = 0
        data['nocss'] = "modal-md"
        data['css'] = "modal-exo"
        student = Student.objects.get(user = request.user)
        mdone = Masteringcustom_done.objects.filter( mastering = mastering , student = student)
        if mdone.count() == 1 :
            md = Masteringcustom_done.objects.get( mastering = mastering , student = student)
            form = MasteringcustomDoneForm(instance = md )
        else :
            form = MasteringcustomDoneForm(request.POST or None )
    elif mastering.video != "" :
        resp = 1
    elif mastering.exercise :
        resp = 2
        data['duration'] = "<i class='fa fa-clock'></i> "+ str(mastering.customexercise.duration)+" min." 
        data['consigne'] = "Exercice"
        data['nocss'] = "modal-md"
        data['css'] = "modal-exo"
    elif len(mastering.courses.all()) > 0 :
        resp = 3
        data['css'] = "modal-exo"
        data['nocss'] = "modal-md"
    elif mastering.mediation != "" :
        resp = 4
        data['nocss'] = "modal-md"
        data['css'] = "modal-exo"

    context = { 'mastering' : mastering , 'resp' : resp , 'form' : form }

    html = render_to_string('qcm/mastering/modal_box.html',context)
    data['html'] = html       

    return JsonResponse(data)



def mastering_custom_done(request):
 
    mastering = Masteringcustom.objects.get(pk = request.POST.get("mastering"))
    student = Student.objects.get(user=request.user)

    mdone = Masteringcustom_done.objects.filter( mastering = mastering , student = student)

    if mdone.count() == 0 : 
        form = MasteringcustomDoneForm(request.POST or None )
    else :
        md = Masteringcustom_done.objects.get( mastering = mastering , student = student)
        form = MasteringcustomDoneForm(request.POST or None , instance = md )
    if form.is_valid() :
        nf = form.save(commit = False)
        nf.student =  student
        nf.mastering =  mastering
        nf.save()

    return redirect('mastering_custom_student_show', mastering.customexercise.id)