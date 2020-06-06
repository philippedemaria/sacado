from django.shortcuts import render, redirect
from account.models import  Student, Teacher, User,Resultknowledge, Resultskill, Resultlastskill
from account.forms import StudentForm, TeacherForm, UserForm
from django.contrib.auth.forms import  AuthenticationForm
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from sendmail.forms import  EmailForm
from group.forms import GroupForm 
from group.models import Group 
from qcm.models import  Parcours , Studentanswer, Exercise, Relationship,Resultexercise, Supportfile,Remediation, Constraint
from qcm.forms import ParcoursForm , ExerciseForm, RemediationForm, UpdateParcoursForm , UpdateSupportfileForm, SupportfileKForm, RelationshipForm, SupportfileForm 
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
from qcm.decorators import user_is_parcours_teacher
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
import re
import pytz
import csv

def time_zone_user(user):
    if user.time_zone :
        time_zome = user.time_zone
        timezone.activate(pytz.timezone(time_zome))
        current_tz = timezone.get_current_timezone()
        today = timezone.localtime(timezone.now())
        today = timezone.now()
     
    else :
        today = timezone.now()
    return today



def cleanhtml(raw_html): #nettoie le code des balises HTML
    cleantext = re.sub('<.*?>', '', raw_html)
    cleantext = re.sub('\n', '', cleantext)
    return cleantext


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



def  admin_tdb(request):
    teacher = Teacher.objects.get(user_id = request.user.id)
    levels = Level.objects.all()
    return render(request, 'dashboard_admin.html', {'teacher': teacher , 'levels': levels })




def  advises(request):
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
        send_mail("Nouvel exercice SacAdo",  msg , "sacado_Tache@erlm.tn" , rcv)
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
            i+=1

    if len(parcours.students.all())>0 :
        return redirect("list_parcours_group" , group.id )
    else :
        return redirect("index") 



#######################################################################################################################################################################
#######################################################################################################################################################################
#################   parcours
#######################################################################################################################################################################
#######################################################################################################################################################################


 

@csrf_exempt # PublieDépublie un exercice depuis organize_parcours
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

            r = Relationship.objects.get(parcours_id=parcours_id, exercise_id = exercise_id)        
            r.delete()         
            statut = 0
            data["statut"] = "False"
            data["class"] = "btn btn-danger"
            data["noclass"] = "btn btn-success"
            data["html"] = "<i class='fa fa-times'></i>"


            students = parcours.students.all()
            for student in students :
                for e in parcours.exercises.all():
                    e.students.remove(student)

        else:
            statut = 1

            relation = Relationship.objects.create(parcours_id=parcours_id, exercise_id = exercise_id, order = 100, situation = exercise.supportfile.situation , duration = exercise.supportfile.duration)  
            relation.skills.set(exercise.supportfile.skills.all()) 

            students = parcours.students.all()
            for student in students :
                for e in parcours.exercises.all():
                    e.students.add(student)
            data["statut"] = "True"
            data["class"] = "btn btn-success"
            data["noclass"] = "btn btn-danger"
            data["html"] = "<i class='fa fa-check-circle fa-2x'></i>"

    return JsonResponse(data) 




@login_required
@user_is_parcours_teacher
def peuplate_parcours(request,id):
    teacher = Teacher.objects.get(user_id = request.user.id)
    levels =  teacher.levels.all() 
 
    parcours = Parcours.objects.get(id=id)
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
 
        # modifie les exercices sélectionnés
        exercises_all = parcours.exercises.filter(supportfile__is_title=0)
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
                r = Relationship.objects.create(parcours = nf , exercise = exercise , order =  i,situation = exercise.supportfile.situation , duration = exercise.supportfile.duration , skills = exercise.supportfile.skills )  
                i+=1
            except :
                pass

    try :
        group_id = request.session.get("group_id")
    except :
        group_id = None
        # fin ---- modifie les exercices sélectionnés
    context = {'form': form, 'parcours': parcours,       'teacher': teacher, 'exercises': exercises , 'levels': levels , 'themes' : themes_tab , 'user': request.user , 'group_id' : group_id , 'relationships' :relationships  }

    return render(request, 'qcm/form_peuplate_parcours.html', context)






@login_required
@user_is_parcours_teacher
def individualise_parcours(request,id):
    teacher = Teacher.objects.get(user_id = request.user.id)
    parcours = Parcours.objects.get(pk = id)
    relationships = Relationship.objects.filter(parcours = parcours).order_by("order")
    students = parcours.students.all().order_by("user__last_name")
    return render(request, 'qcm/form_individualise_parcours.html', { 'relationships': relationships , 'parcours': parcours , 'students': students  })





@csrf_exempt # PublieDépublie un exercice depuis organize_parcours
def ajax_individualise(request):  

    exercise_id = int(request.POST.get("exercise_id"))
    parcours_id = int(request.POST.get("parcours_id"))
    student_id = int(request.POST.get("student_id"))

    exercise = Exercise.objects.get(pk = exercise_id)
    parcours = Parcours.objects.get(pk = parcours_id)
    statut = request.POST.get("statut") 

    relationship = Relationship.objects.get(parcours=parcours,exercise=exercise) 
    data = {}
    teacher = Teacher.objects.get(user= request.user)     
    if parcours.teacher == teacher :
        if student_id == 0 :  
            if statut=="true" or statut == "True" :
                try :
                    for s in parcours.students.all() :
                        relationship.students.remove(s)
                except :
                    pass
                statut = 0
                data["statut"] = "False"
                data["class"] = "btn btn-danger"
                data["noclass"] = "btn btn-success"
                
            else : 
                relationship.students.set(parcours.students.all())
                statut = 1    
                data["statut"] = "True"
                data["class"] = "btn btn-success"
                data["noclass"] = "btn btn-danger"
     
        else :
            student = Student.objects.get(pk = student_id)        
            if statut=="true" or statut == "True":
                relationship.students.remove(student)
                statut = 0
                data["statut"] = "False"
                data["class"] = "btn btn-danger"
                data["noclass"] = "btn btn-success" 
            else:
                statut = 1
                relationship.students.add(student) 
                data["statut"] = "True"
                data["class"] = "btn btn-success"
                data["noclass"] = "btn btn-danger"


    return JsonResponse(data) 


