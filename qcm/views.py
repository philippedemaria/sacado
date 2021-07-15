from django.conf import settings # récupération de variables globales du settings.py
from django.shortcuts import render, redirect
from account.models import  Student, Teacher, User,Resultknowledge, Resultskill, Resultlastskill
from account.forms import StudentForm, TeacherForm, UserForm
from django.contrib.auth.forms import  AuthenticationForm
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import  permission_required,user_passes_test, login_required
from sendmail.forms import  EmailForm
from group.forms import GroupForm 
from group.models import Group , Sharing_group
from school.models import Stage, School
from qcm.models import  Parcours , Studentanswer, Exercise, Exerciselocker ,  Relationship,Resultexercise, Generalcomment , Resultggbskill, Supportfile,Remediation, Constraint, Course, Demand, Mastering, Masteringcustom, Masteringcustom_done, Mastering_done, Writtenanswerbystudent , Customexercise, Customanswerbystudent, Comment, Correctionknowledgecustomexercise , Correctionskillcustomexercise , Remediationcustom, Annotation, Customannotation , Customanswerimage , DocumentReport , Tracker
from qcm.forms import ParcoursForm ,  RemediationForm, UpdateParcoursForm , UpdateSupportfileForm, SupportfileKForm, RelationshipForm, SupportfileForm, AttachForm ,   CustomexerciseNPForm, CustomexerciseForm ,CourseForm , DemandForm , CommentForm, MasteringForm, MasteringcustomForm , MasteringDoneForm , MasteringcustomDoneForm, WrittenanswerbystudentForm,CustomanswerbystudentForm , WAnswerAudioForm, CustomAnswerAudioForm , RemediationcustomForm , CustomanswerimageForm , DocumentReportForm
from socle.models import  Theme, Knowledge , Level , Skill , Waiting
from django.http import JsonResponse 
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from tool.consumers import *
import uuid
import time
import math
import json
import random
from datetime import datetime , timedelta
from django.db.models import Q
from django.core.mail import send_mail
from group.decorators import user_is_group_teacher 
from qcm.decorators import user_is_parcours_teacher, user_can_modify_this_course, student_can_show_this_course , user_is_relationship_teacher, user_is_customexercice_teacher , parcours_exists
from account.decorators import user_can_create, user_is_superuser, user_is_creator , user_is_testeur
##############bibliothèques pour les impressions pdf  #########################
import os
from pdf2image import convert_from_path # convertit un pdf en autant d'images que de pages du pdf
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
from html import escape
from operator import attrgetter
cm = 2.54
import os
import re
import pytz
import csv
import html
from general_fonctions import *


#################################################################
#Récupération du marocurs Seconde to Maths complémentaires
#################################################################


def get_teacher_id_by_subject_id(subject_id):

    if subject_id == 1 or subject_id == "1" :
        teacher_id = 2480

    elif  subject_id == 2 or subject_id == "2" :
        teacher_id = 35487

    elif subject_id == 3 or subject_id == "3"  :
        teacher_id = 2480

    else :
        teacher_id = 2480

    return teacher_id



def get_seconde_to_math_comp(request):

    teacher = request.user.teacher
 
    group = Group.objects.get(id=1921)#groupe fixe sur le serveur 1921

    parcourses = group.group_parcours.all()

    cod = "_e-test_"+ str(uuid.uuid4())[:4]  
    user = User.objects.create(last_name=teacher.user.last_name, first_name =teacher.user.first_name+cod , email="", user_type=0,
                                                      school=request.user.school, time_zone=request.user.time_zone,
                                                      is_manager=0, username = teacher.user.username+ cod  ,  password ="sacado2020",
                                                      is_extra = 0 )
    student = Student.objects.create(user=user, level=group.level, task_post=1)

    group.pk = None
    group.teacher = teacher
    group.code = str(uuid.uuid4())[:8]  
    group.lock = 0
    group.save()

    group.students.add(student)

    all_new_parcours_folders , all_new_parcours_leaves  = [],[]

    for parcours in parcourses :

        relationships = parcours.parcours_relationship.all() 
        courses = parcours.course.all()
        #################################################
        # clone le parcours
        #################################################
        parcours.pk = None
        parcours.teacher = teacher
        parcours.is_publish = 1
        parcours.is_archive = 0
        parcours.is_share = 0
        parcours.is_favorite = 1
        parcours.code = str(uuid.uuid4())[:8]  
        parcours.save()
        if parcours.is_folder :
            all_new_parcours_folders.append(parcours)
        else :
            all_new_parcours_leaves.append(parcours)
        parcours.groups.add(group)
        parcours.students.add(student)
        #################################################
        # clone les exercices attachés à un cours 
        #################################################
        former_relationship_ids = []

        for course in courses :

            old_relationships = course.relationships.all()
            # clone le cours associé au parcours
            course.pk = None
            course.parcours = parcours
            course.save()



            for relationship in old_relationships :
                # clone l'exercice rattaché au cours du parcours 
                if not relationship.id in former_relationship_ids :
                    relationship.pk = None
                    relationship.parcours = parcours
                    relationship.save()


                course.relationships.add(relationship)
                former_relationship_ids.append(relationship.id)

        #################################################
        # clone tous les exercices rattachés au parcours 
        #################################################
        for relationship in relationships :
            try :
                relationship.pk = None
                relationship.parcours = parcours
                relationship.save()       
                relationship.students.add(student)
            except :
                pass

        for prcr in all_new_parcours_folders :
            prcr.leaf_parcours.set(all_new_parcours_leaves)

    School.objects.filter(pk = request.user.school.id).update(get_seconde_to_comp=1)

    messages.success(request,"Tous les parcours du groupe PREPA Maths Complémentaires ont été placés dans tous les dossiers. Vous devez manuellement les sélectionner pour personnaliser vos dossiers.")

    return redirect('admin_tdb' )

##################################################################################################################################
##################################################################################################################################
##################################################################################################################################

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
    teacher = request.user.teacher
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

    sending_mail("Nouvel exercice SacAdo",  msg , settings.DEFAULT_FROM_EMAIL , rcv)
 

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
        access = True
        
    return role, group , group_id , access


def get_stage(user):

    try :
        if user.school :
            school = user.school
            stg = Stage.objects.get(school = school)
            stage = { "low" : stg.low ,  "medium" : stg.medium  ,  "up" : stg.up  }
        else : 
            stage = { "low" : 50 ,  "medium" : 70 ,  "up" : 85  }
    except :
        stage = { "low" : 50 ,  "medium" : 70 ,  "up" : 85  }  
    return stage

def group_has_parcourses(group,is_evaluation ,is_archive ):
    pses_tab = []

    for s in group.students.all() :
        pses = s.students_to_parcours.filter(is_evaluation=is_evaluation,is_archive=is_archive,is_leaf = 0)
        for p in pses :
            if p not in  pses_tab :
                pses_tab.append(p)
 
    return pses_tab







def teacher_has_parcourses_folder(teacher,is_evaluation ,is_archive ):
    """
    Renvoie les parcours dont le prof est propriétaire et donc les parcours lui sont partagés
    """
    sharing_groups = teacher.teacher_sharingteacher.all()
    parcourses =  set(teacher.teacher_parcours.filter(is_evaluation=is_evaluation,is_archive=is_archive,is_leaf = 0))
    pacourses_co = teacher.coteacher_parcours.filter(is_evaluation=is_evaluation,is_archive=is_archive,is_leaf = 0)

    parcourses.update(pacourses_co)
    for sg in sharing_groups :
        pcs = group_has_parcourses(sg.group,is_evaluation ,is_archive )
        parcourses.update(pcs) 

    return parcourses


def teacher_has_own_parcourses_and_folder(teacher,is_evaluation,is_archive ):
    """
    Renvoie les parcours et les dossiers dont le prof est propriétaire
    """
    parcourses =  teacher.teacher_parcours.filter(is_evaluation=is_evaluation,is_archive=is_archive,is_leaf = 0)

    return parcourses



def teacher_has_parcourses(teacher,is_evaluation ,is_archive ):
    """
    Renvoie les parcours dont le prof est propriétaire et donc les parcours lui sont partagés
    """
    sharing_groups = teacher.teacher_sharingteacher.all()
    parcourses = list(teacher.teacher_parcours.filter(is_evaluation=is_evaluation,is_archive=is_archive))


    for sg in sharing_groups :
        pcs = group_has_parcourses(sg.group,is_evaluation ,is_archive )
        for p in pcs :
            if p not in parcourses:
                parcourses.append(p) 
    return parcourses

def teacher_has_permisson_to_share_inverse_parcourses(request,teacher,parcours):
    """
    Quand un enseignant partage son groupe, il doit aussi voir les parcours que son co animateur propose.
    """
    test_has_permisson = False
    for student in parcours.students.all() :
        for group in teacher.groups.all() :
            if student in group.students.all()  :
                test_has_permisson = True
                break
    return test_has_permisson

def teacher_has_permisson_to_parcourses(request,teacher,parcours):


    test_has_permisson = teacher_has_permisson_to_share_inverse_parcourses(request,teacher,parcours)

    if test_has_permisson or parcours in teacher_has_parcourses(teacher,0,0) or parcours in teacher_has_parcourses(teacher,0,1) or parcours in teacher_has_parcourses(teacher,1,0) or parcours in teacher_has_parcourses(teacher,1,1):
        has_permisson = True
    elif request.user.is_superuser or request.user.is_creator or request.user.is_testeur :
        has_permisson = True
    else :
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        has_permisson = False
    return has_permisson 

def skills_in_parcours(request,parcours):

    relationships = Relationship.objects.filter(parcours=parcours)
    skillsInParcours = set()
    for r in relationships:
        skillsInParcours.update(r.skills.all()) # skill des exo sacado

    customexercises = Customexercise.objects.filter(parcourses=parcours)
    for c in customexercises :
        skillsInParcours.update(c.skills.all()) # skill des exo perso

    skills = Skill.objects.filter(subject__in = request.user.teacher.subjects.all())

    union_skills = []
    for s in skills :
        if s in skillsInParcours :
            union_skills.append(s)

    return union_skills

# def skills_in_parcours(parcours):
#     """
#     version moins rapide sans request
#     """
#     skills = []
#     for exercise in parcours.exercises.all():
#         relationships = exercise.exercise_relationship.filter(parcours=parcours)
#         for r in relationships :
#             for sk in r.skills.all() :
#                 if sk not in skills :
#                     skills.append(sk)
#     for ce in parcours.parcours_customexercises.all():
#         for sk in ce.skills.all() :
#             if sk not in skills :
#                 skills.append(sk)   
#     return skills


def knowledges_in_parcours(parcours):

    knowledges = []
    for exercise in parcours.exercises.filter(supportfile__is_title=0):
        relationships = exercise.exercise_relationship.filter(parcours=parcours,is_publish=1)
        for r in relationships :
            sr = r.exercise.knowledge
            if sr not in knowledges :
                    knowledges.append(sr)
    for ce in parcours.parcours_customexercises.all():
        for sk in ce.knowledges.all() :
            if sk not in knowledges :
                knowledges.append(sk)
    return knowledges

def total_by_skill_by_student(skill,relationships, parcours,student) : # résultat d'un élève par comptétnece sur un parcours donné
    total_skill = 0            
    scs = student.student_correctionskill.filter(skill = skill, parcours = parcours)
    nbs = scs.count()

    for sc in scs :
        total_skill += int(sc.point)

    # Ajout éventuel de résultat sur la compétence sur un exo SACADO
    result_sacado_skills = Resultggbskill.objects.filter(skill= skill,student=student, relationship__in = relationships) 
    for rss in result_sacado_skills :
        total_skill += rss.point
        nbs += 1

    ################################################################

    if nbs != 0 :
        tot_s = total_skill//nbs
    else :
        tot_s = -10

    return tot_s


def total_by_knowledge_by_student(knowledge,relationships, parcours,student) : # résultat d'un élève par comptétnece sur un parcours donné
    total_knowledge = 0            
    sks = student.student_correctionknowledge.filter(knowledge = knowledge, parcours = parcours)
    nbk = sks.count()

    for sk in sks :
        total_knowledge += int(sk.point)

    # Ajout éventuel de résultat sur la compétence sur un exo SACADO
    result_sacado_knowledges = Studentanswer.objects.filter(parcours= parcours,student=student, exercise__knowledge = knowledge) 
    for rsk in result_sacado_knowledges :
        total_knowledge += rsk.point
        nbk += 1

    ################################################################
    if nbk !=0  :
        tot_k = total_knowledge//nbk
    else :
        tot_k  = -10
    return tot_k



################################################################
##  Trace les élève lors l'exécution d'exercice : Real time
################################################################


def tracker_execute_exercise(track_untrack ,  user , idp=0 , ide=None , custom=0) :
    """ trace l'utilisateur. Utile pour le real time """
 

    if track_untrack : # Si True alors on garde la trace
        Tracker.objects.create(user =  user, parcours_id = idp ,  exercise_id =  ide,  is_custom =  custom )
        parcours = Parcours.objects.get(pk=idp)

        #send_exercise_student_to_teacher(parcours.teacher.id, ide, user.id)
        #tracker, created = Tracker.objects.get_or_create(user =  user, defaults={  'parcours_id' : idp , 'exercise_id' : ide, 'is_custom' : custom})
        # if not created :
        #     Tracker.objects.filter(user =  user).update(  parcours_id = idp )
        #     Tracker.objects.filter(user =  user).update( exercise_id= ide)
        #     Tracker.objects.filter(user =  user).update( is_custom= custom)
    else :
        trackers = Tracker.objects.filter(user =  user)
        for tracker in trackers :    
            tracker.delete()








#######################################################################################################################################################################
#######################################################################################################################################################################
#################   parcours par defaut
#######################################################################################################################################################################
#######################################################################################################################################################################
def associate_parcours(request,id):
    teacher = request.user.teacher
    group = Group.objects.get(pk = id)
    theme_theme_ids = request.POST.getlist("themes")
    for theme_id in theme_theme_ids :
        theme = Theme.objects.get(pk = int(theme_id))
        parcours, created = Parcours.objects.get_or_create(title=theme.name, color=group.color, author=teacher, teacher=teacher, level=group.level,  is_favorite = 1,  is_share = 0, linked = 1)
        exercises = Exercise.objects.filter(level= group.level,theme = theme, supportfile__is_title=0)
        parcours.students.set(group.students.all())
        i  = 0
        for e in exercises:
            relationship, created = Relationship.objects.get_or_create(parcours = parcours, exercise=e, ranking = i)
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
    teacher = request.user.teacher
    level_id = request.POST.get("level_selected_id")
    theme_ids = request.POST.getlist("themes")
    n = 0
    for theme_id in theme_ids :
        theme = Theme.objects.get(pk = int(theme_id))
        parcours, created = Parcours.objects.get_or_create(title=theme.name, color="#5d4391", author=teacher, teacher=teacher, level_id=level_id,  is_favorite = 1,  is_share = 0, linked = 0)
        exercises = Exercise.objects.filter(level_id=level_id,theme = theme, supportfile__is_title=0)
        i  = 0
        for e in exercises:
            relationship, created = Relationship.objects.get_or_create(parcours = parcours, exercise=e, ranking = i)
            if created :
                relationship.skills.set(e.supportfile.skills.all()) 
            i+=1
        n +=1
    if n > 1 :
        messages.info(request, "Les parcours sont créés avec succès. Penser à leur attribuer des élèves et à les publier.")
    else :
        messages.info(request, "Le parcours est créé avec succès. Penser à lui attribuer des élèves et à le publier.")
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

    thms = level.themes.values_list('id', 'name').filter(subject_id=id_subject).order_by("name")
    data['themes'] = list(thms)

    # gère les propositions d'image d'accueil
    data['imagefiles'] = None
    imagefiles = level.level_parcours.values_list("vignette", flat = True).filter(subject_id=id_subject).exclude(vignette=" ").distinct()
    if imagefiles.count() > 0 :
        data['imagefiles'] = list(imagefiles)

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
            relation = Relationship.objects.create(parcours_id=parcours_id, exercise_id = exercise_id, ranking = 100, maxexo = parcours.maxexo ,
                                                                            situation = exercise.supportfile.situation , duration = exercise.supportfile.duration) 
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




