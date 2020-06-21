from django.shortcuts import render,redirect
from django.contrib.auth.forms import  UserCreationForm,  AuthenticationForm
from account.forms import  UserForm, TeacherForm, StudentForm
from django.contrib.auth import   logout
from account.models import  User, Teacher, Student  ,Parent
from qcm.models import Parcours, Exercise,Relationship,Studentanswer
from group.models import Group
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



def index(request):

    if request.user.is_authenticated:
        if request.user.time_zone:
            time_zome = request.user.time_zone
            timezone.activate(pytz.timezone(time_zome))
            current_tz = timezone.get_current_timezone()
            today = timezone.localtime(timezone.now())
        else:
            today = timezone.now()

        if request.user.last_login.date() != today.date() :
            request.user.last_login = today
            request.user.save()

        if request.user.user_type == User.TEACHER:

            if request.user.is_manager and request.user.school :
                request.session["school_id"] = request.user.school.id 

            teacher = Teacher.objects.get(user=request.user)
            groups = Group.objects.filter(teacher=teacher)
            this_user = request.user
            nb_teacher_level = teacher.levels.count()

            relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__teacher=teacher, date_limit__gte=today).order_by("date_limit").order_by("parcours")
            
            parcourses = teacher.teacher_parcours.order_by("-is_publish")

            communications = Communication.objects.values('id', 'subject', 'texte').filter(active=1)

            parcours_tab = Parcours.objects.filter(students=None, teacher=teacher, is_favorite=1) ## Parcours favoris non affectés

            context = {'this_user': this_user, 'teacher': teacher, 'groups': groups, 'parcourses': parcourses,
                       'relationships': relationships, 'communications': communications, 'parcours_tab': parcours_tab,
                       'nb_teacher_level': nb_teacher_level}


        elif request.user.user_type == User.STUDENT: ## student
            student = Student.objects.get(user=request.user.id)
            parcourses = Parcours.objects.filter(students=student, is_evaluation=0, is_publish=1)

            parcours = []

            for p in parcourses:
                parcours.append(p)

            relationships = Relationship.objects.filter(Q(is_publish=1) | Q(start__lte=today), parcours__in=parcours, date_limit__gte=today).order_by("date_limit")

            exercise_tab = []
            for r in relationships:
                if r not in exercise_tab:
                    exercise_tab.append(r.exercise)
            num = 0
            for e in exercise_tab:
                if Studentanswer.objects.filter(student=student, exercise=e).count() > 0:
                    num += 1

            nb_relationships = Relationship.objects.filter(Q(is_publish=1) | Q(start__lte=today), parcours__in=parcours, date_limit__gte=today).count()
            try:
                ratio = int(num / nb_relationships * 100)
            except:
                ratio = 0

            ratiowidth = int(0.9*ratio)

            timer = timezone.now().time()

            evaluations = Parcours.objects.filter(start__lte=today, stop__gte=today, students=student, is_evaluation=1)

            exercises = []
            studentanswers = Studentanswer.objects.filter(student = student)
            for studentanswer in studentanswers:
                if not studentanswer.exercise in exercises:
                    exercises.append(studentanswer.exercise)

            relationships_in_late = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__in=parcours, is_evaluation=0, date_limit__lt=today).exclude(exercise__in=exercises).order_by("date_limit")
            relationships_in_tasks = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__in=parcours, date_limit__gte=today).exclude(exercise__in=exercises).order_by("date_limit")

            context = {'student_id': student.user.id, 'student': student, 'relationships': relationships,
                       'evaluations': evaluations, 'ratio': ratio,
                       'ratiowidth': ratiowidth, 'relationships_in_late': relationships_in_late,
                       'relationships_in_tasks': relationships_in_tasks}

        elif request.user.user_type == User.PARENT:  ## parent
            parent = Parent.objects.get(user=request.user)
            students = parent.students.order_by("user__first_name")
            context = {'parent': parent, 'students': students, }

        return render(request, 'dashboard.html', context)


    else:  ## Anonymous
        form = AuthenticationForm()
        u_form = UserForm()
        t_form = TeacherForm()
        s_form = StudentForm()
        levels = Level.objects.all()

        exercise_nb = Exercise.objects.filter(supportfile__is_title=0).count()
        exercises = Exercise.objects.filter(supportfile__is_title=0)

        i = random.randint(1, len(exercises))
        exercise = exercises[i]

        context = {'form': form, 'u_form': u_form, 't_form': t_form, 's_form': s_form, 'levels': levels,
                   'exercise_nb': exercise_nb, 'exercise': exercise, }



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
    context = {'form': form, 'u_form': u_form, 't_form': t_form, 's_form': s_form, 'levels': levels, }
    return render(request, 'home.html', context)




def send_message(request):

    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    message = request.POST.get("message")
    token = request.POST.get("token")

    if message :
        send_mail(subject, "Bonjour, vous venez d'envoyer le message suivant :\n\n"+message+" \n\n Ceci est un mail automatique. Ne pas répondre.", 'sacado.sas@gmail.com', [email])
        send_mail(subject,  message , email , ["philippe.demaria-lgf@erlm.tn","brunoserres33@gmail.com","sacado.sas@gmail.com"])
    return redirect("index")



def inscription(request):

    context =  {  }
    return render(request, 'setup/register.html', context )




def test_display(request):

    context =  {  }
    return render(request, 'setup/test_display.html', context )



##############################################  AJAX ############################################################
import fileinput



def ajax_changecoloraccount(request):
    """
    Appel Ajax pour afficher la liste des élèves du groupe sélectionné
    """
    if request.user.is_authenticated:
        code = request.POST.get('code')

    color  = request.user.color
    filename1 = "static/css/navbar-fixed-left.min.css"
    filename2 = "static/css/AdminLTEperso.css"

    User.objects.filter(pk=request.user.id).update(color=code)

    change_color(filename1,color,code)
    change_color(filename2,color,code)

    return redirect("index")



def change_color(filename,color,code):
        # Read in the file
    with open(filename, 'r') as file :
      filedata = file.read()
    # Replace the target string
    filedata = filedata.replace(color,code)
    # Write the file out again
    with open(filename, 'w') as file:
        file.write(filedata)


 




def  admin_tdb(request):

    school = request.user.school   
    nb_teachers = User.objects.filter(school = school, user_type=2).count()  
    nb_students = User.objects.filter(school = school, user_type=0).count()    
    nb_groups = Group.objects.filter(teacher__user__school = school).count()  
 
    
    try :
        stage = Stage.objects.get(school= school)
        if stage :
            eca, ac , dep = stage.medium - stage.low ,  stage.up - stage.medium ,  100 - stage.up
        else :
            eca, ac , dep = 20 , 15 ,  15           

    except : 
        stage = { "low" : 50 ,  "medium" : 70 ,  "up" : 85  }
        eca, ac , dep = 20 , 15 ,  15

    return render(request, 'dashboard_admin.html', {'nb_teachers': nb_teachers , 'nb_students': nb_students , 
                                                    'nb_groups': nb_groups, 'school': school, 'stage': stage,  
                                                     'eca' : eca, 'ac' : ac , 'dep' : dep
                                                     })