@login_required
def list_parcours(request):
    teacher = Teacher.objects.get(user_id = request.user.id)
    parcourses = Parcours.objects.filter(teacher = teacher).order_by("-is_favorite")     

    try :
        del request.session["group_id"]
    except:
        pass  

    return render(request, 'qcm/list_parcours.html', { 'parcourses' : parcourses})



@login_required
@user_is_group_teacher
def list_parcours_group(request,id):

    group = Group.objects.get(pk = id)
    request.session["group_id"] = group.id
    group_tab = []
    data = {}
    parcours_tab = []
    students = group.students.all()
    for student in students :
        pcs = Parcours.objects.filter(students= student,is_favorite=1).order_by("-is_publish")
        for parcours in pcs : 
            if parcours not in parcours_tab :
                parcours_tab.append(parcours)

    return render(request, 'qcm/list_parcours_group.html', {'parcours_tab': parcours_tab , 'group': group })


@login_required
def all_parcourses(request):
    teacher = Teacher.objects.get(user=request.user)
    parcourses = Parcours.objects.exclude(Q(author=None) | Q(author=teacher), teacher=teacher).filter(
        linked=0).order_by("author").prefetch_related('exercises__knowledge__theme').select_related('author')
    # parcourses = parcourses[:15] #limite pour le debuggage
    return render(request, 'qcm/all_parcourses.html', {'parcourses': parcourses})


@login_required
@user_passes_test(user_can_create)
def create_parcours(request):


    teacher = Teacher.objects.get(user_id = request.user.id)
    levels =  teacher.levels.all()    
    form = ParcoursForm(request.POST or None, request.FILES or None, teacher = teacher)

    themes_tab = []
    for level in levels :
        for theme in level.themes.all():
            if not theme in themes_tab:
                themes_tab.append(theme)


    groups = Group.objects.filter(teacher  = teacher).order_by("level")

    if form.is_valid():
        nf = form.save(commit=False)
        nf.author = teacher
        nf.teacher = teacher
        nf.save()
        nf.students.set(form.cleaned_data.get('students'))
        i = 0
        for exercise in form.cleaned_data.get('exercises'):
            exercise = Exercise.objects.get(pk=exercise.id)
            relationship = Relationship.objects.create(parcours=nf, exercise=exercise, order=i,
                                                       duration=exercise.supportfile.duration,
                                                       situation=exercise.supportfile.situation)
            relationship.students.set(form.cleaned_data.get('students'))
            i += 1

        return redirect('parcours')
    else:
        print(form.errors)

    context = {'form': form,   'teacher': teacher,  'groups': groups,  'levels': levels,    'themes' : themes_tab  }

    return render(request, 'qcm/form_parcours.html', context)


@user_is_parcours_teacher 
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

    if request.method == "POST":
        if form.is_valid():
            nf = form.save(commit=False)
            nf.author = teacher
            nf.teacher = teacher
            nf.save()
            nf.students.set(form.cleaned_data.get('students'))
            try:
                for exercise in parcours.exercises.all():
                    relationship = Relationship.objects.get(parcours=nf, exercise=exercise)
                    relationship.students.set(form.cleaned_data.get('students'))
            except:
                pass

            if idg == 99999999999:
                return redirect('index')
            elif idg == 0:
                return redirect('parcours')
            else:
                return redirect('list_parcours_group', idg)

    if idg > 0 and idg < 99999999999 :
        group_id = idg
        request.session["group_id"] = idg
    else :
        group_id = None


    students_checked = parcours.students.count()  # nombre d'étudiant dans le parcours

    context = {'form': form, 'parcours': parcours, 'groups': groups, 'idg': idg, 'teacher': teacher, 'group_id': group_id ,  'relationships': relationships, 
               'exercises': exercises, 'levels': levels, 'themes': themes_tab, 'students_checked': students_checked}

    return render(request, 'qcm/form_parcours.html', context)



@user_is_parcours_teacher 
def delete_parcours(request, id, idg=0):
    parcours = Parcours.objects.get(id=id)

    relationships  = Relationship.objects.filter(parcours = parcours)
    for r in relationships :
        r.delete()

    parcours.delete()
    if idg == 99999999999:
        return redirect('index')
    elif idg == 0 :
        return redirect('parcours')
    else :
        return redirect('list_parcours_group', idg)


@login_required
def show_parcours(request, id):
    parcours = Parcours.objects.get(id=id)
    user = User.objects.get(pk=request.user.id)
    teacher = Teacher.objects.get(user=user)
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

    try:
        group_id = request.session["group_id"]
    except:
        group_id = None

    students_p_or_g = students_from_p_or_g(request,parcours)

    skills = Skill.objects.all()
    
    nb_exercises = parcours.exercises.filter(supportfile__is_title=0).count()
    context = {'relationships': relationships, 'parcours': parcours, 'teacher': teacher, 'skills': skills, 'students_from_p_or_g': students_p_or_g,  
               'nb_exercises': nb_exercises, 'nb_exo_visible': nb_exo_visible, 'nb_exo_only': nb_exo_only, 
               'group_id': group_id}

    return render(request, 'qcm/show_parcours.html', context)





@login_required
def show_parcours_student(request, id):
    parcours = Parcours.objects.get(id=id)
    user = User.objects.get(pk = request.user.id)
    student = Student.objects.get(user = user)
    relationships = Relationship.objects.filter(parcours=parcours, students=student, is_publish=1 ).order_by("order")
    nb_exo_only = [] 
    i=0

    for r in relationships :
        if r.exercise.supportfile.is_title or r.exercise.supportfile.is_subtitle:
            i=0
        else :
            i+=1
        nb_exo_only.append(i)

    today = time_zone_user(request.user)

    nb_exercises = parcours.exercises.filter(supportfile__is_title=0).count()
    context = {'relationships': relationships,  'parcours': parcours, 'student': student, 'nb_exercises': nb_exercises,'nb_exo_only': nb_exo_only, 'today': today ,  }
 
    return render(request, 'qcm/show_parcours_student.html', context)