def peuplate_parcours(request,id):
    teacher = request.user.teacher
    levels =  teacher.levels.all() 
    parcours = Parcours.objects.get(id=id)

    role, group , group_id , access = get_complement(request, teacher, parcours)
 

    if not authorizing_access(teacher,parcours, access ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    form = UpdateParcoursForm(request.POST or None , instance=parcours, teacher = parcours.teacher  )
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("ranking")
    """ affiche le parcours existant avant la modif en ajax""" 
    exercises = parcours.exercises.filter(supportfile__is_title=0).order_by("theme","knowledge__waiting","knowledge","ranking")
    """ fin """
    themes_tab = []
    for level in levels :
        for theme in level.themes.all():
            if not theme in themes_tab:
                themes_tab.append(theme)
    
    if request.method == 'POST' :
        level = request.POST.get("level") 
        # modifie les exercices sélectionnés
        exercises_all = parcours.exercises.filter(supportfile__is_title=0,level=level).order_by("theme","knowledge__waiting","knowledge","ranking")
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
                    r = Relationship.objects.create(parcours = nf , exercise = exercise , ranking =  i, situation = exercise.supportfile.situation , duration = exercise.supportfile.duration )  
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
    teacher = request.user.teacher
    levels =  teacher.levels.all() 
 
    parcours = Parcours.objects.get(id=id)

    role, group , group_id , access = get_complement(request, teacher, parcours)

    if not authorizing_access(teacher,parcours, access ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')



    form = UpdateParcoursForm(request.POST or None , instance=parcours, teacher = teacher  )
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("ranking")
    """ affiche le parcours existant avant la modif en ajax""" 
    exercises = parcours.exercises.filter(supportfile__is_title=0).order_by("theme","knowledge__waiting","knowledge","ranking")
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
                    r = Relationship.objects.create(parcours = nf , exercise = exercise , ranking =  i, situation = exercise.supportfile.situation , duration = exercise.supportfile.duration )  
                    r.skills.set(exercise.supportfile.skills.all()) 
                    i+=1
                else :
                    pass
            except :
                pass
 
        # fin ---- modifie les exercices sélectionnés
    context = {'form': form, 'parcours': parcours, 'communications':[], 'group' : group , 'role' : role , 'teacher': teacher, 'exercises': exercises , 'levels': levels , 'themes' : themes_tab , 'user': request.user , 'group_id' : group_id , 'relationships' :relationships  }

    return render(request, 'qcm/form_peuplate_parcours.html', context)



def individualise_parcours(request,id):
    teacher = request.user.teacher
    parcours = Parcours.objects.get(pk = id)
    relationships = Relationship.objects.filter(parcours = parcours).order_by("ranking")
    students = parcours.students.all()

    customexercises = Customexercise.objects.filter(parcourses = parcours).order_by("ranking")  

    role, group , group_id , access = get_complement(request, teacher, parcours)

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

        if relationship.students.count() != relationship.parcours.students.count() :
            data["indiv_hide"] = True
        else :
            data["indiv_hide"] = False
 
    return JsonResponse(data) 




def ajax_individualise_this_exercise(request):

    relationship_id = int(request.POST.get("relationship_id"))
    custom = int(request.POST.get("custom"))
    if custom :
        rc = Customexercise.objects.get(pk=relationship_id)
    else :
        rc = Relationship.objects.get(pk=relationship_id)
        parcours = rc.parcours
    
    students = rc.students.all
    data = {}
    data['html'] = render_to_string('qcm/ajax_individualise_this_exercise.html', {'rc' : rc, 'parcours' : parcours, 'students' : students, })

    return JsonResponse(data)







def list_parcours(request):

    teacher = request.user.teacher
    today = time_zone_user(teacher.user)

    parcourses = teacher_has_parcourses_folder(teacher,0 ,0 ) #  is_evaluation ,is_archive 
    nb_archive =  len(  teacher_has_own_parcourses_and_folder(teacher,0,1 )   ) 

    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche
 

    try :
        del request.session["group_id"]
    except:
        pass 
    try :
        del request.session["parcours_folder_id"]
    except:
        pass 

    return render(request, 'qcm/list_parcours.html', { 'parcourses' : parcourses , 'communications' : [] , 'relationships' : [],  'parcours' : None , 'group' : None , 'today' : today ,  'teacher' : teacher , 'nb_archive' : nb_archive })




def list_archives(request):

    teacher = request.user.teacher
    parcourses = teacher_has_parcourses(teacher,0 ,1 ) #  is_evaluation ,is_archive  
    today = time_zone_user(teacher.user)
    try :
        del request.session["group_id"]
    except:
        pass   

    return render(request, 'qcm/list_archives.html', { 'parcourses' : parcourses , 'parcours' : None , 'teacher' : teacher ,  'communications' : [] , 'relationships' : [], 'today' : today , })



def list_evaluations(request):
    teacher = request.user.teacher
    today = time_zone_user(teacher.user)
    parcourses = teacher_has_parcourses(teacher,1 ,0 ) #  is_evaluation ,is_archive    
    nb_archive = len( teacher_has_own_parcourses_and_folder(teacher,1,1 )  )
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche

    try :
        del request.session["group_id"]
    except:
        pass  

    return render(request, 'qcm/list_evaluations.html', { 'parcourses' : parcourses, 'parcours' : None ,  'teacher' : teacher ,  'communications' : [] , 'relationships' : []   ,  'today' : today , 'nb_archive' : nb_archive })

def list_evaluations_archives(request):
    teacher = request.user.teacher
    parcourses = teacher_has_parcourses(teacher,1 ,1 ) #  is_evaluation ,is_archive      
    today = time_zone_user(teacher.user)
    try :
        del request.session["group_id"]
    except:
        pass  

    return render(request, 'qcm/list_evaluations_archives.html', { 'parcourses' : parcourses, 'parcours' : None , 'teacher' : teacher , 'communications' : [] ,  'today' : today , 'relationships' : []   })



def clear_realtime(parcours_tab , today,  timer ):
    """  efface le realtime de plus de timer secondes sur un ensemble de parcours parcours_tab """
    today_delta = today.now() - timedelta(seconds = timer)
    Tracker.objects.filter(Q(parcours__in = parcours_tab)|Q(parcours__leaf_parcours__in = parcours_tab), date_created__lte= today_delta).delete()


##@user_is_group_teacher
def list_parcours_group(request,id):

    teacher = request.user.teacher
    today = time_zone_user(request.user)
    group = Group.objects.get(pk = id) 

    request.session["group_id"] = group.id

    role, group , group_id , access = get_complement(request, teacher, group)

    if not authorizing_access(teacher,group, access ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

 
    parcours_tab = []
    students = group.students.all()


    for student in students :
        if access :
            #if group.subject :
            #    pcs = Parcours.objects.filter(Q(teacher=teacher)|Q(author=teacher)|Q(coteachers = teacher),subject= group.subject, students= student, is_favorite=1).exclude(is_leaf=1).order_by("is_evaluation","ranking")
            #else :
            pcs = Parcours.objects.filter(Q(teacher=teacher)|Q(author=teacher)|Q(coteachers = teacher),students= student, is_favorite=1).exclude(is_leaf=1).order_by("is_evaluation","ranking")
        else :
            #if group.subject :
            #    pcs = student.students_to_parcours.filter(Q(teacher=teacher)|Q(author=teacher), is_favorite=1 ,subject= group.subject ).exclude(is_leaf=1).order_by("is_evaluation","ranking")
            #else :
            pcs = student.students_to_parcours.filter(Q(teacher=teacher)|Q(author=teacher), is_favorite=1 ).exclude(is_leaf=1).order_by("is_evaluation","ranking")
        for parcours in pcs : 
            if parcours not in parcours_tab   :
                parcours_tab.append(parcours)
            if len(parcours_tab) == teacher.teacher_parcours.count() :
                break

    ###efface le realtime de plus de 2 h
    clear_realtime(parcours_tab , today.now() ,  3600 )

    return render(request, 'qcm/list_parcours_group.html', {'parcours_tab': parcours_tab , 'teacher' : teacher , 'group': group,  'parcours' : None , 'communications' : [] , 'relationships' : [] , 'role' : role , 'today' : today })


@parcours_exists
def list_sub_parcours_group(request,idg,id):

    teacher = request.user.teacher
    today = time_zone_user(teacher.user)
    parcours = Parcours.objects.get(pk = id) 
    group = Group.objects.get(pk = idg) 
 
    role, group , group_id , access = get_complement(request, teacher, parcours)
    request.session["parcours_id"] = parcours.id
    request.session["group_id"] = group_id

    request.session["parcours_folder_id"] = parcours.id

    if not authorizing_access(teacher,parcours, True ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    parcours_tab = parcours.leaf_parcours.order_by("is_evaluation", "ranking")

    ###efface le realtime de plus de 2 h
    clear_realtime(parcours_tab , today.now() ,  3600 )

    context = {'parcours_tab': parcours_tab , 'teacher' : teacher , 'group' : group , 'parcours' : parcours,  'parcours_folder' : parcours,   'communications' : [] , 'relationships' : [] , 'role' : True , 'today' : today }

    return render(request, 'qcm/list_sub_parcours_group.html', context )






def parcours_progression(request,id,idg):

    parcours = Parcours.objects.get(id=id)
    teacher = request.user.teacher
    role, group , group_id , access = get_complement(request, teacher, parcours)
 

    if not authorizing_access(teacher,parcours, True ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')
    if idg :
        group = Group.objects.get(id = idg) 
        students_group = group.students.all()
        students_parcours = parcours.students.order_by("user__last_name")
        students = [student for student in students_parcours if student   in students_group] # Intersection des listes
        group_id = idg
    else :
        students = parcours.students.order_by("user__last_name")

    context = {'students': students, 'parcours': parcours, 'communications':[], 'group' : group , 'role' : role , 'teacher': teacher, 'group_id' : group_id   }

    return render(request, 'qcm/progression_group.html', context)




def parcours_progression_student(request,id):

    parcours = Parcours.objects.get(id=id)
    student = request.user.student
    if parcours.is_achievement : 
 
        students = parcours.students.order_by("user__last_name")
        context = {'students': students, 'parcours': parcours, 'student':student,  }
        return render(request, 'qcm/progression_group_student.html', context)
    else :
        messages.error(request,"accès interdit")
        return redirect('index')




def all_parcourses(request,is_eval):
    teacher = request.user.teacher
    #parcours_ids = Parcours.objects.values_list("id",flat=True).filter(Q(teacher__user__school = teacher.user.school)| Q(teacher__user_id=2480),is_evaluation = is_eval, is_share = 1,level__in = teacher.levels.all()).exclude(teacher=teacher).order_by('level').distinct()
    parcours_ids = []  

    parcourses , tab_id = [] , [] 
    for p_id in parcours_ids :
        if not p_id in tab_id :
            p =  Parcours.objects.get(pk = p_id)
            if p.exercises.count() > 0 :
                parcourses.append(p)
                tab_id.append(p_id)
 
    try :
        group_id = request.session.get("group_id",None)
        if group_id :
            group = Group.objects.get(pk = group_id)
        else :
            group = None   
    except :
        group = None

    try :
        parcours_id = request.session.get("parcours_id",None)
        if parcours_id :
            parcours = Parcours.objects.get(pk = parcours_id)
        else :
            parcours = None   
    except :
        parcours = None


    if request.user.school != None :
        inside = True
    else :
        inside = False

    #return render(request, 'qcm/all_parcourses.html', { 'teacher' : teacher ,   'parcourses': parcourses , 'inside' : inside , 'communications' : [] , 'parcours' : parcours , 'group' : group })
    return render(request, 'qcm/list_parcours_shared.html', { 'is_eval' : is_eval ,  'teacher' : teacher ,   'parcourses': parcourses , 'inside' : inside ,   'parcours' : parcours , 'group' : group   })



def ajax_all_parcourses(request):

    teacher = request.user.teacher
    data = {}
    is_eval = int(request.POST.get('is_eval',0))
    level_id = request.POST.get('level_id',0)
    subject_id = request.POST.get('subject_id',None)

    teacher_id = get_teacher_id_by_subject_id(subject_id)

    parcours_ids = Parcours.objects.values_list("id",flat=True).distinct().filter(Q(teacher__user__school = teacher.user.school)| Q(teacher__user_id=teacher_id),is_share = 1,is_evaluation = is_eval).exclude(exercises=None ,teacher=teacher).order_by('level')

    keywords = request.POST.get('keywords',None)

    if int(level_id) > 0 :
        level = Level.objects.get(pk=int(level_id))
        theme_ids = request.POST.getlist('theme_id',[])

        if len(theme_ids) > 0 :

            if theme_ids[0] != '' :
                themes_tab = []

                for theme_id in theme_ids :
                    themes_tab.append(theme_id) 

                if keywords :
                    parcourses = Parcours.objects.filter(Q(teacher__user__school = teacher.user.school)| Q(teacher__user_id=teacher_id),is_share = 1, is_evaluation = is_eval,
                                                        exercises__knowledge__theme__in = themes_tab, 
                                                        exercises__supportfile__title__contains = keywords, level_id = int(level_id)).exclude(teacher=teacher).order_by('author').distinct()
                else :
                    parcourses = Parcours.objects.filter(Q(teacher__user__school = teacher.user.school)| Q(teacher__user_id=teacher_id),is_share = 1, is_evaluation = is_eval,
                                                        exercises__knowledge__theme__in = themes_tab, level_id = int(level_id)).exclude(teacher=teacher).order_by('author').distinct()  
                    
            else :
                if keywords :
                    parcourses = Parcours.objects.filter(Q(teacher__user__school = teacher.user.school)| Q(teacher__user_id=teacher_id),is_share = 1, is_evaluation = is_eval,
                                                            exercises__supportfile__title__contains = keywords, level_id = int(level_id) ).exclude(teacher=teacher).order_by('author').distinct()

                else :
                    parcourses = Parcours.objects.filter(Q(teacher__user__school = teacher.user.school)| Q(teacher__user_id=teacher_id),is_share = 1, is_evaluation = is_eval,
                                                            level_id = int(level_id) ).exclude(teacher=teacher).order_by('author').distinct()

        else :
            if keywords:
                parcourses = Parcours.objects.filter(Q(teacher__user__school = teacher.user.school)| Q(teacher__user_id=teacher_id),is_share = 1,is_evaluation = is_eval, 
                                                        exercises__supportfile__title__contains = keywords  , level_id = int(level_id) ).exclude(teacher=teacher).order_by('author').distinct()
            else :
                parcourses = Parcours.objects.filter(Q(teacher__user__school = teacher.user.school)| Q(teacher__user_id=teacher_id),is_share = 1, is_evaluation = is_eval,
                                                        level_id = int(level_id) ).exclude(teacher=teacher).order_by('author').distinct()
    else :
        if keywords:
            parcourses = Parcours.objects.filter(Q(teacher__user__school = teacher.user.school)| Q(teacher__user_id=teacher_id),is_share = 1 , is_evaluation = is_eval, exercises__supportfile__title__contains = keywords ).exclude(teacher=teacher).order_by('author').distinct()
        else :
            parcourses = Parcours.objects.filter(Q(teacher__user__school = teacher.user.school)| Q(teacher__user_id=teacher_id),is_share = 1, is_evaluation = is_eval,).exclude(teacher=teacher).order_by('author').distinct()


    data['html'] = render_to_string('qcm/ajax_list_parcours.html', {'parcourses' : parcourses, 'teacher' : teacher ,  })
 
    return JsonResponse(data)


@csrf_exempt
def ajax_chargethemes_parcours(request):
    level_id =  request.POST.get("id_level")
    id_subject =  request.POST.get("id_subject")
    teacher = request.user.teacher

    teacher_id = get_teacher_id_by_subject_id(id_subject)

    data = {}
    level =  Level.objects.get(pk = level_id)

    thms = level.themes.values_list('id', 'name').filter(subject_id=id_subject).order_by("name")
    data['themes'] = list(thms)
    parcourses = Parcours.objects.filter(Q(teacher__user__school = teacher.user.school)| Q(teacher__user_id=teacher_id),is_share = 1, exercises__level_id = level_id ).exclude(teacher=teacher).order_by('author').distinct()

    data['html'] = render_to_string('qcm/ajax_list_parcours.html', {'parcourses' : parcourses, })

    return JsonResponse(data)


@csrf_exempt
def ajax_chargethemes_exercise(request):
    level_id =  request.POST.get("id_level")
    id_subject =  request.POST.get("id_subject")
    teacher = request.user.teacher

    data = {}
    level =  Level.objects.get(pk = level_id)

    thms = level.themes.values_list('id', 'name').filter(subject_id=id_subject).order_by("name")
    data['themes'] = list(thms)
    exercises = Exercise.objects.filter(level_id = level_id , theme__subject_id = id_subject ,  supportfile__is_title=0 ).order_by("theme","knowledge__waiting","knowledge","supportfile__ranking")

    #data['html'] = render_to_string('qcm/ajax_list_exercises_by_level.html', { 'exercises': exercises  , "teacher" : teacher , "level_id" : level_id })
    data['html'] = "<div class='alert alert-info'>Choisir un thème</div>"




    return JsonResponse(data)
 
 


def lock_all_exercises_for_student(dateur,parcours):

    for student in parcours.students.all() :
        for exercise in  parcours.exercises.all() :
            relationship = Relationship.objects.get(parcours=parcours, exercise = exercise) 
            if dateur :
                result, created = Exerciselocker.objects.get_or_create(student = student , relationship = relationship, custom = 0, defaults={"lock" : dateur})
                if not created :
                    Exerciselocker.objects.filter(student = student , relationship = relationship, custom = 0).update(lock = dateur)
            else :
                if Exerciselocker.objects.filter(student = student , relationship = relationship, custom = 0).exists():
                    res = Exerciselocker.objects.get(student = student , relationship = relationship, custom = 0)
                    res.delete() 

        for ce in Customexercise.objects.filter(parcourses = parcours) :
            if dateur :    
                result, created = Exerciselocker.objects.get_or_create(student = student , customexercise = ce, custom = 1, defaults={"lock" : dateur})
                if not created :
                    Exerciselocker.objects.filter(student = student , customexercise = ce, custom = 1).update(lock = dateur)
            else :
                if Exerciselocker.objects.filter(student = student , customexercise = ce, custom = 1).exists():
                    res = Exerciselocker.objects.get(student = student ,  customexercise = ce, custom = 1)
                    res.delete() 



def create_parcours(request,idp=0):
    """ 'parcours_is_folder' : False pour les vignettes et différencier si folder ou pas """
    teacher         = request.user.teacher
    levels          = teacher.levels.all()

    try :
        group_id = request.session.get("group_id")
        group = Group.objects.get(pk=group_id)
        form = ParcoursForm(request.POST or None, request.FILES or None, teacher = teacher, initial = {'subject': group.subject,'level': group.level,   })
    except :
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

    if idp > 0 :
        parcours_folder = Parcours.objects.get(pk = idp)
    else :
        parcours_folder = None

    if form.is_valid():
        nf = form.save(commit=False)
        nf.author = teacher
        nf.teacher = teacher
        nf.is_evaluation = 0

        if request.POST.get("this_image_selected",None) : # récupération de la vignette précréée et insertion dans l'instance du parcours.
            nf.vignette = request.POST.get("this_image_selected",None)

        if idp > 0 :
            nf.is_leaf = 1
        nf.save()
        ################################################
        ### Si le parcours est créé à partir d'un groupe
        try :
            nf.groups.add(group)
        except :
            pass
        ################################################
        form.save_m2m()

        group_ckeched_ids = request.POST.getlist('groups')
        nf.groups.set(group_ckeched_ids)

        for group_ckeched_id in group_ckeched_ids :
            group_ckeched = Group.objects.get(pk = group_ckeched_id)
            for s in group_ckeched.students.all() :
                nf.students.add(s)
        ################################################
        ### Si idp > 0 alors idp est le parcours dossier
        if idp > 0 :
            parcours_folder = Parcours.objects.get(pk = idp)
            parcours_folder.leaf_parcours.add(nf)
        else :
            for pid in request.POST.getlist("folder_parcours") :
                parcours_folder = Parcours.objects.get(pk = pid)
                parcours_folder.leaf_parcours.add(nf)            
        ################################################

        sg_students =  request.POST.getlist('students_sg')
        for s_id in sg_students :
            student = Student.objects.get(user_id = s_id)
            nf.students.add(student)

        if nf.stop  :
            locker = 1
        else :
            locker = 0 

        i = 0
        for exercise in form.cleaned_data.get('exercises'):
            exercise = Exercise.objects.get(pk=exercise.id)
            relationship = Relationship.objects.create(parcours=nf, exercise=exercise, ranking=i, is_lock = locker ,
                                                       duration=exercise.supportfile.duration,
                                                       situation=exercise.supportfile.situation)
            relationship.students.set(form.cleaned_data.get('students'))
            relationship.skills.set(exercise.supportfile.skills.all()) 
            i += 1

        lock_all_exercises_for_student(nf.stop,nf)  


        if request.POST.get("save_and_choose") :
            return redirect('peuplate_parcours', nf.id)
        elif group_id and idp > 0 :
            if group_id > 0 and idp > 0 :
                return redirect('list_sub_parcours_group' , group_id, idp)              
        elif request.session.has_key("group_id") :
            group_id = request.session.get("group_id")
            if group_id :
                return redirect('list_parcours_group' , group_id)
            else :
                return redirect('parcours')
        else:
            return redirect('parcours')
    else:
        print(form.errors)
    # gestion des images vignettes    
    images = [] 
    if request.session.has_key("group_id") :
        group_id = request.session.get("group_id",None)        
        if group_id :
            group = Group.objects.get(pk = group_id)
            images = group.level.level_parcours.values_list("vignette", flat = True).filter(subject_id=group.subject).exclude(vignette=" ").distinct()
        else :
            group = None
        
    else :
        group_id = None
        group = None
        request.session["group_id"]  = None
 

    context = {'form': form,  'parcours_is_folder' : False,   'teacher': teacher,  'groups': groups,  'levels': levels, 'idg': 0,  'parcours_folder': parcours_folder ,  'themes' : themes_tab, 'group_id': group_id , 'parcours': None,  'relationships': [], 'share_groups' : share_groups , 
               'exercises': [], 'levels': levels, 'themes': themes_tab, 'students_checked': 0 , 'communications' : [],  'group': group , 'role' : True , 'idp' : idp , 'images' : images }

    return render(request, 'qcm/form_parcours.html', context)
 



@parcours_exists
def update_parcours(request, id, idg=0 ):
    """ 'parcours_is_folder' : False pour les vignettes et différencier si folder ou pas """

    teacher = Teacher.objects.get(user_id=request.user.id)
    levels = teacher.levels.all()
 
    parcours = Parcours.objects.get(id=id)
    folder_parcourses = teacher.teacher_parcours.filter(leaf_parcours= parcours).order_by("level") 
 
    form = UpdateParcoursForm(request.POST or None, request.FILES or None, instance=parcours, teacher=teacher, initial={ 'folder_parcours' : folder_parcourses })

    """ affiche le parcours existant avant la modif en ajax"""
    exercises = parcours.exercises.filter(supportfile__is_title=0).order_by("theme","knowledge__waiting","knowledge","ranking")
    """ fin """
    themes_tab = []
    for level in levels:
        for theme in level.themes.all():
            if not theme in themes_tab:
                themes_tab.append(theme)

    groups = Group.objects.filter(teacher=teacher).prefetch_related('students').order_by("level")
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("ranking")


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

            if request.POST.get("this_image_selected",None) : # récupération de la vignette précréée et insertion dans l'instance du parcours.
                nf.vignette = request.POST.get("this_image_selected",None)

            nf.save()
            form.save_m2m()

            nf.groups.clear()
            nf.groups.set(request.POST.getlist('groups'))
            

            for pid in request.POST.getlist("folder_parcours") :
                parcours_folder = Parcours.objects.get(pk = pid)
                parcours_folder.leaf_parcours.add(nf)  

 
            sg_students =  request.POST.getlist('students_sg')
            for s_id in sg_students :
                student = Student.objects.get(user_id = s_id)
                nf.students.add(student)

            try:
                for exercise in parcours.exercises.all():
                    relationship = Relationship.objects.get(parcours=nf, exercise=exercise)
                    if len( form.cleaned_data.get('students') ) > 0  : 
                        relationship.students.set(form.cleaned_data.get('students'))
                    if len(sg_students) > 0  : 
                        relationship.students.set(sg_students)
            except:
                pass
            
            lock_all_exercises_for_student(nf.stop,parcours)

            if request.POST.get("save_and_choose") :
                return redirect('peuplate_parcours', nf.id)
            elif idg == 99999999999:
                return redirect('index')
            elif request.session.get("parcours_folder_id",None) :
                parcours_folder_id = request.session.get("parcours_folder_id",None)
                return redirect('list_sub_parcours_group' , idg , parcours_folder_id )  
            elif idg > 0:
                return redirect('list_parcours_group', idg)     
            else:
                return redirect('parcours')

        else :
            print(form.errors)
    images = []
    if idg > 0 and idg < 99999999999 :
        group_id = idg
        request.session["group_id"] = idg
        group = Group.objects.get(pk = group_id)
        images = group.level.level_parcours.values_list("vignette", flat = True).filter(subject_id=group.subject).exclude(vignette=" ").distinct()
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
               'exercises': exercises, 'parcours_is_folder' : False, 'levels': levels, 'themes': themes_tab, 'students_checked': students_checked, 'communications' : [], 'role' : role , 'images' : images }

    return render(request, 'qcm/form_parcours.html', context)

#@user_is_parcours_teacher 
def archive_parcours(request, id, idg=0):

    parcours = Parcours.objects.filter(id=id).update(is_archive=1,is_favorite=0,is_publish=0)
    teacher = request.user.teacher 

    if idg == 99999999999:
        return redirect('index')
    elif idg == 0 :
        return redirect('parcours')
    else :
        return redirect('list_parcours_group', idg)

@parcours_exists
def unarchive_parcours(request, id, idg=0):

    parcours = Parcours.objects.filter(id=id).update(is_archive=0,is_favorite=0,is_publish=0)
    teacher = request.user.teacher

    if idg == 99999999999:
        return redirect('index')
    elif idg == 0 :
        return redirect('parcours')
    else :
        return redirect('list_parcours_group', idg)

@parcours_exists
def delete_parcours(request, id, idg=0):

    parcours = Parcours.objects.get(id=id)
    parcours_is_evaluation = parcours.is_evaluation
    parcours.students.clear()

    teacher = request.user.teacher

    if not authorizing_access(teacher, parcours, False ):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

 
    for r in parcours.parcours_relationship.all() :
        r.students.clear()
        r.skills.clear()
        ls = r.relationship_exerciselocker.all()
        for l in ls :
            l.delete()
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
    elif idg == 0 and parcours_is_evaluation :
        return redirect('evaluations')
    elif idg == 0 :
        return redirect('parcours')
    else :
        return redirect('list_parcours_group', idg)



def ordering_number(parcours):

    listing_ordered = set() 
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("ranking")
    customexercises = Customexercise.objects.filter(parcourses=parcours).order_by("ranking") 
    listing_ordered.update(relationships)
    listing_ordered.update(customexercises)

    listing_order = sorted(listing_ordered, key=attrgetter('ranking')) #set trié par ranking


    nb_exo_only, nb_exo_visible  = [] , []   
    i , j = 0, 0

    for item in listing_order :

        try :
            if not item.exercise.supportfile.is_title and not item.exercise.supportfile.is_subtitle:
                i += 1
            nb_exo_only.append(i)
            if not item.exercise.supportfile.is_title and not item.exercise.supportfile.is_subtitle and item.is_publish != 0:
                j += 1
            nb_exo_visible.append(j)
        except :
            i += 1
            nb_exo_only.append(i)
            if item.is_publish :
                j += 1
            nb_exo_visible.append(j)

    return listing_order , nb_exo_only, nb_exo_visible  




def rcs_for_realtime(parcours):

    listing_ordered = set() 
    relationships = Relationship.objects.filter(is_publish=1,parcours=parcours,exercise__supportfile__is_title=0).prefetch_related('exercise__supportfile').order_by("ranking")
    customexercises = Customexercise.objects.filter(is_publish=1,parcourses=parcours).order_by("ranking") 
    listing_ordered.update(relationships)
    listing_ordered.update(customexercises)

    listing_order = sorted(listing_ordered, key=attrgetter('ranking')) #set trié par ranking

    return listing_order



@parcours_exists
def show_parcours(request, id):
    """ show parcours coté prof """
    parcours = Parcours.objects.get(id=id)
    user = User.objects.get(pk=request.user.id)
    teacher = Teacher.objects.get(user=user)

    today = time_zone_user(user)

    role, group , group_id , access = get_complement(request, teacher, parcours)

    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')
 
    relationships_customexercises , nb_exo_only, nb_exo_visible  = ordering_number(parcours)

    students_p_or_g = students_from_p_or_g(request,parcours)
    parcours_group = []
    for s in students_p_or_g :
        pses = s.students_to_parcours.all()
        for p in pses :
            if p not in  parcours_group :
                parcours_group.append(p)

    nb_students_p_or_g = len(students_p_or_g)

    skills = Skill.objects.all()

    parcours_folder_id = request.session.get("parcours_folder_id",None)
    parcours_folder = None
    if parcours_folder_id :
        parcours_folder = Parcours.objects.get(pk = parcours_folder_id)


    form_reporting = DocumentReportForm(request.POST or None )
 
    context = { 'parcours': parcours, 'teacher': teacher,  'communications' : [] ,  'today' : today , 'skills': skills,  'form_reporting': form_reporting, 'user' : user ,
               'students_from_p_or_g': students_p_or_g,   'nb_exo_visible': nb_exo_visible , 'nb_students_p_or_g' : nb_students_p_or_g ,  'relationships_customexercises': relationships_customexercises,
               'nb_exo_only': nb_exo_only,'group_id': group_id, 'group': group, 'role' : role, 'parcours_group' : parcours_group , 'parcours_folder' : parcours_folder   }

    return render(request, 'qcm/show_parcours.html', context) 




def ordering_number_for_student(parcours,student):
    """ créer une seule liste des exercices personnalisés et des exercices sacado coté eleve """
    listing_ordered = set() 
    relationships = Relationship.objects.filter(parcours=parcours, students=student, is_publish=1).prefetch_related('exercise__supportfile').order_by("ranking")
    customexercises = Customexercise.objects.filter(parcourses=parcours, students=student, is_publish=1).order_by("ranking") 
    listing_ordered.update(relationships)
    listing_ordered.update(customexercises)

    listing_order = sorted(listing_ordered, key=attrgetter('ranking')) #set trié par ranking


    nb_exo_only, nb_exo_visible  = [] , []   
    i , j = 0, 0

    for item in listing_order :
        try :
            if not item.exercise.supportfile.is_title and not item.exercise.supportfile.is_subtitle:
                i += 1
            nb_exo_only.append(i)
            if not item.exercise.supportfile.is_title and not item.exercise.supportfile.is_subtitle and item.is_publish != 0:
                j += 1
            nb_exo_visible.append(j)
        except :
            i += 1
            nb_exo_only.append(i)
            if item.is_publish :
                j += 1
            nb_exo_visible.append(j)

    return listing_order , nb_exo_only, nb_exo_visible


@parcours_exists
def show_parcours_student(request, id):

    parcours = Parcours.objects.get(id=id)
    user = request.user
    student = user.student
    today = time_zone_user(user)
    stage = get_stage(user)

    #tracker_execute_exercise(True ,  user , id , None , 0)
 
    if parcours.is_folder :

        parcourses = parcours.leaf_parcours.filter(Q(is_publish=1)|Q(start__lte=today,stop__gte=today)).order_by("ranking")
        nb_parcourses = parcourses.count()
        context = {'parcourses': parcourses , 'nb_parcourses': nb_parcourses ,   'parcours': parcours ,   'stage' : stage , 'today' : today ,  }

        return render(request, 'qcm/show_parcours_folder_student.html', context)

    else :

        relationships_customexercises , nb_exo_only, nb_exo_visible  = ordering_number_for_student(parcours,student)
        nb_exercises = len(relationships_customexercises)

        courses = parcours.course.filter(Q(is_publish=1)|Q(publish_start__lte=today,publish_end__gte=today)).order_by("ranking")
        quizzes = parcours.quizz.filter(Q(is_publish=1)|Q(start__lte=today,stop__gte=today)).order_by("-date_modified")

        context = { 'stage' : stage , 'relationships_customexercises': relationships_customexercises,
                    'courses':courses , 'parcours': parcours, 'student': student, 'nb_exercises': nb_exercises,'nb_exo_only': nb_exo_only, 
                    'today': today , 'quizzes': quizzes ,   }

        return render(request, 'qcm/show_parcours_student.html', context)


@parcours_exists
def show_parcours_visual(request, id):

    parcours = Parcours.objects.get(id=id)
    teacher = request.user.teacher 

    role, group , group_id , access = get_complement(request, teacher, parcours)


    relationships = Relationship.objects.filter(parcours=parcours,  is_publish=1 ).order_by("ranking")
    nb_exo_only = [] 
    i=0
    for r in relationships :
        if r.exercise.supportfile.is_title or r.exercise.supportfile.is_subtitle:
            i=0
        else :
            i+=1
        nb_exo_only.append(i)
    nb_exercises = parcours.exercises.filter(supportfile__is_title=0).count()
    context = {'relationships': relationships,  'parcours': parcours,   'nb_exo_only': nb_exo_only, 'nb_exercises': nb_exercises,  'group' : group ,  }
 
    return render(request, 'qcm/show_parcours_visual.html', context)



def replace_exercise_into_parcours(request):

    exercise_id = request.POST.get("change_parcours_exercise_id")
    parcours_id = request.POST.get("change_parcours_parcours_id")
    custom = request.POST.get("change_parcours_custom")

    parcourses_id = request.POST.getlist("change_into_parcours")
    parcours = Parcours.objects.get(pk = parcours_id)

    if request.method == "POST" :

        if custom == "0" :
            relationship = Relationship.objects.get(pk = exercise_id)
            
            for p_id in parcourses_id :
                prcrs = Parcours.objects.get(pk = p_id)                
                Relationship.objects.filter(pk = int(exercise_id)).update(parcours = prcrs)
                try :
                    Studentanswer.objects.filter(exercise = relationship.exercise, parcours = parcours).update(parcours = prcrs)
                except :
                    pass

        else :
            customexercise = Customexercise.objects.get(pk = exercise_id)
            parcours = Parcours.objects.get(pk = parcours_id)
            customexercise.parcourses.remove(prcrs)
            for p_id in parcourses_id :
                prcrs = Parcours.objects.get(pk = p_id)
                customexercise.parcourses.add(prcrs)
                try :
                    Customanswerbystudent.objects.filter(customexercise = customexercise, parcours = parcours).update(parcours =  prcrs)
                    Correctionskillcustomexercise.objects.filter(customexercise = customexercise, parcours = parcours).update(parcours =  prcrs)
                    Correctionknowledgecustomexercise.objects.filter(customexercise = customexercise, parcours = parcours).update(parcours =  prcrs)
                except :
                    pass


    return redirect('show_parcours', parcours_id)

@parcours_exists 
def result_parcours(request, id):

    parcours = Parcours.objects.get(id=id)
    students = students_from_p_or_g(request,parcours) # liste des élèves d'un parcours donné 
    teacher = request.user.teacher

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

    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')

    if parcours.is_folder :
        relationships = Relationship.objects.filter(parcours__in=parcours.leaf_parcours.all(),exercise__supportfile__is_title=0).prefetch_related('exercise').order_by("ranking")

        custom_set = set()
        for p in parcours.leaf_parcours.all():
            cstm = p.parcours_customexercises.all() 
            custom_set.update(set(cstm))
        customexercises = list(custom_set)

    else :
        relationships = Relationship.objects.filter(parcours=parcours, exercise__supportfile__is_title=0).prefetch_related('exercise').order_by("ranking")
        customexercises = parcours.parcours_customexercises.all() 


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



    form = EmailForm(request.POST or None )

    stage = get_stage(teacher.user)

    context = {  'customexercises': customexercises, 'relationships': relationships, 'parcours': parcours, 'students': students, 'themes': themes_tab, 'form': form,  'group_id' : group_id  , 'stage' : stage, 'communications' : [] , 'role' : role }

    return render(request, 'qcm/result_parcours.html', context )

########## Sans doute plus utilisée ???? 
@parcours_exists
def result_parcours_theme(request, id, idt):

    teacher = Teacher.objects.get(user=request.user)

    parcours = Parcours.objects.get(id=id)
    students = students_from_p_or_g(request,parcours)

    role, group , group_id , access = get_complement(request, teacher, parcours)

    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')

    theme = Theme.objects.get(id=idt)
    exercises = Exercise.objects.filter(knowledge__theme = theme, supportfile__is_title=0).order_by("id")
    


    if parcours.is_folder :
        relationships = Relationship.objects.filter(parcours__in=parcours.leaf_parcours.all(),exercise__in=exercises, exercise__supportfile__is_title=0).order_by("ranking")

        custom_set = set()
        for p in parcours.leaf_parcours.all():
            cstm = p.parcours_customexercises.all() 
            custom_set.update(set(cstm))
        customexercises = list(custom_set)

    else :
        relationships = Relationship.objects.filter(parcours= parcours,exercise__in=exercises, exercise__supportfile__is_title=0 ).order_by("ranking")
        customexercises = parcours.parcours_customexercises.all() 


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

def get_items_from_parcours(parcours) :
    """
    Permet de déterminer les compétences dans l'ordre d'apparition du BO dans un parcours
    """
    if parcours.is_folder :
        relationships = Relationship.objects.filter(parcours__in=parcours.leaf_parcours.all(), exercise__supportfile__is_title=0).prefetch_related('exercise__supportfile').order_by("ranking")

        custom_set = set()
        for p in parcours.leaf_parcours.all():
            cstm = p.parcours_customexercises.all() 
            custom_set.update(set(cstm))
        customexercises = list(custom_set)

    else :
        relationships = Relationship.objects.filter(parcours= parcours, exercise__supportfile__is_title=0).prefetch_related('exercise__supportfile').order_by("ranking")
        customexercises = parcours.parcours_customexercises.all() 

    skill_set = set()
    for relationship in relationships :
        skill_set.update(set(relationship.skills.all()))


    for ce in  customexercises :
        skill_set.update(set(ce.skills.all()))

    skill_tab = []
    for s in Skill.objects.filter(subject__in = parcours.teacher.subjects.all()):
        if s in skill_set :
            skill_tab.append(s)

    return relationships , skill_tab 


@parcours_exists
def result_parcours_skill(request, id):

    teacher = Teacher.objects.get(user=request.user)
    parcours = Parcours.objects.get(id=id)
    students = students_from_p_or_g(request,parcours)

    role, group , group_id , access = get_complement(request, teacher, parcours)

    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')
    form = EmailForm(request.POST or None)

 
    relationships = get_items_from_parcours(parcours)[0]
    skill_tab =  get_items_from_parcours(parcours)[1]

 
    stage = get_stage(teacher.user)
    context = {  'relationships': relationships,  'students': students, 'parcours': parcours,  'form': form, 'skill_tab' : skill_tab, 'group' : group, 'group_id' : group_id, 'stage' : stage , 'communications' : [] , 'role' : role  }

    return render(request, 'qcm/result_parcours_skill.html', context )




@parcours_exists
def result_parcours_knowledge(request, id):

    teacher = Teacher.objects.get(user=request.user)
    parcours = Parcours.objects.get(id=id)
    students = students_from_p_or_g(request,parcours)

    form = EmailForm(request.POST or None)
 

    if parcours.is_folder :
        relationships = Relationship.objects.filter(parcours__in=parcours.leaf_parcours.all(), exercise__supportfile__is_title=0).prefetch_related('exercise__supportfile').order_by("ranking")

        custom_set = set()
        for p in parcours.leaf_parcours.all():
            cstm = p.parcours_customexercises.all() 
            custom_set.update(set(cstm))
        customexercises = list(custom_set)

        knowledge_set = set()
        for p in parcours.leaf_parcours.all():
            knw = p.exercises.values_list("knowledge",flat=True).filter(supportfile__is_title=0).order_by("knowledge").distinct()
            knowledge_set.update(set(knw))
        knwldgs = list(knowledge_set)        

    else :
        relationships = Relationship.objects.filter(parcours=parcours, exercise__supportfile__is_title=0).prefetch_related('exercise__supportfile').order_by("ranking")
        customexercises = parcours.parcours_customexercises.all() 
        knwldgs = parcours.exercises.values_list("knowledge_id",flat=True).filter(supportfile__is_title=0).order_by("knowledge").distinct()



    knowledges,knowledge_ids = [], []
         
    role, group , group_id , access = get_complement(request, teacher, parcours)
 

    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')


    for ce in  customexercises :
        for knowledge in ce.knowledges.all() :
            knowledges.append(knowledge)

    for k_id in knwldgs :
        if k_id not in knowledge_ids :
            k = Knowledge.objects.get(pk = k_id)
            knowledge_ids.append(k_id)
            knowledges.append(k)

    stage = get_stage(teacher.user)
    context = {  'relationships': relationships,  'students': students, 'parcours': parcours,  'form': form, 'exercise_knowledges' : knowledges, 'group_id' : group_id, 'stage' : stage , 'communications' : [] , 'role' : role  }

    return render(request, 'qcm/result_parcours_knowledge.html', context )
 


@parcours_exists
def result_parcours_waiting(request, id):

    teacher = request.user.teacher
    parcours = Parcours.objects.get(id=id)
    students = students_from_p_or_g(request,parcours)

    form = EmailForm(request.POST or None)
 

    if parcours.is_folder :
        relationships = Relationship.objects.filter(parcours__in=parcours.leaf_parcours.all(), exercise__supportfile__is_title=0).prefetch_related('exercise__supportfile').order_by("ranking")

        custom_set = set()
        for p in parcours.leaf_parcours.all():
            cstm = p.parcours_customexercises.all() 
            custom_set.update(set(cstm))
        customexercises = list(custom_set)

        knowledge_set = set()
        for p in parcours.leaf_parcours.all():
            knw = p.exercises.values_list("knowledge",flat=True).filter(supportfile__is_title=0).order_by("knowledge").distinct()
            knowledge_set.update(set(knw))
        knwldgs = list(knowledge_set)        

    else :
        relationships = Relationship.objects.filter(parcours=parcours, exercise__supportfile__is_title=0).prefetch_related('exercise__supportfile').order_by("ranking")
        customexercises = parcours.parcours_customexercises.all() 
        knwldgs = parcours.exercises.values_list("knowledge_id",flat=True).filter(supportfile__is_title=0).order_by("knowledge").distinct()


    waitings,waiting_ids , wtngs = [], [] , []
 

    role, group , group_id , access = get_complement(request, teacher, parcours)


    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')

    for ce in  customexercises :
        for knowledge in ce.knowledges.all() :
            waitings.append(knowledge.waiting)

    for k_id in knwldgs :
        k = Knowledge.objects.get(pk = k_id)
        if k.waiting.name not in waiting_ids :
            waiting_ids.append(k.waiting.name)
            waitings.append(k.waiting)


    stage = get_stage(teacher.user)
    context = {  'relationships': relationships,  'students': students, 'parcours': parcours,  'form': form, 'exercise_waitings' : waitings, 'group_id' : group_id, 'stage' : stage , 'communications' : [] , 'role' : role  }

    return render(request, 'qcm/result_parcours_waiting.html', context )





def check_level_by_point(student, point):
    point = int(point)
    if student.user.school :
        school = student.user.school
        stage = Stage.objects.get(school = school)

        if point > stage.up :
            level = "darkgreen"
        elif point > stage.medium :
            level = "green"
        elif point > stage.low :
            level = "warning"
        elif point > -1 :
            level = "danger"
        else :
            level = "default"
    else : 
        stage = { "low" : 50 ,  "medium" : 70 ,  "up" : 85  }

        if point > stage["up"]  :
            level = "darkgreen"
        elif point > stage["medium"]  :
            level = "green"
        elif point > stage["low"]  :
            level = "warning"
        elif point > -1 :
            level = "warning"
        else :
            level = "default"
    rep = "<i class='fa fa-square text-"+level+" pull-right'></i>"
 
    return rep
 



def get_student_result_from_eval(s, parcours, exercises,relationships,skills, knowledges,parcours_duration) : 

    customexercises = parcours.parcours_customexercises.filter(students=s).order_by("ranking")

    student = {"percent" : "" , "total_numexo" : "" , "good_answer" : "" , "test_duration" : False ,  "duration" : "" , "average_score" : "" ,"last_connexion" : "" ,"median" : "" ,"score" : "" ,"score_tab" : "" }
    student.update({"total_note":"", "details_note":"" ,  "detail_skill":"" ,  "detail_knowledge":"" , "ajust":"" , })
    student["name"] = s

    studentanswers =  Studentanswer.objects.filter(student=s,  exercise__in = exercises , parcours=parcours).order_by("-date")

    studentanswer_tab , student_tab  = [], []
    for studentanswer in studentanswers :
        if studentanswer.exercise not in studentanswer_tab :
            studentanswer_tab.append(studentanswer.exercise)
            student_tab.append(studentanswer)

    #nb_exo_w = s.student_written_answer.filter(relationship__exercise__in = studentanswer_tab, relationship__parcours = parcours, relationship__is_publish = 1 ).count()
    nb_exo_ce = s.student_custom_answer.filter(parcours = parcours, customexercise__is_publish = 1 ).count()
    #nb_exo  = len(studentanswer_tab) + nb_exo_w + nb_exo_ce
    nb_exo  = len(studentanswer_tab) +  nb_exo_ce
    student["nb_exo"] = nb_exo
    duration, score, total_numexo, good_answer = 0, 0, 0, 0
    tab, tab_date = [], []
    student["legal_duration"] = parcours.duration
    total_nb_exo = len(relationships)
    student["total_nb_exo"] = total_nb_exo       

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
            if duration > 0 :
                student["duration"] = convert_seconds_in_time(duration)
            else :
                student["duration"] = ""
            student["average_score"] = int(average_score)
            student["good_answer"] = int(good_answer)
            student["total_numexo"] = int(total_numexo)
            student["last_connexion"] = studentanswer.date
            student["score"] = int(score)
            student["score_tab"] = student_tab
            if duration > parcours_duration : 
                student["test_duration"] = True
            else :
                student["test_duration"] = False 
            tab.sort()
            if len(tab)%2 == 0 :
                med = (tab[len(tab)//2-1]+tab[(len(tab))//2])/2 ### len(tab)-1 , ce -1 est causé par le rang 0 du tableau
            else:
                med = tab[(len(tab)-1)//2]
            student["median"] = int(med)
            student["percent"] = math.ceil( int(good_answer)/int(total_numexo) * 100 )  
            student["ajust"] = math.ceil( (nb_exo / total_nb_exo ) * int(good_answer)/int(total_numexo) * 100  )   
        else :
            try :
                average_score = int(score)
                if duration > 0 :
                    student["duration"] = convert_seconds_in_time(duration)
                else :
                    student["duration"] = ""
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
                student["ajust"] = math.ceil( (nb_exo / total_nb_exo ) * int(good_answer)/int(total_numexo) * 100  )   
            except :
                pass         
    except :
        pass

    details_c , score_custom , cen , score_total = "" , 0 , [] , 0
    total_knowledge, total_skill, detail_skill, detail_knowledge = 0,0, "",""
    for ce in customexercises :
        score_total += float(ce.mark)
        if ce.is_mark :
            try:
                cen = Customanswerbystudent.objects.get(customexercise = ce, student=s, parcours = parcours)
                if cen.point :
                    score_custom +=  float(cen.point)
            except :
                pass

    student["score_custom"] = score_custom
    student["tab_custom"] = cen
    student["score_total"] = int(score_total)

    for skill in  skills:

        tot_s = total_by_skill_by_student(skill,relationships,parcours,s)
       
        detail_skill += skill.name + " " +check_level_by_point(s,tot_s) + "<br>" 

    student["detail_skill"] = detail_skill

    for knowledge in  knowledges :

        tot_k = total_by_knowledge_by_student(knowledge,relationships,parcours,s)

        detail_knowledge += knowledge.name + " "  +check_level_by_point(s,tot_k) + "<br>" 

    student["detail_knowledge"] = detail_knowledge 

    return student


@parcours_exists
def stat_evaluation(request, id):

    teacher = request.user.teacher
    stage = get_stage(teacher.user)
    parcours = Parcours.objects.get(id=id)
    skills = skills_in_parcours(request,parcours)
    knowledges = knowledges_in_parcours(parcours)
    #exercises = parcours.exercises.all()
    relationships = Relationship.objects.filter(parcours=parcours,is_publish = 1,exercise__supportfile__is_title=0).order_by("ranking")
    parcours_duration = parcours.duration #durée prévue pour le téléchargement
    exercises = []
    for r in relationships :
        parcours_duration += r.duration
        exercises.append(r.exercise)

    form = EmailForm(request.POST or None )
    stats = []
 
    role, group , group_id , access = get_complement(request, teacher, parcours)


    if not authorizing_access(teacher, parcours,access):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    students = students_from_p_or_g(request,parcours) 

    for s in students :
        student = get_student_result_from_eval(s, parcours, exercises,relationships,skills, knowledges,parcours_duration) 
        stats.append(student)


    context = { 'parcours': parcours, 'form': form, 'stats':stats , 'group_id': group_id , 'group': group , 'relationships' : relationships , 'stage' : stage , 'role' : role  }

    return render(request, 'qcm/stat_parcours.html', context )




 
def redo_evaluation(request):

    data = {}     
    parcours_id = request.POST.get("parcours_id", None)
    student_id  = request.POST.get("student_id", None)
    student     = Student.objects.get(pk=int(student_id) )
    parcours    = Parcours.objects.get(pk=int(parcours_id) )

    student.answers.filter(parcours=parcours).delete() # toutes les répones de cet élève à ce parcours/évaluation
    student.student_correctionskill.filter(parcours= parcours).delete()
    student.student_resultggbskills.filter(relationship__parcours = parcours).delete()  
    student.student_exerciselocker.filter( relationship__parcours = parcours, custom = 0).delete()     
    student.student_correctionknowledge.filter(parcours = parcours).delete()

    skills = skills_in_parcours(request,parcours)
    knowledges = knowledges_in_parcours(parcours)

    detail_knowledge = ""
    detail_skill     = ""

    for knowledge in  knowledges :
        detail_knowledge += knowledge.name + "<i class='fa fa-square text-default pull-right'></i> <br>" 

    for skill in  skills :
        detail_skill += knowledge.name + "<i class='fa fa-square text-default pull-right'></i> <br>" 

    data["skills"]    = detail_skill 
    data["knowledges"] = detail_knowledge  

    return JsonResponse(data)




def add_exercice_in_a_parcours(request):

    e = request.POST.get('exercise',None)
    if e :
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

            relation = Relationship.objects.create(parcours = parcours , exercise = exercise , ranking=  r, is_publish= 1 , start= None , date_limit= None, duration= exercise.supportfile.duration, situation= exercise.supportfile.situation ) 
            relation.skills.set(exercise.supportfile.skills.all())   
            i +=1

    return redirect('exercises')


@parcours_exists
def clone_parcours(request, id, course_on ):
    """ cloner un parcours """

    teacher = request.user.teacher
    parcours = Parcours.objects.get(pk=id) # parcours à cloner
    relationships = parcours.parcours_relationship.all() 
    courses = parcours.course.filter(is_share = 1)
    # clone le parcours
    parcours.pk = None
    parcours.title = parcours.title+"-2"
    parcours.teacher = teacher
    parcours.is_publish = 0
    parcours.is_leaf = 0
    parcours.is_archive = 0
    parcours.is_share = 0
    parcours.is_favorite = 1
    parcours.code = str(uuid.uuid4())[:8]  
    parcours.save()
    # ajoute le parcours cloné dans le dossier prcrs
    try :
        prcrs_id = request.session.get("parcours_id",None)
        if prcrs_id :
            prcrs = Parcours.objects.get(pk = prcrs_id)
            parcours.is_leaf = 1
            prcrs.leaf_parcours.add(parcours)
        else :
            prcrs = None   
    except :
        prcrs_id = None
        prcrs = None


    # ajoute le group au parcours si group    
    try :
        group_id = request.session.get("group_id",None)
        if group_id :
            group = Group.objects.get(pk = group_id)
            parcours.groups.add(group)
            if prcrs_id : 
                Parcours.objects.filter(pk = prcrs_id).update(subject = group.subject)
                Parcours.objects.filter(pk = prcrs_id).update(level = group.level)
        else :
            group = None   
    except :
        group = None



    former_relationship_ids = []

    if course_on == 1 : 
        for course in courses :

            old_relationships = course.relationships.all()
            # clone le cours associé au parcours
            course.pk = None
            course.parcours = parcours
            course.save()


            for relationship in old_relationships :
                # clone l'exercice rattaché au cours du parcours 
                if not relationship.id in former_relationship_ids :
                    relationship.pk = None
                    relationship.parcours = parcours
                    relationship.save() 
                course.relationships.add(relationship)

                former_relationship_ids.append(relationship.id)

    # clone tous les exercices rattachés au parcours 
    for relationship in relationships :
        try :
            relationship.pk = None
            relationship.parcours = parcours
            relationship.save()  
        except :
            pass

    messages.success(request, "Duplication réalisée avec succès. Bonne utilisation.")


    if group_id :
        if parcours.is_evaluation :
            return redirect('update_evaluation',  parcours.id, group_id)
        else :
            return redirect('update_parcours',  parcours.id, group_id)
    else :
        if parcours.is_evaluation :
            return redirect('update_evaluation' , parcours.id, 0)
        else :
            return redirect('all_parcourses', 0 )



 
def ajax_parcours_get_exercise_custom(request):

    teacher = request.user.teacher 
    exercise_id =  int(request.POST.get("exercise_id"))
    customexercise = Customexercise.objects.get(pk=exercise_id)
    parcourses =  teacher.teacher_parcours.all()    

    context = {  'customexercise': customexercise , 'parcourses': parcourses , 'teacher' : teacher  }
    data = {}
    data['html'] = render_to_string('qcm/ajax_parcours_get_exercise_custom.html', context)
 
    return JsonResponse(data)
 
def parcours_clone_exercise_custom(request):

    teacher = request.user.teacher
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
        usr = request.user
        email = ""
        if usr.email :
            email = usr.email
        msg = "Message envoyé par l'utilisateur #"+str(usr.id)+", "+usr.last_name+", "+email+" :\n\nL'exercice dont l'id est -- "+str(exercise_id)+" --  décrit ci-dessous : \n Savoir faire visé : "+exercise.knowledge.name+ " \n Niveau : "+exercise.level.name+  "  \n Thème : "+exercise.theme.name +" comporte un problème. \n  S'il est identifié par l'utilisateur, voici la description :  \n" + message   
        response = "\n\n Pour répondre, utiliser ces liens en remplaçant le - par un slash :  sacado.xyz-account-response_from_mail-"+str(usr.id)+"\n\n Pour voir l'exercice en question, utiliser ce lien en remplaçant le - par un slash :   sacado.xyz-qcm-show_this_exercise-"+str(exercise_id)+"-"
        sending_mail("Avertissement SacAdo Exercice "+str(exercise_id),  msg + response , settings.DEFAULT_FROM_EMAIL , ["sacado.asso@gmail.com"])

    else :
        usr = "non connecté"
        msg = "Message envoyé par l'utilisateur #Non connecté :\n\nL'exercice dont l'id est -- "+str(exercise_id)+" --  décrit ci-dessous : \n Savoir faire visé : "+exercise.knowledge.name+ " \n Niveau : "+exercise.level.name+  "  \n Thème : "+exercise.theme.name +" comporte un problème. \n  S'il est identifié par l'utilisateur, voici la description :  \n" + message   
        response = "\n\n Pour voir l'exercice en question, utiliser ce lien en remplaçant le - par un slash :   sacado.xyz-qcm-show_this_exercise-"+str(exercise_id)+"-"

        sending_mail("Avertissement SacAdo Exercice "+str(exercise_id),  msg + response , settings.DEFAULT_FROM_EMAIL , ["sacado.asso@gmail.com"])


    data = {}
    data["htmlg"]= "Envoi réussi, merci.<br/>Nous traitons votre demande."
    return JsonResponse(data) 



@parcours_exists
def parcours_tasks_and_publishes(request, id):

    today = time_zone_user(request.user)
    parcours = Parcours.objects.get(id=id)
    teacher = Teacher.objects.get(user=request.user)

    role, group , group_id , access = get_complement(request, teacher, parcours) 
 

    relationships_customexercises , nb_exo_only, nb_exo_visible  = ordering_number(parcours)


    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')

    form = AttachForm(request.POST or None, request.FILES or None)

 


    context = {'relationships_customexercises': relationships_customexercises,  'parcours': parcours, 'teacher': teacher  , 'today' : today , 'group' : group , 'group_id' : group_id , 'communications' : [] , 'form' : form , 'role' : role , }
    return render(request, 'qcm/parcours_tasks_and_publishes.html', context)





@parcours_exists
def result_parcours_exercise_students(request,id):
    teacher = request.user.teacher
    parcours = Parcours.objects.get(pk = id)
 

    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')

    role, group , group_id , access = get_complement(request, teacher, parcours)


    relationships = Relationship.objects.filter(parcours = parcours, is_publish = 1) 
    customexercises = parcours.parcours_customexercises.filter( is_publish = 1).order_by("ranking")
    stage = get_stage(teacher.user)

    return render(request, 'qcm/result_parcours_exercise_students.html', {'customexercises': customexercises , 'stage':stage ,   'relationships': relationships ,  'parcours': parcours , 'group_id': group_id ,  'group' : group , 'role' : role , })


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
    """ tri des exercices""" 



    try :

        parcours = request.POST.get("parcours")

        exercise_ids = request.POST.get("valeurs")
        exercise_tab = exercise_ids.split("-") 

        customizes = request.POST.get("customizes")
        customize_tab = customizes.split("-") 


        for i in range(len(exercise_tab)-1):
            if int(customize_tab[i]) == 1 :
                Customexercise.objects.filter(pk = exercise_tab[i]).update(ranking = i)
            else :
                Relationship.objects.filter(parcours = parcours , exercise_id = exercise_tab[i]).update(ranking = i)
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

    Parcours.objects.filter(pk = int(parcours_id)).update(is_publish = statut)
 
    return JsonResponse(data) 

@csrf_exempt
def ajax_dates(request):  # On conserve relationship_id par commodité mais c'est relationship_id et non customexercise_id dans tout le script
    data = {}
    relationship_id = request.POST.get("relationship_id")
    duration =  request.POST.get("duration") 
    custom =  request.POST.get("custom") 
    try :
        typp =  request.POST.get("type")
        if typp : 
            typ = int(typp)
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
                    msg = "Pour le "+str(date)+": \n Un exercice vous est assigné. Rejoindre sacado.xyz. \n. Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte."
                    data["dateur"] = date 
                    students = r.students.all()
                    rec = []
                else :
                    Customexercise.objects.filter(pk = int(relationship_id)).update(date_limit = date)
                    ce = Customexercise.objects.get(pk = int(relationship_id))
                    data["class"] = "btn-success"
                    data["noclass"] = "btn-default"
                    msg = "Pour le "+str(date)+": \n Un exercice vous est assigné. Rejoindre sacado.xyz. Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte."
                    data["dateur"] = date 
                    students = ce.students.all()
                    rec = []


                for s in students :
                    if s.task_post : 
                        if  s.user.email :                  
                            rec.append(s.user.email)

                sending_mail("SacAdo Tâche à effectuer avant le "+str(date),  msg , settings.DEFAULT_FROM_EMAIL , rec ) 
                sending_mail("SacAdo Tâche à effectuer avant le "+str(date),  msg , settings.DEFAULT_FROM_EMAIL , [r.parcours.teacher.user.email] )   

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
                sending_mail("SacAdo. Annulation de tâche à effectuer",  msg , settings.DEFAULT_FROM_EMAIL , rec ) 
                sending_mail("SacAdo. Annulation de tâche à effectuer",  msg , settings.DEFAULT_FROM_EMAIL , [r.parcours.teacher.user.email] ) 

        else :
            if custom == "0" :
                Relationship.objects.filter(pk = int(relationship_id)).update(start = date)
                r = Relationship.objects.get(pk = int(relationship_id))
                msg = "Pour le "+str(date)+": \n Faire l'exercice : https://sacado.xyz/qcm/show_this_exercise/"+str(r.exercise.id)+" : " +str(r.exercise)+" \n. Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte. Ceci est un mail automatique. Ne pas répondre."
                students = r.students.all()
            else :
                Customexercise.objects.filter(pk = int(relationship_id)).update(start = date)
                Customexercise.objects.filter(pk = int(relationship_id)).update(date_limit = None)
                ce = Customexercise.objects.get(pk = int(relationship_id))
                msg = "Pour le "+str(date)+": \n Faire l'exercice : https://sacado.xyz/qcm/show_this_exercise/"+str(ce.id)+"\n Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte. Ceci est un mail automatique. Ne pas répondre."
                students = ce.students.all()

            data["class"] = "btn-success"
            data["noclass"] = "btn-default"
 
            rec = []
            for s in students :
                if s.task_post : 
                    if  s.user.email :                  
                        rec.append(s.user.email)

            sending_mail("SacAdo Tâche à effectuer avant le "+str(date),  msg , settings.DEFAULT_FROM_EMAIL , rec ) 
            sending_mail("SacAdo Tâche à effectuer avant le "+str(date),  msg , settings.DEFAULT_FROM_EMAIL , [r.parcours.teacher.user.email] ) 

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
def ajax_notes(request):  
    data = {}
    relationship_id = request.POST.get("relationship_id")
    mark =  request.POST.get("mark")
    relationship  = Relationship.objects.filter(pk = relationship_id ).update(is_mark = 1, mark = mark)
    return JsonResponse(data) 


@csrf_exempt
def ajax_maxexo(request):  
    data = {}
    relationship_id = request.POST.get("relationship_id")
    maxexo =  request.POST.get("maxexo")
    Relationship.objects.filter(pk = relationship_id ).update(maxexo = maxexo)
    return JsonResponse(data) 



@csrf_exempt
def ajax_delete_notes(request):  
    data = {}
    relationship_id = request.POST.get("relationship_id")
    relationship  = Relationship.objects.filter(pk = relationship_id ).update(is_mark = 0, mark = "")
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

    today = time_zone_user(request.user)

    students = students_from_p_or_g(request,parcours)

    try :
        relationship = Relationship.objects.get(exercise_id = exercise_id, parcours = parcours)
    except :
        relationship = None
    
    data = {}
    if custom == 0 :
        exercise = Exercise.objects.get(id = exercise_id) 
        stats = []
        for s in students :
            student = {}
            student["name"] = s 

            studentanswers = Studentanswer.objects.filter(student=s, exercise = exercise ,  parcours = parcours)
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

 
        context = { 'parcours': parcours, 'exercise':exercise ,  'stats': stats ,  'today' : today ,  'num_exo':num_exo , 'relationship':relationship, 'communications' : [] , }

        data['html'] = render_to_string('qcm/ajax_detail_parcours.html', context)

    else :
        customexercise = Customexercise.objects.get(pk = exercise_id, parcourses = parcours) 
        students = customexercise.students.order_by("user__last_name")  
        duration, score = 0, 0
        tab = []
        cas =  customexercise.customexercise_custom_answer.filter(parcours=parcours)
        
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


        context = {  'parcours': parcours,  'customexercise':customexercise ,'average':average ,  'today': today ,   'students' : students , 'relationship':[], 'num_exo' : num_exo, 'communications' : [] , 'median' : med , 'communications' : [] , }

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



def ajax_locker_exercise(request):

    custom =  int(request.POST.get("custom"))
    student_id =  request.POST.get("student_id")
    exercise_id =  request.POST.get("exercise_id")

    today = time_zone_user(request.user).now()

    data = {}    
    
    if custom == 1 :
        if Exerciselocker.objects.filter(student_id = student_id, customexercise_id = exercise_id, custom = 1).exists() :
            result =  Exerciselocker.objects.get(student_id = student_id, customexercise_id = exercise_id, custom = 1 )
            result.delete()
            lock_result = '<i class="fa fa-unlock text-default"></i>'
        else :
            Exerciselocker.objects.create(student_id = student_id, customexercise_id = exercise_id, custom = 1, relationship = None, lock = today )
            lock_result = '<i class="fa fa-lock text-danger"></i>'
    else :
        if Exerciselocker.objects.filter(student_id = student_id, relationship_id = exercise_id, custom = 0).exists() :
            result =  Exerciselocker.objects.get(student_id = student_id, relationship_id = exercise_id, custom = 0)
            result.delete()
            lock_result = '<i class="fa fa-unlock text-default"></i>'
        else :
            Exerciselocker.objects.create(student_id = student_id, relationship_id = exercise_id, custom = 0,customexercise = None,lock = today )
            lock_result = '<i class="fa fa-lock text-danger"></i>'
 
    data["html"] = lock_result

    return JsonResponse(data)
 



def real_time(request,id):
    """ module de real time"""
    parcours = Parcours.objects.get(pk = id)
    teacher = request.user.teacher
    today = time_zone_user(request.user).now()

    role, group , group_id , access = get_complement(request, teacher, parcours)

 
    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')

    students = parcours.students.order_by("user__last_name")
    rcs      = rcs_for_realtime(parcours)

    return render(request, 'qcm/real_time.html', { 'teacher': teacher , 'parcours': parcours, 'rcs': rcs, 'students': students , 'group': group , 'role': role , 'access': access })



def time_done(arg):
    """
    convertit 1 entier donné  (en secondes) en durée h:m:s
    """
    if arg == "":
        return arg
    else:
        arg = int(arg)
        s = arg % 60
        m = arg // 60 % 60
        h = arg // 3600
        
        if arg < 60:
            return f"{s}s"
        if arg < 3600:
            return f"{m}min.{s}s"
        else:
            return f"{h}h.{m}min.{s}s"




def ajax_real_time_live(request):
    """ Envoie la liste des exercices d'un parcours """
    data = {} # envoie vers JSON
    parcours_id = request.POST.get("parcours_id")
    parcours = Parcours.objects.get(pk=int(parcours_id))
    today = time_zone_user(request.user).now()
    trackers =  Tracker.objects.filter(parcours = parcours )

    i , line, cell, result =  0 , "", "", ""
    for tracker in trackers :
        tui = tracker.user.id
        tr = "tr_student_"+str(tui)
        exo_id = "rc_"+parcours_id+"_"+str(tracker.exercise_id)+"_"+tr

        if tracker.is_custom :
            trck = "en_compo"
        else :

            if tracker.parcours.answers.filter(student=tracker.user.student, exercise_id = tracker.exercise_id) :
                ans = tracker.parcours.answers.filter(student=tracker.user.student, exercise_id = tracker.exercise_id).last()
                trck = str(ans.numexo)+" > "+str(ans.point)+"% "+str(time_done(ans.secondes))
            else :
                trck = "en composition"
            
        if i == trackers.count()-1:
            line +=  tr 
            cell +=  exo_id 
            result +=  trck
        else :
            line +=  tr + "====="
            cell +=  exo_id  + "====="
            result +=  trck  + "====="
        i+=1
      
    data["line"] = line
    data["cell"] = cell
    data["result"] = result

    return JsonResponse(data)

 
def get_values_canvas(request):
    """ Récupère la réponse élève en temps réel """
    data = {} # envoie vers JSON
    parcours_id = request.POST.get("parcours_id")
    customexercise_id = request.POST.get("customexercise_id")
    student_id = request.POST.get("student_id")
 
    ce = Customanswerbystudent.objects.get(customexercise_id = customexercise_id, parcours_id = parcours_id, student_id = student_id )
    values = ce.answer

    data["values"] = values
 

    return JsonResponse(data)

#######################################################################################################################################################################
#######################################################################################################################################################################
#################   Exercise
#######################################################################################################################################################################
#######################################################################################################################################################################



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

        datas.append(levels_dict)
    return datas



def list_exercises(request):
    
    user = request.user
    if user.is_teacher:  # teacher
        teacher = Teacher.objects.get(user=user)
        datas = all_levels(user, 0)
        request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche
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




def ajax_list_exercises_by_level(request):
    """ Envoie la liste des exercice pour un seul niveau """
    teacher = request.user.teacher
    level_id =  int(request.POST.get("level_id"))  
 
    level = Level.objects.get(pk=level_id)
    exercises = Exercise.objects.filter(level_id = level_id , supportfile__is_title=0).order_by("theme","knowledge__waiting","knowledge","supportfile__ranking")
 
    data = {}
    data['html'] = render_to_string('qcm/ajax_list_exercises_by_level.html', { 'exercises': exercises  , "teacher" : teacher , "level_id" : level_id })
 
    return JsonResponse(data)





def ajax_list_exercises_by_level_and_theme(request):
    """ Envoie la liste des exercice pour un seul niveau """
    teacher = request.user.teacher
    level_id =  int(request.POST.get("level_id",0))  
    theme_ids =  request.POST.getlist("theme_id")

    subject_id =  request.POST.get("subject_id",None)
    level = Level.objects.get(pk=level_id)

    try : 
        test  = theme_ids[0]
        exercises = Exercise.objects.filter(level_id = level_id , theme_id__in= theme_ids ,  supportfile__is_title=0).order_by("theme","knowledge__waiting","knowledge","supportfile__ranking")
    except :
        if subject_id :
            exercises = Exercise.objects.filter(level_id = level_id , theme__subject_id = subject_id,  supportfile__is_title=0).order_by("theme","knowledge__waiting","knowledge","supportfile__ranking")
        else :
            exercises = Exercise.objects.filter(level_id = level_id , supportfile__is_title=0).order_by("theme","knowledge__waiting","knowledge","supportfile__ranking")
 
    data= {}
    data['html'] = render_to_string('qcm/ajax_list_exercises_by_level.html', { 'exercises': exercises  , "teacher" : teacher , "level_id" : level_id })
 
    return JsonResponse(data)





@user_passes_test(user_is_superuser)
def admin_list_associations(request,id):
    level = Level.objects.get(pk = id)
    user = request.user

    teacher  = Teacher.objects.get(user=user)
    subjects = teacher.subjects.all()
    exercises = level.exercises.filter(theme__subject__in=subjects,supportfile__is_title=0).order_by("theme","knowledge__waiting","knowledge","ranking")

    return render(request, 'qcm/list_associations.html', {'exercises': exercises, 'teacher': teacher , 'parcours': None, 'relationships' : [] , 'communications' : []   })
 

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


@user_passes_test(user_is_creator)
def admin_list_supportfiles(request,id):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    if user.is_superuser or user.is_extra :  # admin and more

        teacher = Teacher.objects.get(user=user)
        level = Level.objects.get(pk=id)

        waitings = level.waitings.filter(theme__subject__in= teacher.subjects.all()).order_by("theme__subject" , "theme")
 
    return render(request, 'qcm/list_supportfiles.html', { 'waitings': waitings, 'teacher':teacher , 'level':level , 'relationships' : [] , 'communications' : [] , 'parcours' :  None })


@parcours_exists
def parcours_exercises(request,id):
    user = request.user
    parcours = Parcours.objects.get(pk=id)
    student = Student.objects.get(user=user)

    relationships = Relationship.objects.filter(parcours=parcours,is_publish=1).order_by("exercise__theme")

    return render(request, 'qcm/student_list_exercises.html', {'parcours': parcours  , 'relationships': relationships, })

def exercises_level(request, id):
    exercises = Exercise.objects.filter(level_id=id,supportfile__is_title=0).order_by("theme","knowledge__waiting","knowledge","ranking")
    level = Level.objects.get(pk=id)
    themes =  level.themes.all()
    form = AuthenticationForm() 
    u_form = UserForm()
    t_form = TeacherForm()
    s_form = StudentForm()
    return render(request, 'list_exercises.html', {'exercises': exercises, 'level':level , 'themes':themes , 'form':form , 'u_form':u_form , 's_form': s_form , 't_form': t_form , 'levels' : [] })



@user_passes_test(user_is_creator)
def create_supportfile(request):

    code = str(uuid.uuid4())[:8]
    teacher = request.user.teacher
    form = SupportfileForm(request.POST or None,request.FILES or None,teacher = teaher)
    is_ggbfile = request.POST.get("is_ggbfile")
    if request.user.is_superuser or request.user.is_extra :
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.code = code
            nf.author = teacher
            if is_ggbfile :
                nf.annoncement = unescape_html(cleanhtml(nf.annoncement)) 
            send_to_teachers(nf.level)        
            nf.save()
            form.save_m2m()
            # le supprot GGB est placé comme exercice par défaut.
            Exercise.objects.create(supportfile = nf, knowledge = nf.knowledge, level = nf.level, theme = nf.theme )


            return redirect('admin_supportfiles' , nf.level.id )

    context = {'form': form,   'teacher': teacher, 'knowledge': None,  'knowledges': [], 'relationships': [],  'supportfiles': [],   'levels': [], 'parcours': None, 'supportfile': None, 'communications' : [] ,  }

    return render(request, 'qcm/form_supportfile.html', context)

@user_passes_test(user_is_creator)
def create_supportfile_knowledge(request,id):

    code = str(uuid.uuid4())[:8]
    knowledge = Knowledge.objects.get(id = id)
    teacher = request.user.teacher
    form = SupportfileKForm(request.POST or None,request.FILES or None, knowledge = knowledge )
    levels = Level.objects.all()
    supportfiles = Supportfile.objects.filter(is_title=0).order_by("level","theme","knowledge__waiting","knowledge","ranking")
    knowledges = Knowledge.objects.all().order_by("level")

    is_ggbfile = request.POST.get("is_ggbfile")

    if request.user.is_superuser or request.user.is_extra : 
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.code = code
            nf.author = teacher
            nf.knowledge = knowledge
            if is_ggbfile :
                nf.annoncement = unescape_html(cleanhtml(nf.annoncement)) 
            #send_to_teachers(nf.level)    
            nf.save()
            form.save_m2m()
            # le support GGB est placé comme exercice par défaut.
            Exercise.objects.create(supportfile = nf, knowledge = nf.knowledge, level = nf.level, theme = nf.theme )
            return redirect('admin_supportfiles' , nf.level.id )
        else :
            print(form.errors)


    context = {'form': form,   'teacher': teacher,  'knowledges': knowledges, 'relationships': [],  'knowledge': knowledge,  'supportfile': None,  'supportfiles': supportfiles,   'levels': levels , 'parcours': None, 'communications' : [] ,  }

    return render(request, 'qcm/form_supportfile.html', context)

@user_passes_test(user_is_creator)
def update_supportfile(request, id, redirection=0):

    teacher = request.user.teacher
    if request.user.is_superuser or request.user.is_extra :
        supportfile = Supportfile.objects.get(id=id)
        knowledge = supportfile.knowledge
        supportfile_form = UpdateSupportfileForm(request.POST or None, request.FILES or None, instance=supportfile, knowledge = knowledge)
        levels = Level.objects.all()
        supportfiles = Supportfile.objects.filter(is_title=0).order_by("level","theme","knowledge__waiting","knowledge","ranking")
        knowledges = Knowledge.objects.all().order_by("level")
        is_ggbfile = request.POST.get("is_ggbfile")
        if request.method == "POST":
            if supportfile_form.is_valid():
                nf = supportfile_form.save(commit=False)
                nf.code = supportfile.code
                if is_ggbfile :
                    nf.annoncement = unescape_html(cleanhtml(nf.annoncement)) 
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



@user_passes_test(user_is_testeur)
def show_this_supportfile(request, id):

    if request.user.is_teacher:
        teacher = Teacher.objects.get(user=request.user)
        parcours = Parcours.objects.filter(teacher=teacher)
    else :
        parcours = None


    user = request.user    
    form_reporting = DocumentReportForm(request.POST or None )
 
    supportfile = Supportfile.objects.get(id=id)
    request.session['level_id'] = supportfile.level.id
    start_time = time.time()
    context = {'supportfile': supportfile, 'start_time': start_time, 'communications' : [] ,  'parcours': parcours , "user" :  user , "form_reporting" :  form_reporting , }

    if supportfile.is_ggbfile :
        url = "qcm/show_supportfile.html" 
    elif supportfile.is_python :
        url = "basthon/index_supportfile.html"
    else :
        wForm = WrittenanswerbystudentForm(request.POST or None, request.FILES or None )
        context = {'exercise': exercise, 'start_time': start_time, 'parcours': parcours , 'communications' : [] , 'relationships' : [] , 'today' : today , 'wForm' : wForm }
        url = "qcm/show_teacher_writing.html"  

    return render(request, url , context)




@csrf_exempt
def ajax_sort_supportfile(request):
    """ tri des supportfiles""" 


    exercise_ids = request.POST.get("valeurs")
    exercise_tab = exercise_ids.split("-") 
    for i in range(len(exercise_tab)-1):
        Supportfile.objects.filter( pk = exercise_tab[i]).update(ranking = i)



    data = {}
    return JsonResponse(data) 



@user_passes_test(user_is_creator)
def create_exercise(request, supportfile_id):
 
    knowledges = Knowledge.objects.all().select_related('level').order_by("level")
    supportfile = Supportfile.objects.get(id=supportfile_id)

    if request.user.is_superuser or user_is_creator : 
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





@user_passes_test(user_is_creator)
def ajax_load_modal(request):
    """ crée la modale pour changer les savoir faire"""

    exercise_id  = request.POST.get('exercise_id', None)
    exercise = Exercise.objects.get(pk = exercise_id)
    waitings = exercise.level.waitings.filter(level_id=exercise.level.id)
    k_id = exercise.knowledge.id

    data = {}
 
    data['listing_w'] = render_to_string('qcm/ajax_load_modal.html', { 'waitings': waitings , 'k_id' : k_id , 'exercise' : exercise   })
 
    return JsonResponse(data)


@csrf_exempt
@user_passes_test(user_is_creator)
def change_knowledge(request):

    exercise_id  = request.POST.get('exercise_id', None)
    knowledge_id = request.POST.get('knowledge_id', None)
    exercise = Exercise.objects.get(pk=exercise_id)


    if knowledge_id :
        Exercise.objects.filter(pk=exercise_id).update(knowledge_id = knowledge_id)
 

    return redirect( 'admin_associations', exercise.level.id)




@csrf_exempt
def ajax_sort_exercise_from_admin(request):
    """ tri des exercices""" 



    exercise_ids = request.POST.get("valeurs")
    exercise_tab = exercise_ids.split("-") 

    try :
        for i in range(len(exercise_tab)-1):
            Exercise.objects.filter(pk = exercise_tab[i]).update(ranking = i)
    except :
        pass

    data = {}
    return JsonResponse(data)






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
        wForm = WrittenanswerbystudentForm(request.POST or None, request.FILES or None )
        context = {'exercise': exercise,   'form': form , 'u_form' : u_form , 's_form' : s_form , 's_form' : s_form , 't_form' : t_form ,  'wForm' : wForm , 'levels' : [],   'communications' : [] , 'relationships' : []  }
        url = "qcm/show_teacher_writing.html"  

    return render(request, url , context)





def show_this_exercise(request, id):

    exercise  = Exercise.objects.get(pk = id)
    ranking   = exercise.level.ranking 
    level_inf = ranking - 1
    level_sup = ranking + 1

    if request.user.is_authenticated:
        today = time_zone_user(request.user)
        if request.user.is_teacher:
            teacher = Teacher.objects.get(user=request.user)
            parcours = Parcours.objects.filter(Q(teacher=teacher)|Q(coteachers=teacher), level__lte = level_sup, level__gte = level_inf    )
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


    if not request.user.is_authenticated :
        return redirect("index")
        
    parcours = Parcours.objects.get(id= idp)
    exercise = Exercise.objects.get(id= ide)
    if Relationship.objects.filter(parcours=parcours, exercise=exercise).count() == 0 :
        messages.error("Cet exercercice n'est plus disponible.")
        return redirect("index")

    relation = Relationship.objects.get(parcours=parcours, exercise=exercise)
    request.session['level_id'] = exercise.level.id
    start_time =  time.time()
    student = request.user.student
    today = time_zone_user(request.user)
    timer = today.time()

    tracker_execute_exercise(True, request.user , idp , ide , 0)


    context = {'exercise': exercise,  'start_time' : start_time,  'student' : student,  'parcours' : parcours,  'relation' : relation , 'timer' : timer ,'today' : today , 'communications' : [] , 'relationships' : [] }
    return render(request, 'qcm/show_relation.html', context)

@csrf_exempt    
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
 
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        score = round(float(request.POST.get("score")),2)*100
        if score > 100 :
            score = 100

        ##########################################################
        ########################### Storage student answer
        ##########################################################
        this_studentanswer, new_studentanswer =  Studentanswer.objects.get_or_create(exercise  = relation.exercise , parcours  = relation.parcours ,  student  = student, defaults = { "numexo" : numexo,  "point" : score, "secondes" : timer }   )
        if not new_studentanswer : 
            Studentanswer.objects.filter(pk = this_studentanswer.id).update( numexo   = numexo, point    = score , secondes = timer )
        ##########################################################

        result, createded = Resultexercise.objects.get_or_create(exercise  = relation.exercise , student  = student , defaults = { "point" : score , })
        if not createded :
            Resultexercise.objects.filter(exercise  = relation.exercise , student  = student).update(point= score)

        # Moyenne des scores obtenus par savoir faire enregistré dans Resultknowledge
        knowledge = relation.exercise.knowledge
        scored = 0
        studentanswers = Studentanswer.objects.filter(student = student,exercise__knowledge = knowledge) 
        for studentanswer in studentanswers:
            scored += studentanswer.point 
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
            msg = "Exercice : "+str(unescape_html(cleanhtml(name_title)))+"\n Parcours : "+str(relation.parcours.title)+"\n Fait par : "+str(student.user)+"\n Nombre de situations : "+str(numexo)+"\n Score : "+str(score)+"%"+"\n Temps : "+str(convert_seconds_in_time(timer))
            rec = []
            for g in student.students_to_group.filter(teacher = relation.parcours.teacher):
                if not g.teacher.user.email in rec : 
                    rec.append(g.teacher.user.email)

            if g.teacher.notification :
                sending_mail("SacAdo Exercice posté",  msg , settings.DEFAULT_FROM_EMAIL , rec )
                pass

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

        #####################################################################
        # Enregistrement à la volée pour les évaluations 
        #####################################################################
        is_ajax =  request.POST.get("is_ajax", None)
        init =  request.POST.get("init", None)
        if is_ajax :
            data = {}
            if init :
                data["html"] = "<span class= 'verif_init_and_answer' >Exercice initialisé</span>"
                data["nb_situation"] = -100
            else :
                data["html"] = "<span class= 'verif_init_and_answer' >Score enregistré</span>"
                data["nb_situation"] = Studentanswer.objects.get(pk = this_studentanswer.id).numexo
            return JsonResponse(data)
        #####################################################################

    if relation.parcours.is_evaluation and relation.parcours.is_next :
        parcours      = relation.parcours
        new_rank      = relation.ranking + 1 
        i             = 0
        relationships = Relationship.objects.filter(parcours=parcours)

        for r in relationships :
            Relationship.objects.filter(pk=r.id).update(ranking = i)
            i += 1

        if new_rank < relationships.count():
            new_relation = Relationship.objects.get(parcours=parcours, ranking = new_rank)
            return redirect('execute_exercise' , parcours.id , new_relation.exercise.id )
        else :
            return redirect('show_parcours_student' ,  parcours.id )

    else :
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
    level_id = request.POST.get('level_id', None)
    theme_ids = request.POST.getlist('theme_id', None)
    parcours_id = request.POST.get('parcours_id', None)

    if  parcours_id :
        parcours = Parcours.objects.get(id = int(parcours_id))
        ajax = True

    else :
        parcours = None
        ajax = False
        parcours_id = None

    if level_id and theme_ids[0] != "" : 
        exercises = Exercise.objects.filter(level_id = level_id , theme_id__in= theme_ids ,  supportfile__is_title=0).order_by("theme","knowledge__waiting","knowledge","ranking")
 
     
        data['html'] = render_to_string('qcm/ajax_list_exercises.html', { 'exercises': exercises , "parcours" : parcours, "ajax" : ajax, "teacher" : teacher , 'parcours_id' : parcours_id })
 
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
        relation = Relationship.objects.create(exercise=exe, parcours_id=parcours_id, ranking=0)

        parcours = Parcours.objects.get(pk = parcours_id)
        for student in parcours.students.all():
            relation.students.add(student)



        if supportfile.attach_file != "" :
            attachment = "<a href='#' target='_blank'>"+ supportfile.title +"</a>"
        else :
            attachment = supportfile.title


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

 



def ajax_search_exercise(request):

    code =  request.POST.get("search") 
    knowledges = Knowledge.objects.filter(name__contains= code)

    if request.user.user_type == 0 :
        student = True
    else :
        student = False

    relationship = Relationship.objects.filter(Q(exercise__knowledge__in = knowledges)|Q(exercise__supportfile__annoncement__contains= code)|Q(exercise__supportfile__code__contains= code)).last()
    data = {}
    html = render_to_string('qcm/search_exercises.html',{ 'relationship' : relationship ,  'student' : student })
 
    data['html'] = html       

    return JsonResponse(data)



def create_evaluation(request):
    """ 'parcours_is_folder' : False pour les vignettes et différencier si folder ou pas """
    if not request.user.is_authenticated :
        redirect('index')

    teacher = request.user.teacher
    levels =  teacher.levels.all()  
    images = []


    if request.session.has_key("group_id") :
        group_id = request.session.get("group_id",None) 
        if group_id :
            group = Group.objects.get(pk = group_id)

            try : 
                folder_parcourses = teacher.teacher_parcours.filter(leaf_parcours= parcours).order_by("level") 
                images = group.level.level_parcours.values_list("vignette", flat = True).filter(subject_id=group.subject).exclude(vignette=" ").distinct()
                form = ParcoursForm(request.POST or None, request.FILES or None, teacher = teacher, initial = {'subject': group.subject,'level': group.level, 'folder_parcours' : folder_parcourses  })
            except :
                form = ParcoursForm(request.POST or None, request.FILES or None, teacher = teacher, initial = {'subject': group.subject,'level': group.level,   }  )
        else :
            form = ParcoursForm(request.POST or None, request.FILES or None, teacher = teacher)
            
    else :
        group_id = None
        group = None
        request.session["group_id"]  = None 
        form = ParcoursForm(request.POST or None, request.FILES or None, teacher = teacher )



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

        if request.POST.get("this_image_selected",None) : # récupération de la vignette précréée et insertion dans l'instance du parcours.
            nf.vignette = request.POST.get("this_image_selected",None)

        nf.save()
        form.save_m2m()

        nf.students.set(form.cleaned_data.get('students'))

        group_ckeched_ids = request.POST.getlist('groups')
        nf.groups.set(group_ckeched_ids)

        for group_ckeched_id in group_ckeched_ids :
            group_ckeched = Group.objects.get(pk = group_ckeched_id)
            for s in group_ckeched.students.all() :
                nf.students.add(s)



        sg_students =  request.POST.getlist('students_sg')
        for s_id in sg_students :
            student = Student.objects.get(user_id = s_id)
            nf.students.add(student)


        i = 0
        for exercise in form.cleaned_data.get('exercises'):
            exercise = Exercise.objects.get(pk=exercise.id)
            relationship = Relationship.objects.create(parcours=nf, exercise=exercise, ranking=i, 
                                                       duration=exercise.supportfile.duration,
                                                       situation=exercise.supportfile.situation)
            relationship.students.set(form.cleaned_data.get('students'))
            relationship.skills.set(exercise.supportfile.skills.all()) 
            i += 1

            lock_all_exercises_for_student(nf.lock,nf)

        for pid in request.POST.getlist("folder_parcours") :
            parcours_folder = Parcours.objects.get(pk = pid)
            parcours_folder.leaf_parcours.add(nf)   

        print(group_id)    
        if request.POST.get("save_and_choose") :
            return redirect('peuplate_parcours', nf.id)
        elif group_id :
            return redirect('list_parcours_group', group_id ) 
        else :
            return redirect('evaluations')   
    else:
        print(form.errors)

    context = {'form': form, 'parcours_is_folder' : False, 'images' : images  , 'teacher': teacher, 'parcours': None, 'groups': groups, 'idg': 0,  'group_id': group_id , 'group': group , 'relationships': [], 'communications' : [], 'share_groups' : share_groups , 
               'exercises': [], 'levels': levels, 'themes': themes_tab, 'students_checked': 0 , 'role':True , 'idp' : 0 }

    return render(request, 'qcm/form_evaluation.html', context)


#@user_is_parcours_teacher 
def update_evaluation(request, id, idg=0 ):
    """ 'parcours_is_folder' : False pour les vignettes et différencier si folder ou pas """
    teacher = Teacher.objects.get(user_id=request.user.id)
    levels = teacher.levels.all()

    parcours = Parcours.objects.get(id=id)

    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')


    folder_parcourses = teacher.teacher_parcours.filter(leaf_parcours= parcours).order_by("level") 
    form = UpdateParcoursForm(request.POST or None, request.FILES or None, instance=parcours, teacher=teacher, initial={ 'folder_parcours' : folder_parcourses })


    """ affiche le parcours existant avant la modif en ajax"""
    exercises = parcours.exercises.filter(supportfile__is_title=0).order_by("theme","knowledge__waiting","knowledge","ranking")
    """ fin """
    themes_tab = []
    for level in levels:
        for theme in level.themes.all():
            if not theme in themes_tab:
                themes_tab.append(theme)

    groups = Group.objects.filter(teacher=teacher).prefetch_related('students').order_by("level")
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("ranking")
    share_groups = Sharing_group.objects.filter(teacher  = teacher,role=1).order_by("group__level")
    if request.method == "POST":
        if form.is_valid():
            nf = form.save(commit=False)
            nf.author = teacher
            nf.teacher = teacher
            nf.is_evaluation = 1 

            if request.POST.get("this_image_selected",None) : # récupération de la vignette précréée et insertion dans l'instance du parcours.
                nf.vignette = request.POST.get("this_image_selected",None)

            nf.save()
            nf.students.set(form.cleaned_data.get('students'))
            group_ckeched_ids = request.POST.getlist('groups')
            nf.groups.set(group_ckeched_ids)

            for group_ckeched_id in group_ckeched_ids :
                group_ckeched = Group.objects.get(pk = group_ckeched_id)
                for s in group_ckeched.students.all() :
                    nf.students.add(s)
 
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
 
            lock_all_exercises_for_student(nf.stop,parcours)

            for pid in request.POST.getlist("folder_parcours") :
                parcours_folder = Parcours.objects.get(pk = pid)
                parcours_folder.leaf_parcours.add(nf)   

            
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
        images = group.level.level_parcours.values_list("vignette", flat = True).filter(subject_id=group.subject).exclude(vignette=" ").distinct()
    else :
        group_id = None
        group = None
        request.session["group_id"] = None
        images = []

    role, group , group_id , access = get_complement(request, teacher, parcours)


    students_checked = parcours.students.count()  # nombre d'étudiant dans le parcours

    context = {'form': form, 'parcours_is_folder' : False, 'images' : images  , 'parcours': parcours, 'groups': groups, 'idg': idg, 'teacher': teacher, 'group_id': group_id ,  'relationships': relationships, 'communications' : [], 'role': role,  'share_groups' : share_groups , 
               'exercises': exercises, 'levels': levels, 'themes': themes_tab, 'students_checked': students_checked}

    return render(request, 'qcm/form_evaluation.html', context)



 


def delete_evaluation(request,id):

    parcours = Parcours.objects.get(pk=id)
    teacher = Teacher.objects.get(user=request.user)

    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')

    if parcours.teacher == teacher :
        parcours.exercices.clear() 
        parcours.delete() 
    return redirect('index')



#@user_is_parcours_teacher 
def show_evaluation(request, id):

    parcours = Parcours.objects.get(id=id)
    teacher =  parcours.teacher

    today = time_zone_user(parcours.teacher.user)

    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')

    relationships_customexercises , nb_exo_only, nb_exo_visible  = ordering_number(parcours)

    role, group , group_id , access = get_complement(request, teacher, parcours)

    students_p_or_g = students_from_p_or_g(request,parcours)
    nb_students_p_or_g = len(students_p_or_g)

    skills = Skill.objects.all()

    nb_exercises = parcours.exercises.filter(supportfile__is_title=0).count()

    context = {'relationships_customexercises': relationships_customexercises, 'parcours': parcours, 'teacher': teacher, 'skills': skills, 'communications' : [] ,  
               'students_from_p_or_g': students_p_or_g, 'nb_exercises': nb_exercises, 'nb_exo_visible': nb_exo_visible, 'nb_students_p_or_g' : nb_students_p_or_g , 
               'nb_exo_only': nb_exo_only, 'group_id': group_id, 'group': group, 'role' : role , 'today' : today }

    return render(request, 'qcm/show_parcours.html', context)


 
#####################################################################################################################################
#####################################################################################################################################
######   Correction des exercices
#####################################################################################################################################
#####################################################################################################################################



def correction_exercise(request,id,idp,ids=0):
    """
    script qui envoie au prof les fichiers à corriger custom et SACADO
    """

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

        context = {'relationship': relationship,  'teacher': teacher, 'stage' : stage , 'comments' : comments   , 'formComment' : formComment , 'custom':  False , 'nb':nb, 'w_a':w_a, 'annotations':annotations,  'communications' : [] ,  'parcours' : relationship.parcours , 'parcours_id': relationship.parcours.id, 'group' : None , 'student' : student }
 
        return render(request, 'qcm/correction_exercise.html', context)
    else :
        customexercise = Customexercise.objects.get(pk=id)
        parcours = Parcours.objects.get(pk = idp)
        c_e = False 
        customannotations = []
        images_pdf = []

        if student :
            nb = 0
            images_pdf = []            
            if Customanswerbystudent.objects.filter(customexercise = customexercise ,  parcours = parcours , student_id = student).exists():
                c_e = Customanswerbystudent.objects.get(customexercise = customexercise ,  parcours = parcours , student_id = student)
                images_pdf = [] 
                customannotations = Customannotation.objects.filter(customanswerbystudent = c_e)
                nb = customannotations.count()                 
                if c_e.file :
                    images_pdf = c_e.file

                elif customexercise.is_image :
                    images_pdf = Customanswerimage.objects.filter(customanswerbystudent = c_e)
                elif customexercise.is_realtime :
                    images_pdf = Customanswerimage.objects.filter(customanswerbystudent = c_e).last() 

        context = {'customexercise': customexercise,  'teacher': teacher, 'stage' : stage , 'images_pdf' : images_pdf   ,  'comments' : comments   , 'formComment' : formComment , 'nb':nb, 'c_e':c_e, 'customannotations':customannotations,  'custom': True,  'communications' : [], 'parcours' : parcours, 'group' : None , 'parcours_id': parcours.id, 'student' : student }
 
        return render(request, 'qcm/correction_custom_exercise.html', context)



 
def ajax_closer_exercise(request):

    today = time_zone_user(request.user)
    now = today.now()
    custom =  int(request.POST.get("custom")) 
    exercise_id =  int(request.POST.get("exercise_id")) 

    data = {}

    if custom == 1:
        parcours_id =  int(request.POST.get("parcours_id"))
        if Customexercise.objects.filter(pk = exercise_id).exclude(lock = None).exists() :
            Customexercise.objects.filter(pk = exercise_id ).update(lock = None)   
            data["html"] = "<i class='fa fa-unlock'></i>"    
            data["btn_off"] = "btn-danger"
            data["btn_on"] = "btn-default" 
        else :    
            Customexercise.objects.filter(pk = exercise_id ).update(lock = now) 
            data["html"] = "<i class='fa fa-lock'></i>" 
            data["btn_off"] = "btn-default"
            data["btn_on"] = "btn-danger"      
    else :
        if Relationship.objects.filter(pk = exercise_id,is_lock = 1).exists():
            Relationship.objects.filter(pk = exercise_id).update(is_lock = 0) 
            data["html"] = "<i class='fa fa-unlock'></i>"    
            data["btn_off"] = "btn-danger"
            data["btn_on"] = "btn-default" 
        else :
            Relationship.objects.filter(pk = exercise_id).update(is_lock = 1)  
            data["html"] = "<i class='fa fa-lock'></i>"    
            data["btn_off"] = "btn-default"
            data["btn_on"] = "btn-danger"    
    return JsonResponse(data) 



def ajax_correction_viewer(request):

    custom =  int(request.POST.get("custom")) 
    exercise_id =  int(request.POST.get("exercise_id")) 

    data = {}


    if custom == 1:
        parcours_id =  int(request.POST.get("parcours_id"))
        if Customexercise.objects.filter(pk = exercise_id).exclude(is_publish_cor = 1).exists() :
            Customexercise.objects.filter(pk = exercise_id ).update(is_publish_cor = 1)   
            data["html"] = "<i class='fa fa-eye-slash'></i>"    
            data["btn_off"] = "btn-danger"
            data["btn_on"] = "btn-default" 
        else :    
            Customexercise.objects.filter(pk = exercise_id ).update(is_publish_cor = 0)  
            data["html"] = "<i class='fa fa-eye'></i>" 
            data["btn_off"] = "btn-default"
            data["btn_on"] = "btn-danger"      
    else :
        if Relationship.objects.filter(pk = exercise_id,is_correction_visible = 1).exists():
            Relationship.objects.filter(pk = exercise_id).update(is_correction_visible = 0) 
            data["html"] = "<i class='fa fa-eye-slash'></i>"    
            data["btn_off"] = "btn-danger"
            data["btn_on"] = "btn-default" 
        else :
            Relationship.objects.filter(pk = exercise_id).update(is_correction_visible = 1)  
            data["html"] = "<i class='fa fa-eye'></i>"    
            data["btn_off"] = "btn-default"
            data["btn_on"] = "btn-danger"    
    return JsonResponse(data) 






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
    teacher = request.user.teacher
    answer_id = request.POST.get("answer_id") 
    try :
        if custom :
            Customannotation.objects.get(customanswerbystudent_id = answer_id,  attr_id = attr_id ).delete()
        else :  
            Annotation.objects.get(writtenanswerbystudent_id  = answer_id, attr_id = attr_id).delete()
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
    tab_value = [-1, stage["low"]-1,stage["medium"]-1,stage["up"]-1,100]       


    if typ == 0 : 

        knowledge_id = request.POST.get("knowledge_id",None)       
        skill_id = request.POST.get("skill_id",None)

        relationship_id =  int(request.POST.get("relationship_id"))   
        relationship = Relationship.objects.get(pk = relationship_id)

        Writtenanswerbystudent.objects.filter(relationship  = relationship  , student  = student).update(is_corrected = True)

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

    else :
       
        customexercise_id =  int(request.POST.get("customexercise_id"))  
 
        parcours_id =  int(request.POST.get("parcours_id")) 
        knowledge_id = request.POST.get("knowledge_id",None)       
        skill_id = request.POST.get("skill_id",None)

        Customanswerbystudent.objects.filter(parcours_id = parcours_id , customexercise_id = customexercise_id, student = student).update(is_corrected = True)

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

    return JsonResponse(data)  


 

def ajax_annotate_exercise_no_made(request): # Marquer un exercice non fait

    student_id =  int(request.POST.get("student_id"))
    exercise_id =  int(request.POST.get("exercise_id"))  
    parcours_id =  int(request.POST.get("parcours_id")) 
    custom =  int(request.POST.get("custom")) 
    data = {}
    if custom :
        Customanswerbystudent.objects.update_or_create(parcours_id = parcours_id , customexercise_id = exercise_id, student_id = student_id,defaults={"answer":"", "comment":"Non rendu", "point":0,"is_corrected":1})
    else :
        Writtenanswerbystudent.objects.update_or_create(relationship_id = exercise_id , student_id = student_id,defaults={"answer":"", "comment":"Non rendu",  "is_corrected":1})     

    return JsonResponse(data)  




def ajax_mark_evaluate(request): # Evaluer un exercice custom par note

    student_id =  int(request.POST.get("student_id"))
    mark =  request.POST.get("mark")
    data = {}
    student = Student.objects.get(user_id = student_id) 
    if int(request.POST.get("custom")) == 1 :

        customexercise_id =  int(request.POST.get("customexercise_id"))  
        parcours_id =  int(request.POST.get("parcours_id")) 
        this_custom = Customanswerbystudent.objects.filter(parcours_id = parcours_id , customexercise_id = customexercise_id, student = student)
        this_custom.update(is_corrected= 1)
        this_custom.update(point= mark)
        exercise =  Customexercise.objects.get(pk = customexercise_id)

    else :

        relationship_id =  int(request.POST.get("relationship_id"))  
        this_exercise = Writtenanswerbystudent.objects.filter(relationship_id = relationship_id ,   student = student)
        this_exercise.update(is_corrected= 1)
        this_exercise.update(point= mark)
        relationship = Relationship.objects.get(pk = relationship_id)
        exercise = relationship.exercise.supportfile.annoncement

    if student.user.email :
        msg = "Vous venez de recevoir la note : "+ str(mark)+" pour l'exercice "+str(exercise) 
        sending_mail("SacAdo Exercice posté",  msg , settings.DEFAULT_FROM_EMAIL , [student.user.email] )


    data['eval'] = "<i class = 'fa fa-check text-success pull-right'></i>"             

    return JsonResponse(data)  





def ajax_comment_all_exercise(request): # Ajouter un commentaire à un exercice non auto-corrigé

    student_id =  int(request.POST.get("student_id"))
    comment =  cleanhtml(unescape_html(request.POST.get("comment")))

    exercise_id =  int(request.POST.get("exercise_id"))  

    saver =  int(request.POST.get("saver"))

    student = Student.objects.get(user_id = student_id)  

    if int(request.POST.get("typ")) == 0 :
        relationship = Relationship.objects.get(pk = exercise_id)
        Writtenanswerbystudent.objects.filter(relationship = relationship, student = student).update(comment = comment )
        Writtenanswerbystudent.objects.filter(relationship = relationship, student = student).update(is_corrected = 1 )
        exercise = relationship.exercise.supportfile.annoncement
        if saver == 1:
            Generalcomment.objects.create(comment=comment, teacher = relationship.parcours.teacher)

    else  :
        parcours_id =  int(request.POST.get("parcours_id"))     
        exercise = Customexercise.objects.get(pk = exercise_id)
        Customanswerbystudent.objects.filter(customexercise = exercise, student = student, parcours_id = parcours_id).update(comment = comment )
        Customanswerbystudent.objects.filter(customexercise = exercise, student = student, parcours_id = parcours_id).update(is_corrected = 1 )

        if saver == 1:
            Generalcomment.objects.create(comment=comment, teacher = exercise.teacher)

    if student.user.email :
        msg = "Vous venez de recevoir une appréciation pour l'exercice "+str(exercise)+"\n\n  "+str(comment) 
        sending_mail("SacAdo Exercice posté",  msg , settings.DEFAULT_FROM_EMAIL , [student.user.email] )

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
        exercise = Relationship.objects.get(pk = id_relationship)

        if Writtenanswerbystudent.objects.filter(student = student , relationship = exercise).exists() :
            w_a = Writtenanswerbystudent.objects.get(student = student , relationship = exercise) # On récupère la Writtenanswerbystudent
            form = WAnswerAudioForm(request.POST or None, request.FILES or None,instance = w_a )
        else :
            form = WAnswerAudioForm(request.POST or None, request.FILES or None )

        if form.is_valid() :
            nf =  form.save(commit = False)
            nf.audio = audio_text
            nf.relationship = exercise
            nf.student = student
            nf.is_corrected = True                     
            nf.save()

    else  :

        parcours_id =  int(request.POST.get("id_parcours"))  
        parcours = Parcours.objects.get(pk = parcours_id)
        exercise = Customexercise.objects.get(pk = id_relationship)
        
        if Customanswerbystudent.objects.filter(customexercise  = exercise, student = student , parcours = parcours).exists() :
            c_e = Customanswerbystudent.objects.get(customexercise  = exercise, student = student , parcours = parcours) # On récupère la Customanswerbystudent
            form = CustomAnswerAudioForm(request.POST or None, request.FILES or None,instance = c_e )
        else :
            form = CustomAnswerAudioForm(request.POST or None, request.FILES or None )

        if form.is_valid() :
            nf =  form.save(commit = False)
            nf.audio = audio_text
            nf.customexercise = exercise
            nf.student = student
            nf.parcours = parcours
            nf.is_corrected = True    
            nf.save()


    if student.user.email :
        msg = "Vous venez de recevoir une appréciation orale pour l'exercice "+str(exercise)+"\n\n  "+str(comment) 
        sending_mail("SacAdo Exercice posté",  msg , settings.DEFAULT_FROM_EMAIL , [student.user.email] )

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





def ajax_read_my_production(request): # Propose à un élève de lire sa copie depuis son parcours

    student_id =  int(request.POST.get("student_id"))
    exercise_id =  int(request.POST.get("exercise_id"))  
    custom =  int(request.POST.get("custom")) 
    student = Student.objects.get(pk=student_id)

    data = {}

    if custom :
        customexercise = Customexercise.objects.get(pk=exercise_id)
        response = Customanswerbystudent.objects.get(customexercise  = customexercise , student  = student )
        annotations = Customannotation.objects.filter(customanswerbystudent  = response)

        context = { 'customexercise' : customexercise , 'student': student ,   'custom' : True , 'response' :  response,   'annotations' : annotations   }

    else :
        relationship = Relationship.objects.get(pk=exercise_id)
        response = Writtenanswerbystudent.objects.get(relationship  = relationship  , student  = student )
        annotations = Annotation.objects.filter(writtenanswerbystudent = response)
 
        context = { 'relationship' : relationship , 'student': student ,   'custom' : False , 'response' :  response,   'annotations' : annotations   }

    html = render_to_string('qcm/ajax_student_restitution.html', context )
     
    data['html'] = html    
            

    return JsonResponse(data)  

 
###################################################################
######   Création des commentaires de correction
###################################################################
@csrf_exempt  
def ajax_create_or_update_appreciation(request):

    data = {}
    comment_id = request.POST.get("comment_id",None)
    comment = request.POST.get("comment",None)
    teacher = request.user.teacher

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


    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')

    ceForm = CustomexerciseForm(request.POST or None, request.FILES or None , teacher = teacher , parcours = parcours) 


    if request.method == "POST" :
        if ceForm.is_valid() :
            nf = ceForm.save(commit=False)
            nf.teacher = teacher
            if nf.is_scratch :
                nf.is_image = True
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
                if nf.is_scratch :
                    nf.is_image = True
                nf.save()
                ceForm.save_m2m()
            else :
                print(ceForm.errors)
            return redirect('exercises' )
     
        context = {  'teacher': teacher, 'stage' : stage ,  'communications' : [] , 'form' : ceForm , 'customexercise' : custom ,'parcours': None, }

    else :
 
        parcours = Parcours.objects.get(pk=id)
        if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
            return redirect('index')

        ceForm = CustomexerciseForm(request.POST or None, request.FILES or None , teacher = teacher , parcours = parcours, instance = custom ) 

        if request.method == "POST" :
            if ceForm.is_valid() :
                nf = ceForm.save(commit=False)
                nf.teacher = teacher
                if nf.is_scratch :
                    nf.is_image = True
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

    tracker_execute_exercise(True ,  student.user , relationship.parcours.id  , relationship.exercise.id , 0)

    today = time_zone_user(student.user)
    if Writtenanswerbystudent.objects.filter(student = student, relationship = relationship ).exists() : 
        w_a = Writtenanswerbystudent.objects.get(student = student, relationship = relationship )
        wForm = WrittenanswerbystudentForm(request.POST or None, request.FILES or None, instance = w_a )  
    else :
        wForm = WrittenanswerbystudentForm(request.POST or None, request.FILES or None ) 
        w_a = False



    if request.method == "POST":
        if wForm.is_valid():
            w_f = wForm.save(commit=False)
            w_f.relationship = relationship
            w_f.student = student
            w_f.answer = escape_chevron(wForm.cleaned_data['answer'])
            w_f.is_corrected = 0  # si l'élève soumets une production alors elle n'est pas corrigée 
            w_f.save()

            ### Envoi de mail à l'enseignant
            msg = "Exercice : "+str(unescape_html(cleanhtml(relationship.exercise.supportfile.annoncement)))+"\n Parcours : "+str(relationship.parcours.title)+", posté par : "+str(student.user) +"\n\n sa réponse est \n\n"+str(wForm.cleaned_data['answer'])
            if relationship.parcours.teacher.notification :
                sending_mail("SACADO Exercice posté",  msg , settings.DEFAULT_FROM_EMAIL , [relationship.parcours.teacher.user.email] )
                pass

            return redirect('show_parcours_student' , relationship.parcours.id )

    context = {'relationship': relationship, 'communications' : [] , 'w_a' : w_a , 'parcours' : relationship.parcours ,  'form' : wForm, 'today' : today  }

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


    tracker_execute_exercise(True ,  student.user , idp  , id , 1)  


    if customexercise.is_realtime :
        on_air = True
    else :
        on_air = False   
 

    if Customanswerbystudent.objects.filter(student = student, customexercise = customexercise ).exists() : 
        c_e = Customanswerbystudent.objects.get(student = student, customexercise = customexercise )
        cForm = CustomanswerbystudentForm(request.POST or None, request.FILES or None, instance = c_e )
        images = Customanswerimage.objects.filter(customanswerbystudent = c_e) 

    else :
        cForm = CustomanswerbystudentForm(request.POST or None, request.FILES or None )
        c_e = False
        images = False

    if customexercise.is_image :
        form_ans = inlineformset_factory( Customanswerbystudent , Customanswerimage , fields=('image',) , extra=1)
    else :
        form_ans = None

 

    if request.method == "POST":
        if cForm.is_valid():
            w_f = cForm.save(commit=False)
            w_f.customexercise = customexercise
            w_f.parcours_id = idp
            w_f.answer =  escape_chevron(cForm.cleaned_data['answer'])
            w_f.student = student
            w_f.is_corrected = 0
            w_f.save()

            if customexercise.is_image :
                form_images = form_ans(request.POST or None,  request.FILES or None, instance = w_f)
                for form_image in form_images :
                    if form_image.is_valid():
                        form_image.save()

            ### Envoi de mail à l'enseignant
            msg = "Exercice : "+str(unescape_html(cleanhtml(customexercise.instruction)))+"\n Parcours : "+str(parcours.title)+", posté par : "+str(student.user) +"\n\n sa réponse est \n\n"+str(cForm.cleaned_data['answer'])

            if customexercise.teacher.notification :
                sending_mail("SACADO Exercice posté",  msg , settings.DEFAULT_FROM_EMAIL , [customexercise.teacher.user.email] )
                pass

            return redirect('show_parcours_student' , idp )

    context = {'customexercise': customexercise, 'communications' : [] , 'c_e' : c_e , 'form' : cForm , 'images':images, 'form_ans' : form_ans , 'parcours' : parcours ,'student' : student, 'today' : today , 'on_air' : on_air}

    if customexercise.is_python :
        url = "basthon/index_custom.html" 
    else :
        url = "qcm/form_writing_custom.html" 

    return render(request, url , context)




#################################################################################################################
#################################################################################################################
################   Canvas
#################################################################################################################
#################################################################################################################
@login_required
def show_canvas(request):
    user = request.user
    context = { "user" :  user  }
 
    return render(request, 'qcm/show_canvas.html', context)



@login_required
def ajax_save_canvas(request):

    actions           = request.POST.get("actions",None)
    customexercise_id = request.POST.get("customexercise_id",0)
    parcours_id       = request.POST.get("parcours_id",0)
    student           = request.user.student  
    customexercise    = Customexercise.objects.get(pk = customexercise_id)
    parcours          = Parcours.objects.get(pk = parcours_id)
    today             = time_zone_user(student.user).now()
    data = {}
 

    if request.method == "POST":
        c_ans , created = Customanswerbystudent.objects.get_or_create(customexercise_id = customexercise_id , parcours_id = parcours_id , student = student , defaults = { 'date' : today , 'answer' : actions} )
        if not created :
            Customanswerbystudent.objects.filter(customexercise_id = customexercise_id , parcours_id = parcours_id , student = student ).update(date = today)
            Customanswerbystudent.objects.filter(customexercise_id = customexercise_id , parcours_id = parcours_id , student = student ).update(answer = actions)
 
    return JsonResponse(data)
 





def ajax_delete_custom_answer_image(request):
    data = {}
    custom = request.POST.get("custom")
    image_id = request.POST.get("image_id")
    Customanswerimage.objects.get(pk = int(image_id)).delete()
    return JsonResponse(data)  


 


def asking_parcours_sacado(request,pk):
    """demande de parcours par un élève"""
    group = Group.objects.get(pk = pk)

    teacher_id = get_teacher_id_by_subject_id(group.subject.id)

    teacher = Teacher.objects.get(pk=teacher_id)
    student = request.user.student

    subject = group.subject
    level = group.level

    parcourses = teacher.teacher_parcours.filter(level = level, subject = subject)


    test = attribute_all_documents_to_student(parcourses, student)

    if test :
        test_string = "Je viens de récupérer les exercices."
    else :
        test_string = "Je ne parviens pas à récupérer les exercices."    

    msg = "Je souhaite utiliser les parcours Sacado de mon niveau de "+str(level)+", mon enseignant ne les utilise pas. "+test_string+" Merci.\n\n"+str(student)

    sending_mail("Demande de parcours SACADO",  msg , settings.DEFAULT_FROM_EMAIL , ["brunoserres33@gmail.com", "sacado.asso@gmail.com"] )

    return redirect("dashboard_group",pk)

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

  
def detail_task_parcours(request,id,s,c):

  
    parcours = Parcours.objects.get(pk=id) 
    teacher = parcours.teacher

    today = time_zone_user(teacher.user)
    date_today = today.date() 

    role, group , group_id , access = get_complement(request, teacher, parcours)

    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')

    if s == 0 : # groupe

        if parcours.is_folder :
            relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__in = parcours.leaf_parcours.all(), exercise__supportfile__is_title=0).exclude(date_limit=None).order_by("-date_limit")
            custom_set = set()
            for p in parcours.leaf_parcours.all():
                custom_set.update(Customexercise.objects.filter(parcourses = p ))
            customexercises = list(custom_set)
        else :
            relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours =parcours,exercise__supportfile__is_title=0).exclude(date_limit=None).order_by("-date_limit") 
            customexercises = Customexercise.objects.filter( parcourses = parcours,  )


        context = {'relationships': relationships, 'customexercises': customexercises ,  'parcours': parcours ,  'today':today ,  'communications' : [] ,  'date_today':date_today ,  'group_id' : group_id ,  'role' : role ,  }
 
        return render(request, 'qcm/list_tasks.html', context)
    else : # exercice
        if c == 0:
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

        else :
            exercise = Customexercise.objects.get(pk=s)
            students = students_from_p_or_g(request,parcours) 
            details_tab = []
            for s in students :
                details = {}
                details["student"]=s.user
                try : 
                    customanswer = Customanswerbystudent.objects.filter(exercise= exercise, parcours = parcours, student = s).last()
                    details["point"]= customanswer.point
                    details["numexo"]=  customanswer.comment
                    details["date"]= ""
                    details["secondes"]= ""
                except :
                    details["point"]= ""
                    details["numexo"]=  ""
                    details["date"]= ""
                    details["secondes"]= ""
                details_tab.append(details)
                relationship = Customexercise.objects.get( parcours =parcours,exercise= exercise)


         
        context = {'details_tab': details_tab, 'parcours': parcours ,   'exercise' : exercise , 'relationship': relationship,  'date_today' : date_today, 'communications' : [] ,  'group_id' : group_id , 'role' : role }

        return render(request, 'qcm/task.html', context)


 
def detail_task(request,id,s):

    parcours = Parcours.objects.get(pk=id) 
    teacher = Teacher.objects.get(user= request.user)

    today = time_zone_user(teacher.user) 

    role, group , group_id , access = get_complement(request, teacher, parcours)

    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
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
    teacher = request.user.teacher 
    parcourses = Parcours.objects.filter(is_publish=  1,teacher=teacher ) 
    relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__teacher=teacher, date_limit__gte=today,exercise__supportfile__is_title=0).order_by("parcours") 
    context = {'relationships': relationships, 'parcourses': parcourses, 'parcours': None,  'communications' : [] , 'relationships' : [] , 'group_id' : None  , 'role' : False , }
    return render(request, 'qcm/all_tasks.html', context)



def these_all_my_tasks(request):
    today = time_zone_user(request.user) 
    teacher = request.user.teacher 
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

    role, group , group_id , access = get_complement(request, teacher, group)

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

    role, group , group_id , access = get_complement(request, teacher, group)

    relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today),  parcours__in=parcourses_tab, exercise__supportfile__is_title=0).exclude(date_limit=None).order_by("parcours") 
    context = { 'relationships': relationships ,    'group' : group , 'parcours' : None , 'relationships' : [] , 'communications' : [] ,  'group_id' : group.id , 'role' : role ,  }
    
    return render(request, 'qcm/group_task.html', context )




def my_child_tasks(request,id):
    user = request.user
    today = time_zone_user(user) 
    parent = user.parent
    student = Student.objects.get(pk = id) 

    if not student in parent.students.all() :
        return redirect('index')

    relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__students = student, exercise__supportfile__is_title=0).exclude(date_limit=None).order_by("date_limit")


    context = {'relationships': relationships,  'communications' : [] ,  'relationships' : [] ,  'parent' : parent , 'student' : student , } 
    return render(request, 'qcm/my_child_tasks.html', context)




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
    teacher = request.user.teacher
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
def json_delete_remediation(request,id,idp,typ):

    parcours = Parcours.objects.get(pk=idp) 

    if parcours.teacher == request.user.teacher :
        if typ == 0 :
            remediation = Remediation.objects.get(id=id)
        else :
            remediation = Remediationcustom.objects.get(id=id)  
        remediation.delete()

    return redirect( 'show_parcours', idp )

 

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
        
        relationships = Relationship.objects.filter(parcours_id = parcours_id, ranking__lt= this_relationship.ranking)
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
def get_level(tot,stage):
    if tot < stage["low"] :
        clr = "red"
    elif tot < stage["medium"] : 
        clr = "yellow"
    elif tot < stage["up"] : 
        clr = "green"
    else  : 
        clr = "blue" 
    return clr



def export_results_after_evaluation(request):

    skill = request.POST.get("skill",None)  
    knowledge =   request.POST.get("knowledge",None)  

    mark  = request.POST.get("mark",None) 
    mark_on  = request.POST.get("mark_on")  
    signature  = request.POST.get("signature",None) 
    parcours_id  = request.POST.get("parcours_id") 
    parcours = Parcours.objects.get(pk = int(parcours_id) ) 
    elements = []     

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+str(parcours.title)+'.pdf"'

    doc = SimpleDocTemplate(response,   pagesize=A4, 
                                        topMargin=0.3*inch,
                                        leftMargin=0.3*inch,
                                        rightMargin=0.3*inch,
                                        bottomMargin=0.3*inch     )

    sample_style_sheet = getSampleStyleSheet()

    sacado = ParagraphStyle('sacado', 
                            fontSize=20, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )

    title = ParagraphStyle('title',  fontSize=20, textColor=colors.HexColor("#00819f"),)                   
    title_black = ParagraphStyle('title', fontSize=20, )
    subtitle = ParagraphStyle('title', fontSize=16,  textColor=colors.HexColor("#00819f"),)
 
    normal = ParagraphStyle(name='Normal',fontSize=12,)    
    red = ParagraphStyle(name='Normal',fontSize=12,  textColor=colors.HexColor("#cb2131"),) 
    yellow = ParagraphStyle(name='Normal',fontSize=12,  textColor=colors.HexColor("#ffb400"),)
    green = ParagraphStyle(name='Normal',fontSize=12,  textColor=colors.HexColor("#1bc074"),)
    blue = ParagraphStyle(name='Normal',fontSize=12,  textColor=colors.HexColor("#005e74"),)

    stage = get_stage(request.user)    
    exercises = []
    relationships = Relationship.objects.filter(parcours=parcours,is_publish = 1,exercise__supportfile__is_title=0).prefetch_related('exercise__supportfile').order_by("ranking")
    parcours_duration = parcours.duration #durée prévue pour le téléchargement
    for r in relationships :
        parcours_duration += r.duration
        exercises.append(r.exercise)


    for s in parcours.students.order_by("user__last_name") :
        skills =  skills_in_parcours(request,parcours) 
        knowledges = knowledges_in_parcours(parcours)
        data_student = get_student_result_from_eval(s, parcours, exercises,relationships,skills, knowledges,parcours_duration) 

 
        #logo = Image('D:/uwamp/www/sacado/static/img/sacadoA1.png')
        logo = Image('https://sacado.xyz/static/img/sacadoA1.png')
        logo_tab = [[logo, "SACADO \nSuivi des acquisitions de savoir faire" ]]
        logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5*inch])
        logo_tab_tab.setStyle(TableStyle([ ('TEXTCOLOR', (0,0), (-1,0), colors.Color(0,0.5,0.62))]))
        
        elements.append(logo_tab_tab)
        elements.append(Spacer(0, 0.2*inch))


        ##########################################################################
        #### Parcours
        ##########################################################################
        paragraph = Paragraph( str(parcours.title) , title_black )
        elements.append(paragraph)
        elements.append(Spacer(0, 0.2*inch))
        ##########################################################################
        #### Elève
        ##########################################################################
        paragraph = Paragraph( str(s.user.last_name)+" "+str(s.user.first_name) , title )
        elements.append(paragraph)
        elements.append(Spacer(0, 0.4*inch)) 

        ##########################################################################
        #### Nombre d'exercices traités
        ##########################################################################
        paragraph = Paragraph( "Nombre d'exercices traités : " + str(data_student["nb_exo"]) +  " sur " + str(data_student["total_nb_exo"])+" proposés"  , normal )
        elements.append(paragraph)
        elements.append(Spacer(0, 0.1*inch)) 
        ##########################################################################
        #### Nombre d'exercices traités
        ##########################################################################
        paragraph = Paragraph( "Durée du travail (h:m:s) : " + str(data_student["duration"]) , normal )
        elements.append(paragraph)
        elements.append(Spacer(0, 0.1*inch)) 


        if knowledge : 
            ##########################################################################
            #### Savoir faire ciblés
            ##########################################################################
            elements.append(Spacer(0, 0.3*inch)) 
            paragraph = Paragraph( "Savoir faire ciblés : "   , subtitle )
            elements.append(paragraph)
            elements.append(Spacer(0, 0.1*inch)) 

            tableauK = []
 
            for knwldg in knowledges :
                data = []
                data.append(knwldg.name[:80])
                tot_k = total_by_knowledge_by_student(knwldg,relationships,parcours,s)
                couleur = get_level(tot_k,stage)                
                if tot_k < 0 :
                    tot_k, couleur = "NE", "n"
                if couleur == "red" :
                    paragraphknowledge = Paragraph(  str(tot_k)  , red )
                elif couleur == "yellow" :
                    paragraphknowledge = Paragraph( str(tot_k)  , yellow )
                elif couleur == "green" :
                    paragraphknowledge = Paragraph(  str(tot_k)  , green )
                elif couleur == "blue" :
                    paragraphknowledge = Paragraph( str(tot_k)  , blue )
                else :
                    paragraphknowledge = Paragraph( str(tot_k)  , normal )


                data.append(paragraphknowledge)
                tableauK.append(data) 
            tk = Table(tableauK)
            elements.append(tk)
            elements.append(Spacer(0, 0.05*inch)) 


       
        if skill : 
            tableauSkill = []
            ##########################################################################
            #### Compétences ciblées
            ##########################################################################
            elements.append(Spacer(0, 0.3*inch)) 
            paragraph = Paragraph( "Compétences ciblées : "   , subtitle )
            elements.append(paragraph)
            elements.append(Spacer(0, 0.1*inch)) 

            for skll in  skills:
                data = []
                data.append(skll)
                tot_s = total_by_skill_by_student(skll,relationships,parcours,s)
                couleur = get_level(tot_s,stage)                
                if tot_s < 0 :
                    tot_s, couleur = "NE", "n"

                if couleur == "red" :
                    paragraphskill = Paragraph(  str(tot_s)   , red )
                elif couleur == "yellow" :
                    paragraphskill = Paragraph( str(tot_s)  , yellow )
                elif couleur == "green" :
                    paragraphskill = Paragraph(  str(tot_s)   , green )
                elif couleur == "blue" :
                    paragraphskill = Paragraph( str(tot_s)   , blue )
                else :
                    paragraphskill = Paragraph( str(tot_s)   , normal )

                data.append(paragraphskill)
                tableauSkill.append(data) 
            tSk = Table(tableauSkill)
            elements.append(tSk)
            elements.append(Spacer(0, 0.05*inch)) 



        if mark : 

            ##########################################################################
            #### Score par exercice 
            ##########################################################################
            elements.append(Spacer(0, 0.3*inch)) 
            paragraph = Paragraph( "Score par exercice "   , subtitle )
            elements.append(paragraph)
            elements.append(Spacer(0, 0.1*inch)) 

            i = 1
            for score in data_student["score_tab"] :
                paragraph = Paragraph( "Exercice "+str(i)+" : "+str(score)+"%"  , normal )
                elements.append(paragraph)
                elements.append(Spacer(0, 0.1*inch)) 
                i += 1

            elements.append(Spacer(0, 0.2*inch)) 
            ##########################################################################
            #### Note sur
            ##########################################################################

            exo_sacado = request.POST.get("exo_sacado",0)  

            if data_student["percent"] != "" :

                final_mark = float(data_student["score_total"]) * (float(mark_on) - float(exo_sacado)) + float(data_student["percent"]) * float(exo_sacado)/100

                coefficient = data_student["nb_exo"]  /  data_student["total_nb_exo"] 
                final_mark = math.ceil( coefficient *  final_mark)
                paragraphsco = Paragraph( "Note globale : " + str(final_mark)  , normal )
            else :
                paragraphsco = Paragraph( "Note globale : NE"  , normal )

 
            elements.append(paragraphsco)
            elements.append(Spacer(0, 0.3*inch)) 

        if signature : 
            paragraph = Paragraph( "Signature parent "   , subtitle )
            elements.append(paragraph)
 
        elements.append(PageBreak())

    doc.build(elements)

    return response

