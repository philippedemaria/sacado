from django.shortcuts import render, redirect, get_object_or_404
from account.models import Student, Teacher, User, Resultknowledge, Resultlastskill
from account.forms import UserForm
from group.models import Group, Sharing_group
from socle.models import Knowledge, Theme, Level, Skill
from qcm.models import Exercise, Parcours, Relationship, Studentanswer, Resultexercise
from group.forms import GroupForm , GroupTeacherForm
from sendmail.models import Email
from sendmail.forms import EmailForm
from school.models import Stage
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
import uuid
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from group.decorators import user_is_group_teacher
from account.decorators import user_can_create
from templated_email import send_templated_mail


############### bibliothèques pour les impressions pdf  #########################
import os
from django.utils import formats, timezone
from io import BytesIO, StringIO
from django.http import  HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape , letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image , PageBreak,Frame , PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import yellow, red, black, white, blue
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT
from cgi import escape
cm = 2.54
#################################################################################
import re
import pytz
from datetime import datetime 
from general_fonctions import *

 

def student_parcours_studied(student):  
    parcourses = student.students_to_parcours.all()
    if Parcours.objects.filter(pk__in=parcourses,linked=1,is_publish=1).count() > 0 :
        parcourses = student.students_to_parcours.all()
    else :
        parcourses = student.students_to_parcours.filter(linked=0)
    return parcourses


def knowledges_of_a_student(student):
    parcourses_tab = []
    parcourses_student_tab, exercise_tab = [] ,  []
    parcourses = student_parcours_studied(student)
    parcourses_student_tab.append(parcourses)
    for parcours in parcourses :
        if not parcours in parcourses_tab :
            parcourses_tab.append(parcours)

    for parcours in parcourses_tab :
        exercises = parcours.exercises.order_by("theme")
        for exercise in exercises:
            if not exercise in exercise_tab :
                exercise_tab.append(exercise)
    
    knowledges = []
    for exercise in exercise_tab :
        if not exercise.knowledge in knowledges:
            knowledges.append(exercise.knowledge)

    return knowledges


def count_unique(datas):
    tab, nb = [], 0
    for d in datas:
        if not d in tab:
            nb += 1
            tab.append(d)
    return nb


def include_students(liste, group):

    students_tab = liste.split("\r\n")

    for student_tab in students_tab:
        try:
            details = student_tab.split(";")
            fname = str(cleanhtml(details[0].replace(" ", ""))).strip()
            lname = str(cleanhtml(details[1].replace(" ", ""))).strip()
            password = make_password("sacado2020")
            username = lname + fname

            try:
                email = cleanhtml(details[2])
            except IndexError:
                email = ""

            if email != "":
                send_templated_mail(
                    template_name="student_registration_by_teacher",
                    from_email="info@sacado.xyz",
                    recipient_list=[email],
                    context={"last_name": lname, "first_name": fname, "username": username}, )

            user, created = User.objects.get_or_create(username=username,
                                                       defaults={"last_name": lname, "first_name": fname,
                                                                 "password": password, "email": email,
                                                                 "user_type": User.STUDENT})

            if created:
                student = Student.objects.create(user=user, level=group.level)
                group.students.add(student)
                parcours_tab = []
                for student in group.students.all():
                    parcourses = student.students_to_parcours.all()
                    for parcours in parcourses:
                        if not parcours in parcours_tab:
                            parcours_tab.append(parcours)

                for p in parcours_tab:
                    p.students.add(student)
                    relationships = Relationship.objects.filter(parcours=p)
                    for relationship in relationships:
                        relationship.students.add(student)
            else:
                messages.error(request, "Erreur lors de l'enregistrement. L'identifiant {} est déjà utilisé. Modifier le prénom ou le nom.".format(username))
                break
        except:
            pass




def include_students_in_a_model(liste,model):
 
    students_tab = liste.split("\r\n")
 
    for student_tab in students_tab :
        details = student_tab.split(";")
        try:
            fname = cleanhtml(details[0].replace(" ", ""))
            lname = cleanhtml(details[1].replace(" ", ""))
            password = make_password("sacado2020")
            username = str(lname).strip()+str(fname).strip()

            try:
                email = cleanhtml(details[2])
                send_mail("Inscription SacAdo", "Bonjour "+fname+", \n Votre enseignant vous a inscrit à SACADO.\n Vos identifiants sont \n Identifiant : "+username+"\n Mot de passe : sacado2020 \n Pour plus de sécurité, changez votre mot de passe lors de votre première connexion.\n Merci." , "saca_do_not_reply@sacado.xyz" , [email])
            except IndexError:
                email = ""
            user = User.objects.create(last_name=str(lname), first_name=str(fname), username=username, password=password, email=email,user_type=0)
            code = str(uuid.uuid4())[:8] # code pour la relation avec les parents
            student = Student.objects.create(user=user, level=group.level, code=code)
            model.students.add(student)  
        except:
            pass


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