@login_required
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
    context = {'relationships': relationships,  'parcours': parcours,   'nb_exo_only': nb_exo_only, 'nb_exercises': nb_exercises,  }
 
    return render(request, 'qcm/show_parcours_visual.html', context)





@user_is_parcours_teacher 
def result_parcours(request, id):

    parcours = Parcours.objects.get(id=id)
    students = students_from_p_or_g(request,parcours) # liste des élèves d'un parcours donné 

    try :
        group_id = request.session["group_id"]
    except :
        group_id = None

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

    form = EmailForm(request.POST or None )


    context = {  'relationships': relationships, 'parcours': parcours, 'students': students, 'themes': themes_tab, 'form': form,  'group_id' : group_id    }

    return render(request, 'qcm/result_parcours.html', context )



 ########## Sans doute pus utilisée ???? 
@user_is_parcours_teacher 
def result_parcours_theme(request, id, idt):


    parcours = Parcours.objects.get(id=id)
    students = students_from_p_or_g(request,parcours)

    try :
        group_id = request.session["group_id"]
    except :
        group_id = None


    parcours = Parcours.objects.get(id=id)
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
 
    form = EmailForm(request.POST or None)
    context = {  'relationships': relationships, 'parcours': parcours, 'students': students,  'themes': themes_tab,'form': form, 'group_id' : group_id }

    return render(request, 'qcm/result_parcours.html', context )
 



 
@user_is_parcours_teacher 
def result_parcours_knowledge(request, id):

    parcours = Parcours.objects.get(id=id)
    students = students_from_p_or_g(request,parcours)

    form = EmailForm(request.POST or None)


    knowledges = []
    
    try :
        group_id = request.session["group_id"]
    except :
        group_id = None
    
    knowledge_ids = parcours.exercises.values_list("knowledge",flat=True).order_by("knowledge").distinct()
    for k_id in knowledge_ids : 
        knowledges.append(Knowledge.objects.get(pk = k_id))

    context = {  'students': students, 'parcours': parcours,  'form': form, 'exercise_knowledges' : knowledges, 'group_id' : group_id }

    return render(request, 'qcm/result_parcours_knowledge.html', context )



@user_is_parcours_teacher 
def stat_parcours(request, id):
    parcours = Parcours.objects.get(id=id)
    exercises = parcours.exercises.all()
    relationships = Relationship.objects.filter(parcours=parcours).prefetch_related('exercise__supportfile').order_by("order")
    parcours_duration = parcours.duration #durée prévue pour le téléchargement
    for e in exercises :
        r = Relationship.objects.get(exercise = e, parcours = parcours)
        parcours_duration += r.duration


    form = EmailForm(request.POST or None )
    stats = []

    try :
        group_id = request.session["group_id"]
    except :
        group_id = None


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
        stats.append(student)

    context = {  'parcours': parcours, 'form': form, 'stats':stats , 'group_id':group_id , 'relationships':relationships }

    return render(request, 'qcm/stat_parcours.html', context )



@login_required
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

        Relationship.objects.create(parcours = parcours , exercise = exercise , order=  r, is_publish= 1 , start= None , date_limit= None, duration= exercise.supportfile.duration, situation= exercise.supportfile.situation   )    
        i +=1

    return redirect('exercises')

 
@login_required 
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

    return redirect('parcours')
 
 
def ajax_exercise_error(request):

    message = request.POST.get("message")  
    exercise_id = request.POST.get("exercise_id")
    exercise = Exercise.objects.get(id = int(exercise_id))
    if request.user :
        usr = request.user.email
    else :
        usr = "sacado_bug_exercise@erlm.tn"

    msg = "L'exercice dont l'id est -- "+exercise_id+" --  décrit ci-dessous : \n Savoir faire visé : "+exercise.knowledge.name+ " \n Niveau : "+exercise.level.name+  "  \n Thème : "+exercise.theme.name +" comporte un problème. \n  S'il est identifié par l'utilisateur, voici la description :  \n" + message   

    send_mail("Avertissement SacAdo Exercice "+exercise_id,  msg , request.user.email , ["brunoserres33@gmail.com", "philippe.demaria83@gmail.com", str(exercise.supportfile.author.user.email)])
    data = {}
    data["htmlg"]= "Envoi réussi, merci."
    return JsonResponse(data) 


@user_is_parcours_teacher
def parcours_tasks_and_publishes(request, id):

    today = time_zone_user(request.user)
    parcours = Parcours.objects.get(id=id)
    teacher = Teacher.objects.get(user=request.user)
 
    try :
        group_id = request.session.get("group_id")
    except :
        group_id = None
 
 
    relationships = Relationship.objects.filter(parcours=parcours).order_by("exercise__theme")
    context = {'relationships': relationships,  'parcours': parcours, 'teacher': teacher  , 'today' : today , 'group_id' : group_id }
    return render(request, 'qcm/parcours_tasks_and_publishes.html', context)
 

 

 
@login_required
@user_is_parcours_teacher
def result_parcours_exercise_students(request,id):
    teacher = Teacher.objects.get(user_id = request.user.id)
    parcours = Parcours.objects.get(pk = id)
    try :
        group_id = request.session.get("group_id")
    except :
        group_id = None
 
    relationships = Relationship.objects.filter(parcours = parcours) 

    return render(request, 'qcm/result_parcours_exercise_students.html', { 'relationships': relationships , 'parcours': parcours , 'group_id': group_id ,   })




 

@csrf_exempt
def ajax_sort_exercice(request):  

    exercise_ids = request.POST.get("valeurs")
    exercise_tab = exercise_ids.split("-") 
    
    parcours = request.POST.get("parcours")
    print(parcours)
    print(exercise_tab)

    for i in range(len(exercise_tab)-1):
        Relationship.objects.filter(parcours = parcours , exercise_id = exercise_tab[i]).update(order = i)

    data = {}
    return JsonResponse(data) 