def export_notes_after_evaluation(request):

    parcours_id = request.POST.get("parcours_id")  
    parcours = Parcours.objects.get(pk = parcours_id)  

    note_sacado  = request.POST.get("note_sacado",0)  
    note_totale  = request.POST.get("note_totale")  

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=Notes_exercice_{}.csv'.format(parcours.id)
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    
    fieldnames = ("Nom", "Prénom", "Situations proposées", "Réponse juste", "Score rapporté aux meilleurs scores SACADO" , "Score rapporté à tous les exercices SACADO proposés" , "Note proposée"  )
    writer.writerow(fieldnames)

    skills = skills_in_parcours(request,parcours)
    knowledges = knowledges_in_parcours(parcours)
    relationships = Relationship.objects.filter(parcours=parcours,is_publish = 1,exercise__supportfile__is_title=0)
    parcours_duration = parcours.duration #durée prévue pour le téléchargement
    exercises = []
    for r in relationships :
        parcours_duration += r.duration
        exercises.append(r.exercise)


    for student in parcours.students.order_by("user__last_name") :
        data_student = get_student_result_from_eval(student, parcours, exercises,relationships,skills, knowledges,parcours_duration) 
        
        if data_student["percent"] != "" :

            try :
                final_mark = float(data_student["score_total"]) * (float(note_totale) - float(note_sacado)) + float(data_student["percent"]) * float(note_sacado)/100

                coefficient = data_student["nb_exo"]  /  data_student["total_nb_exo"] 
                final_mark = math.ceil( coefficient *  final_mark)
            except :
                final_mark = "NE" 

        else :
            final_mark = "NE" 

        writer.writerow( (str(student.user.last_name).lower() , str(student.user.first_name).lower() , data_student["total_nb_exo"] , data_student["nb_exo"],  data_student["percent"] , data_student["ajust"] , final_mark ) )
    return response

