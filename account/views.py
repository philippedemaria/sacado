
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, REDIRECT_FIELD_NAME, authenticate
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from .forms import   UserForm, UserUpdateForm, StudentForm, TeacherForm, ParentForm
from account.models import User, Teacher, Student, Resultknowledge, Parent
from group.models import Group
import uuid  
from django.views.decorators.csrf import csrf_exempt
from socle.models import Theme, Knowledge
from sendmail.models import Communication
from qcm.models import Exercise, Studentanswer, Parcours, Relationship, Resultexercise, Studentanswer
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.http import JsonResponse
from socle.models import Level
from django.core import serializers
from django.core.exceptions import ValidationError

from account.decorators import user_can_read_details, who_can_read_details
import csv
from statistics import median, StatisticsError
from datetime import date, datetime
from django.apps import apps
from django.db.models import Count, Q, Avg, Sum
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required 
from django.utils import formats, timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
import pytz
import re
import html
 

def time_zone_user(user):
    if user.time_zone :
        time_zome = user.time_zone
        timezone.activate(pytz.timezone(time_zome))
        current_tz = timezone.get_current_timezone()
        today = timezone.localtime(timezone.now())
        
    else :
        today = timezone.now()
    return today
 

def list_teacher(request):
    teachers = User.objects.filter(user_type = 2)
    return render(request, 'account/list_teacher.html', {'teachers': teachers})


def navigation(group,id):  
 
    students_ids = group.students.values_list('user__id',flat=True).order_by("user__last_name") 
    index = list(students_ids).index(id)

    if len(students_ids) > 1 :
        if index == 0 :
            sprev_id = False
            snext_id = students_ids[1]
        elif index == len(students_ids)-1 :
            sprev_id = students_ids[index-1]
            snext_id = False
        else :
            sprev_id = students_ids[index-1]
            snext_id = students_ids[index+1]
    else :
        sprev_id = False
        snext_id = False
 

    return(sprev_id,snext_id)


def cleanhtml(raw_html): #nettoie le code des balises HTML
    cleantext = re.sub('<.*?>', '', raw_html)
    cleantext = re.sub('\n', '', cleantext)
    return cleantext


def unescape_html(string):
        '''HTML entity decode'''
        string = html.unescape(string)
        return string 