@csrf_exempt # PublieDépublie un exercice depuis organize_parcours
def ajax_publish(request):  

    relationship_id = request.POST.get("relationship_id")
    statut = request.POST.get("statut")

    data = {}
 
    if statut=="true" or statut == "True":
        statut = 0
        data["statut"] = "false"
        data["publish"] = "Dépublié"
        data["class"] = "btn btn-danger"
        data["noclass"] = "btn btn-success"
    else:
        statut = 1
        data["statut"] = "true"
        data["publish"] = "Publié"
        data["class"] = "btn btn-success"
        data["noclass"] = "btn btn-danger"

    Relationship.objects.filter(pk = int(relationship_id)).update(is_publish = statut)
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
        data["class"] = "btn-danger"
        data["noclass"] = "btn-success"
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
        data["class"] = "btn-success"
        data["noclass"] = "btn-danger"
        data["label"] = "Publié"
        parcours = Parcours.objects.get(pk = int(parcours_id) )
        print(data)

    Parcours.objects.filter(pk = int(parcours_id)).update(is_publish = statut)
 
    return JsonResponse(data) 


@csrf_exempt
def ajax_dates(request):  
    data = {}
    relationship_id = request.POST.get("relationship_id")
    typ = int(request.POST.get("type"))
    duration =  request.POST.get("duration") 
    try :
        if typ == 0 :
            date = request.POST.get("dateur") 
            if date :
                Relationship.objects.filter(pk = int(relationship_id)).update(start = date)
                data["class"] = "btn-success"
                data["noclass"] = "btn-default"
            else :
                Relationship.objects.filter(pk = int(relationship_id)).update(start = None)
                data["class"] = "btn-default"
                data["noclass"] = "btn-success"
            data["dateur"] = date 

        elif typ == 1 :
            date = request.POST.get("dateur") 
            if date :
                Relationship.objects.filter(pk = int(relationship_id)).update(date_limit = date)
                r = Relationship.objects.get(pk = int(relationship_id))
                data["class"] = "btn-success"
                data["noclass"] = "btn-default"
                msg = "Pour le "+str(date)+": \n Faire l'exercice : http://parcours.erlm.tn/qcm/show_this_exercise/"+str(r.exercise.id)+" : " +str(r.exercise)+" \n. Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte."
                data["dateur"] = date 
                students = r.parcours.students.all()
                rec = []
                for s in students :
                    if s.task_post : 
                        if  s.user.email :                  
                            rec.append(s.user.email)

                send_mail("SacAdo Tâche à effectuer avant le "+str(date),  msg , "sacado_Tache@erlm.tn" , rec ) 
                send_mail("SacAdo Tâche à effectuer avant le "+str(date),  msg , "sacado_Tache@erlm.tn" , [r.parcours.teacher.user.email] )   

            else :
                Relationship.objects.filter(pk = int(relationship_id)).update(date_limit = None)
                r = Relationship.objects.get(pk = int(relationship_id))
                data["class"] = "btn-default"
                data["noclass"] = "btn-success"
                msg = "L'exercice http://parcours.erlm.tn/qcm/show_this_exercise/"+str(r.exercise.id)+" : "+str(r.exercise)+" n'est plus une tâche \n. Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte."
                date = "Tâche ?"          
                data["dateur"] = date 
         
                students = r.parcours.students.all()
                rec = []
                for s in students :
                    if s.task_post : 
                        if  s.user.email :                  
                            rec.append(s.user.email)
                send_mail("SacAdo. Annulation de tâche à effectuer",  msg , "sacado_Tache@erlm.tn" , rec ) 
                send_mail("SacAdo. Annulation de tâche à effectuer",  msg , "sacado_Tache@erlm.tn" , [r.parcours.teacher.user.email] ) 

        else :
            Relationship.objects.filter(pk = int(relationship_id)).update(date_limit = date)
            r = Relationship.objects.get(pk = int(relationship_id))
            data["class"] = "btn-success"
            data["noclass"] = "btn-default"
            msg = "Pour le "+str(date)+": \n Faire l'exercice : http://parcours.erlm.tn/qcm/show_this_exercise/"+str(r.exercise.id)+" : " +str(r.exercise)+" \n. Si vous ne souhaitez plus recevoir les notifications, désactiver la notification dans votre compte."
            
            students = r.parcours.students.all()
            rec = []
            for s in students :
                if s.task_post : 
                    if  s.user.email :                  
                        rec.append(s.user.email)

            send_mail("SacAdo Tâche à effectuer avant le "+str(date),  msg , "sacado_Tache@erlm.tn" , rec ) 
            send_mail("SacAdo Tâche à effectuer avant le "+str(date),  msg , "sacado_Tache@erlm.tn" , [r.parcours.teacher.user.email] ) 


            data["dateur"] = date  




    except :
        try :
            duration =  request.POST.get("duration") 
            Relationship.objects.filter(pk = int(relationship_id)).update(duration = duration)
            data["clock"] = "<i class='fa fa-clock-o'></i> "+str(duration)+"  min."
            try :
                situation =  request.POST.get("situation") 
                Relationship.objects.filter(pk = int(relationship_id)).update(situation = situation)
                data["save"] = "<i class='fa fa-save'></i> "+str(situation)
                data["situation"] = "<i class='fa fa-save'></i> "+str(situation)
            except : 
                pass

        except :
            try :
                situation =  request.POST.get("situation") 
                Relationship.objects.filter(pk = int(relationship_id)).update(situation = situation)
                data["save"] = "<i class='fa fa-save'></i> "+str(situation)
                try :
                    duration =  request.POST.get("duration") 
                    Relationship.objects.filter(pk = int(relationship_id)).update(duration = duration)
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

    parcours_id =  int(request.POST.get("parcours_id"))
    exercise_id =  int(request.POST.get("exercise_id"))
    num_exo =  int(request.POST.get("num_exo"))    
    parcours = Parcours.objects.get(id = parcours_id)

    students = students_from_p_or_g(request,parcours)



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

    context = {  'parcours': parcours,  'exercise':exercise ,'stats':stats ,  'num_exo':num_exo, }

    data = {}

    data['html'] = render_to_string('qcm/ajax_detail_parcours.html', context)
 
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