def export_skills_after_evaluation(request):

    parcours_id = request.POST.get("parcours_id")  
    parcours = Parcours.objects.get(pk = parcours_id)  
    nb_skill = int(request.POST.get("nb_skill"))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=Skills_exercice_{}.csv'.format(parcours.id)
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    

    skills = skills_in_parcours(request,parcours)

    label_in_export = ["Nom", "Prénom"]
    for ski in skills :
        if not ski.name in label_in_export : 
            label_in_export.append(ski.name)

 

    writer.writerow(label_in_export)
 
    for student in parcours.students.order_by("user__last_name") :
        skill_level_tab = [str(student.user.last_name).capitalize(),str(student.user.first_name).capitalize()]

        for skill in  skills:
            total_skill = 0
 
            scs = student.student_correctionskill.filter(skill = skill, parcours = parcours)
            nbs = scs.count() 
            offseter = min(nb_skill, nbs)

            if offseter > 0 :
                result_custom_skills  = scs[:offseter]
            else :
                result_custom_skills  = scs

            nbsk = 0
            for sc in result_custom_skills :
                total_skill += int(sc.point)
                nbsk += 1

            # Ajout éventuel de résultat sur la compétence sur un exo SACADO
            result_skills_set = set()
            result_skills__ = Resultggbskill.objects.filter(skill= skill,student=student,relationship__parcours = parcours).order_by("-id")
            result_skills_set.update(set(result_skills__))
            result_skills = list(result_skills_set)
            nb_result_skill = len(result_skills)
            offset = min(nb_skill, nb_result_skill)

            if offset > 0 :
                result_sacado_skills  = result_skills[:offset]
            else :
                result_sacado_skills  = result_skills

            for result_sacado_skill in result_sacado_skills:
                total_skill += result_sacado_skill.point
                nbsk += 1
            ################################################################

            if nbsk != 0 :
                tot_s = total_skill//nbsk
                level_skill = get_level_by_point(student,tot_s)
            else :
                level_skill = "A"

            skill_level_tab.append(level_skill)
 
        writer.writerow( skill_level_tab )
    return response

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
            score = float(studentanswer.point)
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
                score = float(studentanswer.point * value/100)
            else :
                score = float(studentanswer.point) 
        except :
            score = "Abs"
        writer.writerow( (full_name , score) )
    return response