def get_stage(group):

    teacher = group.teacher

    try :
        if teacher.user.school :
            school = teacher.user.school
            stage = Stage.objects.get(school = school)
        else : 
            stage = { "low" : 50 ,  "medium" : 70 ,  "up" : 85  }
    except :
            stage = { "low" : 50 ,  "medium" : 70 ,  "up" : 85  }        
    return stage


def get_complement(request, teacher, parcours_or_group):

    data = {}

    try :
        group_id = request.session.get("group_id",None)
        if group_id :
            group = Group.objects.get(pk = group_id)
        else :
            group = None   

        if Sharing_group.objects.filter(group = group  , teacher = teacher).exists() :
            sh_group = Sharing_group.objects.get(group = group , teacher = teacher)
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

    data["group_id"] = group_id
    data["group"] = group
    data["role"] = True
    data["access"] = access

    return data



def authorizing_access_group(teacher,group ):

    test = False
    if teacher.teacher_sharingteacher.filter(group = group).count() > 0 :
        test = True

    if group.teacher == teacher or test :
        test = True   

    if not test :
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

#####################################################################################################################################
#####################################################################################################################################
####    Group
#####################################################################################################################################
#####################################################################################################################################



def list_groups(request):
    groups = Group.objects.filter(teacher__user_id = request.user.id)
    return render(request, 'group/list_group.html', {'groups': groups, 'communications' : [] , })


 
def create_group(request):
    teacher = Teacher.objects.get(user_id=request.user.id)
    form = GroupTeacherForm(request.POST or None, teacher = teacher )


    if form.is_valid():
        nf = form.save(commit=False)
        nf.teacher = teacher
        nf.save()
        stdts = request.POST.get("students")
        if stdts : 
            if len(stdts) > 0 :
                include_students(stdts,nf)


        if  teacher.groups.count() == 1 :
            messages.success(request, "Félicitations... Votre compte sacado est maintenant configuré et votre premier groupe créé !")

        return redirect('index')
    else:
        print(form.errors)

    context = {'form': form, 'teacher': teacher, 'group': None, 'communications' : [] , }

    return render(request, 'group/form_group.html', context)



#@user_is_group_teacher
def update_group(request, id):


    teacher = Teacher.objects.get(user= request.user)
    group = Group.objects.get(id=id)

    authorizing_access_group(teacher,group )

    if group.teacher.user.school :
        students = Student.objects.filter(user__school=group.teacher.user.school).order_by("user__last_name")
    else :
        students = []

    
    form = GroupTeacherForm(request.POST or None, teacher = teacher , instance=group )

    if form.is_valid():
        nf = form.save(commit = False)
        nf.teacher = teacher
        nf.code = group.code
        nf.save()
        stdts = request.POST.get("students")
        if stdts : 
            if len(stdts) > 0 :
                tested = include_students(stdts,group)
                if not tested :
                    messages.error(request, "Erreur lors de l'enregistrement. Un étudiant porte déjà cet identifiant. Modifier le prénom ou le nom.")
        
        return redirect('index')
    else:
        print(form.errors)

    context = {'form': form,  'group': group, 'teacher': teacher, 'students': students, 'communications' : [] , }

    return render(request, 'group/form_group.html', context )




def delete_group(request, id):
    group = Group.objects.get(id=id)
    # Si le prof n'appartient pas à un établissement
    teacher = group.teacher
    authorizing_access_group(teacher,group )
    if not teacher.user.school :
        # Si les élèves n'appartiennent pas à un établissement
        for student in group.students.all():
            if not student.user.school :
                if Group.objects.filter(students=student).exclude(pk=group.id) == 0 : 
                    #Si les élèves n'appartiennent pas à un autre groupe
                    student.student_user.delete()
                    student.delete() # alors on les supprime
        group.delete()
        return redirect('index')
    else :
        group.delete()
        return redirect('school_groups')        

 