#######################################################################################################################################################################
#######################################################################################################################################################################
#################   Exercise
#######################################################################################################################################################################
#######################################################################################################################################################################

def all_datas(user, status):
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
                exercises = Exercise.objects.filter(knowledge=knowledge,supportfile__is_title=0).select_related('supportfile').order_by("theme")
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
    if user.user_type == 2 : # teacher
        teacher = Teacher.objects.get(user=user)
        datas =  all_datas(user, 0)

        return render(request, 'qcm/list_exercises.html', {'datas': datas, 'teacher':teacher})
    
    elif user.user_type == 0 : # student
        student = Student.objects.get(user=user)
        parcourses = student.students_to_parcours.all()

        nb_exercises = Relationship.objects.filter(parcours__in=parcourses,is_publish=1,exercise__supportfile__is_title=0).count()
        relationships = Relationship.objects.filter(parcours__in=parcourses,is_publish=1,exercise__supportfile__is_title=0).order_by("exercise__theme")

        return render(request, 'qcm/student_list_exercises.html', {'relationships': relationships, 'nb_exercises': nb_exercises,   })

    else :  
        exercises = Exercise.objects.all().order_by("level")
        return render(request, 'qcm/list_exercises.html', {'exercises': exercises})



@login_required
@user_passes_test(user_is_superuser)
def admin_list_associations(request):
    user = request.user
    if user.user_type == 2 : # teacher
        teacher = Teacher.objects.get(user=user)
        datas =  all_datas(user, 1)

        return render(request, 'qcm/list_associations.html', {'datas': datas, 'teacher':teacher})


@login_required
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




@login_required
@user_passes_test(user_is_superuser)
def admin_list_supportfiles(request):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    if user.is_superuser:  # admin and more

        teacher = Teacher.objects.get(user=user)
        datas = []

        levels = Level.objects.all().order_by("id")
        #levels = levels[6:8]
        for level in levels:
            levels_dict = {}
            levels_dict["name"] = level

            themes = level.themes.all().order_by("id")
            themes_tab = []
            for theme in themes:
                themes_dict = {}
                themes_dict["name"] = theme.name
                knowlegdes = Knowledge.objects.filter(theme=theme, level=level).order_by("theme")
                knowledges_tab = []
                for knowledge in knowlegdes:
                    supportfiles = knowledge.supportfiles.filter(is_title=0).order_by("theme")
                    exercises = Exercise.objects.filter(knowledge=knowledge, level=level, theme=theme).exclude(
                        supportfile__in=supportfiles).order_by("theme")

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
            datas.append(levels_dict)



    return render(request, 'qcm/list_supportfiles.html', {'datas': datas, 'teacher':teacher  })



@user_is_parcours_teacher
def parcours_exercises(request,id):
    user = request.user
    parcours = Parcours.objects.get(pk=id)
    student = Student.objects.get(user=user)

    relationships = Relationship.objects.filter(parcours=parcours,is_publish=1).order_by("exercise__theme")

    return render(request, 'qcm/student_list_exercises.html', {'parcours': parcours  , 'relationships': relationships, })




def exercises_level(request, id):
    exercises = Exercise.objects.filter(level_id=id,supportfile__is_title=0).order_by("theme")
    level = Level.objects.get(pk=id)
    themes =  level.themes.all()
    form = AuthenticationForm() 

    return render(request, 'list_exercises.html', {'exercises': exercises, 'level':level, 'themes':themes, 'form':form, })





@login_required
@user_passes_test(user_is_superuser)
def create_supportfile(request):

    code = str(uuid.uuid4())[:8]
    teacher = Teacher.objects.get(user_id = request.user.id)
    form = SupportfileForm(request.POST or None,request.FILES or None)
    if request.user.is_superuser :
        if form.is_valid():
            nf =  form.save(commit = False)
            nf.code = code
            nf.author = teacher
            send_to_teachers(nf.level)        
            nf.save()
            # le supprot GGB est placé comme exercice par défaut.
            Exercise.objects.create(supportfile = nf, knowledge = nf.knowledge, level = nf.level, theme = nf.theme )


        return redirect('admin_supportfiles')

    context = {'form': form,   'teacher': teacher}

    return render(request, 'qcm/form_supportfile.html', context)


@login_required
@user_passes_test(user_is_superuser)
def create_supportfile_knowledge(request,id):

    code = str(uuid.uuid4())[:8]
    knowledge = Knowledge.objects.get(id = id)
    teacher = Teacher.objects.get(user_id = request.user.id)
    form = SupportfileKForm(request.POST or None,request.FILES or None)
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
            return redirect('admin_supportfiles')
        else :
            print(form.errors)


    context = {'form': form,   'teacher': teacher,  'knowledges': knowledges,  'knowledge': knowledge,   'supportfiles': supportfiles,   'levels': levels}

    return render(request, 'qcm/form_supportfile.html', context)


@login_required
@user_passes_test(user_is_superuser)
def update_supportfile(request, id, redirection = 0):

    if request.user.is_superuser :  
        supportfile = Supportfile.objects.get(id=id)
        supportfile_form = UpdateSupportfileForm(request.POST or None, request.FILES or None, instance=supportfile )
        levels = Level.objects.all()
        supportfiles = Supportfile.objects.filter(is_title=0).order_by("level")
        knowledges = Knowledge.objects.all().order_by("level")

        if request.method == "POST" :
            if supportfile_form.is_valid():
                nf =  supportfile_form.save(commit = False)
                nf.code = supportfile.code
                nf.save()
                supportfile_form.save_m2m()
                messages.success(request, "L'exercice a été modifié avec succès !")

                
                return redirect('admin_supportfiles') 

        context = {'form': supportfile_form,  'supportfile': supportfile,  'knowledges': knowledges,    'supportfiles': supportfiles,   'levels': levels}

        return render(request, 'qcm/form_supportfile.html', context )

 