#######################################################################################################################################################################
#######################################################################################################################################################################
##################    Course     
#######################################################################################################################################################################
#######################################################################################################################################################################



def list_courses(request):

    teacher = request.user.teacher
    courses = Course.objects.filter(teacher = teacher)

    return render(request, 'qcm/course/list_course.html', {'courses': courses,  })



#@user_is_parcours_teacher
def create_course(request, idc , id ):
    """
    idc : course_id et id = parcours_id pour correspondre avec le decorateur
    """
    ######################################################    
    #  Pour modifier un annoncement de cours
    #courses = Course.objects.filter(annoncement__contains="iframe",author_id=2480)
    #for course in courses :
    #    annoncement = course.annoncement
    #    course.annoncement = annoncement.replace("/888888/","/FFFFFF/")
    #    course.save()

    ######################################################


    parcours = Parcours.objects.get(pk =  id)
    teacher =  request.user.teacher


    role, group , group_id , access = get_complement(request, teacher, parcours)
    
    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')

    form = CourseForm(request.POST or None , parcours = parcours )
    relationships = Relationship.objects.filter(parcours = parcours,exercise__supportfile__is_title=0).order_by("ranking")
    if request.method == "POST" :
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.parcours = parcours
            nf.teacher = teacher
            nf.author = teacher
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
    teacher =  request.user.teacher
    course = Course.objects.get(id=idc)
    course_form = CourseForm(request.POST or None, instance=course , parcours = parcours )
    relationships = Relationship.objects.filter(parcours = parcours,exercise__supportfile__is_title=0).order_by("ranking")
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

    role, group , group_id , access = get_complement(request, teacher, parcours)


    context = {'form': course_form,  'course': course, 'teacher': teacher , 'parcours': parcours  , 'relationships': relationships , 'communications' : [] , 'group' : group, 'group_id' : group_id , 'role' : role }

    return render(request, 'qcm/course/form_course.html', context )



