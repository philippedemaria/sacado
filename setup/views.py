from django.shortcuts import render,redirect
from django.contrib.auth.forms import  UserCreationForm,  AuthenticationForm
from account.forms import  UserForm, TeacherForm, StudentForm
from django.contrib.auth import   logout
from account.models import  User, Teacher, Student  ,Parent
from qcm.models import Parcours, Exercise,Relationship,Studentanswer, Supportfile, Customexercise
from group.models import Group, Sharing_group
from group.views import student_dashboard
from setup.models import Formule
from school.models import Stage
from sendmail.models import Communication
from socle.models import Level
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db.models import Count, Q
from datetime import date, datetime
from django.utils import formats, timezone
import random
import pytz
import uuid
import os
from itertools import chain
from account.decorators import is_manager_of_this_school
from general_fonctions import *
import fileinput 




def end_of_contract() :

    data = {}
    date = datetime.now()

    if date.month < 6 :
        end = date.year
    else :
        end = int(date.year) + 1
    return end
 
def index(request):

    if request.user.is_authenticated :
  
        today = time_zone_user(request.user)

        ############################################################################################
        #### Mise à jour et affichage des publications  
        ############################################################################################  
        # relationships = Relationship.objects.filter(is_publish = 0,start__lte=today)
        # for r in relationships :
        #     Relationship.objects.filter(id=r.id).update(is_publish = 1)

        # parcourses = Parcours.objects.filter(start__lte=today).exclude(start = None)
        # for p in parcourses :
        #     Parcours.objects.filter(id=p.id).update(is_publish = 1)

        # customexercises = Customexercise.objects.filter(start__lte=today).exclude(start = None)
        # for c in customexercises :
        #     Customexercise.objects.filter(id=c.id).update(is_publish = 1)
        ############################################################################################
        #### Fin de Mise à jour et affichage des publications
        ############################################################################################
        timer = today.time()

        if request.user.last_login.date() != today.date() :
            request.user.last_login = today
            request.user.save()

        if request.user.is_teacher:

            if request.user.is_manager and request.user.school :
                request.session["school_id"] = request.user.school.id 

            teacher = Teacher.objects.get(user=request.user)

            grps = Group.objects.filter(teacher=teacher)
            shared_grps_id = Sharing_group.objects.filter(teacher=teacher).values_list("group_id", flat=True)
            sgps = []
            for sg_id in shared_grps_id :
                grp = Group.objects.get(pk=sg_id)
                sgps.append(grp)

            groups = chain(grps, sgps)

            this_user = request.user
            nb_teacher_level = teacher.levels.count()

            relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__teacher=teacher, date_limit__gte=today).order_by("date_limit").order_by("parcours")
            
            parcourses = teacher.teacher_parcours.filter(is_evaluation=0, is_favorite =1).order_by("-is_publish")

            communications = Communication.objects.values('id', 'subject', 'texte').filter(active=1).order_by("-id")

            parcours_tab = Parcours.objects.filter(students=None, teacher=teacher, is_favorite=1) ## Parcours favoris non affectés

            template = 'dashboard.html'
            context = {'this_user': this_user, 'teacher': teacher, 'groups': groups, 'parcourses': parcourses, 'parcours': None, 'today' : today , 'timer' : timer , 
                       'relationships': relationships, 'communications': communications, 'parcours_tab': parcours_tab,
                       'nb_teacher_level': nb_teacher_level}
        
        elif request.user.is_student: ## student

 
            #return redirect("dashboard_group", 0)
            context = student_dashboard(request, 0)[1]
            template = student_dashboard(request, 0)[0] 


        elif request.user.is_parent:  ## parent
            parent = Parent.objects.get(user=request.user)
            students = parent.students.order_by("user__first_name")
            context = {'parent': parent, 'students': students, 'today' : today ,  }
            template = 'dashboard.html'

        return render(request, template , context)


    else:  ## Anonymous
        form = AuthenticationForm()
        u_form = UserForm()
        t_form = TeacherForm()
        s_form = StudentForm()
        levels = Level.objects.all()
        try:
            cookie = request.session.get("cookie")
        except:
            pass

        exercise_nb = Exercise.objects.filter(supportfile__is_title=0).count()
        exercises = Exercise.objects.filter(supportfile__is_title=0)

        i = random.randint(1, len(exercises))
        exercise = exercises[i]

        context = {'form': form, 'u_form': u_form, 't_form': t_form, 's_form': s_form, 'levels': levels, 
                   'cookie': cookie, 'nb_exercise': exercise_nb, 'exercise': exercise, }



        return render(request, 'home.html', context)