def show_group(request, id ):

    group = Group.objects.get(id=id)
    teacher = Teacher.objects.get(user=request.user)
    request.session["group_id"] = id
    data = get_complement(request, teacher, group)
    role = data['role']
    access = data['access']
    authorizing_access_group(teacher,group )
    context = {  'group': group,  'communications' : [] , 'teacher' : group.teacher  }

    return render(request, 'group/show_group.html', context )



def aggregate_group(request):

    code_groupe = request.POST.get("groupe")
    student = Student.objects.get(user=request.user)

    if Group.objects.exclude(students = student).filter(code = code_groupe).exists()  :    
        group = Group.objects.get(code = code_groupe)
        group.students.add(student)
    else :
        print(code_groupe)    

    return redirect("index") 




def chargelisting(request):

    group_id = int(request.POST.get("group_id"))
    group = Group.objects.get(id=group_id)

    is_remove = False 
 
    data = {}

    data['html_modal_group_name'] = group.name 
   
    data['html_list_students'] = render_to_string('group/listingOfStudents.html', {  'group':group, 'is_remove' : is_remove })
 
 
    return JsonResponse(data)



def student_select_to_school(request):

    group_id = int(request.POST.get("group_id"))
    student_id = int(request.POST.get("student_id"))
    group = Group.objects.get(id=group_id) 
    student = Student.objects.get(user_id=student_id) 


    p_tab = []    
    for std in group.students.all() :
        parcourses = std.students_to_parcours.all()
        for p in parcourses :
            if not p in p_tab :
                p_tab.append(p)
                
    for p in p_tab:
        p.students.add(student)
        relationships = p.parcours_relationship.all()
        for r in relationships:
            r.students.add(student)

    group.students.add(student)


    data = {}

    data['html'] =  "<tr id='tr_school"+str(student.user.id)+"'><td>"+str(student.user.last_name)+"</td><td>"+str(student.user.first_name)+"</td><td>"+str(student.user.username)+"</td><td><a class='btn btn-xs btn-danger' data_student_id='"+str(student.user.id)+"' data_group_id='"+str(group.id)+"' ><i class='fa fa-trash'></i></a></td></tr>"
    return JsonResponse(data)


def student_remove_from_school(request):

    group_id = int(request.POST.get("group_id"))
    student_id = int(request.POST.get("student_id"))
    group = Group.objects.get(id=group_id) 
    student = Student.objects.get(user_id=student_id) 

    for p in student.students_to_parcours.all() :
        p.students.remove(student) 
  
    for r in student.students_relationship.all() :
        r.students.remove(student) 

    group.students.remove(student)

    groups = student.students_to_group.all()
    gr = ""
    for g in groups :
        gr = gr +str(g.name)+" "

    data = {}
    data['html'] =  "<tr id='tr"+str(student.user.id)+"'><td><input type='checkbox' class='student_select_to_school' data_student_id='"+str(student.user.id)+"' data_group_id='"+str(group.id)+"' /> </td><td>"+str(student.user.last_name)+"</td><td>"+str(student.user.first_name)+"</td><td>"+gr+"</td></tr>"
 
    return JsonResponse(data)
 


def chargelistgroup(request):

    parcours_id = int(request.POST.get("parcours_id"))
    parcours = Parcours.objects.get(id=parcours_id) 
    data = {}

    is_remove = True

    data['html_modal_group_name'] = parcours.title 
   
    data['html_list_students'] = render_to_string('group/listingOfStudents.html', {  'group':parcours, 'is_remove' : is_remove   })
 
 
    return JsonResponse(data)



def sender_mail(request,form):
    if request.method == "POST" : 
        subject = request.POST.get("subject") 
        texte = request.POST.get("texte") 
        student_id = request.POST.get("student_id")
 
        student_user =  User.objects.get(pk=student_id)
        rcv = []
        if form.is_valid():
            nf = form.save(commit = False)
            nf.author =  request.user
            nf.save()
            nf.receivers.add(student_user)

            for r in nf.receivers.all():
                rcv.append(r.email)
            print("sending")
            send_mail( cleanhtml(subject), cleanhtml(texte) , "info@sacado.xyz" , rcv)

        else :
            print(form.errors)
            print("no_sending")