def delete_course(request, idc , id  ):
    """
    idc : course_id et id = parcours_id pour correspondre avec le decorateur
    """

    parcours = Parcours.objects.get(pk =  id)
    teacher = Teacher.objects.get(user= request.user)

    course = Course.objects.get(id=idc)

    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
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
    teacher = Teacher.objects.get(user= request.user)

    role, group , group_id , access = get_complement(request, teacher, parcours)
    
    if not teacher_has_permisson_to_parcourses(request,teacher,parcours) :
        return redirect('index')

    if parcours.is_folder :
        courses = set()
        for p in parcours.leaf_parcours.all() :
            courses.update(set(p.course.order_by("ranking"))) 
    else :    
        courses = parcours.course.all().order_by("ranking") 

    if len(courses) > 0 :
        course = list(courses)[0]
    else :
        course = None
 
    
    context = {  'courses': courses, 'course': course, 'teacher': teacher , 'parcours': parcours , 'group_id' : group_id, 'communications' : [] , 'relationships' : [] , 'group' : group ,  'group_id' : group_id , 'role' : role }
    return render(request, 'qcm/course/show_course.html', context)

 



def ajax_parcours_get_course(request):
    """ Montre un cours"""
    teacher = request.user.teacher
    sacado_asso = False
    if teacher.user.school   :
        sacado_asso = True

    course_id =  request.POST.get("course_id",0)
    if course_id > 0 : 
        course = Course.objects.get(pk=course_id)
    else:
        course = None


    parcours_id =  request.POST.get("parcours_id",None)
    if parcours_id :
        parcours = Parcours.objects.get(pk = parcours_id)
    else :
        parcours = None


    role, group , group_id , access = get_complement(request, teacher, parcours)
    request.session["parcours_id"] = parcours.id
    request.session["group_id"] = group_id


    parcourses =  teacher.teacher_parcours.order_by("level")    

    context = {  'course': course , 'parcours': parcours ,  'parcourses': parcourses , 'teacher' : teacher , 'sacado_asso' : sacado_asso , 'group' : group }
    data = {}
    data['html'] = render_to_string('qcm/course/ajax_parcours_get_course.html', context)
 
    return JsonResponse(data)
 