@login_required
@user_passes_test(user_is_superuser)
def delete_supportfile(request, id):
    if request.user.is_superuser : 
        supportfile = Supportfile.objects.get(id=id)
        if Relationship.objects.filter(exercise__supportfile = supportfile).count() == 0 :
            supportfile.delete()
            messages.success(request, "Le support GGB a été supprimé avec succès !")
        else :
            messages.error(request," Des parcours utilisent ce support GGB. Il n'est pas possible de le supprimer.")

    return redirect('admin_supportfiles') 


@login_required
@user_passes_test(user_is_superuser)
def show_this_supportfile(request, id):

    if request.user.user_type == 2:
        teacher = Teacher.objects.get(user = request.user)
        parcours = Parcours.objects.filter(teacher = teacher)

    supportfile = Supportfile.objects.get(id=id)
    request.session['level_id'] = supportfile.level.id
    start_time =  time.time()
    context = {'supportfile': supportfile,  'start_time' : start_time,  'parcours' : parcours }

    return render(request, 'qcm/show_supportfile.html', context)



@login_required
@user_passes_test(user_is_superuser)
def create_exercise(request,supportfile_id):

    teacher = Teacher.objects.get(user_id = request.user.id)
    knowledges = Knowledge.objects.all().order_by("level")
    supportfile = Supportfile.objects.get(id=supportfile_id)

    if request.user.is_superuser :
        if request.method == "POST" :
            knowledges_id = request.POST.getlist("choice_knowledges")
            knowledges_id_tab = []
            for k_id in knowledges_id :
                knowledges_id_tab.append(int(k_id))


            # les exercices déjà référencés sur le même support par leur knowledge
            exercises = Exercise.objects.filter(supportfile = supportfile)
            exercises_Kno_tab  = []
            for exercise in exercises :
                if exercise.knowledge.id not in exercises_Kno_tab :
                    exercises_Kno_tab.append(int(exercise.knowledge.id))

            delete_list = [value for value in exercises_Kno_tab if value not in knowledges_id_tab]


            for knowledge_id in knowledges_id_tab : 
                knowledge = Knowledge.objects.get(pk = knowledge_id)
                exercise, result = Exercise.objects.get_or_create(supportfile = supportfile, knowledge = knowledge, level = knowledge.level, theme = knowledge.theme)
              
            for kn_id in delete_list :
                knowledge = Knowledge.objects.get(pk = kn_id)
                exercise = Exercise.objects.get(supportfile = supportfile, knowledge = knowledge)

                if Relationship.objects.filter(exercise = exercise).count() == 0 :
                    exercise.delete() # efface les existants sur le niveau sélectionné

 
            return redirect('admin_supportfiles')

    context = {  'teacher': teacher,   'knowledges': knowledges, 'supportfile':supportfile  }

    return render(request, 'qcm/form_exercise.html', context)




def show_exercise(request, id):
    exercise = Exercise.objects.get(id=id)

    request.session['level_id'] = exercise.level.id
    form = AuthenticationForm() 

    context = {'exercise': exercise,   'form': form  }
 
    return render(request, 'show_exercise.html', context)




def show_this_exercise(request, id):

    if request.user.user_type == 2:
        teacher = Teacher.objects.get(user = request.user)
        parcours = Parcours.objects.filter(teacher = teacher)

    else :
        student = Student.objects.get(user = request.user) 
        parcours = None

    exercise = Exercise.objects.get(id=id)
    request.session['level_id'] = exercise.level.id
    start_time =  time.time()
    context = {'exercise': exercise,  'start_time' : start_time,  'parcours' : parcours }
    return render(request, 'qcm/show_exercise.html', context)



@login_required
def execute_exercise(request, ide,idp):

    parcours = Parcours.objects.get(id= idp)
    exercise = Exercise.objects.get(id= ide)
    relation = Relationship.objects.get(parcours=parcours, exercise=exercise)
    request.session['level_id'] = exercise.level.id
    start_time =  time.time()
    context = {'exercise': exercise,  'start_time' : start_time,  'parcours' : parcours,  'relation' : relation }
    return render(request, 'qcm/show_relation.html', context)

@login_required
def store_the_score_ajax(request):
    this_time = request.POST.get("start_time").split(",")[0]
    end_time = str(time.time())
    timer = get_time(this_time,end_time)
    exercise_id = int(request.POST.get("exercise_id"))
    exercise = Exercise.objects.get(pk = exercise_id)    
    if request.POST.get("parcours_id") :
        parcours_id = int(request.POST.get("parcours_id"))
        parcours = Parcours.objects.get(pk = parcours_id)
    else :           
        parcours = None
    data = {}
    student = Student.objects.get(user=request.user)
    numexo = int(request.POST.get("numexo"))
    if request.method == 'POST':
        score = round(float(request.POST.get("score")),2)*100
        if score > 100 :
            score = 100
        if exercise.supportfile.situation <= numexo+2:
            Studentanswer.objects.create(exercise  = exercise , parcours  = parcours , student  = student , numexo= numexo,  point= score, secondes = timer)
            result, created = Resultexercise.objects.get_or_create(exercise  = exercise , student  = student , defaults = { "point" : score , })
            if not created :
                Resultexercise.objects.filter(exercise  = exercise , student  = student).update(point= score)
            # Moyenne des scores obtenus par savoir faire enregistré dans Resultknowledge
            knowledge = exercise.knowledge

            scored = 0
            studentanswers = Studentanswer.objects.filter(student = student,exercise__knowledge = knowledge) 
            for studentanswer in studentanswers:
                scored +=  studentanswer.point 
            try :
                scored = scored/len(studentanswers)
            except :
                scored = 0

            result, created = Resultknowledge.objects.get_or_create(knowledge  = exercise.knowledge , student  = student , defaults = { "point" : scored , })
            if not created :
                Resultknowledge.objects.filter(knowledge  = exercise.knowledge , student  = student).update(point= scored)

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
                result, created = Resultlastskill.objects.get_or_create(student = student, skill = skill, defaults = { "point" : sco_avg , })
                Resultlastskill.objects.filter(student = student, skill = skill).update(point = sco_avg) 

            try :
                msg = "Exercice : "+str(exercise.knowledge.name)+"\n Fait par : "+str(student.user)+"\n Nombre de situations : "+str(numexo)+"\n Score : "+str(score)+"%"+"\n Temps : "+convert_seconds_in_time(timer)+" "
                rec = []
                for g in student.students_to_group.all():
                    if not g.teacher.user.email in rec : 
                        rec.append(g.teacher.user.email)
                if g.teacher.notification :
                    send_mail("SacAdo Exercice posté",  msg , "sacado_Exo@erlm.tn" , rec )
            except:
                pass
    return JsonResponse(data)