#@user_is_group_teacher
def result_group(request, id):

    group = Group.objects.get(id=id)
    teacher = Teacher.objects.get(user=request.user)
    authorizing_access_group(teacher,group )

    parcourses_tab = []
    parcourses_student_tab, exercise_tab = [] ,  []
    for student in group.students.order_by("user__id"):
        parcourses = student_parcours_studied(student) 
        if parcourses in parcourses_student_tab :
            break
        else :
            parcourses_student_tab.append(parcourses)
            for parcours in parcourses :
                if not parcours in parcourses_tab :
                    parcourses_tab.append(parcours)

    for parcours in parcourses_tab :
        exercises = parcours.exercises.all()
        for exercise in exercises:
            if not exercise in exercise_tab :
                exercise_tab.append(exercise)
    
    knowledges = []
    for exercise in exercise_tab :
        if not exercise.knowledge in knowledges:
            knowledges.append(exercise.knowledge)

    stage = get_stage(group)
 
    form = EmailForm(request.POST or None )

    context = { 'group': group,'form': form,  'teacher': teacher,  "knowledges" : knowledges, 'stage' : stage, 'theme': None , 'communications' : [] , 'relationships': []  , 'parcours_tab' : [] , 'parcours' : None }

    return render(request, 'group/result_group.html', context )



#@user_is_group_teacher
def result_group_theme(request, id, idt):

    teacher = Teacher.objects.get(user=request.user)
    group = Group.objects.get(id=id)

    authorizing_access_group(teacher,group ) 
 
    form = EmailForm(request.POST or None )
    theme = Theme.objects.get(id=idt)
    knowledges = Knowledge.objects.filter(level = group.level,theme = theme) 

    number_of_parcours_of_this_level_by_this_teacher = group.teacher.teacher_parcours.filter(level = group.level).count()
    parcours_id_tab , parcours_tab = [] , []
    for student in group.students.all():
        parcourses = student.students_to_parcours.all()
        parcours_tab = [parcours for parcours in  parcourses if  parcours.id not in parcours_id_tab]
        if len(parcours_tab) == number_of_parcours_of_this_level_by_this_teacher :
            break
    stage = get_stage(group)
    context = {  'group': group, 'form': form, 'theme': theme,  'stage' : stage  , "knowledges" : knowledges, "teacher" : teacher,  'parcours_tab' : parcours_tab, 'parcours' : None  , 'communications' :  [] , 'relationships':  []   }

    return render(request, 'group/result_group.html', context )



#@user_is_group_teacher
def result_group_exercise(request, id):
    group = Group.objects.get(id=id)
    form = EmailForm(request.POST or None)
    stage = get_stage(group)

    teacher = Teacher.objects.get(user=request.user)

    authorizing_access_group(teacher,group ) 

    sender_mail(request,form)

    context = {'group': group, 'form': form , 'stage' : stage  , 'teacher': teacher, 'theme' : None  , 'communications' : [], 'relationships': [] , 'parcours_tab' : [] , 'parcours' : None  }

    return render(request, 'group/result_group_exercise.html', context)



#@user_is_group_teacher
def result_group_skill(request, id):

    group = Group.objects.get(id=id)
    skills = Skill.objects.filter(subject=group.subject)

    teacher = Teacher.objects.get(user=request.user)

    authorizing_access_group(teacher,group ) 

    form = EmailForm(request.POST or None )
    stage = get_stage(group)

    context = {  'group': group,'form': form,'skills': skills , 'teacher': teacher, 'stage' : stage   ,  'theme' : None  , 'communications' : [], 'relationships': [] , 'parcours' : None  }

    return render(request, 'group/result_group_skill.html', context )




#@user_is_group_teacher
def result_group_theme_exercise(request, id, idt):
    group = Group.objects.get(id=id)
    form = EmailForm(request.POST or None )
    theme = Theme.objects.get(id=idt)
    stage = get_stage(group)
    teacher = Teacher.objects.get(user=request.user)

    authorizing_access_group(teacher,group ) 

    context = {  'group': group, 'form': form, 'theme': theme, 'teacher': teacher, "slug" : theme.slug , 'stage' : stage   , 'communications' : [], 'relationships': [] , 'parcours': None  }

    return render(request, 'group/result_group_theme_exercise.html', context )

 