def ajax_parcours_clone_course(request):
    """ Clone un parcours depuis la liste des parcours"""
    teacher = request.user.teacher

    all_parcours = request.POST.get("all_parcours")
    checkbox_value = request.POST.get("checkbox_value")
    course_id = request.POST.get("course_id",None)

    if course_id  : 
        course = Course.objects.get(pk=int(course_id))
        if checkbox_value != "" :
            checkbox_ids = checkbox_value.split("-")
            for checkbox_id in checkbox_ids :
                try :
                    if all_parcours == "0" :
                        course.pk = None
                        course.teacher = teacher
                        course.parcours_id = int(checkbox_id)
                        course.save()
                    else :
                        courses = course.parcours.course.all()
                        for course in courses :
                            course.pk = None
                            course.teacher = teacher
                            course.parcours_id = int(checkbox_id)
                            course.save()
                except :
                    pass

    else :
        parcours_id = int(request.POST.get("parcours_id"))
        parcours = Parcours.objects.get(pk = parcours_id) 
        if checkbox_value != "" :
            checkbox_ids = checkbox_value.split("-")
            for checkbox_id in checkbox_ids :
                try :
                    courses = parcours.course.all()
                    for course in courses :
                        course.pk = None
                        course.teacher = teacher
                        course.parcours_id = int(checkbox_id)
                        course.save()
                except :
                    pass

    data = {}
    data["success"] = "<i class='fa fa-check text-success'></i>"

    return JsonResponse(data)


  