@login_required
def store_the_score_relation_ajax(request):

    this_time = request.POST.get("start_time").split(",")[0]
    end_time  =  str(time.time()).split(".")[0]
    numexo = int(request.POST.get("numexo"))
    timer =  int(end_time) - int(this_time)
    relation_id = int(request.POST.get("relation_id"))

    relation = Relationship.objects.get(pk = relation_id)
    data = {}
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        score = round(float(request.POST.get("score")),2)*100

        if score > 100 :
            score = 100
 
        if int(relation.situation) <= int(numexo+2):
            Studentanswer.objects.create(exercise  = relation.exercise , parcours  = relation.parcours ,  student  = student , numexo= numexo,  point= score, secondes = timer)
            result, created = Resultexercise.objects.get_or_create(exercise  = relation.exercise , student  = student , defaults = { "point" : score , })
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
                result, created = Resultlastskill.objects.get_or_create(student = student, skill = skill, defaults = { "point" : sco_avg , })
                Resultlastskill.objects.filter(student = student, skill = skill).update(point = sco_avg) 

            try :
                msg = "Exercice : "+str(relation.exercise.knowledge.name)+"\n Fait par : "+str(student.user)+"\n Nombre de situations : "+str(numexo)+"\n Score : "+str(score)+"%"+"\n Temps : "+str(convert_seconds_in_time(timer))
                rec = []
                for g in student.students_to_group.all():
                    if not g.teacher.user.email in rec : 
                        rec.append(g.teacher.user.email)
 
                if g.teacher.notification :
                    send_mail("SacAdo Exercice posté",  msg , "sacado_Exo@erlm.tn" , rec )

            except:
                pass

    return JsonResponse(data)



def ajax_theme_exercice(request):
    level_id = request.POST.get('level_id', None)
    data = {}
    level = Level.objects.get(id=level_id)
    themes = level.themes.all()
    data = {'themes': serializers.serialize('json', themes)}

    return JsonResponse(data)




def ajax_level_exercise(request):

    teacher = Teacher.objects.get(user= request.user)
    data = {} 
    level_ids = request.POST.getlist('level_id')
    theme_ids = request.POST.getlist('theme_id')

    parcours_id = request.POST.get('parcours_id', None)

    if int(parcours_id) > 0:
        parcours = Parcours.objects.get(id = int(parcours_id))
        ajax = True

    else :
        parcours = None
        ajax = False

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

    data['html'] = render_to_string('qcm/ajax_list_exercises.html', { 'datas': datas , "parcours" : parcours, "ajax" : ajax, "teacher" : teacher    })
 
    return JsonResponse(data)



 

 

def ajax_knowledge_exercice(request):
    theme_id = request.POST.get('theme_id', None)
    level_id = request.POST.get('level_id', None)
    data = {}
 
    knowledges = Knowledge.objects.filter(theme_id=theme_id,level_id=level_id )
    data = {'knowledges': serializers.serialize('json', knowledges)}


    return JsonResponse(data)

 

def ajax_create_title_parcours(request):

    teacher = Teacher.objects.get(user = request.user)
    value = request.POST.get('value', None)
    parcours_id = int(request.POST.get('parcours_id', None))
    subtitle = int(request.POST.get('subtitle', None))
    code = str(uuid.uuid4())[:8]
    data = {}
    supportfile = Supportfile.objects.create(knowledge_id=1, annoncement=value, author=teacher, code=code, level_id=1, theme_id=1, is_title=1, is_subtitle=subtitle )
    exe = Exercise.objects.create(knowledge_id=1, level_id=1, theme_id=1, supportfile =supportfile )
    Relationship.objects.create(exercise=exe, parcours_id=parcours_id, order=0 )

    data["html"] = "<div style='line-height: 30px; background-color : #F2F1F0;   padding:10px; border-bottom:1px dashed #CCC;' id='new_title"+str(exe.id)+"'><a href='#' style='cursor:move;' class='move_inside'><img src='../../../static/img/move_publish.png' width='22px'  /></a><h3>"+str(value)+"</h3><input type='hidden' class='div_exercise_id' value='"+str(exe.id)+"' name='input_exercise_id'/> <a href='#' data-exercise_id='"+str(exe.id)+"'  data-parcours_id='"+str(parcours_id)+"' class='pull-right erase_title'><i class='fa fa-trash'></i></div>"

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
    exercises = Exercise.objects.filter(Q(knowledge__in = knowledges)|Q(supportfile__annoncement__contains= code)|Q(supportfile__code__contains= code)).filter(supportfile__is_title=0)
    data = {}
    html = render_to_string('qcm/search_exercises.html',{ 'exercises' : exercises  })
 
    data['html'] = html       

    return JsonResponse(data)


@login_required
@user_is_parcours_teacher
def create_evaluation(request,id, ide):

    parcours = Parcours.objects.get(id= id)
    exercise = Exercise.objects.get(id= ide)
    relationship = Relationship.objects.get(parcours  = parcours , exercise  = exercise)
    form =  RelationshipForm(request.POST or None , instance = relationship )
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            rcv = []
            for s in parcours.students.all() :
                if s.user.email:
                    rcv.append(s.user.email)

            msg = "Une évaluation est annoncée le {} à {}. Connectez vous à votre interface sacAdo le {} à {}. http://parcours.erlm.tn".format(relationship.start, relationship.beginner,relationship.start, relationship.beginner)
            send_mail("SacAdo Evaluation prévue",  msg , "SacAdo_Evaluation@erlm.tn" , rcv )
            return redirect("show_parcours" , parcours.id )
        else :
            messages.errors(request,"Erreur de création.")

    context = {'form': form,  'relationship' : relationship,  }
    return render(request, 'qcm/form_evaluation.html', context)