def stat_group(request, id):
    group = Group.objects.get(id=id)
    form = EmailForm(request.POST or None )
    teacher = Teacher.objects.get(user=request.user)

    
    authorizing_access_group(teacher,group ) 

    stats = []
    for s in group.students.order_by("user__last_name") :
        student = {}
        student["name"] = s 
        parcours = Parcours.objects.filter(students=s,is_publish=1)
        nb_exo_total = 0
        for p in parcours :
            nb_exo_total += Relationship.objects.filter(parcours=p,is_publish=1).count()
        student["parcours"] = parcours 
        studentanswers = Studentanswer.objects.filter(parcours__in = parcours, student=s)
        nb_exo_done = 0
        nb_exo_done_tab = []
        for studentanswer in studentanswers :
            if studentanswer.id not in nb_exo_done_tab :
                nb_exo_done += 1
                nb_exo_done_tab.append(studentanswer.id)
        student["nb_exo"] = int(nb_exo_done)
        student["nb_exo_total"] = int(nb_exo_total)
        try :
            student["percent"] = int(nb_exo_done / nb_exo_total * 100)
        except : 
            student["percent"] = 0
        studentanswers = Studentanswer.objects.filter(student=s)
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
                student["duration"] = duration
                student["average_score"] = int(average_score)
                student["heure_max"] = tab_date[len(tab_date)-1]
                student["heure_min"] = tab_date[0]
                tab.sort()
                if len(tab)%2 == 0 :
                    med = (tab[(len(tab)-1)//2]+tab[(len(tab)-1)//2+1])/2 ### len(tab)-1 , ce -1 est causÃ© par le rang 0 du tableau
                else:
                    med = tab[(len(tab)-1)//2+1]
                student["median"] = int(med)
            else:
                average_score = int(score)
                student["duration"] = duration
                student["average_score"] = int(score)
                student["heure_max"] = tab_date[0]
                student["heure_min"] = tab_date[0]
                student["median"] = int(score)
        except :
            student["duration"] = ""
            student["average_score"] = ""
            student["heure_max"] = ""
            student["heure_min"] = ""
            student["median"] = ""
        stats.append(student)

    context = {  'group': group, 'form': form, 'stats':stats , 'teacher': teacher, 'parcours' : None }
 
    return render(request, 'group/stat_group.html', context )

 
def task_group(request, id):
    group = Group.objects.get(id=id)
    teacher = Teacher.objects.get(user=request.user)

    
    authorizing_access_group(teacher,group ) 


    stats = []
    for s in group.students.order_by("user__last_name"):
        student = {}
        student["name"] = s
        parcours = Parcours.objects.filter(students=s)
        student["parcours"] = parcours
        relationships = Relationship.objects.filter(parcours__in=parcours).exclude(date_limit=None).select_related('exercise')
        done, late, no_done = 0, 0, 0
        for relationship in relationships:
            nb_ontime = Studentanswer.objects.filter(student=s, exercise=relationship.exercise).count()

            utc_dt = dt_naive_to_timezone(relationship.date_limit, student.user.time_zone)

            nb = Studentanswer.objects.filter(student=s, exercise=relationship.exercise, date__lte=utc_dt).count()
            if nb_ontime == 0:
                no_done += 1
            elif nb > 0:
                done += 1
            else:
                late += 1
        student["nb"] = no_done + done + late
        student["no_done"] = no_done
        student["done"] = done
        student["late"] = late
        stats.append(student)

    context = {'group': group, 'stats': stats, 'teacher': teacher,}

    return render(request, 'group/task_group.html', context)




def select_exercise_by_knowledge(request):
    data = {}
    group_id = request.POST.get("group_id")
    group = Group.objects.get(id=int(group_id))
    teacher = Teacher.objects.get(user=request.user)
    authorizing_access_group(teacher,group ) 


    knowledge_id = request.POST.get("knowledge_id")
    knowledge = Knowledge.objects.get(id=int(knowledge_id))
    exercises = Exercise.objects.filter(knowledge=knowledge)

    data['html'] = render_to_string('qcm/select_exercise_by_knowledge.html',
                                    {'exercises': exercises, 'knowledge': knowledge, 'group': group,
                                     'teacher': teacher})
    return JsonResponse(data)




def associate_exercise_by_parcours(request,id,idt):


    group = Group.objects.get(id = id)
    teacher = Teacher.objects.get(user=request.user)
    authorizing_access_group(teacher,group )  
       
    theme = Theme.objects.get(id = idt)
    knowledge_id = request.POST.get("knowledge_id_modal") 
    knowledge = Knowledge.objects.get(id=int(knowledge_id))

    parcourses = Parcours.objects.filter(teacher = teacher, level = group.level)
 
    return redirect('result_group_theme', group.id, theme.id)





def enroll(request, slug):
    '''
    Création d'un compte élève et inscription à un groupe via le lien donné par l'enseignant
    '''
    group = get_object_or_404(Group, code=slug)
    user_form = UserForm(request.POST or None)

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid() :
            user = user_form.save(commit=False)
            user.user_type = User.STUDENT
            password = request.POST.get("password1")
            user.set_password(password)
            user.save()

            # Liste des parcours des élèves du groupe
            parcourses = []
            for student in group.students.all():
                for p in student.students_to_parcours.filter(teacher=group.teacher) :
                    if p not in parcourses :
                        parcourses.append(p)

            # Création de Student et affections des parcours
            student = Student.objects.create(user=user, level=group.level)
            for parcours in parcourses:
                parcours.students.add(student)
                relationships = parcours.parcours_relationship.all()
                for r in relationships:
                    r.students.add(student)                
                courses = parcours.course.all()
                for c in courses:
                    c.students.add(student)

            group.students.add(student)

            messages.success(request, "Inscription réalisée avec succès ! Si vous avez renseigné votre email, vous avez reçu un mail de confirmation. Connectez-vous avec vos identifiants en cliquant sur le bouton bleu Se connecter.")
            if user_form.cleaned_data['email']:
                send_mail('Création de compte sur Sacado',
                          'Bonjour, votre compte SacAdo est maintenant disponible. \n\n Votre identifiant est '+str(username) +". \n votre mot de passe est "+str(password)+'.\n\n Pour vous connecter, redirigez-vous vers http://sacado.erlm.tn.\n Ceci est un mail automatique. Ne pas répondre.',
                          'info@sacado.xyz',
                          [request.POST.get("email")])

            return redirect('index')    
        else:
            user_form = UserForm(request.POST or None)

    return render(request, 'group/enroll.html', {"u_form": user_form, "slug": slug, "group": group, })




def print_statistiques(request, group_id, student_id):

    themes, subjects = [], []
    group = Group.objects.get(pk = group_id)

    teacher = Teacher.objects.get(user=request.user)

    
    authorizing_access_group(teacher,group ) 


    if student_id == 0  :
        students = group.students.order_by("user__last_name")
        title_of_report = group.name+"_"+str(timezone.now().date())

        knows = Knowledge.objects.filter(level = group.level).order_by("level")
        for know in knows :
            if not know.theme in themes :
                themes.append(know.theme)


    else :
        student = Student.objects.get(pk = student_id)
        students = [student]
        title_of_report = student.user.last_name+"_"+student.user.first_name+"_"+str(timezone.now().date())

        knows = knowledges_of_a_student(student)
        for know in knows :
            if not know.theme in themes :
                themes.append(know.theme)
    
 
    subject = group.subject


    elements = []        

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+str(title_of_report)+'.pdf"'

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

    title = ParagraphStyle('title', 
                            fontSize=20, 
                            textColor=colors.HexColor("#00819f"),
                            )

    subtitle = ParagraphStyle('title', 
                            fontSize=16, 
                            textColor=colors.HexColor("#00819f"),
                            )
 

    normal = ParagraphStyle(name='Normal',fontSize=12,)    
    style_cell = TableStyle(
            [
                ('SPAN', (0, 1), (1, 1)),
                ('TEXTCOLOR', (0, 1), (-1, -1),  colors.Color(0,0.7,0.7))
            ]
        )


    for student in students :
        #logo = Image('D:/uwamp/www/sacado/static/img/sacadoA1.png')
        logo = Image('https://sacado.xyz/static/img/sacadoA1.png')
        logo_tab = [[logo, "SACADO \nSuivi des acquisitions de savoir faire" ]]
        logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5*inch])
        logo_tab_tab.setStyle(TableStyle([ ('TEXTCOLOR', (0,0), (-1,0), colors.Color(0,0.5,0.62))]))
        elements.append(logo_tab_tab)
        elements.append(Spacer(0, 0.2*inch))

        if timezone.now().month < 9 :
            scolar_year = str(timezone.now().year-1)+"-"+str(timezone.now().year)
        else :
            scolar_year = str(timezone.now().year)+"-"+str(timezone.now().year+1)

        sort_of_exercise , nb_exo = [] , 0 
        studentanswer_ids = Studentanswer.objects.values_list("id",flat=True).filter(student=student)
        for studentanswer_id in studentanswer_ids :
            if not studentanswer_id in sort_of_exercise :
                nb_exo += 1


        studentanswers = Studentanswer.objects.filter(student=student)
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
                tab.sort()
                if len(tab)%2 == 0 :
                    med = (tab[(len(tab)-1)//2]+tab[(len(tab)-1)//2+1])/2 ### len(tab)-1 , ce -1 est causÃ© par le rang 0 du tableau
                else:
                    med = tab[(len(tab)-1)//2+1]
                median = int(med)
            else :
                average_score = int(score)
                median = int(score)
        except :
            average_score = 0
            median = 0



        # Vérifie que le parcours par défaut est donné
        nb_k_p , nb_p = 0 , 0 
        parcourses = student_parcours_studied(student)

        knowledges = []
        for parcours in parcourses :
            exercises = parcours.exercises.filter(theme__in= themes , level = student.level)
            nb_p += exercises.count()
            for exercise in exercises :
                if not exercise.knowledge in knowledges:
                    knowledges.append(exercise.knowledge)


            nb_k_p = len(knowledges)
            knows_ids = Studentanswer.objects.values_list("id",flat=True).filter(exercise__knowledge__in = knows, exercise__in= exercises , student=student)
            nb_k = count_unique(knows_ids)
        # Les taux
        try :
            p_k = int(nb_k/nb_k_p * 100 )
            if p_k > 100 :
                p_k = 100
        except :
            p_k = 0
        try :
            p_e = int(nb_exo/nb_p * 100)
            if p_e > 100 :
                p_e = 100
        except :
            p_e = 0


        relationships = Relationship.objects.filter(parcours__in = parcourses).exclude(date_limit=None)
        done, late, no_done = 0 , 0 , 0 
        for relationship in relationships :
            nb_ontime = Studentanswer.objects.filter(student=student, exercise = relationship.exercise ).count()


            nb = Studentanswer.objects.filter(student=student, exercise = relationship.exercise, date__lte= relationship.date_limit ).count()
            if nb_ontime == 0 :
                no_done += 1
            elif nb > 0 :
                done += 1
            else :
                late += 1 
        t_r = no_done + done + late
 
        ##########################################################################
        #### Gestion de l'autonomie
        ##########################################################################
        if nb_exo > nb_p :
            nbr = nb_exo - nb_p
            complt = " dont "+str(nbr)+" en autonomie"
        else :
            complt = ""
        if nb_k > nb_k_p :
            nbrk = nb_k - nb_k_p
            complement = " dont "+str(nbrk)+" en autonomie" 
        else :
            complement = ""

 
        ##########################################################################
        #### Gestion des labels à afficher
        ##########################################################################
        labels = [str(student.user.last_name)+" "+str(student.user.first_name), str(student.level)+", année scolaire "+scolar_year,"Temps de connexion : "+convert_seconds_in_time(duration), "Score moyen : "+str(average_score)+"%" , "Score médian : "+str(median)+"%" , \
                "Les savoir faire  ", "Nombre de savoir faire étudiés : "+str(nb_k)+complement, "Nombre de savoir faire proposés : "+str(nb_k_p), "Taux d'étude : "+str(p_k)+"%",\
                 "Les exercices ", "Nombre d'exercices différents étudiés : "+str(nb_exo)+complt, "Nombre d'exercices proposés : "+str(nb_p), "Taux d'étude : "+str(p_e)+"%",\
                 "Les tâches ", "Tâches proposées : "+str(t_r),  "Tâches remises en temps : "+str(done), "Tâches remises en retard : "+str(late), "Tâches non remises : "+str(no_done),\
                 "Suivi par compétences ",]

        spacers , titles,subtitles = [1,4, 5,8,12,17] ,[0],[ 5,9,13,18]

        i = 0
        for label in labels :
            if i in spacers : 
                height = 0.3
            else :
                height = 0.1
            if i in titles : 
                style = title
                height = 0.2
            elif i in subtitles :
                style = subtitle
                height = 0.1
            else :
                style = normal
            paragraph = Paragraph( label , style )
            elements.append(paragraph)
            elements.append(Spacer(0, height*inch))
            i+=1         
        ##########################################################################
        #### Gestion des compétences
        ##########################################################################
        sk_tab = []
        skills = Skill.objects.filter(subject= subject)
        for skill  in skills :
            try :
                resultlastskill  = Resultlastskill.objects.get(student = student, skill= skill )
                sk_tab.append([skill.name, str(resultlastskill.point)+"%" ])
            except :
                sk_tab.append([skill.name, str(0)+"%" ])
            
        try : # Test pour les élèves qui n'auront rien fait, il n'auront pas de th_tab donc il ne faut l'afficher 
            skill_tab = Table(sk_tab, hAlign='LEFT', colWidths=[5.2*inch,1*inch])
            skill_tab.setStyle(TableStyle([
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))
        except : 
            skill_tab = Table(sk_tab, hAlign='LEFT', colWidths=[5.2*inch,1*inch])

        elements.append(skill_tab)
        ##########################################################################
        #### Gestion des themes
        ##########################################################################
        elements.append(Spacer(0, 0.3*inch))
        paragraph = Paragraph( "Suivi par thèmes " , style )
        elements.append(paragraph)
        elements.append(Spacer(0, 0.2*inch))

        th_tab = []
        for theme  in themes :
            som_theme = 0
            resultexercises = Resultexercise.objects.filter(student = student, exercise__theme= theme )
            for result in resultexercises :
                som_theme += result.point
            try :
                avg_theme = int(som_theme / len(resultexercises))
                th_tab.append([theme.name, str(avg_theme)+"%" ])
            except :
                th_tab.append([theme.name, str(0)+"%" ])
            
        try : # Test pour les élèves qui n'auront rien fait, il n'auront pas de th_tab donc il ne faut l'afficher 
            theme_tab = Table(th_tab, hAlign='LEFT', colWidths=[5.2*inch,1*inch])
            theme_tab.setStyle(TableStyle([
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))
        except : 
            theme_tab = Table(th_tab, hAlign='LEFT', colWidths=[5.2*inch,1*inch])

        elements.append(theme_tab)
        loop  = 0
        for theme  in themes :

            ##########################################################################
            #### Gestion des knowledges par thème
            ##########################################################################
            knowledges = []
            for parcours in parcourses :
                exercises = parcours.exercises.filter(theme= theme , level = student.level)
                for exercise in exercises :
                    if not exercise.knowledge in knowledges:
                        knowledges.append(exercise.knowledge)


            if len(knowledges) > 0 :

                if loop%2 == 0 :
                    elements.append(PageBreak()) # Ouvre une nouvelle page - 2 thèmes
                loop +=1
                # Append le thème 
                paragraph = Paragraph( theme.name , title )  
                elements.append(paragraph)
                elements.append(Spacer(0, 0.2*inch)) 
                knowledge_tab = [['Savoir faire','Score','Nombre de \n fois étudié',]]
                #######


                for knowledge in knowledges :
                    # Savoir faire
                    name  = ""
                    k_tab = knowledge.name.split(" ")
                    for j in range(len(k_tab)) : 
                        if j%11 == 0 and j > 1 :
                            sep = "\n"
                        else :
                            sep = " "
                        name  +=  k_tab[j] + sep
                    ##########################################################################
                    #### Affichage des résultats par knowledge
                    ##########################################################################                    
                    try :      
                        knowledgeResult = Resultknowledge.objects.get(knowledge  = knowledge, student = student)
                        knowledgeResult_nb = Studentanswer.objects.values_list("id",flat=True).filter(exercise__knowledge = knowledge, student=student).count()          
                        knowledge_tab.append(      ( name , str(knowledgeResult.point)+"%" , knowledgeResult_nb )          )
                    except : 
                        knowledge_tab.append(      ( name , 0   , 0  )        )
                
                ##########################################################################
                # Bordure du savoir faire
                ##########################################################################

                knowledge_tab_tab = Table(knowledge_tab, hAlign='LEFT', colWidths=[5.6*inch,0.7*inch,1*inch])
                knowledge_tab_tab.setStyle(TableStyle([
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
                            ('BACKGROUND', (0,0), (-1,0), colors.Color(0,0.5,0.62))
                           ]))

                elements.append(knowledge_tab_tab)


        elements.append(PageBreak())

    doc.build(elements)

    return response





def print_ids(request, id):
    group = Group.objects.get(id=id)
    teacher = Teacher.objects.get(user=request.user)

    authorizing_access_group(teacher,group ) 


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="identifiants_groupe'+group.name+'.pdf"'
    p = canvas.Canvas(response)
    i = 1
    for student in group.students.all() :

    # Create the HttpResponse object with the appropriate PDF headers.
        string0 = "Bonjour {} {},".format(student.user.first_name, student.user.last_name) 
        string1 = "allez sur le site https://sacado.xyz et cliquez sur le bouton bleu Se connecter." 
        string2 = "Votre identifiant est : {}    . Votre mot de passe est :    sacado2020".format(student.user.username)
        p.setFont("Helvetica", 12)

        p.drawString(75, 900-100*i, string0)
        p.drawString(75, 880-100*i, string1)
        p.drawString(75, 860-100*i, string2)
        p.line(75, 830-100*i,550,830-100*i)
        if i%8 == 0 :
            i = 1
            p.showPage()
        else : 
            i +=1
 
    p.save()
    return response 