class DashboardView(TemplateView): # lorsque l'utilisateur vient de se connecter.
    template_name = "dashboard.html"

    # Lors de la connexion, analyse les exercices de tous les parcours qui doivent être visible à partir de cette date

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        this_user = User.objects.get(pk=self.request.user.id)
        
        today = time_zone_user(this_user)
        relationships = Relationship.objects.filter(is_publish = 0,start__lte=today)
        for r in relationships :
            Relationship.objects.filter(id=r.id).update(is_publish = 1) 

        if self.request.user.is_authenticated  : 
            if self.request.user.user_type == 2 : # Teacher
                teacher = Teacher.objects.get(user=self.request.user.id)
                groups = Group.objects.filter(teacher = teacher)
 
                relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__teacher=teacher, date_limit__gte=today).order_by("parcours") 
                parcourses = Parcours.objects.filter(teacher = teacher,linked=0) # parcours non liés à un groupe

                communications = Communication.objects.filter(active = 1)

                parcours_tab = Parcours.objects.filter(students=None,teacher = teacher)




                context = {  'this_user' : this_user , 'teacher' : teacher , 'relationships' : relationships ,  'parcourses' : parcourses ,   'groups' : groups ,  'parcours_tab' : parcours_tab ,     'communications' : communications ,    }


            elif self.request.user.user_type == 0 :  # Student
                student = Student.objects.get(user= self.request.user.id)

                parcourses = Parcours.objects.filter(students = student,linked=0, is_evaluation = 0, is_publish = 1)
                groups = student.students_to_group.all()


                parcours = []
                for p in parcourses :
                    parcours.append(p)
                for g in groups :
                    parcours.append(g.parcours)

   
 
                relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__in=parcours, is_evaluation=0, date_limit__gte=today).order_by("date_limit")
                exercise_tab = []
                for r in relationships:
                    if r not in exercise_tab:
                        exercise_tab.append(r.exercise)

                num = 0
                for e in exercise_tab :
                    if Studentanswer.objects.filter(student=student, exercise = e).count() > 0 :
                        num += 1

                nb_relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__in=parcours, date_limit__gte=today).count()
                try :
                    ratio = int(num/nb_relationships*100)
                except :
                    ratio = 0

                ratiowidth = int(0.9*ratio)
                timer = timezone.now().time()

                evaluations = Parcours.objects.filter(start__lte=today,stop__gte=today, students = student, is_evaluation=1)
                studentanswers = Studentanswer.objects.filter(student = student)


                exercises = []
                for studentanswer in studentanswers:
                    if not studentanswer.exercise in exercises:
                        exercises.append(studentanswer.exercise)

                relationships_in_late = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__in=parcours, is_evaluation=0, date_limit__lt=today).exclude(exercise__in=exercises).order_by("date_limit")

 
                context = {   'student_id' : student.user.id,  'student' : student, 'relationships' : relationships , 'ratio' : ratio ,  'evaluations' : evaluations ,  'ratiowidth' : ratiowidth , 'relationships_in_late' : relationships_in_late }
            
            elif self.request.user.user_type == 1 :  # Parent

                parent = Parent.objects.get(user= self.request.user)
                students = parent.students.order_by("user__first_name")
                context = {    'parent' : parent , 'students' : students, }

        else: ## Anonymous

            form = AuthenticationForm()  
            u_form = UserForm()
            t_form = TeacherForm() 
            s_form = StudentForm() 
            levels = Level.objects.all()
            exercise_nb = Exercise.objects.filter(is_title=0).count()

            exercises = Exercise.objects.filter(is_title=0)
            
            i = random.randint(1,len(exercises))
            exercise = exercises[i]

            context =  { 'form' : form , 'u_form' : u_form , 't_form' : t_form , 's_form' : s_form ,  'levels' : levels , 'exercise_nb' : exercise_nb , 'exercise' : exercise , }
 
        return context




########################################            MON COMPTE               #########################################

def myaccount(request):
 
    if request.user.user_type == User.TEACHER:
        teacher = Teacher.objects.get(user_id=request.session.get('user_id'))
        context = {'teacher': teacher, }
        return render(request, 'account/teacher_account.html', context)
    else:
        student = Student.objects.get(user_id=request.session.get('user_id'))
        context = {'student': student, }

        return render(request, 'account/student_account.html', context)

#####################################


 
def send_to_teachers(request):
    users = User.objects.filter(user_type=2)
    context = {"users" : users, }
    return render(request,'account/send_message_to_teachers.html', context)



@login_required
def message_to_teachers_sent(request):

    subject = request.POST.get("subject") 
    message = request.POST.get("message")  
    users = request.POST.getlist("users")  

    rcv = []
    for u_id in users :
        u = User.objects.get(pk=u_id)
        if u.email:
            rcv.append(u.email)

    send_mail(subject, cleanhtml(unescape_html(message)) , 'sacado.sas@gmail.com', rcv )
    messages.success(request,'message envoyé')

    return redirect("dashboard")  


#########################################Student #####################################################################