def logout_view(request):
    try:
        connexion = Connexion.objects.get(user=user)
        connexion.delete()
    except:
        pass

    form = AuthenticationForm()
    u_form = UserForm()
    t_form = TeacherForm()
    s_form = StudentForm()
    logout(request)
    levels = Level.objects.all()
    context = {'form': form, 'u_form': u_form, 't_form': t_form, 's_form': s_form, 'levels': levels, 'cookie': False}
    return render(request, 'home.html', context)


def send_message(request):

    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    message = request.POST.get("message")
    token = request.POST.get("token")

    if message:
        send_mail(subject,
                  "Bonjour, vous venez d'envoyer le message suivant :\n\n" + message + " \n\n Ceci est un mail automatique. Ne pas répondre.",
                  'sacado.sas@gmail.com',
                  [email])
        send_mail(subject,
                  message,
                  email,
                  ["philippe.demaria-lgf@erlm.tn", "brunoserres33@gmail.com", "sacado.asso@gmail.com"])
    return redirect("index")


def inscription(request):
    context = {}
    return render(request, 'setup/register.html', context)


def test_display(request):
    context = {}
    return render(request, 'setup/test_display.html', context)


def student_to_association(request):

    frml = Formule.objects.get(pk=1)
    formule = Formule.objects.get(pk=4)
    context = { 'frml' : frml , 'formule' : formule }
    return render(request, 'setup/student_association.html', context)


def choice_menu(request,name):
    formules = Formule.objects.filter(name=name)
    end  = end_of_contract()
    context = { 'formules' : formules , 'end' : end , 'name' : name  }
    return render(request, 'setup/menu.html', context)   



##############################################  AJAX ############################################################




def ajax_changecoloraccount(request):
    """
    Appel Ajax pour afficher la liste des élèves du groupe sélectionné
    """
    if request.user.is_authenticated:
        code = request.POST.get('code')

    color = request.user.color
    filename1 = "static/css/navbar-fixed-left.min.css"
    filename2 = "static/css/AdminLTEperso.css"

    User.objects.filter(pk=request.user.id).update(color=code)

    change_color(filename1, color, code)
    change_color(filename2, color, code)

    return redirect("index")


def change_color(filename, color, code):
    # Read in the file
    with open(filename, 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace(color, code)
    # Write the file out again
    with open(filename, 'w') as file:
        file.write(filedata)


@is_manager_of_this_school
def admin_tdb(request):
    school = request.user.school
    nb_teachers = User.objects.filter(school=school, user_type=2).count()
    nb_students = User.objects.filter(school=school, user_type=0).count()
    nb_groups = Group.objects.filter(teacher__user__school=school).count()

    try:
        stage = Stage.objects.get(school=school)
        if stage:
            eca, ac, dep = stage.medium - stage.low, stage.up - stage.medium, 100 - stage.up
        else:
            eca, ac, dep = 20, 15, 15

    except:
        stage = {"low": 50, "medium": 70, "up": 85}
        eca, ac, dep = 20, 15, 15

    return render(request, 'dashboard_admin.html', {'nb_teachers': nb_teachers, 'nb_students': nb_students,
                                                    'nb_groups': nb_groups, 'school': school, 'stage': stage,
                                                    'eca': eca, 'ac': ac, 'dep': dep , 'communications' : [],
                                                    })


def gestion_files(request):
    levels = Level.objects.all()
    if request.method == "POST":

        level_id = request.POST.get("level")
        level = Level.objects.get(pk=level_id)
        supportfiles = Supportfile.objects.filter(level_id=level_id, is_title=0)
    else:
        level, level_id = None, 0
        supportfiles = []

    context = {'levels': levels, 'level': level, 'level_id': level_id, 'level_id': level_id,
               'supportfiles': supportfiles}

    return render(request, 'setup/gestion_files.html', context )


def get_cookie(request):
    request.session["cookie"] = "accept"
    return redirect('index')


 