def get_this_course_for_this_parcours(request,typ,id_target,idp):
    """ Clone un parcours depuis la liste ver un parcours de provenance """

    teacher = request.user.teacher
    if typ==1  : 
        course = Course.objects.get(pk=int(idp))
        course.pk = None
        course.teacher = teacher
        course.parcours_id = id_target
        course.save()

    else :
        parcours = Parcours.objects.get(pk = idp)

        courses = parcours.course.all()
        for course in courses :
            course.pk = None
            course.teacher = teacher
            course.parcours_id = id_target
            course.save()
     
    return redirect("show_course" , 0, id_target )

 
 

def get_course_in_this_parcours(request,id):
    parcours = Parcours.objects.get(pk = id) 
    user = request.user

    teacher_id = get_teacher_id_by_subject_id(parcours.subject.id) 

    if user.is_teacher:  # teacher
    
        teacher = request.user.teacher
        role, group , group_id , access = get_complement(request, teacher, parcours)
        request.session["parcours_id"] = parcours.id
        request.session["group_id"] = group_id

        courses = Course.objects.filter( Q(parcours__teacher__user__school = teacher.user.school)| Q(parcours__teacher__user_id=teacher_id),is_share = 1).exclude(parcours__teacher = teacher).order_by("parcours__level","parcours")

        return render(request, 'qcm/course/list_courses.html', {  'teacher': teacher , 'group': group , 'courses':courses,   'parcours': parcours, 'relationships' : [] ,  'communications': [] , })
    else :
        return redirect('index')  



def course_custom_show_shared(request):
    
    user = request.user
    if user.is_teacher:  # teacher
        teacher = request.user.teacher
        role, group , group_id , access = get_complement(request, teacher, parcours)
        request.session["parcours_id"] = parcours.id
        request.session["group_id"] = group_id


        courses = Course.objects.filter( Q(parcours__teacher__user__school = teacher.user.school)| Q(parcours__teacher__user_id=2480),is_share = 1).exclude(teacher = teacher).order_by("parcours","parcours__level")

        return render(request, 'qcm/course/list_courses.html', {  'teacher': teacher , 'courses':courses, 'group': group ,  'parcours': None, 'relationships' : [] ,  'communications': [] , })
    else :
        return redirect('index')   




def ajax_course_custom_show_shared(request):
    
    teacher = Teacher.objects.get(user= request.user)
 
    data = {} 

    level_id = request.POST.get('level_id',0)

    courses = []
    keywords = request.POST.get('keywords',None)

    parcours_id = request.POST.get('parcours_id',None)
    if parcours_id :
        parcours = Parcours.objects.get(pk = parcours_id)
        teacher = request.user.teacher
        role, group , group_id , access = get_complement(request, teacher, parcours)
        request.session["parcours_id"] = parcours.id
        request.session["group_id"] = group_id


        template = 'qcm/course/ajax_list_courses_for_parcours.html'
    else :
        parcours = None
        group = None
        template = 'qcm/course/ajax_list_courses.html'


    if int(level_id) > 0 :
        
        level = Level.objects.get(pk=int(level_id))
        theme_ids = request.POST.getlist('theme_id')

        datas = []
        themes_tab = []

        for theme_id in theme_ids :
            themes_tab.append(theme_id) 

        if len(themes_tab) > 0 and themes_tab[0] != "" :

            exercises = Exercise.objects.filter(theme_id__in= themes_tab, level_id = level_id)

            parcours_set = set()
            for exercise in exercises :
                parcours_set.update(exercise.exercises_parcours.all())

            parcours_tab = list(parcours_set)
            courses += list(Course.objects.filter( Q(parcours__teacher__user__school = teacher.user.school)| Q(parcours__teacher__user_id=2480),is_share = 1, parcours__in = parcours_tab ) )

        else :
            courses += list(Course.objects.filter( Q(parcours__teacher__user__school = teacher.user.school)| Q(parcours__teacher__user_id=2480), parcours__level = level,is_share = 1 ) )      
    

    if keywords :
        for keyword in keywords.split(' '):
            courses += list(Course.objects.filter(Q(title__icontains=keyword)| Q(annoncement__icontains=keyword),is_share = 1))

    elif int(level_id) == 0 : 
        courses = Course.objects.filter( Q(parcours__teacher__user__school = teacher.user.school)| Q(parcours__teacher__user_id=2480),is_share = 1).exclude(teacher = teacher)


    data['html'] = render_to_string(template , {'courses' : courses, 'teacher' : teacher, 'parcours' : parcours  ,  'group': group })
 
    return JsonResponse(data)




def ajax_course_custom_for_this_parcours(request):
    
    teacher = Teacher.objects.get(user= request.user)
 
    data = {} 

    level_id = request.POST.get('level_id',0)

    courses = []
    keywords = request.POST.get('keywords',None)

    parcours_id = request.POST.get('parcours_id',None)
    if parcours_id :
        parcours = Parcours.objects.get(pk = parcours_id)
    else :
        parcours = None

    if int(level_id) > 0 :
        
        level = Level.objects.get(pk=int(level_id))
        theme_ids = request.POST.getlist('theme_id')

        datas = []
        themes_tab = []

        for theme_id in theme_ids :
            themes_tab.append(theme_id) 

        if len(themes_tab) > 0 and themes_tab[0] != "" :

            exercises = Exercise.objects.filter(theme_id__in= themes_tab, level_id = level_id)

            parcours_set = set()
            for exercise in exercises :
                parcours_set.update(exercise.exercises_parcours.all())

            parcours_tab = list(parcours_set)
            courses += list(Course.objects.filter( Q(parcours__teacher__user__school = teacher.user.school)| Q(parcours__teacher__user_id=2480),is_share = 1, parcours__in = parcours_tab ) )

        else :
            courses += list(Course.objects.filter( Q(parcours__teacher__user__school = teacher.user.school)| Q(parcours__teacher__user_id=2480), parcours__level = level,is_share = 1 ) )      
    

    if keywords :
        for keyword in keywords.split(' '):
            courses += list(Course.objects.filter(Q(title__icontains=keyword)| Q(annoncement__icontains=keyword),is_share = 1))

    elif int(level_id) == 0 : 
        courses = Course.objects.filter( Q(parcours__teacher__user__school = teacher.user.school)| Q(parcours__teacher__user_id=2480),is_share = 1).exclude(teacher = teacher)


    data['html'] = render_to_string('qcm/course/ajax_list_courses_for_parcours.html', {'courses' : courses, 'teacher' : teacher  , 'parcours' : parcours   })
 
    return JsonResponse(data)














@student_can_show_this_course
def show_course_student(request, idc , id ):
    """
    idc : course_id et id = parcours_id pour correspondre avec le decorateur
    """
    this_user = request.user
    parcours = Parcours.objects.get(pk =  id)
    today = time_zone_user(this_user)
    courses = parcours.course.filter(Q(is_publish=1)|Q(publish_start__lte=today),Q(is_publish=1)|Q(publish_end__gte=today)).order_by("ranking")  
    course = courses.first() 

    context = {  'courses': courses,  'course': course, 'parcours': parcours , 'group_id' : None, 'communications' : []}
    return render(request, 'qcm/course/show_course_student.html', context)
 


 
def ajax_parcours_shower_course(request):
    course_id =  int(request.POST.get("course_id"))
    course = Course.objects.get(pk=course_id)
    data = {}
    data['title'] = course.title
    context = {  'course': course   }
 
    data['html'] = render_to_string('qcm/course/ajax_shower_course.html', context)

    return JsonResponse(data)



@csrf_exempt 
def ajax_course_viewer(request):
    """ Lis un cours à partir d'une pop up """

    relation_id =  request.POST.get("relation_id",None)
    data = {}
    if relation_id : 
        relationship = Relationship.objects.get( id = int(relation_id))
        courses = Course.objects.filter(relationships = relationship).order_by("ranking")

        if request.user.user_type == 2 :
            is_teacher = True
        else : 
            is_teacher = False 
        context = { 'courses' : courses , 'parcours' : relationship.parcours , 'is_teacher' : is_teacher , 'teacher' : request.user.teacher  }
        html = render_to_string('qcm/course/course_viewer.html',context)
        data['html'] = html       

    return JsonResponse(data)


@csrf_exempt 
def ajax_this_course_viewer(request):  

    course_id =  request.POST.get("course_id",None)
    course = Course.objects.get(pk=course_id)
    data = {}
 
    
    parcours_id =  int(request.POST.get("parcours_id"))
    parcours = Parcours.objects.get(pk=parcours_id)

    data = {}
    data['title'] = course.title

 
    if request.user.user_type == 2 :
        teacher = request.user.teacher
        url = 'qcm/course/ajax_shower_course_teacher.html'
    else :
        teacher = None
        url = 'qcm/course/ajax_shower_course.html'        



    context = {  'course': course , 'parcours': parcours , 'teacher' : teacher   }
 
 
    html = render_to_string(url, context )
    data['html'] = html       
    data['title'] = course.title   

    return JsonResponse(data)


#######################################################################################################################################################################
#######################################################################################################################################################################
##################    Demand     
#######################################################################################################################################################################
#######################################################################################################################################################################



def list_demands(request):

    demands = Demand.objects.order_by("done")

    return render(request, 'qcm/demand/show_demand.html', {'demands': demands,  })




def create_demand(request):
    teacher = request.user.teacher
    form = DemandForm(request.POST or None  )
    if request.method == "POST" :
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.teacher = teacher
            nf.save()
            messages.success(request, 'La demande a été envoyée avec succès !')
            rec = ['brunoserres33@gmal.com', 'philippe.demaria83@gmal.com', ]
            sending_mail("SacAdo Demande d'exercice",  "Demande d'exercice.... voir dans Demande d'exercices sur sacado.xyz\n Nous essaierons de réaliser l'exercice au plus proche de vos idées." , settings.DEFAULT_FROM_EMAIL , rec )

            sender = [teacher.user.email,]
            sending_mail("SacAdo Demande d'exercice",  "Votre demande d'exercice est en cours de traitement." , settings.DEFAULT_FROM_EMAIL , sender )


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

    sending_mail("SacAdo Demande d'exercice",  "Bonjour " + str(demand.teacher.user.get_full_name())+ ", \n\n Votre exercice est créé. \n\n Pour tester votre exercice, https://sacado.xyz/qcm/show_exercise/"+str(code)  +"\n\n Bonne utilisation de sacado." , settings.DEFAULT_FROM_EMAIL , rec )
    data={}
    return JsonResponse(data)




#######################################################################################################################################################################
#######################################################################################################################################################################
##################    Mastering     
#######################################################################################################################################################################
#######################################################################################################################################################################

def create_mastering(request,id):

    relationship = Relationship.objects.get(pk = id)
    stage = get_stage(request.user)
    form = MasteringForm(request.POST or None, request.FILES or None, relationship = relationship )

    masterings_q = Mastering.objects.filter(relationship = relationship , scale = 4).order_by("ranking")
    masterings_t = Mastering.objects.filter(relationship = relationship , scale = 3).order_by("ranking")
    masterings_d = Mastering.objects.filter(relationship = relationship , scale = 2).order_by("ranking")
    masterings_u = Mastering.objects.filter(relationship = relationship , scale = 1).order_by("ranking")
    teacher = request.user.teacher

    if not teacher_has_permisson_to_parcourses(request,teacher,relationship.parcours) :
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
    teacher = request.user.teacher
    if not teacher_has_permisson_to_parcourses(request,teacher,m.relationship.parcours) :
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
    # Cette fonction est appelé pour les exercices ou pour les customexercises. Du coup pour éviter une erreur, si la relationship n'existe pas on ne fait rien, juste le css

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
    teacher = request.user.teacher
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


##################################################################################################################################################
##################################################################################################################################################
##################################################       FOLDER      #############################################################################    
##################################################################################################################################################
##################################################################################################################################################

def create_folder(request,idg):
    """ 'parcours_is_folder' : True pour les vignettes et différencier si folder ou pas """
    teacher = request.user.teacher 
    group = Group.objects.get(pk = idg)
    form = ParcoursForm(request.POST or None, request.FILES or None, teacher = teacher, initial = {'subject': group.subject,'level': group.level  })
    images = group.level.level_parcours.values_list("vignette", flat = True).filter(subject_id = group.subject).exclude(vignette=" ").distinct()

    parcourses = set()
    for student in group.students.all() :
        parcourses.update(student.students_to_parcours.filter(teacher = teacher).exclude(is_folder=1,is_leaf=1))

    if request.method == "POST" :
        lp = []            
        subparcours =  request.POST.getlist('subparcours')
        for pi in subparcours :
            p = Parcours.objects.get(pk = pi)
            p.is_leaf = 1
            p.save()
            lp.append(p)

        if form.is_valid():
            nf = form.save(commit=False)
            nf.author = teacher
            nf.teacher = teacher
            nf.is_evaluation = 0
            nf.is_folder = 1
            nf.level = group.level
            nf.subject = group.subject
            if request.POST.get("this_image_selected",None) : # récupération de la vignette précréée et insertion dans l'instance du parcours.
                nf.vignette = request.POST.get("this_image_selected",None)
            nf.save() 
            nf.groups.add(group) 
            nf.leaf_parcours.set(lp)        
            for s in request.POST.getlist("these_students"):
                nf.students.add(s)
            return redirect ("list_parcours_group", idg )     
        else:
            print(form.errors)

    context = {'form': form,  'parcours_is_folder' : True,  'teacher': teacher, 'group': group,  'group_id': group.id,  'images' : images ,    'parcours': None, 'parcourses' : parcourses ,  'relationships': [], 'role' : True }

    return render(request, 'qcm/form_folder.html', context)
 



def update_folder(request,id,idg):
    """ 'parcours_is_folder' : True pour les vignettes et différencier si folder ou pas """
    teacher      = request.user.teacher
    groups       = teacher.groups.all() 
    share_groups = teacher.teacher_group.all() 
    parcours     = Parcours.objects.get(id=id)
    form         = UpdateParcoursForm(request.POST or None, request.FILES or None, instance=parcours, teacher=teacher)

    try :
        group = Group.objects.get(pk = idg)     
        group_id = group.id
        parcourses = set()
        for student in group.students.all() :
            parcourses.update(student.students_to_parcours.filter(teacher = teacher).exclude(is_folder=1))
        group_exists = True
        images = group.level.level_parcours.values_list("vignette", flat = True).filter(subject_id = group.subject).exclude(vignette=" ").distinct()

    except :
        group = None
        group_id = None
        group_exists = False
        parcourses = teacher.teacher_parcours.all()
        images = [] 
        parcourses = teacher.teacher_parcours.all()
        images = [] 

    if request.method == "POST" :
        lp = []            
        subparcours =  request.POST.getlist('subparcours')
        for pi in subparcours :
            p = Parcours.objects.get(pk = pi)
            p.is_leaf = 1
            p.save()
            lp.append(p)

        if form.is_valid():
            nf = form.save(commit=False)
            nf.author = teacher
            nf.teacher = teacher
            nf.is_evaluation = 0
            nf.is_folder = 1
            if group_exists : 
                nf.level = group.level
                nf.subject = group.subject
 

            if request.POST.get("this_image_selected",None) : # récupération de la vignette précréée et insertion dans l'instance du parcours.
                nf.vignette = request.POST.get("this_image_selected",None)
            nf.save()  
            nf.leaf_parcours.set(lp)
            ##################################################
            ## Suppression des élèves 
            if group_exists :
                for stu in group.students.exclude(user__username__contains="_e-test") :
                    nf.students.remove(stu)
            ## Insertion des nouveaux élèves
            for s in request.POST.getlist("these_students"):
                nf.students.add(s)
            ##################################################
            if group_exists :
                return redirect ("list_parcours_group", idg ) 
            else :
                return redirect ("index" ) 
        else:
            print(form.errors)

    context = {'form': form, 'parcours_is_folder' : True,   'teacher': teacher,  'group': group, 'groups': groups, 'share_groups': share_groups, 'group_id': group_id,  'parcours': parcours, 'parcourses' : parcourses , 'images' : images ,   'relationships': [], 'role' : True }

    return render(request, 'qcm/form_folder.html', context)
 

@parcours_exists
def folder_archive(request,id):

    parcours = Parcours.objects.get(id=id)
    parcours.is_archive = 1
    parcours.save()
    subparcours = parcours.leaf_parcours.all()
 
    for p in subparcours :
        p.is_archive = 1
        p.save()

    return redirect('parcours')




@parcours_exists
def folder_unarchive(request,id):

    parcours = Parcours.objects.get(id=id)
    parcours.is_archive = 0
    parcours.save()
    subparcours = parcours.leaf_parcours.all()
 
    for p in subparcours :
        p.is_archive = 0
        p.save()

    if parcours.is_evaluation :
        return redirect('evaluations')
    else :
        return redirect('parcours')
 



@parcours_exists
def delete_folder(request,id,idg):

    teacher = request.user.teacher 
    parcours = Parcours.objects.get(id=id) 

    if parcours.teacher == teacher or request.user.is_superuser :
        if parcours.leaf_parcours.count() == 0 :
            parcours.delete()
        else :
            messages.error(request, "Le dossier "+ parcours.title +" n'est pas vide. La suppression n'est pas possible.")
    
    else :
        messages.error(request, "Vous ne pouvez pas supprimer le dossier "+ parcours.title +". Contacter le propriétaire.")
    
    if idg == 0 :
        return redirect ("parcours" )  
    else :
        return redirect ("list_parcours_group", idg )  



def parcours_delete_from_folder(request):

    parcours_id =  request.POST.get("parcours_id",None) 
    if parcours_id :
        parcours = Parcours.objects.get( pk = int(parcours_id))
        if parcours.teacher == request.user.teacher :
            parcours.delete()
    data = {}
         
    return JsonResponse(data)




def actioner(request):

    teacher = request.user.teacher 
    idps = request.POST.getlist("selected_parcours") 
    print(request.POST.get("action") , idps)
    if  request.POST.get("action") == "deleter" :  
        for idp in idps :
            parcours = Parcours.objects.get(id=idp) 
            if parcours.teacher == teacher or request.user.is_superuser :
                if parcours.is_folder :
                    if parcours.leaf_parcours.count() == 0 :
                        parcours.delete()
                    else :
                        messages.error(request, "Le dossier "+ parcours.title +" n'est pas vide. La suppression n'est pas possible.")
                else :
                    parcours.delete()
            
            else :
                messages.error(request, "Vous ne pouvez pas supprimer le dossier "+ parcours.title +". Contacter le propriétaire.")

    else: 

        for idp in idps :
            parcours = Parcours.objects.get(id=idp) 
            parcours.is_archive = 1
            parcours.save()
            subparcours = parcours.leaf_parcours.all()
            for p in subparcours :
                p.is_archive = 1
                p.save()

    return redirect('parcours')








#######################################################################################################################################################################
#######################################################################################################################################################################
#################   Testeurs
#######################################################################################################################################################################
#######################################################################################################################################################################
@user_passes_test(user_is_testeur)
def admin_testeur(request):

    user = request.user
    reporting_s , reporting_p , reporting_c = [] , [] , []
    reportings = DocumentReport.objects.exclude(is_done=1)
    for r in reportings :
        if r.document == "supportfile" :
            reporting_s.append(r.id)
        if r.document == "parcours" :
            reporting_p.append(r.id)
        if r.document == "cours" :
            reporting_c.append(r.id)

    parcourses = Parcours.objects.filter(teacher__user_id = 2480).exclude(pk__in=reporting_s).order_by("level")
    supportfiles = Supportfile.objects.filter(is_title=0).exclude(pk__in=reporting_p).order_by("level","theme","knowledge__waiting","knowledge","ranking")
    courses = Course.objects.filter(teacher__user_id = 2480).exclude(pk__in=reporting_c).order_by("parcours")
    form_reporting = DocumentReportForm(request.POST or None )

    context = { "user" :  user , "parcourses" :  parcourses , "supportfiles" :  supportfiles , "courses" :  courses ,  "form_reporting" :  form_reporting , }
 
    return render(request, 'qcm/dashboard_testeur.html', context)




@user_passes_test(user_is_testeur)
def reporting(request ):

    user = request.user    
    form_reporting = DocumentReportForm(request.POST or None )
    if form_reporting.is_valid() :
        nf = form_reporting.save(commit=False)
        nf.user = request.user
        nf.document = request.POST["document"]
        nf.save()

        rec = ["nicolas.villemain@claudel.org" , "brunoserres33@gmail.com " , "sacado.asso@gmail.com"]
        if nf.report != "<p>RAS</p>" :
            sending_mail("SACADO "+nf.document+" à modifier", str(nf.document)+" #"+str(nf.document_id)+" doit recevoir les modifications suivantes : \n\n "+str(cleanhtml(nf.report))+"\n\n"+str(request.user) , settings.DEFAULT_FROM_EMAIL , rec )
        else :
            DocumentReport.objects.filter(pk=int(nf.document_id)).update(is_done=1)
            sending_mail("SACADO "+nf.document+" #"+str(nf.document_id)+" vérifié", str(nf.document)+" dont l'id: "+str(nf.document_id)+" est validé sans erreur par "+str(request.user) , settings.DEFAULT_FROM_EMAIL , rec )

    return redirect('admin_testeur')


@user_passes_test(user_is_testeur)
def reporting_list(request, code ):

    tab = ["supportfile","parcours","course"]
    user = request.user  
    reportings = DocumentReport.objects.filter(document=tab[code], is_done=0).exclude(report="<p>RAS</p>")

    context = { "user" :  user , "reportings" : reportings , "doc" : tab[code] , "code" : code }
 
    return render(request, 'qcm/reporting_list.html', context)
 


@user_passes_test(user_is_testeur)
def repaired_reporting(request, pk,code ):

    DocumentReport.objects.filter(pk=pk).update(is_done=1)
    return redirect( 'admin_testeur', code)


def simulator(request):
    context = {}
    return render(request, 'qcm/simulator.html', context )