def register_student(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            username  = user_form.cleaned_data['last_name']+user_form.cleaned_data['first_name']
            user = user_form.save(commit=False)
            user.username  = username
            user.user_type = 0
            password = request.POST.get("password1")                     
            print("req : ", request.POST.get("choose_alone"))
            ######################### Choix du groupe  ###########################################
            if request.POST.get("choose_alone") : # groupe sans prof
                print("choose_alone")
                # l'élève rejoint le groupe par défaut sur le niveau choisi
                teacher = Teacher.objects.get(user_id = 2)#2480
                group = Group.objects.get(teacher = teacher, level_id = int(request.POST.get("level_selector")))
                parcours = Parcours.objects.filter(teacher=teacher, level = group.level)

            else :     # groupe du prof  de l'élève        
                print("code_group")
                code_group = request.POST.get("group")  
                if Group.objects.filter(code = code_group).exists() :
                    group = Group.objects.get(code = code_group)
                    parcours = Parcours.objects.filter(teacher=group.teacher, level = group.level)
            #######################################################################################      
            user.save()
            student = Student.objects.create(user=user,level=group.level) 
            group.students.add(student)
            
            for p in parcours :
                p.students.add(student)
                relationships = p.parcours_relationship.all()
                for r in relationships :
                    r.students.add(student)
                    
            user = authenticate(username=username, password = password)
            login(request, user)
            messages.success(request, "Inscription réalisée avec succès !")               
            if user_form.cleaned_data['email'] : 
               send_mail('Création de compte sur Sacado', 'Bonjour, votre compte SacAdo est maintenant disponible. \n\n Votre identifiant est '+str(username) +". \n votre mot de passe est "+str(password)+'.\n\n Pour vous connecter, redirigez-vous vers http://parcours.erlm.tn.\n Ceci est un mail automatique. Ne pas répondre.', 'SacAdo_contact@erlm.tn', [request.POST.get("email")])
        
        else :
            messages.error(request, "Erreur lors de l'enregistrement. Reprendre l'inscription...")
    return redirect('index')


 



def update_student(request, pk):
    user = get_object_or_404(User, pk=pk)
    student = get_object_or_404(Student, pk=pk)
    user_form = UserUpdateForm(request.POST or None, instance=user)
    student_form = StudentUpdateForm(request.POST or None, instance=student)
    if all((user_form.is_valid(), student_form.is_valid())):
        user_form.save()
        student_f = student_form.save(commit=False)
        student_f.user = user
        student_f.save()
        parcours = Parcours.objects.get(id=student_f.level.id)
        parcours.students.add(student_f)
        return redirect('students')

    return render(request, 'account/student_form.html',
                  {'user_form': user_form, 'student_form': student_form, 'student': student})



@csrf_exempt
def update_student_by_ajax(request):

    student_id =  int(request.POST.get("student_id"))
    is_name = int(request.POST.get("is_name"))
    value= request.POST.get("value")
    if is_name== 0 :
        User.objects.filter(id=int(student_id)).update(first_name = value)
    elif is_name== 1 :
        User.objects.filter(id=int(student_id)).update(last_name = value) 
    elif is_name== 2 :
        User.objects.filter(id=int(student_id)).update(email = value)
    else :
        User.objects.filter(id=int(student_id)).update(username = value) 

    data = {}
    data['html'] = value
 
    return JsonResponse(data)



def delete_student(request, id,idg):

    student = get_object_or_404(Student, user_id=id)
    results = Resultknowledge.objects.filter(student=student)
    for r in results :
        r.delete()

    res = Resultexercise.objects.filter(student=student)
    for re in res :
        re.delete()
        
    ress = Studentanswer.objects.filter(student=student)
    for rs in ress :
        rs.delete()

    student.user.delete()
    return redirect('update_group', idg )


def newpassword_student(request, id,idg):

    student = get_object_or_404(Student, user_id=id)
    user = student.user
    user.set_password("sacado2020")
    user.save()  
    send_mail('Réinitialisation de mot de passe Sacado', "Bonjour, votre mot de passe est réinitialisé. Il est générique. Votre mot de passe est : sacado2020.\n\n  Pour plus de sécurité, vous devez le modifier dès votre connexion.\n\n Pour vous connecter, redirigez-vous vers http://parcours.erlm.tn.\n Ceci est un mail automatique. Ne pas répondre.", 'SacAdo_contact@erlm.tn', [user.email])
    return redirect('update_group', idg )


 




def knowledges_of_a_student(student,theme):

    exercise_tab = [] 

    parcourses = student.students_to_parcours.all() 


    for parcours in parcourses :
        exercises = parcours.exercises.filter( theme = theme)
        for exercise in exercises:
            if not exercise in exercise_tab :
                exercise_tab.append(exercise)
    
    knowledges = []
    for exercise in exercise_tab :
        if not exercise.knowledge in knowledges:
            knowledges.append(exercise.knowledge)

    return knowledges 




@login_required
@who_can_read_details
def detail_student(request, id):

    student = Student.objects.get(user_id=id)
 
    parcourses_publish = Parcours.objects.filter(students=student,is_publish=1)
    parcourses = Parcours.objects.filter(students=student)
    
    datas =[]
    themes = student.level.themes.all() # Tous les thèmes du niveau de l'élève
    for t in themes :
        theme={}
        theme["name"]= t
        relationships = Relationship.objects.filter( students=student,  exercise__theme = t,exercise__supportfile__is_title=0).order_by("exercise__knowledge") # Tous les exercices du niveau de l'élève, classé par thème
 
        exercises_tab = [] 
        for r in relationships :
            exo = {}
            exo["name"] = r.exercise
            exo["is_publish"] = r.is_publish
            stas = Studentanswer.objects.filter( exercise = r.exercise , student= student ).order_by("date")
            scores_tab = []
            for sta in stas :
                scores_tab.append(sta) 
            exo["scores"] = scores_tab         
            exercises_tab.append(exo) 
        theme["exercises"]  = exercises_tab

        datas.append(theme)

    if request.user.user_type == 2 :
        teacher = Teacher.objects.get(user=request.user)
        group = Group.objects.get(students = student, teacher = teacher)
        nav = navigation(group,id)
        context = { 'datas': datas,  'parcourses':parcourses, 'group':group,  'sprev_id' :  nav[0]  ,'snext_id' : nav[1]  ,   'themes':themes,   'student': student}
    else :
        group = Group.objects.filter(students = student).first()
        context = { 'datas': datas,  'parcourses':parcourses, 'group':group,     'themes':themes,   'student': student}

    return render(request, 'account/detail_student.html', context)


@login_required
@who_can_read_details
def detail_student_theme(request, id,idt):

    student = Student.objects.get(user_id=id)
    parcourses = Parcours.objects.filter(students = student)
    parcourses_publish = Parcours.objects.filter(students = student,is_publish=1)

    theme = Theme.objects.get(pk=idt)

    themes = student.level.themes.all()
    datas =[]

    knowledges = knowledges_of_a_student(student, theme)

    for k in knowledges:
        knowledge_dict={}
        if Relationship.objects.filter(parcours__in = parcourses, exercise__knowledge = k, students= student).count() > 1 : 
            knowledge_dict["name"]= k
            # liste des exercices du parcours qui correspondent aux savoir faire k mais un même exercice peut être donné sur deux parcours 
            # différents donc deux relationships pour un même exercice
            relationships = Relationship.objects.filter(parcours__in = parcourses, exercise__knowledge = k, students= student)
            # merge les relationships identiques
            relations_tab , relations_tab_code = [], []
            for rel in relationships :
                if rel.exercise.supportfile.code not in relations_tab_code:
                    relations_tab_code.append(rel.exercise.supportfile.code)
                    relations_tab.append(rel)
            # merge les relationships identiques
            exercises_tab = []
            for relation in relations_tab :
                exo = {}
                exo["name"] = relation
                stas = Studentanswer.objects.filter( exercise= relation.exercise , student = student ).order_by("date")
                scores_tab = []
                for sta in stas :
                    scores_tab.append(sta) 
                exo["scores"] = scores_tab         
                exercises_tab.append(exo) 
            knowledge_dict["exercises"]  = exercises_tab
            datas.append(knowledge_dict)


 
    if request.user.user_type == 2 :
        teacher = Teacher.objects.get(user=request.user)
        group = Group.objects.get(students = student, teacher = teacher)
        nav = navigation(group,id)
        context = { 'datas': datas,  'student': student , 'theme' : theme,  'group' : group ,  'sprev_id' :  nav[0]  ,'snext_id' : nav[1]  ,   'parcourses':parcourses, 'themes' : themes }
    
    else :
        group = Group.objects.filter(students = student).first() 
        context = { 'datas': datas,  'student': student , 'theme' : theme,  'group' : group ,   'parcourses':parcourses, 'themes' : themes }
    return render(request, 'account/detail_student_theme.html',  context )




@login_required
@who_can_read_details
def detail_student_parcours(request, id,idp):

    student = Student.objects.get(user_id=id)
    parcours = Parcours.objects.get(pk=idp)
    parcourses = Parcours.objects.filter(students = student)  
    themes = student.level.themes.all()



    relationships = Relationship.objects.filter(parcours = parcours, students = student, is_publish = 1).order_by("order")

 
    if request.user.user_type == 2 :
        teacher = Teacher.objects.get(user=request.user)
        group = Group.objects.get(students = student, teacher = teacher)
        nav = navigation(group,id)
        context = {  'relationships':relationships, 'parcours': parcours ,  'themes' : themes ,   'sprev_id' :  nav[0]  ,'snext_id' : nav[1]  ,  'parcourses':parcourses,   'student': student}
    else :
        context = {  'relationships':relationships, 'parcours': parcours ,  'themes' : themes ,  'parcourses':parcourses,   'student': student}

    return render(request, 'account/detail_student_parcours.html', context)





@login_required
@user_can_read_details
def detail_student_all_views(request, id):

    user = User.objects.get(pk=id)
    student = Student.objects.get(user=user)
    studentanswers = student.answers.all()
    themes = student.level.themes.all()


    parcourses_tab = []
    parcourses_student_tab, exercise_tab = [] ,  []
    parcourses = student.students_to_parcours.all()

    parcourses_student_tab.append(parcourses)
    for parcours in parcourses :
        if not parcours in parcourses_tab :
            parcourses_tab.append(parcours)

    for parcours in parcourses_tab :
        exercises = parcours.exercises.order_by("theme").prefetch_related('knowledge')
        for exercise in exercises:
            if not exercise in exercise_tab :
                exercise_tab.append(exercise)
    
    knowledges = []

    for exercise in exercise_tab :
        if not exercise.knowledge in knowledges:
            knowledges.append(exercise.knowledge)




    parcourses = Parcours.objects.filter(students=student)
    relationships = Relationship.objects.filter(parcours__in = parcourses).exclude(date_limit=None)
 
    done, late, no_done = 0 , 0 , 0 
    for relationship in relationships :
        nb_ontime = Studentanswer.objects.filter(student=student, exercise = relationship.exercise ).count()
        nb = Studentanswer.objects.filter(student=student, exercise = relationship.exercise, date__lte= relationship.date_limit ).count()
        if nb_ontime == 0:
            no_done += 1
        elif nb > 0:
            done += 1
        else:
            late += 1

    std = {
        "nb": no_done + done + late,
        "no_done": no_done,
        "done": done,
        "late": late,
        "nb_exo": studentanswers.count(),
    }

    std.update(studentanswers.aggregate(duration=Sum('secondes'), average_score=Avg('point')))

    if std['duration'] is None:
        std['duration'] = 0
    else:
        std['duration'] = int(std['duration'])

    if std['average_score'] is None:
        std['average_score'] = 0
    else:
        std['average_score'] = int(std['average_score'])

    try:
        std['median'] = int(median(studentanswers.values_list('point', flat=True)))
    except StatisticsError:
        std['median'] = 0


    # import pdb; pdb.set_trace()
    if request.user.user_type == 2:
        teacher = Teacher.objects.get(user=request.user)
        group = Group.objects.get(students=student, teacher=teacher)
        nav = navigation(group, id)
        context = {'knowledges': knowledges, 'parcourses': parcourses, 'std': std, 'themes': themes, 'student': student,
                   'sprev_id': nav[0], 'snext_id': nav[1]}
    else:
        context = {'knowledges': knowledges, 'parcourses': parcourses, 'std': std, 'themes': themes, 'student': student}

    return render(request, 'account/detail_student_all_views.html', context)





 






##############################################################################################################
##
##    Close an account
##
############################################################################################################## 
@login_required
def close_an_account(request):

    user = request.user

    return render(request, 'account/close_my_account.html', {  'user':user,})


@login_required
def close_my_account(request, id):

    user = get_object_or_404(User, user_id=id)
    user.delete()
    return redirect('index')


#########################################Teacher #####################################################################

def register_teacher(request):
 

    if request.method == 'POST':
 
        user_form = UserForm(request.POST)
        if user_form.is_valid():
 
            user = user_form.save(commit=False)
            user.is_staff = 1
            user.user_type=2
            user.set_password(user_form.cleaned_data["password1"])
            user.save()
            username  = user_form.cleaned_data['username']
            password  = user_form.cleaned_data['password1']
            user = authenticate(username=username, password = password)
            login(request, user)
            Teacher.objects.create(user=user)



            if user_form.cleaned_data['email'] :
                send_mail('Création de compte sur Sacado', 'Bonjour, votre compte Sacado est maintenant disponible. \n\n Votre identifiant est '+str(request.POST.get("username")) +".\n Votre mot de passe est "+ str(password)+ ".\n\n  Pour vous connecter, redirigez-vous vers http://parcours.erlm.tn.\n Ceci est un mail automatique. Ne pas répondre.", 'SacAdo_contact@erlm.tn', [request.POST.get("email")])
            
            users = User.objects.filter(is_superuser=1)
            receivers =[]
            for u in users :
                receivers.append(u.email)            

            send_mail("SacAdo", "Un enseignant - "+str(user_form.cleaned_data['last_name'])+" "+str(user_form.cleaned_data['first_name'])+" - vient de s'inscrire sur SacAdo.", "SacAdo",  receivers ) 
        else :
            messages.error(request, user_form.errors)

    return redirect("index")


@login_required 
def update_teacher(request, pk):
    user = get_object_or_404(User, pk=pk)
    teacher = get_object_or_404(Teacher, user=user)
    user_form = UserUpdateForm(request.POST or None, instance=user)
    teacher_form = TeacherForm(request.POST or None, instance=teacher)
    if all((user_form.is_valid(), teacher_form.is_valid())):
        user_form.save()
        teacher_form.save()

        messages.success(request, "Actualisation réussie !")
        return redirect('login')

        

    return render(request, 'account/teacher_form.html',
                  {'user_form': user_form,
                   'teacher_form': teacher_form,
                   'teacher': teacher})


@login_required
def delete_teacher(request, pk):
    if request.POST:
        teacher = get_object_or_404(Teacher, user_id=pk)
        teacher.user.delete()
    return redirect('login')

 
#########################################Lost password #####################################################################
import random
def lost_password(request):
    this_email = request.POST.get("email")
    print(this_email)

    caracteres = "azertyuiopqsdfghjklmwxcvbn@@@_____AZERTYUIOPQSDFGHJKLMWXCVBN0123456789@-_"
    lenght = len(caracteres)-1
    longueur = 8 
    password = "" 
    compteur = 0 
     
    while compteur < longueur:
        lettre = caracteres[random.randint(0,lenght)]  
        password += lettre  
        compteur += 1 

    try :
        emails = []
        users = User.objects.filter(email=this_email)
        for u in users :
            user_password = make_password(password)
            u.password = user_password
            u.save()
            if u.email not in emails :
                emails.append(u.email)
            
        messages.success(request, 'Votre mot de passe a été changé avec succès !')       
        send_mail('Récupération du mot de passe sur sacado', 'Bonjour, \n\n votre identifiant est '+str(u.username)+' \n votre mot de passe sacado est '+str(password)+'.\n\n Vous pourrez le mdifier une fois connecté. Pour vous connecter, redirigez-vous vers http://parcours.erlm.tn .', 'SacAdo_contact@erlm.tn', emails )


    except : 
        messages.error(request, "Votre mot de passe n'a pas été changé. Vérifier votre adresse de courriel !")

    return redirect('index')


import random
def updatepassword(request):
 
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            userport = form.save()
            update_session_auth_hash(request, userport) # Important!
            messages.success(request, 'Votre mot de passe a été modifié avec succès !')
            send_mail('Changement de mot de passe sur sacAdo', 'Bonjour, votre nouveau mot de passe sacAdo est '+str(request.POST.get("new_password1"))+'. Pour vous connecter, redirigez-vous vers http://parcours.erlm.tn .', 'sacado_not_reply@erlm.tn', [request.user.email])
            return redirect('logout')
        else :
            print(form.errors)  
    else:
        form = PasswordChangeForm(request.user)
 
    return render(request, 'account/password_form.html', { 'form': form,  })



##############################################################################################################
##############################################################################################################
#    PARENTS
##############################################################################################################
##############################################################################################################


def register_parent(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            code_student = request.POST.get("code_student")  
            if Student.objects.filter(code = code_student).exists() :
                username  = user_form.cleaned_data['last_name']+user_form.cleaned_data['first_name']
                user = user_form.save(commit=False)
                user.username  = username
                user.user_type = 1
                password = request.POST.get("password1") 
                user.set_password(password)
                user.save()
                parent,result = Parent.objects.get_or_create(user=user)
                student = Student.objects.get(pk = code_student)
                parent.students.add(student)
            
                user = authenticate(username=username, password = password)
                login(request, user)
                messages.success(request, "Inscription réalisée avec succès !")               
                if user_form.cleaned_data['email'] :
                    send_mail('Création de compte sur Sacado', 'Bonjour, votre compte SacAdo est maintenant disponible. \n\n Votre identifiant est '+str(username) +". \n votre mot de passe est "+str(password)+'.\n\n Pour vous connecter, redirigez-vous vers http://parcours.erlm.tn.\n Ceci est un mail automatique. Ne pas répondre.', 'SacAdo_contact@erlm.tn', [request.POST.get("email")])
        else :
            messages.error(request, "Erreur lors de l'enregistrement. Reprendre l'inscription...")
    return redirect('index')



def update_parent(request, id):
    user = get_object_or_404(User, pk=id)
    parent = get_object_or_404(Parent, pk=id)
    user_form = UserUpdateForm(request.POST or None, instance=user)
    parent_form = ParentUpdateForm(request.POST or None, instance=student)
    if all((user_form.is_valid(), parent_form.is_valid())):
        user_form.save()
        parent_f = parent_form.save(commit=False)
        parent_f.user = user
        parent_f.save()
        return redirect('index')

    return render(request, 'account/parent_form.html',
                  {'user_form': user_form, 'parent_form': parent_form, 'parent': parent})


 
def delete_parent(request, id):

    parent = get_object_or_404(Parent, user_id=id)
    parent.delete()
 
    return redirect('index')

 



#####################################

@login_required
def my_profile(request):

    user = User.objects.get(id=request.user.id)
    user_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=user)
 

    if request.user.user_type == 2 :
        
        teacher = Teacher.objects.get(user=user)
        
        teacher_form = TeacherForm(request.POST or None, request.FILES or None, instance=teacher)
        if request.method == "POST" :
            if  all((user_form.is_valid(), teacher_form.is_valid())):
                teacher = teacher_form.save(commit=False)
                teacher.user = user
                teacher.save()
                teacher_form.save_m2m()
                user_form.save()
                messages.success(request, 'Votre profil a été changé avec succès !')
                if teacher.teacher_to_group.count() == 0 :
                    return redirect ('index')
                else :
                    return redirect('profile')
            else :
                print(user_form.errors)
                print(teacher_form.errors)

        return render(request,'account/teacher_form.html', {'teacher_form':teacher_form, 'user_form':user_form, 'teacher':teacher})

    elif request.user.user_type == 0 :

        student = Student.objects.get(user=user)
        form = StudentForm(request.POST or None, request.FILES or None, instance=student)
        if request.method == "POST" :
            if  all((user_form.is_valid(), form.is_valid())):
                user_form.save()
                student_f = form.save(commit=False)
                student_f.user = user
                student_f.save()
                messages.success(request, 'Votre profil a été changé avec succès !')
                return redirect('profile')

            else :
                print(form.errors)
        return render(request,'account/student_form.html', {'form':form, 'user_form':user_form, 'student':student, })

    else :

        parent = Parent.objects.get(user=user)
        form = ParentForm(request.POST or None, request.FILES or None, instance=parent)
        if request.method == "POST" :
            if  all((user_form.is_valid(), form.is_valid())):
                user_form.save()
                parent_f = form.save(commit=False)
                parent_f.user = user
                parent_f.save()
                messages.success(request, 'Votre profil a été changé avec succès !')
                return redirect('profile')

            else :
                print(form.errors)
        return render(request,'account/parent_form.html', {'form':form, 'user_form':user_form, 'student':student, })


def ajax_userinfo(request):
    username = request.POST.get("username")

    data = {}
    try:
        nb_user = User.objects.filter(username=username).count()
        if nb_user > 0:
            data['html'] = "<br><i class='fa fa-times text-danger'></i> Identifiant déjà utilisé."
            data['test'] = False
        else:
            data['html'] = "<br><i class='fa fa-check text-success'></i>"
            data['test'] = True
    except:
        data['html'] = "<br><i class='fa fa-times text-danger'></i> Identifiant déjà utilisé."
        data['test'] = False

    return JsonResponse(data)


def ajax_courseinfo(request):
    groupe_code = request.POST.get("groupe_code")
    data = {}
    try:
        nb_group = Group.objects.filter(code=groupe_code).count()
        if nb_group == 1:
            data['htmlg'] = "<br><i class='fa fa-check text-success'></i>"
        else:
            data['htmlg'] = "<br><i class='fa fa-times text-danger'></i> Groupe inconnu."
    except:
        data['htmlg'] = "<br><i class='fa fa-times text-danger'></i> Groupe inconnu."

    return JsonResponse(data)


def ajax_control_code_student(request):
    data = {}
    try:
        code_student = request.POST.get("code_student")
        nb_user = Student.objects.filter(code=code_student).count()

        if nb_user == 1:
            student = Student.objects.get(code=code_student)
            data[
                'html'] = "<br><i class='fa fa-check text-success'></i> Paire avec " + student.user.first_name + " en " + student.level.name
            data['test'] = True

        else:
            data['html'] = "<br><i class='fa fa-times text-danger'></i> Identifiant déjà utilisé."
            data['test'] = False

    except:
        data['html'] = "<br><i class='fa fa-times text-danger'></i> Identifiant déjà utilisé."
        data['test'] = False

    return JsonResponse(data)



@login_required
def ajax_detail_student(request):
    student_id = int(request.POST.get("student_id"))
    theme_id = int(request.POST.get("theme_id"))
    group_id = int(request.POST.get("group_id"))

    user = User.objects.get(pk=student_id)
    group = Group.objects.get(pk=group_id)
    student = Student.objects.get(user=user)

    if theme_id > 0:
        theme = Theme.objects.get(pk=theme_id)
        knowledges = group.level.knowledges.filter(theme=theme)
        context = {'student': student, 'theme': theme, 'group': group, 'knowledges': knowledges}
    else:
        themes = group.level.themes.all()
        context = {'student': student, 'themes': themes, 'group': group}

    data = {}
    data['html'] = render_to_string('account/ajax_detail_student.html', context)
 
    return JsonResponse(data)


@login_required
def ajax_detail_student_exercise(request):
    student_id = int(request.POST.get("student_id"))
    parcours_id = int(request.POST.get("parcours_id"))

    parcours = Parcours.objects.get(pk=parcours_id)
    student = Student.objects.get(user_id=student_id)

    relationships = Relationship.objects.filter(parcours=parcours, students=student).order_by("order")
    studentanswers = Studentanswer.objects.filter(student=student, parcours=parcours).order_by("exercise")

    context = {'student': student, 'parcours': parcours, 'studentanswers': studentanswers,
               'relationships': relationships}

    data = {}
    data['html'] = render_to_string('account/ajax_detail_student_exercise.html', context)

    return JsonResponse(data)


@login_required
def ajax_detail_student_parcours(request):
    student_id = int(request.POST.get("student_id"))
    parcours_id = int(request.POST.get("parcours_id"))

    student = Student.objects.get(user_id=student_id)
    parcours = Parcours.objects.get(pk=parcours_id)

    relationships = Relationship.objects.filter(parcours=parcours).order_by("order")

    context = {'student': student, 'relationships': relationships}

    data = {}
    data['html'] = render_to_string('account/ajax_detail_student_parcours.html', context)

    return JsonResponse(data)