@login_required
def delete_evaluation(request,id):

    teacher = Teacher.objects.get(user=request.user)
    if relationship.parcours.teacher == teacher :
        relationship = Relationship.objects.get(pk=id)
        Relationship.objects.filter(pk=id).update(is_evaluation=0)
        Relationship.objects.filter(pk=id).update(situation=0)
        Relationship.objects.filter(pk=id).update(beginner=None)
        form =  RelationshipForm(request.POST or None , instance = relationship )
    return redirect("show_parcours" , relationship.parcours.id )

    
#######################################################################################################################################################################
#######################################################################################################################################################################
#################   Task
#######################################################################################################################################################################
#######################################################################################################################################################################

@login_required
@user_is_parcours_teacher 
def detail_task_parcours(request,id,s):

    teacher = Teacher.objects.get(user = request.user)   
    parcours = Parcours.objects.get(pk=id) 
    today = time_zone_user(request.user)
    date_today = time_zone_user(request.user).date() 
    if s == 0 : # groupe

        relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours =parcours,exercise__supportfile__is_title=0).exclude(date_limit=None).order_by("-date_limit")  
        context = {'relationships': relationships, 'parcours': parcours , 'today':today , 'date_today':date_today }
 
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


        context = {'details_tab': details_tab, 'parcours': parcours ,   'exercise' : exercise , 'relationship': relationship,  'date_today' : date_today}

        return render(request, 'qcm/task.html', context)


@login_required
@user_is_parcours_teacher 
def detail_task(request,id,s):

    teacher = Teacher.objects.get(user = request.user)   
    parcours = Parcours.objects.get(pk=id) 
    today = time_zone_user(request.user) 
    if s == 0 : # groupe
 
        relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours =parcours,exercise__supportfile__is_title=0).exclude(date_limit=None).order_by("-date_limit")  
        context = {'relationships': relationships, 'parcours': parcours , 'today':today }
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


        context = {'details_tab': details_tab, 'parcours': parcours ,   'exercise' : exercise , 'relationship': relationship,  'today' : today}

        return render(request, 'qcm/task.html', context)


@login_required
def all_my_tasks(request):
    today = time_zone_user(request.user) 
    teacher = Teacher.objects.get(user = request.user) 
    parcourses = Parcours.objects.filter(is_publish=  1,teacher=teacher )       
    relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__teacher=teacher, date_limit__gte=today,exercise__supportfile__is_title=0).order_by("parcours") 
    context = {'relationships': relationships, 'parcourses': parcourses,  }
    return render(request, 'qcm/all_tasks.html', context)


#######################################################################################################################################################################
#######################################################################################################################################################################
#################   Remédiation
#######################################################################################################################################################################
#######################################################################################################################################################################
@csrf_exempt 
def create_remediation(request,idr):

    relationship = Relationship.objects.get(pk=idr) 
    form = RemediationForm(request.POST or None,request.FILES or None)
 
    if form.is_valid():
        nf =  form.save(commit = False)
        nf.relationship = relationship
        nf.save()
        nf.exercises.add(exercise)
        return redirect('admin_exercises')

    context = {'form': form,  'exercise' : exercise}

    return render(request, 'qcm/form_remediation.html', context)

 



@csrf_exempt 
def update_remediation(request,idr, id):

    remediation = Remediation.objects.get(id=id)
    exercise = Exercise.objects.get(pk=ide) 
    remediation_form = remediationForm(request.POST or None, request.FILES or None, instance=remediation )
 
    if form.is_valid():
        nf.save()
        return redirect('exercises')

    context = {'form': form,  'exercise' : exercise}

    return render(request, 'qcm/form_remediation.html', context )



def delete_remediation(request, id):
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

    relationship_id =  int(request.POST.get("relationship_id"))
    relationship = Relationship.objects.get( id = relationship_id)

    form = RemediationForm(request.POST or None,request.FILES or None)
    data = {}

    remediations = Remediation.objects.filter(relationship = relationship)

    context = {'form': form,  'relationship' : relationship ,  'remediations' : remediations } 
    html = render_to_string('qcm/ajax_remediation.html',context)
    data['html'] = html       

    return JsonResponse(data)


@csrf_exempt  
def json_create_remediation(request,idr):

    relationship = Relationship.objects.get(pk=idr) 
    form = RemediationForm(request.POST or None, request.FILES or None )
 
    if form.is_valid():
        nf =  form.save(commit = False)
        nf.relationship = relationship
        nf.save()

    return redirect( 'show_parcours', relationship.parcours.id )

@csrf_exempt  
def json_delete_remediation(request, id):
    remediation = Remediation.objects.get(id=id)
    remediation.delete()

    return redirect( 'show_parcours', remediation.relationship.parcours.id )

 


@csrf_exempt 
def ajax_remediation_viewer(request): # student_view

    remediation_id =  int(request.POST.get("remediation_id"))
    remediation = Remediation.objects.get( id = remediation_id)
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
    print(code)
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

    print(relationship_id , code, score )
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
#################   exports
#######################################################################################################################################################################
#######################################################################################################################################################################





 
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
    response['Content-Disposition'] = 'attachment;' + 'filename=Notes_{}.csv'.format(parcours.title)
    writer = csv.writer(response)
    fieldnames = ("Eleves", "Compétences", "Scores")
    writer.writerow(fieldnames)
    for student in parcours.students.all() :
        full_name = str(student.user.last_name) +" "+ str(student.user.first_name)  
        try :
            resultknowledges = Resultknowledge.objects.filter(student=student, parcours=parcours).last() 
            for r in resultknowledges : 
                writer.writerow ({"Eleves": full_name, "Compétences": r.knowledge.name , "Scores": score  })
        except :
            pass
    return response

 