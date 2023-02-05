#################################
#### Auteur : philipe Demaria 
#### pour SACADO
#################################

from django.conf import settings # récupération de variables globales du settings.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse , FileResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail

from tool.models import * # Generate_quizz , Generate_qr
from tool.forms import *
from tool.random_questions import *
from group.models import Group 
from socle.models import Level, Waiting , Theme , Knowledge
from qcm.models import  Parcours, Exercise , Folder , Relationship
from account.decorators import  user_is_testeur
from sacado.settings import MEDIA_ROOT
 
from qcm.views import  get_teacher_id_by_subject_id

import uuid
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import  login_required
from django.views.decorators.csrf import csrf_exempt
from django.forms import inlineformset_factory
from templated_email import send_templated_mail
from django.db.models import Q , Sum
from random import  randint, shuffle
import math
import json
import time
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
from html import escape
cm = 2.54
#################################################################################
import re
import pytz
from datetime import datetime , timedelta
from general_fonctions import *
from qcm.views import tracker_execute_exercise
import subprocess
from cryptography.fernet import Fernet
from tool.random_questions import *
#################################################################################
#   Fonctions
#################################################################################
def all_datas(level):

    levels_dict = {}
 
    themes = level.themes.order_by("id")
    themes_tab =   []
    for theme in themes :
        themes_dict =  {}                
        themes_dict["name"]=theme
        waitings = theme.waitings.filter(level=level)
        waitings_tab  =  []
        for waiting in waitings :
            qrs_counter = 0
            waiting_dict  =   {} 
            waiting_dict["name"]=waiting 
            knowlegdes = waiting.knowledges.order_by("name")
            knowledges_tab  =  []
            for knowledge in knowlegdes :
                knowledges_dict  =   {}  
                knowledges_dict["name"]=knowledge 
                qrandoms = knowledge.qrandom.all()
                qrs_counter +=  qrandoms.count()
                knowledges_dict["qrandoms"]=qrandoms
                knowledges_tab.append(knowledges_dict)
            waiting_dict["knowledges"]=knowledges_tab
            waiting_dict["qrs_counter"]=qrs_counter
            waitings_tab.append(waiting_dict)
        themes_dict["waitings"]=waitings_tab
        themes_tab.append(themes_dict)
    levels_dict["themes"]=themes_tab
    return levels_dict 
 


def all_datas_qia(level):

    levels_dict = {}
 
    themes = level.themes.order_by("id")
    themes_tab =   []
    for theme in themes :
        themes_dict =  {}                
        themes_dict["name"]=theme
        waitings = theme.waitings.filter(level=level)
        waitings_tab  =  []
        for waiting in waitings :
            qrs_counter = 0
            waiting_dict  =   {} 
            waiting_dict["name"]=waiting 
            knowlegdes = waiting.knowledges.order_by("name")
            knowledges_tab  =  []
            for knowledge in knowlegdes :
                knowledges_dict  =   {}  
                knowledges_dict["name"]=knowledge 
                questions = knowledge.question.all()
                qrs_counter +=  questions.count()
                knowledges_dict["questions"]=questions
                knowledges_tab.append(knowledges_dict)
            waiting_dict["knowledges"]=knowledges_tab
            waiting_dict["qrs_counter"]=qrs_counter
            waitings_tab.append(waiting_dict)
        themes_dict["waitings"]=waitings_tab
        themes_tab.append(themes_dict)
    levels_dict["themes"]=themes_tab

    return levels_dict 
 

#####################################################################################################################################
#####################################################################################################################################
####    tool
#####################################################################################################################################
#####################################################################################################################################

 
@login_required(login_url= 'index') 
def list_tools(request):
    teacher = request.user.teacher
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Projections"

    if request.user.is_superuser :
        tools = Tool.objects.all()
    else :
        tools = Tool.objects.filter(is_publish=1, is_ebep=0).exclude(teachers = teacher)
    form = ToolForm(request.POST or None, request.FILES or None   )
    return render(request, 'tool/list_tools.html', {'form': form , 'tools' : tools })



def create_tool(request):

    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Projections"

    form = ToolForm(request.POST or None, request.FILES or None,   )
 

    if form.is_valid():
        form.save()

        return redirect('list_tools')
    else:
        print(form.errors)

    context = {'form': form, }
    return render(request, 'tool/form_tool.html', context)


@login_required(login_url= 'index')
def update_tool(request, id):

    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Projections"

    tool = Tool.objects.get(id=id)
 
    teacher = request.user.teacher   
    form = ToolForm(request.POST or None, request.FILES or None, instance = tool  )

    if form.is_valid():
        form.save()
        return redirect('list_tools')
    else:
        print(form.errors)

    context = {'form': form,  'tool': tool, 'teacher': teacher,  }

    return render(request, 'tool/form_tool.html', context )




def delete_tool(request, id):
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Projections"

    tool = Tool.objects.get(id=id)
    tool.delete()
    return redirect('tool_index')
    

 
def show_tool(request, id ):
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Projections"
    tool = Tool.objects.get(id=id)
    if tool.url != "" :
        url = tool.url
    else :
        url = 'tool/show_tool.html'
    context = {  'tool': tool,   }

    return render(request, url , context )

@login_required(login_url= 'index')
def get_this_tool(request):

    data = {} 
    tool_id = int(request.POST.get("tool_id"))
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Projections"
    tool = Tool.objects.get(pk=tool_id) 
    tool.teachers.add(request.user.teacher)

    data['html'] =  "<div class='row' id='this_this_tool'  ><div class='col-lg-12 col-xs-12'><a href= /tool/show/"+str(tool.id)+" >"+str(tool.title)+"</a></div></div>"
 
 
    return JsonResponse(data)


@login_required(login_url= 'index')
def delete_my_tool(request):

    data = {} 
    tool_id = int(request.POST.get("tool_id"))
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Projections"
    tool = Tool.objects.get(pk=tool_id) 
    tool.teachers.remove(request.user.teacher)
 
    return JsonResponse(data)



def tools_to_exercise(request,id):
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Projections"
    exercise = Exercise.objects.get(id=id)
    tools = Tool.objects.all()

    url = 'tool/exercise_tools.html'
    context = {  'tools': tools,  'exercise': exercise,   }

    return render(request, url , context )

 

def ajax_attribute_this_tool_to_exercise(request):

    data = {} 
    tool_id = int(request.POST.get("tool_id"))

    exercise_id = int(request.POST.get("exercise_id"))
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Projections"
    exercise = Exercise.objects.get(pk=exercise_id) 
    tool     = Tool.objects.get(pk=tool_id)
    if exercise in tool.exercises.all() :
        tool.exercises.remove(exercise)
    else :
        tool.exercises.add(exercise)
 
    return JsonResponse(data)


############################################################################################################
############################################################################################################
########## Quizz
############################################################################################################
############################################################################################################
def user_list_of_school(teacher):
    if teacher.sacado :
        user_ids = list(teacher.user.school.users.values_list('id', flat=True).filter(user_type=2))
        user_ids.append(2480)
    else :
        user_ids = [2480]
    return user_ids

@login_required(login_url= 'index')
def all_quizzes(request):

    teacher = request.user.teacher 

    user_ids = user_list_of_school(teacher)
    quizzes = Quizz.objects.filter(is_share = 1 , teacher_id__in = user_ids  , is_random=0  ).exclude(teacher = teacher )

    parcours_id = request.session.get("parcours_id",None)  
    if parcours_id :
        parcours = Parcours.objects.get(pk = parcours_id)
    else :
        parcours = None
 
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"
    form = QuizzForm(request.POST or None, request.FILES or None ,teacher = teacher, group = None, folder = None)
    return render(request, 'tool/all_quizzes.html', {'quizzes': quizzes , 'form': form, 'teacher':teacher , 'parcours':parcours }) 

 
@login_required(login_url= 'index')
def ajax_shared_quizzes(request):

    teacher = request.user.teacher

    user_ids = user_list_of_school(teacher)

    quizzes = Quizz.objects.filter(is_share = 1 , teacher_id__in = user_ids , is_random=0  ).exclude(teacher = teacher )

    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"


    form = QuizzForm(request.POST or None, request.FILES or None ,teacher = teacher, group = None, folder = None )
    return render(request, 'tool/all_quizzes.html', {'quizzes': quizzes , 'form': form, 'teacher':teacher   })



@login_required(login_url= 'index')
def ajax_clone_quizz(request):
    """ cloner un parcours """

    data = {}
    id_quizz     = request.POST.get("this_document_id",None)
    folders      = request.POST.getlist("folders",[])
    parcourses   = request.POST.getlist("parcourses",[])
    groups       = request.POST.getlist("groups",[])

    teacher = request.user.teacher

    if id_quizz :
        quizz = Quizz.objects.get(pk=id_quizz) # parcours à cloner.pk = None
        questions = quizz.questions.all()
        levels = quizz.levels.all()
        qrandoms = quizz.qrandoms.all()
        themes = quizz.themes.all()

        quizz.pk = None
        quizz.teacher = teacher
        quizz.code = str(uuid.uuid4())[:8]
        quizz.save()

        parcours_id = request.session.get("parcours_id",None)  
        if parcours_id :
            parcours = Parcours.objects.get(pk = parcours_id)
            quizz.parcours.add(parcours) 


        tab_id , t_idd = [] , []
        for q in questions :
            tab_id.append(q.id)
            q.pk = None
            q.save()
            t_idd.append(q.id)
            quizz.questions.add(q)

        i = 0
        for tid in tab_id :
            quest = Question.objects.get(pk=tid)
            for c in quest.choices.all():
                c.pk = None
                c.question_id = t_idd[i]
                c.save()
            i+=1


        for l in levels :
            quizz.levels.add(l)
        for qr in qrandoms :
            quizz.qrandoms.add(qr)
        for t in themes :
            quizz.themes.add(t)

        quizz.folders.set(folders)    
        quizz.parcours.set(parcourses)
        quizz.groups.set(groups)

        students = set()
        for fldr_id in folders :
            folder = Folder.objects.get(pk=fldr_id)
            students.update( folder.students.all() )
        for prc_id in parcourses :
            parcours = Parcours.objects.get(pk=prc_id)
            students.update( parcours.students.all() )
        for grp_id in groups :
            group = Group.objects.get(pk=grp_id)
            students.update( group.students.all() )
        quizz.students.set(students)

        data["validation"] = "Duplication réussie. Retrouvez-le depuis le menu Groupes."
    else :
        data["validation"] = "Duplication abandonnée. Le quizz n'est pas reconnu." 

    return JsonResponse(data)



@login_required(login_url= 'index')
def clone_quizz(request, id_quizz):
    """ cloner un parcours """

    teacher = request.user.teacher
    quizz = Quizz.objects.get(pk=id_quizz) # parcours à cloner.pk = None
    questions = quizz.questions.all()
    levels = quizz.levels.all()
    qrandoms = quizz.qrandoms.all()
    themes = quizz.themes.all()

    quizz.pk = None
    quizz.teacher = teacher
    quizz.code = str(uuid.uuid4())[:8]
    quizz.save()

    parcours_id = request.session.get("parcours_id",None)  
    if parcours_id :
        parcours = Parcours.objects.get(pk = parcours_id)
        quizz.parcours.add(parcours) 


    tab_id , t_idd = [] , []
    for q in questions :
        tab_id.append(q.id)
        q.pk = None
        q.save()
        t_idd.append(q.id)
        quizz.questions.add(q)

    i = 0
    for tid in tab_id :
        quest = Question.objects.get(pk=tid)
        for c in quest.choices.all():
            c.pk = None
            c.question_id = t_idd[i]
            c.save()
        i+=1


    for l in levels :
        quizz.levels.add(l)
    for qr in qrandoms :
        quizz.qrandoms.add(qr)
    for t in themes :
        quizz.themes.add(t)

    if parcours_id :
        return redirect('show_parcours' , 0, parcours_id )
    else :
        return redirect('list_quizzes')
 

@login_required(login_url= 'index')
def clone_quizz_sequence(request, id_quizz):
    """ cloner un parcours """

    teacher = request.user.teacher
    quizz = Quizz.objects.get(pk=id_quizz) # parcours à cloner.pk = None
    questions = quizz.questions.all()
    levels = quizz.levels.all()
    qrandoms = quizz.qrandoms.all()
    themes = quizz.themes.all()

    quizz.pk = None
    quizz.teacher = teacher
    quizz.code = str(uuid.uuid4())[:8]
    quizz.save()

    parcours_id = request.session.get("parcours_id",None)  
    if parcours_id :
        parcours = Parcours.objects.get(pk = parcours_id)
        relation = Relationship.objects.create(parcours = parcours , exercise_id = None , document_id = quizz.id  , type_id = 3 , ranking =  200 , is_publish= 1 , start= None , date_limit= None, duration= 10, situation= 0 ) 
        students = parcours.students.all()
        relation.students.set(students)


    tab_id , t_idd = [] , []
    for q in questions :
        tab_id.append(q.id)
        q.pk = None
        q.save()
        t_idd.append(q.id)
        quizz.questions.add(q)

    i = 0
    for tid in tab_id :
        quest = Question.objects.get(pk=tid)
        for c in quest.choices.all():
            c.pk = None
            c.question_id = t_idd[i]
            c.save()
        i+=1


    for l in levels :
        quizz.levels.add(l)
    for qr in qrandoms :
        quizz.qrandoms.add(qr)
    for t in themes :
        quizz.themes.add(t)

    if parcours_id :
        return redirect('show_parcours' , 0, parcours_id )
    else :
        return redirect('list_quizzes')
 

@csrf_exempt
@login_required(login_url= 'index')
def ajax_chargethemes_quizz(request):
    id_level =  request.POST.get("id_level")
    id_subject =  request.POST.get("id_subject")
    teacher = request.user.teacher
    data = {}
    level =  Level.objects.get(pk = id_level)
    thms_id = request.POST.getlist("theme_id")
    quizz = set()

    if len(thms_id) > 0 :
        if thms_id[0] != "" :
            for thm_id in thms_id :
                th = Theme.objects.get(pk=thm_id)
                quizz.update(Quizz.objects.filter(subject_id = id_subject, themes=th, levels = level , is_share = 1 , is_random=0 ).exclude(teacher=teacher)) 
        else :
            quizz.update(Quizz.objects.filter(subject_id = id_subject, levels = level , is_share = 1 , is_random=0 ).exclude(teacher=teacher))  
    else :
        thms = level.themes.values_list('id', 'name').filter(subject_id=id_subject).order_by("name")
        data['themes'] = list(thms)
 
        quizzes = Quizz.objects.filter( subject_id = id_subject,  is_share = 1 , levels = level , is_random=0).exclude(teacher=teacher)
        quizz.update( quizzes )         

    data['html'] = render_to_string('tool/ajax_list_quizz_shared.html', {'quizz' : quizz, })

    return JsonResponse(data)



@login_required(login_url= 'index')
def list_quizzes(request):

    request.session["parcours_id"] = False
    teacher = request.user.teacher 
    quizzes = teacher.teacher_quizz.filter(is_archive=0 , folders=None, is_random=0) # non inclus dans un dossier
    folders = teacher.teacher_quizz.values_list("folders", flat=True).filter(is_archive=0).exclude(folders=None).distinct().order_by("levels","folders")#  inclus dans un dossier
 
    delete_session_key(request, "quizz_id")
    list_folders = list()
    for folder in folders :
        quizzes_folders = dict()
        quizzes_folders["folder"] = Folder.objects.get(pk=folder)
        quizzes_folders["quizzes"] = teacher.teacher_quizz.filter(is_archive=0 , folders=folder, is_random=0).order_by("levels") 
        list_folders.append(quizzes_folders)
 
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    is_archive = False
    nba = teacher.teacher_quizz.filter(  is_archive=1).count()

    groups = teacher.has_groups() # pour ouvrir le choix de la fenetre modale pop-up

    return render(request, 'tool/list_quizzes.html', { 'list_folders': list_folders , 'quizzes': quizzes , 'teacher': teacher, 'is_archive' : is_archive, 'nba' : nba , 'groups' : groups })



@login_required(login_url= 'index')
def all_quizzes_archived(request):


    teacher = request.user.teacher 
    quizzes = teacher.teacher_quizz.filter(is_archive=1 , folders=None, is_random=0) # non inclus dans un dossier
    folders = teacher.teacher_quizz.values_list("folders", flat=True).filter(is_archive=1).exclude(folders=None).distinct().order_by("levels","folders")#  inclus dans un dossier
    list_folders = list()
    for folder in folders :
        quizzes_folders = dict()
        quizzes_folders["folder"] = Folder.objects.get(pk=folder)
        quizzes_folders["quizzes"] = teacher.teacher_quizz.filter(is_archive=1 , folders=folder, is_random=0).order_by("levels") 
        list_folders.append(quizzes_folders)
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"
 
    is_archive = True
    return render(request, 'tool/list_quizzes.html', {   'list_folders': list_folders , 'quizzes': quizzes ,  'teacher': teacher, 'is_archive' : is_archive })


def attribute_student(nf, group_ids, parcours_ids):

    students_g = set()
    students_p = set()
    levels     = set()
    themes     = set()  

    for group_id in group_ids:
        g = Group.objects.get(pk= int(group_id))
        levels.update([g.level])
        students_g.update(g.students.values_list("user__id", flat=True))
    nf.levels.set(levels)
    cpt = 0

    for parcours_id in parcours_ids:
        cpt += 1
        p = Parcours.objects.get(pk= int(parcours_id))
        thms = p.parcours_relationship.values_list("exercise__theme", flat=True) 
        themes.update(thms)
        students_p.update(p.students.values_list("user__id", flat=True))
    nf.themes.set(themes)

    if cpt == 0 :
        nf.students.set(  students_g   ) 
    else :
        nf.students.set(  students_p )  

    return



@login_required(login_url= 'index')
def create_quizz(request):
    
    teacher = request.user.teacher
    group_id   = request.session.get("group_id",None)
    folder_id  = request.session.get("folder_id",None)
    if group_id : group = Group.objects.get(pk=group_id )
    else : group = None

    if folder_id : folder = Folder.objects.get(pk=folder_id )
    else : folder = None

    if teacher.subjects.count() == 1 :
        subject = teacher.subjects.first()
        form = QuizzForm(request.POST or None, request.FILES or None , teacher = teacher , group = group, folder = folder, initial = {'subject': subject , 'folders'  : [folder] ,  'groups'  : [group] } )
    else :
        form = QuizzForm(request.POST or None, request.FILES or None , teacher = teacher , group = group, folder = folder, initial = { 'folders'  : [folder] ,  'groups'  : [group] } )
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"
 

    if form.is_valid():
        nf = form.save(commit = False)
        nf.teacher = teacher
        nf.is_questions = 1
        nf.save()
        form.save_m2m()
        attribute_student(nf, request.POST.getlist("groups") , request.POST.getlist("parcours") ) 

        return redirect('create_question' , nf.pk , 0 )
    else:
        print(form.errors)

    context = {'form': form, 'teacher': teacher, 'group_id' : group_id , 'group' : group , 'folder' : folder }

    return render(request, 'tool/form_quizz.html', context)



@login_required(login_url= 'index')
def create_quizz_sequence(request,id) : 

    teacher = request.user.teacher
    group_id   = request.session.get("group_id",None)
    folder_id  = request.session.get("folder_id",None)
    if group_id : group = Group.objects.get(pk=group_id )
    else : group = None

    if folder_id : folder = Folder.objects.get(pk=folder_id )
    else : folder = None

    if teacher.subjects.count() == 1 :
        subject = teacher.subjects.first()
        form = QuizzForm(request.POST or None, request.FILES or None , teacher = teacher , group = group, folder = folder, initial = {'subject': subject , 'folders'  : [folder] ,  'groups'  : [group] } )
    else :
        form = QuizzForm(request.POST or None, request.FILES or None , teacher = teacher , group = group, folder = folder )
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"
 
    parcours = Parcours.objects.get(pk=id )
    if form.is_valid():
        nf = form.save(commit = False)
        nf.teacher = teacher
        nf.is_questions = 1
        nf.save()
        form.save_m2m()
        attribute_student(nf, request.POST.getlist("groups") , request.POST.getlist("parcours") )

        relation = Relationship.objects.create(parcours = parcours , exercise_id = None , document_id = nf.id  , type_id = 3 , ranking =  200 , is_publish= 1 , start= None , date_limit= None, duration= 10, situation= 0 ) 
        students = parcours.students.all()
        relation.students.set(students)

        return redirect('create_question' , nf.pk , 0 )
    else:
        print(form.errors)

    context = {'form': form, 'teacher': teacher, }

    return render(request, 'tool/form_quizz.html', context)




@login_required(login_url= 'index') 
def create_quizz_folder(request,idf):
    
    teacher = request.user.teacher
    folder  = Folder.objects.get(pk=idf) 
    group_id   = request.session.get("group_id",None)
    if group_id :
        group = Group.objects.get(pk=group_id )
        form = QuizzForm(request.POST or None, request.FILES or None , teacher = teacher , group = group, folder = folder,  initial = { 'subject' : folder.subject , 'folders' : [folder]   ,  'groups' : [group] }   )
    else :
        group = None
        form = QuizzForm(request.POST or None, request.FILES or None , teacher = teacher , group = group, folder = folder,  initial = { 'subject' : folder.subject , 'folders' : [folder]   }   )

    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    if form.is_valid():
        nf = form.save(commit = False)
        nf.teacher = teacher
        nf.is_questions = 1
        nf.save()
        form.save_m2m()

        attribute_student(nf, request.POST.getlist("groups") , request.POST.getlist("parcours") ) 

        return redirect('create_question' , nf.pk , 0 )
    else:
        print(form.errors)


    context = {'form': form, 'teacher': teacher, 'group' : group , 'folder' : folder }

    return render(request, 'tool/form_quizz.html', context)





@login_required(login_url= 'index')
def create_quizz_parcours(request,idp):
    
    teacher = request.user.teacher
    parcours  = Parcours.objects.get(pk=idp) 
    group_id   = request.session.get("group_id",None)
    folder_id  = request.session.get("folder_id",None)
    if group_id : group = Group.objects.get(pk=group_id )
    else : group = None

    if folder_id : folder = Folder.objects.get(pk=folder_id )
    else : folder = None

    form = QuizzForm(request.POST or None, request.FILES or None , teacher = teacher , group = group, folder = folder,  initial = { 'subject' : parcours.subject , 'folders' : [folder] , 'parcours' : [parcours]   ,  'groups' : [group] }   )

    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    if form.is_valid():
        nf = form.save(commit = False)
        nf.teacher = teacher
        nf.is_questions = 1
        nf.save()
        form.save_m2m()

        attribute_student(nf, request.POST.getlist("groups") , request.POST.getlist("parcours") ) 

        return redirect('create_question' , nf.pk , 0 )
    else:
        print(form.errors)


    context = {'form': form, 'teacher': teacher, 'group' : group , 'parcours' : parcours , 'folder' : folder  }

    return render(request, 'tool/form_quizz.html', context)




@login_required(login_url= 'index')
def update_quizz(request,id):    
    
    teacher = request.user.teacher 
    quizz = Quizz.objects.get(pk= id)
    group_id   = request.session.get("group_id",None)
    folder_id  = request.session.get("folder_id",None)
    if group_id : group = Group.objects.get(pk=group_id )
    else : group = None

    if folder_id : folder = Folder.objects.get(pk=folder_id )
    else : folder = None


    form = QuizzForm(request.POST or None, request.FILES or None , instance = quizz , teacher = teacher , group = group, folder = folder, )
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"
    if form.is_valid():
        nf = form.save(commit = False)
        nf.teacher = teacher
        nf.is_questions = 1
        nf.save()
        form.save_m2m()
 
        attribute_student(nf, request.POST.getlist("groups") , request.POST.getlist("parcours") ) 


        parcours_id = request.session.get("parcours_id")
        if parcours_id :
            return redirect('show_parcours' , 0 ,  parcours_id )
        else :
            return redirect('list_quizzes' )
    else:
        print(form.errors)

    context = {'form': form, 'quizz': quizz, 'teacher': teacher, }

    return render(request, 'tool/form_quizz.html', context)


@login_required(login_url= 'index')
def delete_quizz(request,id):

    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"
    quizz = Quizz.objects.get(pk= id)
    if quizz.teacher == request.user.teacher :
        quizz.delete() 

    return redirect('list_quizzes')




@login_required(login_url= 'index')
def peuplate_quizz_parcours(request,idp):

    teacher = request.user.teacher
    parcours = Parcours.objects.get(id=idp)

    quizzes = Quizz.objects.filter(parcours=parcours , is_random=0)


    context = {'parcours': parcours, 'teacher': teacher , 'quizzes' : quizzes, 'type_of_document' : 2 }

    return render(request, 'tool/form_peuplate_quizz_parcours.html', context)


@login_required(login_url= 'index')
def ajax_find_peuplate_sequence(request):

    id_parcours = request.POST.get("id_parcours",0)
    subject_id  = request.POST.get("id_subject",0) 
    level_id    = request.POST.get("id_level",None) 
    keyword     = request.POST.get("keyword",None)  

    if keyword and level_id :
        level = Level.objects.get(pk=level_id)
        quizzes = Quizz.objects.filter(  Q(teacher__user__school = request.user.school)|Q(teacher__user=request.user)|Q(is_share =  1) ,title__icontains=keyword, subject_id=subject_id,levels=level,is_numeric=1 , is_random=0  )
    elif keyword :
        quizzes = Quizz.objects.filter( Q(teacher__user__school = request.user.school)|Q(teacher__user=request.user)|Q(is_share =  1) , title__icontains=keyword, subject_id=subject_id, is_numeric=1  , is_random=0 )
    else :
        level = Level.objects.get(pk=level_id)
        quizzes = Quizz.objects.filter( Q(teacher__user__school = request.user.school)|Q(teacher__user=request.user)|Q(is_share =  1) ,  subject_id=subject_id,levels=level,is_numeric=1  , is_random=0)
    
    context = { "quizzes" : quizzes }


    data = {}
    data['html']    = render_to_string( 'tool/ajax_quizz_peuplate_sequence.html' , context)

    return JsonResponse(data)  






def show_quizz_numeric(request,id,idp):
    """ permet à un prof de voir son quizz """
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk= id)
    parcours = Parcours.objects.get(pk= idp)
    questions =  quizz.questions.filter(is_publish=1).order_by("ranking")
    context = {  "quizz" : quizz , 'parcours' : parcours  , 'questions' : questions }

    return render(request, 'tool/show_quizz_numeric.html', context)




 
def show_quizz(request,id):
    """ permet à un prof de voir son quizz """
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk= id)
    questions = quizz.questions.filter(is_publish=1).order_by("ranking")
    context = {  "quizz" : quizz , "questions" : questions }

    return render(request, 'tool/show_quizz.html', context)

 



 
def show_quizz_student(request,idgq):
    """ permet à un prof de voir son quizz """
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk= idgq)
    questions = quizz.questions.filter(is_publish=1).order_by("ranking")
    context = {  "quizz" : quizz , "questions" : questions }

    return render(request, 'tool/show_quizz.html', context)



def show_quizz_shared(request,id):
    """ permet à un prof de voir le quizz mutualisé """
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk= id)
    questions = quizz.questions.filter(is_publish=1).order_by("ranking")
    context = {  "quizz" : quizz , "questions" : questions }

    return render(request, 'tool/show_quizz_shared.html', context)


 


def result_quizz(request,id,idp=0):
    
    if idp :
        parcours = Parcours.objects.get(pk=idp)
    else :
        parcours = None 

    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk= id)
    questions =  quizz.questions.filter(is_publish=1).order_by("ranking")
    context = {  "quizz" : quizz  , 'parcours' : parcours , 'questions' : questions }

    return render(request, 'tool/result_quizz.html', context)




@login_required(login_url= 'index')
def delete_historic_quizz(request,id):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk= id)

    if quizz.teacher == request.user.teacher :
        quizz.delete()

    return redirect("list_quizzes")


 

def ajax_show_detail_question(request):
    question_id = request.POST.get("question_id",0) 
    quizz_id    = request.POST.get("quizz_id",None) 
    group_ids   = request.POST.getlist("groups",None) 
    data = {}

    students = list()
    student_set  = set()

    quizz = Quizz.objects.get(pk = quizz_id)    
    percent = "Non traité"
    percent_done = "0"

    if int(question_id) > 0 :
        question = Question.objects.get(pk=question_id)
        data_set = Answerplayer.objects.filter(question = question, quizz = quizz )
        good_answerplayers = data_set.filter(is_correct = 1 ).count()
        answerplayers = data_set.count()
        try : 
            percent = str(int((good_answerplayers*100)/answerplayers)) +"%"
        except :
            percent = "Non traité"

    for group_id in group_ids :
        group = Group.objects.get(pk = group_id)
        stds = group.students.exclude(user__username__contains="_e-test").order_by("user__last_name")
        student_set.update(stds)

    try :
        percent_done = str(int((data_set.count()*100)/len(student_set))) +"%"
    except :
        percent_done = "0%"


    total = quizz.questions.aggregate(Sum('point'))['point__sum']
    for student in student_set :
        student_dico = dict()
        student_dico["this"] = student
        if int(question_id) == 0 :
            question = None
            answer = Answerplayer.objects.filter(quizz = quizz , student = student).aggregate(Sum('score'))['score__sum']
            student_dico["answer"] = answer
        else :
            question = Question.objects.get(pk=question_id)
            try :
                answer = Answerplayer.objects.get(quizz = quizz , question = question , student = student)
                student_dico["answer"] = answer
            except: student_dico["answer"] = None

        students.append(student_dico)
    
    students.sort(key = lambda d : d["this"].user.last_name  )

    context = { "students" : students , "question" : question , "quizz" : quizz , 'percent' : percent , 'total' : total  }


    data['percent_done'] = percent_done
    data['html']    = render_to_string( 'tool/ajax_display_question_detail.html' , context)

    return JsonResponse(data)  


 




def ajax_affectation_to_group(request):
    group_id    = request.POST.get('group_id') 
    status      = request.POST.get('status')
    target_id   = request.POST.get('target_id')
    checked     = request.POST.get('checked')

    group       = Group.objects.get(pk=group_id)
    data        = {}
    html        = ""
    change_link = "no"
 
    quizz   = Quizz.objects.get(pk=target_id)
    if checked == "false" :
        quizz.groups.remove(group)
    else :
        quizz.groups.add(group)
        groups = (group,)
        attribute_all_documents_of_groups_to_all_new_students(groups)
    for g in quizz.groups.all():
        html += "<small>"+g.name +" (<small>"+ str(g.just_students_count())+"</small>)</small> "
    change_link = "change"

    data['html']        = html
    data['change_link'] = change_link
    return JsonResponse(data)


@login_required(login_url= 'index')
def ajax_show_generated(request):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    gq_id = request.POST.get("gq_id")
    data = {}  
    g_quizz = Generate_quizz.objects.get(pk= gq_id, quizz__teacher = request.user.teacher) 
    context = { "g_quizz" : g_quizz   }

    data['html'] = render_to_string('tool/ajax_show_generated.html', context)

    return JsonResponse(data)  

@login_required(login_url= 'index')
def ajax_charge_groups(request):  # utilisé par form_quizz et form_folder aussi

    teacher = request.user.teacher
    data = {} 
    subject_id = request.POST.get('id_subject', None)
    groups = Group.objects.values_list("id","name").filter(Q(teacher=teacher)|Q(teachers=teacher),subject_id =  subject_id)

    data["groups"] = list(groups)

    return JsonResponse(data)

@login_required(login_url= 'index')
def ajax_charge_groups_level(request):  # utilisé par form_folder aussi

    teacher = request.user.teacher
    data = {} 
    subject_id = request.POST.get('id_subject', None)
    level_id   = request.POST.get('id_level', None)


    if subject_id and level_id :
        groups     = Group.objects.values_list("id","name").filter(Q(teacher=teacher)|Q(teachers=teacher),subject_id =  subject_id, level_id =  level_id)
        data["groups"] = list(groups)

        # gère les propositions d'image d'accueil    
        level =  Level.objects.get(pk = level_id)
        data['imagefiles'] = None
        imagefiles = level.level_folders.values_list("vignette", flat = True).filter(subject_id=subject_id).exclude(vignette=" ").distinct()
        if imagefiles.count() > 0 :
            data['imagefiles'] = list(imagefiles)

    return JsonResponse(data)

@login_required(login_url= 'index')
def ajax_charge_folders(request):  

    teacher = request.user.teacher
    data = {} 
    group_ids = request.POST.getlist('group_ids', None)

    if len(group_ids) :
        fldrs = set()
        prcs  = set()
        for group_id in group_ids :
            group = Group.objects.get(pk=group_id)
            fldrs.update(group.group_folders.values_list("id","title").filter(is_trash=0))
            prcs.update(group.group_parcours.values_list("id","title").filter(is_trash=0,folders=None))
        data['folders'] =  list( fldrs )
        data['parcours'] =  list( prcs )
    else :
        data['folders'] =  []
        data['parcours'] =  []
    return JsonResponse(data)

@login_required(login_url= 'index')
def ajax_charge_parcours(request): # utilisé par form_quizz et form_folder aussi

    teacher = request.user.teacher
    data = {} 
    folder_ids = request.POST.getlist('folder_ids', None)

    if len(folder_ids) :
        parcourses = set()
        for folder_id in folder_ids :
            folder = Folder.objects.get(pk=folder_id)
            parcourses.update(folder.parcours.values_list("id","title").filter(is_trash=0))

        data['parcours'] =  list( parcourses )
    else :
        data['parcours'] =  []

    return JsonResponse(data)


@login_required(login_url= 'index')
def ajax_charge_parcours_without_folder(request): # utilisé que par form_folder mais placé ici pour homogénéiser la structure 

    teacher = request.user.teacher
    data = {} 
    groups_ids = request.POST.getlist('groups_ids', None)

    if len(groups_ids) :
        parcourses = set()
        for groups_id in groups_ids :
            group = Group.objects.get(pk=groups_id)
            parcourses.update(group.group_parcours.values_list("id","title").filter(is_trash=0))

        data['parcours'] =  list( parcourses )
    else :
        data['parcours'] =  []

    return JsonResponse(data)



 

def get_qr(quizz_id,group_id,mode) :

    """ fonction qui génére un historique de questions aléatoires à partir du modèle du quizz"""

    quizz = Quizz.objects.get(pk= quizz_id)
    save = get_save_new_gquizz(quizz) 

    list_qr = list(quizz.qrandoms.filter(is_publish=1))
    qrandoms = []
    nb_lqr = len(list_qr) 
    if nb_lqr == 1 :
        for i in range(quizz.nb_slide) :
            qrandoms.append(list_qr[0])  
    else :
        for i in range( nb_lqr ) :
            qrandoms.append(list_qr[i])

        nleft = math.abs(quizz.nb_slide - nb_lqr)

        for i in range(nleft) :
            random = randint(0, len(qrandoms)-1)
            qrandoms.append(list_qr[random]) 
        random.shuffle(qrandoms)
    
 
    if save :
        gquizz  = Generate_quizz.objects.create(quizz  = quizz  ,  group_id = group_id ,is_game=mode)
        i=1 
        for qrandom in qrandoms :
            qr_text  = qrandom.instruction()
            gqr = Generate_qr.objects.create( gquizz = gquizz ,  qr_text = qr_text , ranking = i , qrandom = qrandom )
            i+=1  
    else :
        qrandoms = []
        gquizz   = Generate_quizz.objects.filter(quizz  = quizz  ,  group_id = group_id ,is_game=mode).last()
        gqrs   = gquizz.generate_qr.all()[:quizz.interslide]
        for gqr in gqrs :
            gqr_dict                = dict()
            gqr_dict["duration"]    = gqr.qrandom.duration
            gqr_dict["qtype"]       = gqr.qrandom.qtype
            gqr_dict["tool"]        = gqr.qrandom.tool
            gqr_dict["calculator"]  = gqr.qrandom.calculator
            gqr_dict["title"]       = gqr.qr_text
            gqr_dict["id"]          = gqr.id
            qrandoms.append(gqr_dict)

    return quizz ,  gquizz , qrandoms , save


 
 
def show_quizz_group(request,id,idg):

    """ show quizz d'un groupe classe """
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk = id)
    questions = quizz.questions.filter(is_publish=1).order_by("ranking")
    group = Group.objects.get(pk = idg)

    context = {  "quizz" : quizz , "questions" : questions , "group" : group }     
    return render(request, 'tool/show_quizz.html', context) 


@login_required(login_url= 'index') 
def show_quizz_parcours_student(request,id,idp):

    """ show quizz d'un groupe classe """
    try :
        parcours  = Parcours.objects.get(pk=idp)
        groups    = parcours.groups.all()
        group     = Group.objects.get(pk__in = groups, students = request.user.student)
    except :
        return redirect("show_parcours_student", id)

    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk = id)
    questions = quizz.questions.filter(is_publish=1).order_by("ranking")
 
    context = {  "quizz" : quizz , "questions" : questions , "group" : group  }     
    return render(request, 'tool/show_quizz.html', context) 


 


 
def create_quizz_code(request,id,idg):
    """ show quizz d'un groupe classe """
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk = id)

    return redirect("show_quizz_group", id , idg ) 



############################################################################################################
############################################################################################################
########## Play quizz
############################################################################################################
############################################################################################################

def play_quizz_teacher(request,id,idg):
    """ Lancer d'un play quizz """
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    if request.session.get("gquizz_questions",None) :
        del request.session["gquizz_questions"] 

    if request.session.get("gquizz_id",None) :
        del request.session["gquizz_id"]

    quizz = Quizz.objects.get(pk=id)
    if quizz.is_random :
        quizz , gquizz , qrandoms, save = get_qr(id,idg,1) 
        students = gquizz.students.all() # Affichage du nom des élèves.
        nb_student = students.count()    # Nombres d'élèves.
    else :
        quizz , gquizz , questions , save = get_date_play(id,idg,1)
        students = gquizz.students.all()   # Affichage du nom des élèves.
        nb_student = students.count()      # Nombres d'élèves.
    context = {"quizz" : quizz , "gquizz" : gquizz ,   "nb_student" : nb_student , "students" : students , 'idg' : idg , 'save' : save}
    return render(request, 'tool/play_quizz_teacher.html', context)




def launch_play_quizz(request):
    """ Lancer d'un play quizz """
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    gquizz_id = request.POST.get("gquizz_id",None)
    group_id  = request.POST.get("group_id",None)
    gquizz = Generate_quizz.objects.get(pk = gquizz_id) 
    #####################################################################################
    ### les variables  group_id , gquizz  sont définies
    #####################################################################################
    #####################################################################################
    ######## Mise en session des questions
    #####################################################################################
    #####################################################################################
    gquizz_questions = request.session.get("gquizz_questions",None)
    if gquizz_questions :
        questions = gquizz_questions
        save      = False
    else :
        if gquizz.quizz.is_random :
            quizz_n , gquizz_n ,  questions ,  save = get_qr( gquizz.quizz.id , group_id , 1) ## les variables  quizz_n ,  gquizz_n  ne sont pas utilisées
        else :
            quizz_n , gquizz_n , quests , save = get_date_play(gquizz.quizz.id , group_id , 1)## les variables  quizz_n ,  gquizz_n  ne sont pas utilisées
            questions = []                                                                    ## Création des questions pour être passées en session
            for q in quests :                                                                 ## Pas d'object en JSON donc cette manip
                questions.append(q.id)                                                        ## vraiment pas top !

        request.session["gquizz_questions"] = questions
    #####################################################################################
    ### les variables  gquizz_questions , save sont définies
    #####################################################################################
    #####################################################################################
    ######## Navigation dans le quizz
    #####################################################################################
    #####################################################################################
    quizz_nav = int(request.POST.get("quizz_nav",0))
    if quizz_nav == len(questions) :
        context = { 'gquizz' : gquizz , 'group_id' : group_id }
        return render(request, 'tool/results_play_quizz.html', context)
    else :
        if gquizz.quizz.is_random :
            question = questions[quizz_nav]
        else :
            nav = questions[quizz_nav]
            question = Question.objects.get(pk = nav) 

    quizz_nav += 1

    context = {   "gquizz" : gquizz , "question" : question , "group_id" : group_id  , "save" : save , "quizz_nav" : quizz_nav }

    return render(request, 'tool/launch_play_quizz.html', context)




def this_student_can_play(student,gquizz):
    """ Vérifie qu'un joueur peut participer au quiz"""
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    can_play = False
    groups = gquizz.quizz.groups.all()
    group_set = set()
    for group in groups :
        group_set.update(group.students.all())
    if student in group_set :
        can_play = True
    return can_play


 
@login_required(login_url= 'index')
def play_quizz_student(request):
    """ Lancer le play quizz élève """

    tracker_execute_exercise(False, request.user)

    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    starter = True
    if request.method == 'POST' :
        code = request.POST.get("code",None)
        if None :
            return redirect("play_quizz_student")
        else :
            student = request.user.student
            if Generate_quizz.objects.filter(code= code).count() == 1 :
                gquizz = Generate_quizz.objects.get(code= code)
                if this_student_can_play(student,gquizz):
                    gquizz.students.add(student)
                    context = { 'student' : request.user.student , 'gquizz' : gquizz , 'starter' : True }
                    return render(request, 'tool/play_quizz_start.html', context)
            else :
                messages.error(request,"vous n'êtes pas autorisé à participer à ce quizz")

    context = {}
    return render(request, 'tool/play_quizz_student.html', context)

 

@csrf_exempt 
def ajax_quizz_show_result(request):  
    """ affichage des résultats après la question du quizz"""
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    all_results = request.POST.get("all",None)
    question_id = request.POST.get("question_id",None)
    random      = int(request.POST.get("random",0))
    data        = {}

    if random == 0 :
        answers    = Answerplayer.objects.filter(question_id = question_id, is_correct = 1 ).order_by("-score")
        no_answers = Answerplayer.objects.filter(question_id = question_id, is_correct = 0 ).order_by("-score")
    else :
        answers    = Answerplayer.objects.filter(qrandom_id = question_id, is_correct = 1 ).order_by("id")
        no_answers = Answerplayer.objects.filter(qrandom_id = question_id, is_correct = 0 ).order_by("-score")

    no_answers_display = True
    if all_results == "0" :
        answers            = answers[:3]
        no_answers_display = False
 

    context = { "answers" : answers , "no_answers" : no_answers , "no_answers_display" : no_answers_display   }
 
    data['html'] = render_to_string('tool/show_quizz_results.html', context)

    return JsonResponse(data) 



@csrf_exempt 
def ajax_display_question_for_student(request):  
    """ cree un timestamp pour signifier l'affichage de la question """ 
    data = {}
    
    gquizz_id   = request.POST.get("gquizz_id",None)
    question_id = request.POST.get("question_id",None)

    if gquizz_id and question_id :
        timestamp = datetime.now().timestamp()
        Display_question.objects.create(gquizz_id = gquizz_id, question_id = question_id, timestamp = timestamp )

    return JsonResponse(data) 



@csrf_exempt
@login_required(login_url= 'index') 
def ajax_display_question_to_student(request):  
    """ Affichage de la question aux élèves par envoie du timestamp
        Appel Ajax de la vue élève
    """
    quizz_id = request.POST.get("quizz_id",None)
    student   = request.user.student
    form      = AnswerplayerForm(request.POST or None)
    time_zone = time_zone_user(request.user)
    timestamp = time_zone.timestamp()
    data      = {}
    data['is_valid'] = "False"
    if quizz_id :
        quizz = Quizz.objects.get(pk = quizz_id)
        dq     = Display_question.objects.filter(quizz=quizz).last()

        if not student in dq.students.all() : #Si l'élève n'a pas chargé la question et que le temps est inférieur à 2 minutes
            if quizz.is_random :
                generate_qr = Generate_qr.objects.get(pk = dq.question_id)
                question    =  { "qtype" : generate_qr.qrandom.qtype , "title" : generate_qr.qr_text , "id" : generate_qr.id, "duration" : generate_qr.qrandom.duration  }
                timer       = int(generate_qr.qrandom.duration)*1000 + 5000
            else :
                question = Question.objects.get(pk = dq.question_id)
                timer    = int(question.duration)*1000 + 5000

            context = { "question" : question , "form" : form ,  "quizz_id" : quizz_id ,  "timestamp" : timestamp   }  

            data['html']     = render_to_string('tool/ajax_display_question_to_student.html', context)
            data['is_valid'] = "True"
            data['timer']    = timer

        dq.students.add(student)

    return JsonResponse(data) 
 

def answer_is_right(form , answer,question) :
    """ réponse donnée est-elle juste ? """
    right = False
    question_choices_answers = question.choices.values("answer").filter(is_correct = 1)
    if question.qtype == 1 : ## V/F
        form.answer = answer       
        if int(question.is_correct) == int(answer) :
            right = True

    elif question.qtype == 2 : ## Réponse
        choice_answer = question_choices_answers.last()
        answer_tab = answer.split("____")
        for choice in question_choices_answers :
            if choice["answer"] in answer_tab :
                right = True
                break

    elif question.qtype == 3 : ## QCM
        form.answer = answer  
        nb_c = 0       
        for choice in question_choices_answers :
            if choice["answer"] in answer :
                nb_c+=1 
        if question_choices_answers.count() == nb_c :
            right = True

    elif question.qtype == 4 :## QCS
        form.answer = answer
        for choice in question_choices_answers :
            if answer in choice.values()  :
                right = True
                break      
    return right


@login_required(login_url= 'index')
def store_student_answer(request):
    """ Lancer le play quizz élève """
    form         = AnswerplayerForm(request.POST or None)
    time         = request.POST.get("timestamp")
    timestamp    = time.split(",")[0]
    time_zone    = time_zone_user(request.user)
    milliseconds = float(round(time_zone.timestamp())) 
    timer        = float(milliseconds) - float(timestamp) - 2 # 2 secondes délai d'affichage
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    if request.method == "POST" :
        quizz_id = request.POST.get("quizz_id")
        quizz    = Quizz.objects.get(pk = quizz_id)
        if form.is_valid() :
            if quizz.is_random :
                qrandom_id = request.POST.get("question_id")
                question_id = None
            else :
                qrandom_id = None
                question_id       = request.POST.get("question_id")
                question          = Question.objects.get(pk = question_id)
                if question.qtype == 1 :
                    answer = form.cleaned_data["answer"]
                elif question.qtype == 2 :
                    answer = form.cleaned_data["answer"]
                elif question.qtype == 3 :
                    answer_brut = request.POST.getlist("answer")
                    choices = question.choices.values("answer")
                    answer = []
                    for ab in answer_brut : 
                        answer.append(choices[int(ab)]['answer'])
                else :
                    choices = question.choices.values("answer")
                    answer_brut = request.POST.get("answer")
                    answer =  choices[int(answer_brut)]['answer'] 

                answer_is_correct = answer_is_right(form, answer,question)
                if answer_is_correct :
                    score = (question.point/question.duration)*(question.duration - timer)
                else :
                    score = 0
            Answerplayer.objects.get_or_create(quizz = quizz , student = request.user.student , question = question , qrandom_id = qrandom_id , defaults = {"answer": answer , "score" :score , "timer" : timer , "is_correct" : answer_is_correct} )

        else :
            print(form.errors)
    else :
        messages.error(request,"Erreur d'enregistrement")
 

    context = { 'student' : request.user.student , 'quizz' : quizz , 'starter' : False }
    return render(request, 'tool/play_quizz_start.html', context)


@login_required(login_url= 'index')
def list_quizz_student(request):
    """ Lancer le play quizz élève """
    

    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"
    student = request.user.student
    tracker_execute_exercise(False, request.user)
    delete_session_key(request, "quizz_id")
    quizzes = set()
    for g in student.students_to_group.all() : 
        teacher_user = g.teacher.user
        today = time_zone_user(teacher_user)
        quizzes.update(g.quizz.filter(Q(is_publish = 1)| Q(start__lte= today, start__gte= today) ,is_random=0))

    context = { 'quizzes' : quizzes , }
    return render(request, 'tool/list_quizz_student.html', context)




 
def store_quizz_solution( quizz_id,student,q_id, solutions,t,hashed):
    """ Enregistrement des solutions postées 
    par les id des choices proposés"""
    answer,sep = "" , ","
    i , score  = 1 , 0
    is_correct = 0
    for ans in solutions : # est une liste d'id des réponses choisies par les réponses proposées
        question = Question.objects.get(pk=q_id)
        if question.qtype == 1 :
            if int(ans) == question.is_correct :
                is_correct = 1
                score      = question.point
        elif question.qtype == 2 :
            # choices = question.choices.all()
            # for choice in choices :
            #     if ans == choice.answer :
            #         is_correct = 1
            #         score      = question.point
            quizz = Quizz.objects.get(pk=quizz_id)
            if quizz.is_random : 
                ans = hash(str(ans))
                if ans == hashed :
                    is_correct = 1
                    score      = question.point

            else :
                ans_tab = question.answer.split('____')
                if ans in ans_tab :
                    is_correct = 1
                    score      = question.point
                    break
        else :
            choices  = question.choices.values_list('id',flat=True).filter(is_correct=1)
            corrects = 0
            a = ""
            if int(ans) in choices :
                corrects += 1
            if corrects == len(choices):
                is_correct = 1
                score      = question.point 
        if i == len(solutions):
            sep = ""
        answer += str(escape_chevron(ans))+sep

        i +=1
 
    timer = int(t)
    answ, create_ans = Answerplayer.objects.get_or_create(quizz_id  = quizz_id , student=student,question = question, qrandom_id = None, defaults={ "answer"  : answer , "score"  : score ,"timer"  : timer , "is_correct" : is_correct} )
    if not create_ans :
        Answerplayer.objects.filter(quizz_id = quizz_id , student=student,question = question, qrandom_id = None).update( answer = answer )
        Answerplayer.objects.filter(quizz_id = quizz_id , student=student,question = question, qrandom_id = None).update( score = score )
        Answerplayer.objects.filter(quizz_id = quizz_id , student=student,question = question, qrandom_id = None).update( timer = timer )
        Answerplayer.objects.filter(quizz_id = quizz_id , student=student,question = question, qrandom_id = None).update( is_correct = is_correct )

 

def goto_quizz_numeric(request,id):
    """ participation à un quizz sur poste"""
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"
    quizz = Quizz.objects.get(pk= id)
    fl = False
    #Génération des questions
    question_ids = list(quizz.questions.values_list("id",flat=True).order_by("ranking"))
    quizz_id     = request.session.get("quizz_id",None) 
    if not quizz_id :
        quizz_id                    = quizz.id
        request.session["quizz_id"] = quizz_id

        if quizz.is_ranking :
            random.shuffle(question_ids)
        
        request.session["question_ids"] = question_ids
    else :
        quizz_id     = request.session.get("quizz_id")
        question_ids = request.session.get("question_ids")

    #Génération des réponses 
    is_shuffle = False
    if quizz.is_shuffle :
        is_shuffle = True

    #Retour arrière
    is_back = False
    if quizz.is_back :
        is_back = True

    #duration   
    duration = False
    if quizz.stop and quizz.start :
        duration = quizz.stop - quizz.start 

    #####################################################################################
    ######## Navigation dans le quizz
    #####################################################################################
    #####################################################################################
    quizz_nav      = int(request.POST.get("quizz_nav",-1))
    quizz_nav_prev = int(request.POST.get("quizz_nav_prev",0))
    end_of_quizz   = False
    stop_time  = time.time()
    solutions  = request.POST.getlist("solution", None)

    if solutions and len(solutions) > 0 :
        q_id    = request.POST.get("question_id")
        start_time_tab = request.POST.get("start_time").split(",")
        start_time =  int(start_time_tab[0])
        timer =  stop_time - start_time
        today = time_zone_user(quizz.teacher.user)

    if quizz_nav == len(question_ids) :
        end_of_quizz = True
        question = None
        if quizz.is_random : fl=True
        else : fl = False
        ##request.POST["quizz_id"] = None : Plante avec les quetsions flash
        try :
            del request.session["quizz_id"] 
        except :
            pass

    elif quizz_nav > -1 : 
        question_id = question_ids[quizz_nav]
        question = Question.objects.get(pk = question_id)

    else :
        question = None

    quizz_nav += 1
    quizz_nav_prev = quizz_nav - 1


    context = {  "quizz" : quizz , "question" : question , 'duration' : duration , "quizz_nav" : quizz_nav, "quizz_nav_prev" : quizz_nav_prev ,"end_of_quizz" : end_of_quizz ,"stop_time" : stop_time , 'fl' : fl }

    return render(request, 'tool/goto_quizz_numeric.html', context)




@login_required(login_url= 'index')
def goto_quizz_student(request,id):
    """ participation à un quizz sur poste"""
    student = request.user.student
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"
    quizz = Quizz.objects.get(pk= id)

    #Génération des questions
    question_ids = list(quizz.questions.values_list("id",flat=True).order_by("ranking"))
    quizz_id     = request.session.get("quizz_id",None) 

    if not quizz_id :
        quizz_id                    = quizz.id
        request.session["quizz_id"] = quizz_id

        if quizz.is_ranking :
            random.shuffle(question_ids)
        
        request.session["question_ids"] = question_ids
    else :
        quizz_id     = request.session.get("quizz_id")
        question_ids = request.session.get("question_ids")

    #Génération des réponses 
    is_shuffle = False
    if quizz.is_shuffle :
        is_shuffle = True

    #Retour arrière
    is_back = False
    if quizz.is_back :
        is_back = True

    #duration   
    duration = False
    if quizz.stop and quizz.start :
        duration = quizz.stop - quizz.start 

    #####################################################################################
    ######## Navigation dans le quizz
    #####################################################################################
    #####################################################################################
    quizz_nav      = int(request.POST.get("quizz_nav",-1))
    quizz_nav_prev = int(request.POST.get("quizz_nav_prev",0))
    end_of_quizz   = False

    solutions  = request.POST.getlist("solution", None)
 
    #### Gestion du timer
    stop_time  = time.time()
    timer          =  stop_time
    start_time = request.POST.get("start_time",None)
    if start_time : 
        start_time_tab = start_time.split(",")
        start_time     =  int(start_time_tab[0])
        timer          =  stop_time - start_time

    q_id     = request.POST.get("question_id", None)
    if q_id :
        question = Question.objects.get(pk=q_id)
    hashed = request.POST.get("answer_type", None)
    title  = request.POST.get("title", None)

    if q_id and question.qtype == 2 :
        is_correct , score = 0 , 0
        if quizz.is_random  :
            if question.mental.html : 
                # on crée la chaine de caractère de la réponse  
                variables = question.mental.variables.split(';')
                rep, loop , ans_stu = "" , 1 , ""
                for variable in variables :
                    if loop < len(variables)  : sep, sepa = "_##_" , " ; "
                    else : sep, sepa = "" , ""
                    value = request.POST.getlist(variable)
                    new_val = value[0].replace(" ","")
                    rep += "{}={}{}".format(variable,new_val,sep)
                    ans_stu += "${}${}".format(new_val,sepa)
                    loop += 1

                if question.mental.jquery :
                    origin  = request.POST.get("origin"+quizz_nav, None)
                    value   = request.POST.get("value"+quizz_nav, None)      
                    stick   = request.POST.get("stick"+quizz_nav, None)
                    unit    = request.POST.get("unit"+quizz_nav, None)
                    frmt    = request.POST.get("format"+quizz_nav, None)

                    if frmt == 'pizza' : sol = origine + ((value-150)/stick)/unit
                    reps_hash = str(hash(solutions[quizz_nav]))
                    hashed = str(hash(sol))

                    
                ############ on la hashe
                reps_hash = str(hash(str(rep)))
            # et on la compare 
            else :
                rep = solutions[0] 
                reps_hash = str(hash(solutions[0]))
    
            if reps_hash == hashed :
                is_correct = 1
                score      = question.point

            rep = title +"<br/>"+ans_stu 

        else :
            ans_tab = question.answer.split('____')
            if len(solutions) :
                rep = solutions[0]
                if rep  in ans_tab :
                    is_correct = 1
                    score      = question.point


        timer = int(timer)
        answ, create_ans = Answerplayer.objects.get_or_create(quizz_id  = quizz_id , student=student,question = question, qrandom_id = None, defaults={ "answer"  : rep , "score"  : score ,"timer"  : timer , "is_correct" : is_correct} )
        if not create_ans :
            Answerplayer.objects.filter(quizz_id = quizz_id , student=student,question = question, qrandom_id = None).update( answer = rep , is_correct = is_correct, score = score , timer = timer )

    elif solutions and len(solutions) > 0 :
        today = time_zone_user(quizz.teacher.user)
        store_quizz_solution(quizz_id,student,q_id, solutions,timer,hashed)

    if quizz_nav == len(question_ids) :
        end_of_quizz = True
        question = None

    elif quizz_nav > -1 :
        question_id = question_ids[quizz_nav]
        question = Question.objects.get(pk = question_id)
    else :
        question = None

    quizz_nav += 1
    quizz_nav_prev = quizz_nav - 1

    context = {  "quizz" : quizz , "question" : question , 'duration' : duration , "quizz_nav" : quizz_nav, "quizz_nav_prev" : quizz_nav_prev ,"end_of_quizz" : end_of_quizz ,"stop_time" : stop_time , 'student' : student  }

    return render(request, 'tool/pass_quizz_student.html', context)




def ajax_show_retroaction(request):

    question_id = request.POST.get("question_id")
    question = Question.objects.get(pk=question_id)
    data = {}
    choices = question.choices.values_list('id', 'retroaction')
    data['choices'] = list(choices)
    return JsonResponse(data)

@login_required(login_url= 'index')
def ajax_show_my_result(request):


    student   = request.user.student
    quizz_id  = request.POST.get("quizz")

    quizz     = Quizz.objects.get(pk= quizz_id)

    questions = quizz.questions.filter(is_publish=1).order_by("ranking")

    score, total , answers = 0 , 0 , []
    for question in questions :
        try :
            a = Answerplayer.objects.get(quizz=quizz,question=question,student = request.user.student)
            score += a.score
            total += a.question.point
            answers.append(a)
        except :
            score = False

    data = {}
    data['html'] = render_to_string('tool/quizz_student_results.html', {'questions' : questions, 'quizz' : quizz , 'total' : total, 'score' : score, 'student' : student , 'answers' : answers })
 
    return JsonResponse(data)





@login_required(login_url= 'index')
def quizz_actioner(request):

    teacher = request.user.teacher 
    idqs = request.POST.getlist("selected_quizz")

    if  request.POST.get("action") == "deleter" :
        
        for idq in idqs :
            quizz = Quizz.objects.get(id=idq) 
            if quizz.teacher == teacher or request.user.is_superuser :
                quizz.levels.clear()
                quizz.themes.clear()  
                quizz.folders.clear()
                quizz.groups.clear()
                quizz.parcours.clear()
                quizz.questions.clear()
                quizz.students.clear()
                quizz.qrandoms.clear()
                quizz.delete()
            else :
                messages.error(request, "Vous ne pouvez pas supprimer ce quizz. Contacter le propriétaire.")

    elif  request.POST.get("action") == "archiver" :  
        for idq in idqs :
            quizz = Quizz.objects.get(id=idq) 
            quizz.is_archive = 1
            quizz.is_favorite = 0
            quizz.save()

    else : 
        for idq in idqs :
            quizz = Quizz.objects.get(id=idq) 
            quizz.is_archive = 0
            quizz.is_favorite = 0
            quizz.save()
     
    return redirect('list_quizzes')



@login_required(login_url= 'index')
def quizz_unarchive(request):
    teacher = request.user.teacher 
    idps = request.POST.getlist("selected_quizz") 
 
    if  request.POST.get("action") == "deleter" :  
        for idp in idps :
            quizz = Quizz.objects.get(id=idp) 
            if quizz.teacher == teacher or request.user.is_superuser :
                    quizz.delete()
                    messages.success(request, "Quizz Supprimé.")
            else :
                messages.error(request, "Vous ne pouvez pas supprimer ce quizz. Contacter le propriétaire.")
    else: 

        for idp in idps :
            quizz = Quizz.objects.get(id=idp) 
            quizz.is_archive = 0
            quizz.save()
 
    return redirect('list_quizzes')



def print_quizz_to_pdf(request):

    idq           = request.POST.get("idq",None)
    is_order      = request.POST.get("is_order",None)
    is_marker     = request.POST.get("is_mark",None) 
    is_sf         = request.POST.get("is_sf",None)
    is_correction = request.POST.get("is_correction",None) 
    point         = request.POST.get("point",None)

    if not idq :
        return redirect('list_quizzes')

    quizz = Quizz.objects.get(pk = idq) 
 
    preamb = settings.TEX_PREAMBULE_PDF_QCM
    entetes=open(preamb,"r")
    elements=entetes.read()
    entetes.close()

    elements +=r"\begin{document}"+"\n"
    today = datetime.now()

    question_ids =  list(quizz.questions.values_list("id",flat=True).filter(is_publish=1).order_by("ranking"))
    elements += r"\\"

    if len(question_ids) < 6 : nb_loop = 3
    if len(question_ids) < 8 : nb_loop = 2
    else : nb_loop = 1 


    if quizz.is_random : elements +=r"\textbf{"+quizz.title+r"}\\ \vspace{0.1cm}"
    else : elements +=r"\titreFiche{"+quizz.title+r"} \\"
    elements +=r" Nom : \ldots\ldots\ldots\ldots\ldots\ldots\ldots\ldots\ldots\ldots \\ \vspace{0.1cm}"
    if is_sf :
        elements += r"\begin{description}"
        for sf in quizz.mental_activities():
            elements += r" \savoirs{ " +  sf.content + r"}"
        elements += r"\end{description}" 
    i=1
    letters = ["A","B","C","D","E","F","G","H","I","J","K"]
    for question_id in question_ids :
        question = Question.objects.get(pk=question_id)

        if is_marker :
            if point and int(point) <= 1 : point_str = "point"
            else : point_str = "points"
            elements += r" \textbf{"+ str(i) + r".} " +question.title+r"\hfill{"+str(point)+" "+point_str+r"}\\"
        elif quizz.is_mark :    
            elements += r" \textbf{"+ str(i) + r".} " +question.title+r"\hfill{"+str(question.point)+r" points}\\"
        else :
            elements += r" \textbf{"+ str(i) + r".} " +question.title

        if question.imagefile :
            elements += r" \includegraphics[scale=1]{"+question.imagefile.url+r"}"

        if question.qtype == 2 :
            elements += r"\vspace{0,2cm}\\"
            elements += r" \hrule  "
            elements += r"\vspace{0,2cm}\\"
        elif question.qtype > 2 :
            if  question.qtype == 3 : elements += r" \textit{Vous devez cocher les réponses qui vous semblent bonnes.}"
            elif  question.qtype == 4 : elements += r" \textit{Vous devez cocher la réponse qui vous semble bonne.}" 
            elements += r"\begin{description}"
            choice_ids = list(question.choices.values_list("id",flat=True))
            if not is_order :
                random.shuffle(choice_ids)
            j=0
            for choice_id in choice_ids :
                choice = Choice.objects.get(pk=choice_id)
                if choice.imageanswer :
                    elements += r"\includegraphics[scale=1]{"+choice.imageanswer.url+r"}"
                else :
                    elements += r" \item[\quad "+letters[j]+".] " +  choice.answer
                j+=1  
            elements += r"\end{description}"
            elements += r"\vspace{0,2cm}\\"
            elements += r" \hrule  "
            elements += r"\vspace{0,2cm}\\"
        else :
            elements += r" \textit{Vous devez cocher la réponse qui vous semble bonne.}"
            elements += r"\begin{description}"
            elements += r" \item[\quad  VRAI] " 
            elements += r" \item[\quad  FAUX] " 
            elements += r"\end{description}" 
            elements += r"\vspace{0,2cm}\\"
            elements += r" \hrule  "
            elements += r"\vspace{0,2cm}\\"
        i+=1
    
    if is_correction :
        elements += r"\newpage "
        elements +=r"\titreFiche{Correction}"
        j = 1   
        for question_id in question_ids :
            question = Question.objects.get(pk=question_id)
            elements += r"\textbf{Exercice "+str(j)+r".} \\" + question.writinganswer
            elements += r"\vspace{0,2cm}\\"
            j+=1

    elements += r"\end{document}"
    elements += settings.DIR_TMP_TEX    

    ################################################################# 
    ################################################################# Attention ERREUR si non modif
    # pour windows
    #file = settings.DIR_TMP_TEX+r"\\quizz_pdf_"+str(quizz.id)
    # pour Linux
    file = settings.DIR_TMP_TEX+"/quizz_pdf_"+str(quizz.id)
    ################################################################# 
    ################################################################# 
    f_tex = open(file+".tex","w")
    f_tex.write(elements)
    f_tex.close()


    result = subprocess.run(["pdflatex", "-interaction","nonstopmode",  "-output-directory", settings.DIR_TMP_TEX ,  file ])
    return FileResponse(open(file+".pdf", 'rb'),  as_attachment=True, content_type='application/pdf')


def print_qf_to_pdf(request):

    idq           = request.POST.get("idq",None)
    is_order      = request.POST.get("is_order",None)
    is_marker     = request.POST.get("is_mark",None) 
    is_correction = request.POST.get("is_correction",None) 
    point         = request.POST.get("point",None)

    if not idq :
        return redirect('list_quizzes')

    quizz = Quizz.objects.get(pk = idq) 
 
    preamb = settings.TEX_PREAMBULE_FILE
    entetes=open(preamb,"r")
    elements=entetes.read()
    entetes.close()

    elements +=r"\begin{document}"+"\n"
    today = datetime.now()

    question_ids =  list(quizz.questions.values_list("id",flat=True).filter(is_publish=1).order_by("ranking"))
    elements += r"\\"

    if len(question_ids) < 6 : nb_loop  = 3 
    if len(question_ids) < 8 : nb_loop  = 2 
    else :  nb_loop  = 1 

    for n in range(nb_loop):
        for k in range(2):
            elements +=r"\begin{minipage}{0.5\linewidth}"

            if len(question_ids)<8 : start, stop = 0, len(question_ids)
            else : 
                quotient , reste  = len(question_ids)//2 , len(question_ids)%2
                if reste == 0 : start, stop = 0, quotient+1
                else : 
                    if k == 0 : start, stop = 0, quotient + 1
                    else : start, stop = quotient + 1, len(question_ids)

            elements += r" \includegraphics[scale=0.4]{/var/www/sacado/static/img/sacadologoqf.png}"
            elements += r" Nom : \ldots\ldots\ldots\ldots\ldots Date \ldots\ldots\ldots"
            elements += r" \vspace{0.05cm}"
            if is_marker :
                elements += r"\framebox{ \ldots / \ldots} \\ \vspace{0.1cm}"
            else : 
                elements += r" \ldots\ldots\ldots\ldots  \\ \vspace{0.1cm}"

            elements += r"\vspace{0,2cm} "
            elements +=r"\begin{tabular}{|>{\centering\arraybackslash}p{0.5cm}|p{7.5cm}|}\hline"

            for i in range(start ,stop) :
                question = Question.objects.get(pk=question_ids[i])

                elements += r" \textbf{"+ str(i+1) + r".} & " +question.title
                if question.imagefile :
                    elements += r" \includegraphics[scale=0.5]{"+question.imagefile.url+r"}"
                elements += r"\\"
                if 'Complète' in question.title or 'complète' in question.title : elements += r" \hline"
                else : elements += r" & {\scriptsize Écris ta réponse :} \vspace{1.2cm} \\ \hline"
            elements += r"\end{tabular}\end{minipage}"


    
        elements += r"\\ \noindent\raisebox{-2.8pt}[0pt][0.75\baselineskip]{\small\ding{34}}\unskip{\tiny\dotfill}"
        elements += r"\\"

    if is_correction :
        elements += r"\newpage "
        elements += r" \includegraphics[scale=1]{/var/www/sacado/static/img/sacadologoqf.png}"
        elements += r"\titreFiche{Correction}"
        j = 1   
        for question_id in question_ids :
            question = Question.objects.get(pk=question_id)
            elements += r"\textbf{Exercice "+str(j)+r".} \\ {\small" + question.title + +r"}"
            elements += r"\\" + question.writinganswer
            elements += r"\vspace{0,2cm}\\"
            j+=1

    elements += r"\end{document}"
    elements += settings.DIR_TMP_TEX    

    ################################################################# 
    ################################################################# Attention ERREUR si non modif
    # pour windows
    #file = settings.DIR_TMP_TEX+r"\\quizz_pdf_"+str(quizz.id)
    # pour Linux
    file = settings.DIR_TMP_TEX+"/quizz_pdf_"+str(quizz.id)
    ################################################################# 
    ################################################################# 
    f_tex = open(file+".tex","w")
    f_tex.write(elements)
    f_tex.close()


    result = subprocess.run(["pdflatex", "-interaction","nonstopmode",  "-output-directory", settings.DIR_TMP_TEX ,  file ])
    return FileResponse(open(file+".pdf", 'rb'),  as_attachment=True, content_type='application/pdf')


############################################################################################################
############################################################################################################
########## Question
############################################################################################################
############################################################################################################
def list_questions(request):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"
    questions = Question.objects.all()
    return render(request, 'tool/list_question.html', {'questions': questions  })




@login_required(login_url= 'index')
def create_question(request,idq,qtype):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk = idq)
    questions = quizz.questions.order_by("ranking")

    parcours_id = request.session.get("parcours_id", None)
    if parcours_id :
        parcours = Parcours.objects.values('id', 'title', 'color', 'is_sequence').get(pk = parcours_id)
    else :
        parcours = None
 
    form = QuestionForm(request.POST or None, request.FILES or None, quizz = quizz)
    formSetvar = inlineformset_factory( Question , Variableq , fields=('name','question', 'is_integer','is_notnull','minimum','maximum', 'words') , extra=0)

    ########################################################################################################################################
    ######## Attendus pour la Banque de questions
    ########################################################################################################################################
    themes   = quizz.themes.all()
    levels   = quizz.levels.all()
    subjects = quizz.teacher.subjects.all()
    if themes.count() and levels.count():
        waitings = Waiting.objects.filter(theme__subject__in=subjects , theme__in=quizz.themes.all(), level__in=quizz.levels.all())
    elif levels.count():
        waitings = Waiting.objects.filter(theme__subject__in=subjects ,level__in=quizz.levels.all())
    elif themes.count():
        waitings = Waiting.objects.filter(theme__subject__in=subjects ,theme__in=quizz.themes.all())
    ########################################################################################################################################
    ########################################################################################################################################
    qtypes = Qtype.objects.filter(is_online=1).order_by("ranking") 

    if qtype > 0 :   
        qt = Qtype.objects.get(pk=qtype)
    else :
        qt = None

    if qtype == 3 or  qtype == 4  :
        if quizz.is_numeric : extra = 2
        else : extra = 4
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct','retroaction') , extra=extra)
        form_ans = formSet(request.POST or None,  request.FILES or None)

    elif  qtype == 13 :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct','retroaction') , extra=1)
        form_ans = formSet(request.POST or None,  request.FILES or None)

    elif qtype == 5 or qtype == 11  or qtype == 15  :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','answerbis','imageanswerbis','is_correct','retroaction') , extra=2)
        form_ans = formSet(request.POST or None,  request.FILES or None)

    if qtype == 7  or qtype == 12 :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct','retroaction') , extra=2)
        form_ans = formSet(request.POST or None,  request.FILES or None)

    elif qtype == 18  :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','answerbis','imageanswerbis','is_correct','retroaction') , extra=1)
        form_ans = formSet(request.POST or None,  request.FILES or None)

    elif qtype == 6 or qtype == 8 or qtype == 10 or qtype == 14   :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct','retroaction') , extra=2)
        form_ans = formSet(request.POST or None,  request.FILES or None)
        formSubset   = inlineformset_factory( Choice , Subchoice , fields=('answer','imageanswer','is_correct','retroaction') , extra=2)
        form_sub_ans = formSubset(request.POST or None,  request.FILES or None)


    if request.method == "POST"  :
        if form.is_valid():
            nf           = form.save(commit=False) 
            nf.teacher   = request.user.teacher
            nf.qtype     = qtype          
            nf.save()
            quizz.questions.add(nf)
            form_var = formSetvar(request.POST or None,  instance = nf) 
            for form_v in form_var :
                if form_v.is_valid():
                    var = form_v.save()
                else :
                    print(form_v.errors)
            form.save_m2m() 
            if qtype == 3 or qtype == 4 or qtype == 5 or qtype == 10  or  qtype == 8 or qtype == 11 or qtype == 12 or qtype == 13 or qtype == 15 or qtype == 18 :
                form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
                for form_answer in form_ans :
                    if form_answer.is_valid():
                        form_answer.save()
            elif qtype == 6 or qtype == 14  :
                form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
                for form_answer in form_ans :
                    if form_answer.is_valid():
                        fa = form_answer.save()
                        form_sub_ans = formSubset(request.POST or None,  request.FILES or None, instance = fa)
                        for form_sub in form_sub_ans :
                            if form_sub.is_valid():
                                form_sub.save()

            return redirect('create_question' , idq,0)

        else :
            print(form.errors)

    bgcolors = ["bgcolorRed", "bgcolorBlue","bgcolorOrange", "bgcolorGreen"] 
    context = { 'bgcolors' : bgcolors , "parcours" : parcours ,  'form' : form, 'qtype' : qtype , "question" : None ,   'questions': questions,  'waitings' : waitings , "quizz_id" : quizz.id ,
                "quizz" : quizz , 'qtypes' : qtypes ,  'qt' : qt , "class_quizz_box" : False ,  'form_var' : formSetvar}

    
    if quizz.is_random :

        all_mentals = list()
        mentaltitles = Mentaltitle.objects.filter(subject = quizz.subject, is_display=1).order_by("ranking")
        if quizz.levels.count()==1 : levels = quizz.levels.all()
        else : levels = quizz.teacher.levels.all()
        for level  in levels :
            level_dict = dict()
            level_dict["level"] = level 
            list_mentals = list()
            for mentaltitle in mentaltitles :
                dict_mentals = dict()
                dict_mentals["mentaltitle"] = mentaltitle 
                mentals = Mental.objects.filter(mentaltitle  = mentaltitle, levels = level, is_display=1 ).order_by("ranking") 
                dict_mentals["mentals"] = mentals
                list_mentals.append(dict_mentals)
            level_dict["sub"] = list_mentals
            print(level ,  level_dict )
        all_mentals.append(level_dict)
 

        context.update( {  'title_type_of_question' : "Questions aléatoires" , "all_mentals" : all_mentals  })
        template = 'tool/quizz_random.html'

    elif qtype == 0 :
        context.update( {  'title_type_of_question' : "Choisir un type de question"   })
        template = 'tool/choice_type_of_question.html'

    elif qtype == 1 or qtype == 2 or qtype == 7 or qtype == 9  :
        context.update( {  'title_type_of_question' : qt.title , })
        template = 'tool/'+qt.template+'.html'

    #QCM ou QCS
    elif qtype == 3 or qtype == 4  :
        context.update( {  'title_type_of_question' : "QCM" , 'form_ans' : form_ans   })
        if quizz.is_numeric :
            template = 'tool/question_qcm_numeric.html'
        else :
            template = 'tool/question_qcm.html'

    elif qtype == 6 or qtype == 14  :
        context.update( {  'form_ans' : form_ans,'form_sub_ans' : form_sub_ans, 'title_type_of_question' : qt.title , })
        template = 'tool/'+qt.template+'.html'

    else : 
        context.update( { 'form_ans' : form_ans, 'title_type_of_question' : qt.title , })
        template = 'tool/'+qt.template+'.html'

    return render(request, template , context)





@login_required(login_url= 'index')
def update_question(request,id,idq,qtype):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk = idq)
    questions = quizz.questions.order_by("ranking")
    question = Question.objects.get(pk=id) 
    qt  = Qtype.objects.get(pk=question.qtype)

    ########################################################################################################################################
    ######## Attendus pour la Banque de questions
    ########################################################################################################################################
    themes   = quizz.themes.all()
    levels   = quizz.levels.all()
    subjects = quizz.teacher.subjects.all()
    if themes.count() and levels.count():
        waitings = Waiting.objects.filter(theme__subject__in=subjects , theme__in=quizz.themes.all(), level__in=quizz.levels.all())
    elif levels.count():
        waitings = Waiting.objects.filter(theme__subject__in=subjects ,level__in=quizz.levels.all())
    elif themes.count():
        waitings = Waiting.objects.filter(theme__subject__in=subjects ,theme__in=quizz.themes.all())
    ########################################################################################################################################
    ########################################################################################################################################
    parcours_id = request.session.get("parcours_id", None)
    if parcours_id :
        parcours = Parcours.objects.values('id', 'title', 'color').get(pk = parcours_id)
    else :
        parcours = None

    if qtype > 2 :
        formSet = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct','retroaction') , extra=0)
        form_ans = formSet(request.POST or None,  request.FILES or None, instance = question)

    form = QuestionForm(request.POST or None, request.FILES or None, instance = question,  quizz = quizz)    

    parcours_id = request.session.get("parcours_id", None)
    if parcours_id :
        parcours = Parcours.objects.values('id', 'title', 'color').get(pk = parcours_id)
    else :
        parcours = None

    formSetvar = inlineformset_factory( Question , Variableq , fields=('name','question', 'is_integer','is_notnull','minimum','maximum', 'words') , extra=0)
    formset_var = formSetvar(request.POST or None,  instance = question)

    qtypes = Qtype.objects.filter(is_online=1).order_by("ranking") 
   
    qtype = question.qtype
 
    if qtype == 3 or  qtype == 4  or  qtype == 7   or qtype == 12  or qtype == 13 :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct','retroaction') , extra=0)
        form_ans = formSet(request.POST or None,  request.FILES or None, instance = question)

    elif qtype == 5 or qtype == 11  or qtype == 15 or qtype == 18  :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','answerbis','imageanswerbis','is_correct','retroaction') , extra=0)
        form_ans = formSet(request.POST or None,  request.FILES or None, instance = question)
 
    elif qtype == 6 or qtype == 8 or qtype == 10 or qtype == 14   :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct','retroaction') , extra=0)
        form_ans = formSet(request.POST or None,  request.FILES or None, instance = question)
        formSubset   = inlineformset_factory( Choice , Subchoice , fields=('answer','imageanswer','is_correct','retroaction') , extra=0)
        form_sub_ans = formSubset(request.POST or None,  request.FILES or None)


    if request.method == "POST"  :
        if form.is_valid():
            nf           = form.save(commit=False) 
            nf.teacher   = request.user.teacher
            nf.qtype     = qtype
            nf.knowledge = knowledge
            nf.is_ia     = 1
            nf.save()
            form.save_m2m()
            for form_v in formset_var :
                if form_v.is_valid():
                    var = form_v.save()
                else :
                    print(form_v.errors)

            if qtype == 3 or qtype == 4 or qtype == 5 or qtype == 10  or  qtype == 8 or qtype == 11 or qtype == 12 or qtype == 13 or qtype == 15 or qtype == 18 :
                for form_answer in form_ans :
                    if form_answer.is_valid():
                        form_answer.save()

            elif qtype == 6 or qtype == 14  :
                form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
                for form_answer in form_ans :
                    if form_answer.is_valid():
                        fa = form_answer.save()
                        form_sub_ans = formSubset(request.POST or None,  request.FILES or None, instance = fa)
                        for form_sub in form_sub_ans :
                            if form_sub.is_valid():
                                form_sub.save()

            return redirect('create_question' , idq,0)

        else :
            print(form.errors)
 
    bgcolors = ["bgcolorRed","bgcolorBlue","bgcolorOrange","bgcolorGreen"] 
    context = { 'bgcolors' : bgcolors , "parcours" : parcours ,  'form' : form, 'qtype' : qtype , "question" : question ,   'questions': questions,  'waitings' : waitings , "quizz_id" : quizz.id ,
                "quizz" : quizz , 'qtypes' : qtypes ,  'qt' : qt , "class_quizz_box" : False ,  'form_var' : formSetvar}

    if quizz.is_random :

        all_mentals = list()
        mentaltitles = Mentaltitle.objects.filter(subject = quizz.subject, is_display=1).order_by("ranking")
        for level  in levels :
            level_dict = dict()
            level_dict["level"] = level 
            list_mentals = list()
            for mentaltitle in mentaltitles :
                dict_mentals = dict()
                dict_mentals["mentaltitle"] = mentaltitle 
                mentals = Mental.objects.filter(mentaltitle  = mentaltitle, levels = level, is_display=1 ).order_by("ranking") 
                dict_mentals["mentals"] = mentals
                list_mentals.append(dict_mentals)
            level_dict["sub"] = list_mentals
        all_mentals.append(level_dict)


        context.update( {  'title_type_of_question' : "Questions aléatoires" , "all_mentals" : all_mentals  })
        template = 'tool/quizz_random.html'

    elif qtype == 0 :
        context.update( {  'title_type_of_question' : "Choisir un type de question"   })
        template = 'tool/choice_type_of_question.html'

    elif qtype == 1 or qtype == 2 or qtype == 7 or qtype == 9  :
        context.update( {  'title_type_of_question' : qt.title , })
        template = 'tool/'+qt.template+'.html'

    #QCM ou QCS
    elif qtype == 3 or qtype == 4  :
        context.update( {  'title_type_of_question' : "QCM" , 'form_ans' : form_ans   })
        if quizz.is_numeric :
            template = 'tool/question_qcm_numeric.html'
        else :
            template = 'tool/question_qcm.html'

    elif qtype == 6 or qtype == 14  :
        context.update( {  'form_ans' : form_ans,'form_sub_ans' : form_sub_ans, 'title_type_of_question' : qt.title , })
        template = 'tool/'+qt.template+'.html'

    else : 
        context.update( { 'form_ans' : form_ans, 'title_type_of_question' : qt.title , })
        template = 'tool/'+qt.template+'.html'

    return render(request, template , context)




 
def delete_question(request,id,idq):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    question = Question.objects.get(pk= id)
    if question.quizz.count() == 0 :
        question.delete()
    else :
        messages.error(request, "  !!!  Cette question est utiolisée dans un quizz  !!! Suppression interdite.")
    return redirect ('create_question', idq, 0)



@login_required(login_url= 'index')
def remove_question(request,id,idq):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk = idq)
    if quizz.teacher == request.user.teacher :
        question = Question.objects.get(pk = id)
        quizz.questions.remove(question)
    return redirect ('create_question', idq, 0)




@login_required(login_url= 'index')
def remove_question_ia(request,id,idq):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk = idq)
    if quizz.teacher == request.user.teacher :
        question = Question.objects.get(pk = id)
        quizz.questions.remove(question)
    return redirect ('show_quizz_numeric', id )


 
def show_question(request,id):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    question = Question.objects.get(pk= id)
    context = {'form': form, "question" : question }

    return render(request, 'tool/form_question.html', context)



 
@csrf_exempt 
def ajax_find_question(request): 

    data = {}
    keywords = request.POST.get('keywords',None)
    quizz_id = request.POST.get('quizz_id',None)

    if keywords == "no_finder" :
        questions =  Question.objects.filter(is_publish=1)
    else :
        key_tab = keywords.split(" ")
        questions = set()
        for k in key_tab:
            questions.update( set(Question.objects.filter(  title__contains = k , is_publish=1  ) ) )

    data['html'] = render_to_string('tool/ajax_finder_question.html', {'all_questions' : questions , "quizz_id" : quizz_id })
    return JsonResponse(data)



 
@csrf_exempt 
def ajax_find_question_knowledge(request): 

    data = {}
    id_knowledge = request.POST.get('id_knowledge',None)
    quizz_id     = request.POST.get('quizz_id',None)

    if id_knowledge and quizz_id : 
        questions=Question.objects.filter(  knowledge__id= id_knowledge , is_publish=1  ) 

        data['html'] = render_to_string('tool/ajax_finder_question.html', {'all_questions' : questions , "quizz_id" : quizz_id })
    else :
        data['html'] = render_to_string('tool/ajax_finder_question.html', {'all_questions' : [] })
    return JsonResponse(data)






def get_this_question(request):

    question_id = request.POST.get('question_id')
    idquizz     = request.POST.get('quizz_id')
    question    = Question.objects.get(pk = question_id)
    choices     = Choice.objects.filter(question = question)    
    question.pk = None
    question.save()

    for c in choices :
        c.pk = None
        c.question = question
        c.save()

    quizz    = Quizz.objects.get(pk = idquizz)
    quizz.questions.add(question)
    data = dict() 

    return JsonResponse(data)


def clone_question(request,id,idq,qtype):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Quizz"

    quizz = Quizz.objects.get(pk = idq)
    question = Question.objects.get(pk = id)
    answer_choices = question.choices.all()
    question.pk = None
    question.save()
    quizz.questions.add(question)

    if qtype > 2 :
        for a in answer_choices :
            a.pk = None
            a.question = question
            a.save()
 
    return redirect("update_question", id = question.id , idq=quizz.id , qtype=qtype)




#######################################################################################################################
############################ Ajax  ####################################################################################
#######################################################################################################################
 
@csrf_exempt 
def question_sorter(request):  
    try :
        question_ids = request.POST.get("valeurs")
        question_tab = question_ids.split("-") 

        for i in range(len(question_tab)-1):
            Question.objects.filter(  pk = question_tab[i]).update(ranking = i)
    except :
        pass

    data = {}
    return JsonResponse(data)  

 
def play_printing_teacher(request, id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    quizz = Quizz.objects.get(id=id)
 

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="fiche_reponse_'+str(quizz.id)+'.pdf"'
    p = canvas.Canvas(response)

    img_file = 'https://sacado.xyz/static/img/sacado-icon-couleur.jpg'
    x_start , y_start = 20 , 760
    p.drawImage(img_file, x_start, y_start, width=50, preserveAspectRatio=True )
    x_starting , y_starting = 540 , 760
    p.drawImage(img_file, x_starting, y_starting, width=50, preserveAspectRatio=True )

    p.setFont("Helvetica", 8)
    p.drawString(24, 750, "SACADO"  )
    p.setFont("Helvetica", 8)
    p.drawString(544, 750, "SACADO"  )

    p.setFont("Helvetica", 16)
    p.drawString(75, 800, quizz.title +"                               "+quizz.title )    

    p.setFont("Helvetica", 12)
    p.drawString(75, 770, "Classe  : ________________________           Classe  : _______________________ " )  
    p.drawString(75, 740, "Nom :  _________________________            Nom :  _________________________" )  

    for i in range(1,quizz.questions.count()+1) :
        p.setFont("Helvetica", 12)  
        string0 = str(i)+". _____________________________          " + str(i)+". _____________________________" 
        p.drawString(75, 740-30*i, string0)


    p.line(75, 740-30*(i+1) ,550,735-30*(i+1) )

    x_start , y_start = 20 , 735-30*(i+2)
    p.drawImage(img_file, x_start, y_start, width=50, preserveAspectRatio=True )
    x_starting , y_starting = 540 , 735-30*(i+2)
    p.drawImage(img_file, x_starting, y_starting, width=50, preserveAspectRatio=True )


    p.setFont("Helvetica", 8)
    p.drawString(24, 725-30*(i+2), "SACADO"  )
    p.setFont("Helvetica", 8)
    p.drawString(544, 725-30*(i+2), "SACADO"  )



    p.setFont("Helvetica", 16)
    p.drawString(75, 740-30*(i+2), quizz.title +"                               "+quizz.title )    

    p.setFont("Helvetica", 12)
    p.drawString(75, 740-30*(i+3), "Classe  : ________________________           Classe  : _______________________ " )  
    p.drawString(75, 740-30*(i+4), "Nom :  _________________________            Nom :  _________________________" )  



    for j in range(1,quizz.questions.count()+1) :
        p.setFont("Helvetica", 12)  
        string0 = str(j)+". _____________________________          " + str(j)+". _____________________________" 
        p.drawString(75, 740-30*(i+4)-30*j, string0)


    p.line(75, 740-30*(i+5)-30*j ,550,740-30*(i+5)-30*j )



    p.line(300, 800  ,300,740-30*(i+5)-30*j )
 
    p.showPage()
    p.save()
    return response 


############################################################################################################
############################################################################################################
########## diaporama
############################################################################################################
############################################################################################################
@login_required(login_url= 'index')
def list_diaporama(request):
    
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Presentations" 
    teacher = request.user.teacher 
    diaporamas = Diaporama.objects.filter(teacher =teacher,is_archive=0 )
    nbd = Diaporama.objects.filter(teacher =teacher,is_archive=1 ).count()

    form = DiaporamaForm(request.POST or None, request.FILES or None ,teacher = teacher)
    return render(request, 'tool/list_diaporama.html', {'diaporamas': diaporamas , 'form': form, 'is_archive' : False , 'nbd' : nbd  })


@login_required(login_url= 'index')
def all_diaporama_archived(request):
    
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Presentations"


    teacher = request.user.teacher 
    diaporamas = Diaporama.objects.filter(teacher =teacher ,is_archive=1 )
    nbd = Diaporama.objects.filter(teacher =teacher,is_archive=0 ).count()
    form = DiaporamaForm(request.POST or None, request.FILES or None ,teacher = teacher)
    return render(request, 'tool/list_diaporama.html', {'diaporamas': diaporamas , 'form': form, 'is_archive' : True , 'nbd' : nbd  })


@login_required(login_url= 'index')
def diaporama_actioner(request):

    teacher = request.user.teacher 
    idps = request.POST.getlist("selected_diaporama") 

    if  request.POST.get("action") == "deleter" :  
        for idp in idps :
            diaporama = Diaporama.objects.get(id=idp) 
            if diaporama.teacher == teacher or request.user.is_superuser :
                diaporama.delete()
                messages.success(request, "La présentation "+ diaporama.title +" est supprimée.")
            else :
                messages.error(request, "Vous ne pouvez pas supprimer la présentation "+ diaporama.title +". Contacter le propriétaire.")

    else: 

        for idp in idps :
            diaporama = Diaporama.objects.get(id=idp) 
            diaporama.is_archive = 1
            diaporama.save()

    return redirect('list_diaporama')



@login_required(login_url= 'index') 
def create_diaporama(request):
    
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Presentations"

    teacher = request.user.teacher 
    form = DiaporamaForm(request.POST or None, request.FILES or None , teacher = teacher  )
 

    if form.is_valid():
        nf = form.save(commit = False)
        nf.teacher = teacher
        nf.interslide = 0
        nf.save()
        form.save_m2m()
        return redirect('create_slide' , nf.pk )
    else:
        print(form.errors)


    context = {'form': form,  }

    return render(request, 'tool/form_diaporama.html', context)


@login_required(login_url= 'index') 
def update_diaporama(request,id):
    
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Presentations"

    teacher = request.user.teacher
    diaporama = Diaporama.objects.get(pk= id)
    form = DiaporamaForm(request.POST or None, request.FILES or None , instance = diaporama , teacher = teacher  )
 
    if form.is_valid():
        nf = form.save(commit = False)
        nf.teacher = teacher
        nf.interslide = 0
        nf.save()
        form.save_m2m()

        return redirect('list_diaporama' )
    else:
        print(form.errors)

    context = {'form': form,   }

    return render(request, 'tool/form_diaporama.html', context)

def show_diaporama(request,id):
    
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Presentations"
    diaporama = Diaporama.objects.get(pk= id)
    slides = diaporama.slides.order_by("ranking")
 
    context = {  "diaporama" : diaporama ,'slides' : slides }

    return render(request, 'tool/show_diaporama.html', context)

@login_required(login_url= 'index')
def delete_diaporama(request,id):
    
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "Presentations" 
    diaporama = Diaporama.objects.get(pk= id)
    if diaporama.teacher == request.user.teacher :
        diaporama.delete() 
 
    return redirect ('list_diaporama')
############################################################################################################
############################################################################################################
########## Slides
############################################################################################################
############################################################################################################
 

@login_required(login_url= 'index')
def create_slide(request,id):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Presentations"
    diaporama = Diaporama.objects.get(pk = id)
    teacher = request.user.teacher
    form = SlideForm(request.POST or None)
 
    if request.method == "POST"  :  
        if form.is_valid():
            nf = form.save() 
            print("laaaaaa")    
            diaporama.slides.add(nf)
        else :
            print(form.errors)
 

    
    slides = diaporama.slides.order_by("ranking")

    context = { 'diaporama': diaporama, 'slides': slides, 'form': form, }

    return render(request, 'tool/form_slide.html', context)

@login_required(login_url= 'index') 
def delete_slide(request,id,idp):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Presentations"
    slide = Slide.objects.get(pk= id)
    diaporama = Diaporama.objects.get(pk = idp)
    if request.user.teacher ==  diaporama.teacher : 
        slide.delete()

 
    return redirect ('create_slide', idp)


@login_required(login_url= 'index') 
def remove_slide(request,id,idq):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Presentations" 
    diaporama = Diaporama.objects.get(pk = idq)
    if diaporama.teacher == request.user.teacher :
        slide = Slide.objects.get(pk= id)
        diaporama.slides.remove(question)
    return redirect ('create_question', idq, 0)


@login_required(login_url= 'index')
def update_slide(request,id,idp):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "Presentations" 
    diaporama = Diaporama.objects.get(pk = idp)

    slide= Slide.objects.get(pk = id)
    teacher = request.user.teacher
    form = SlideForm(request.POST or None , instance = slide  )
    if request.method == "POST" :
        if form.is_valid():
            form.save()     
            return redirect ('create_slide', idp)

    slides = diaporama.slides.order_by("ranking")
    context = { 'diaporama': diaporama, 'slides': slides, 'form': form, 'slide': slide, }

    return render(request, 'tool/form_slide.html', context)


 



@csrf_exempt 
def slide_sorter(request):  

    try :
        slide_ids = request.POST.get("valeurs")
        slide_tab = slide_ids.split("-") 

        for i in range(len(slide_tab)-1):
            Slide.objects.filter(  pk = slide_tab[i]).update(ranking = i)
    except :
        pass

    data = {}
    return JsonResponse(data)  

 
 



@csrf_exempt 
def ajax_chargewaitings(request):  

    id_level =  request.POST.get("id_level")
    id_theme =  request.POST.get("id_theme")
    data = {}

    level =  Level.objects.get(pk = id_level)

    waitings = level.waitings.values_list('id', 'name').filter(theme_id=id_theme) 
    data['waitings'] = list(waitings)
 
    return JsonResponse(data)



@csrf_exempt 
def ajax_chargeknowledges(request): 

    id_waiting =  request.POST.get("id_waiting")

    data = {}
    waiting =  Waiting.objects.get(pk = id_waiting)

    knowledges = waiting.knowledges.values_list('id', 'name')
    data['knowledges'] = list(knowledges)
 
    return JsonResponse(data)



############################################################################################################
############################################################################################################
########## Question Random
############################################################################################################
############################################################################################################
def create_questions_flash_random_variable(m_ids,quizz,noq) :

    list_of_ids = [0]*noq
    length = len(m_ids)
    i , j = 0 , 0
    while i < noq :
        for j in range (length) :
            list_of_ids[i] = int(m_ids[j])
            i+=1
            if i == noq  : break
                
    shuffle(list_of_ids) # la liste des ids des questions flash
    mentaltitles = set()

    
    same_titles = []

    print(list_of_ids)

    for mental_id in list_of_ids :
        mental = Mental.objects.get(pk=mental_id)
        variables  = dict()
        i = 1
        not_same_title = True
        print(not_same_title)
        while not_same_title :
            exec(mental.script,globals(),variables)
            title    = variables['title']
            answer   = variables['answer']
            wanswer  = variables['wans']
            if not title in same_titles or i > 10:
                same_titles.append(title)
                not_same_title = False
                question = Question.objects.create(title = title, answer = answer, mental_id = mental_id, qtype=2 , size = 48, writinganswer = wanswer)
            
            print(i)

            i+=1

        quizz.questions.add(question)
        mentaltitles.add(mental.mentaltitle)

    return mentaltitles




def create_quizz_random(request,id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    quizz = Quizz.objects.get(pk= id)
    noq = int(request.POST.get('noq',quizz.nb_slide)) 
    quizz = Quizz.objects.filter(pk=quizz.id).update(nb_slide = noq )

    mental_ids = request.POST.getlist("mental_ids",None)
    if len(mental_ids) :
        mentaltitles = create_questions_flash_random_variable(mental_ids, quizz, noq)
        quizz.mentaltitles.set( mentaltitles )

    return redirect('list_quizzes' )



############################################################################################################
############################################################################################################
########## Définitions Random    A EFFACER avec leur url
############################################################################################################
############################################################################################################


def show_quizz_random(request,id):
    """ Vue pour l'enseignant """
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "QFlash"
    quizz , gquizz , qrandoms , save = get_qr(id, None,0)  
 
    context = {  "quizz" : quizz , "gquizz" : gquizz , "qrandoms" : qrandoms  , "save" : save }

 
    return render(request, 'tool/show_quizz_random.html', context)


def show_quizz_random_group(request,id,idg):
    """ Vue pour le groupe en vidéo projection """
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "QFlash"
    group = Group.objects.get(id = idg)
    quizz ,  gquizz , qrandoms , save = get_qr(id,idg,0)

    context = {   "quizz" : quizz , "gquizz" : gquizz , "qrandoms" : qrandoms , "group" : group  , "save" : save }
 
    return render(request, 'tool/show_quizz_random.html', context)


@login_required(login_url= 'index')
def list_qrandom(request):
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "QFlash"
    if request.user.is_superuser :
        qrandoms = Qrandom.objects.all()
        context = {  "qrandoms" : qrandoms  }
        return render(request, 'tool/list_qrandom.html', context)
    else :
        return redirect('index')


@login_required(login_url= 'index')
def create_qrandom(request):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "QFlash"
    teacher = request.user.teacher
    if request.user.is_superuser :
        form = QrandomForm(request.POST or None )
        formSet = inlineformset_factory( Qrandom , Variable , fields=('name','qrandom', 'is_integer','minimum','maximum', 'words') , extra=1)

        if request.method == "POST"  :
            if form.is_valid():
                qr = form.save(commit = False)
                qr.teacher = teacher
                qr.save()
                form_var = formSet(request.POST or None,  instance = qr) 
                for form_v in form_var :
                    if form_v.is_valid():
                        var = form_v.save()
                    else :
                        print(form_v.errors)
                    files = request.FILES.getlist("images-"+var.name)
                    for file in files :
                        VariableImage.objects.create(variable = var , image = file)
 

                return redirect('create_qrandom' )
        context = {  "form" : form , "form_var" : formSet ,'teacher' : teacher,'qrandom' : None }
        return render(request, 'tool/form_qrandom.html', context)

    else :
        return redirect('index')

@login_required(login_url= 'index')
def update_qrandom(request,id):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "QFlash"
    teacher = request.user.teacher
    if request.user.is_superuser :
        qr = Qrandom.objects.get(pk=id)
        form = QrandomForm(request.POST or None , instance = qr )
        formSet = inlineformset_factory( Qrandom , Variable , fields=('name','qrandom', 'is_integer','minimum','maximum','words') , extra=0)
        form_var = formSet(request.POST or None,  request.FILES or None , instance = qr) 
        if request.method == "POST"  :
            if form.is_valid():
                qr = form.save(commit = False)
                qr.teacher = teacher
                qr.save()
                
                for form_v in form_var :
                    if form_v.is_valid():
                        form_v.save()
                    else :
                        print(form_v.errors)

                return redirect('list_qrandom')
        context = {  "form" : form , "form_var" : form_var ,'teacher' : teacher ,'qrandom' : qr }
        return render(request, 'tool/form_qrandom.html', context)
        
    else :
        return redirect('index')


@login_required(login_url= 'index')
def delete_qrandom(request,id):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "QFlash"
    if request.user.is_superuser :
        qr = Qrandom.objects.get(pk= id)
        qr.delete()
    else :
        return redirect('index')
 
    return redirect("list_qrandom")


@login_required(login_url= 'index')
def admin_qrandom(request,id_level):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "QFlash"
    if request.user.is_superuser :
        level = Level.objects.get(pk = id_level)
        data = all_datas(level)
        return render(request, 'tool/list_qr.html', {'data': data ,'level': level   })
    else :
        return redirect('index')



@login_required(login_url= 'index')
def create_qrandom_admin(request,id_knowledge):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "QFlash"
    teacher = request.user.teacher
    if request.user.is_superuser :
        knowledge = Knowledge.objects.get(pk=id_knowledge)
        form = QrandomForm(request.POST or None )
        formSet = inlineformset_factory( Qrandom , Variable , fields=('name','qrandom', 'is_integer','minimum','maximum', 'words') , extra=1)

        if request.method == "POST"  :
            if form.is_valid():
                qr = form.save(commit = False)
                qr.teacher = teacher
                qr.save()
                form_var = formSet(request.POST or None,  instance = qr) 
                for form_v in form_var :
                    if form_v.is_valid():
                        var = form_v.save()
                    else :
                        print(form_v.errors)
                    files = request.FILES.getlist("images-"+var.name)
                    for file in files :
                        VariableImage.objects.create(variable = var , image = file)

                return redirect('create_qrandom_admin' , id_knowledge)

        context = {  "form" : form , "form_var" : formSet ,'teacher' : teacher,'qrandom' : None , 'knowledge' : knowledge }
        return render(request, 'tool/form_qrandom_admin.html', context)

    else :
        return redirect('index')


@login_required(login_url= 'index')
def update_qrandom_admin(request,id_knowledge,id):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "QFlash"
    teacher = request.user.teacher
    if request.user.is_superuser :
        knowledge = Knowledge.objects.get(pk=id_knowledge)
        qr = Qrandom.objects.get(pk = id)
        form = QrandomForm(request.POST or None , instance =  qr )
        formSet = inlineformset_factory( Qrandom , Variable , fields=('name','qrandom', 'is_integer','minimum','maximum', 'words') , extra=0)
        form_var = formSet(request.POST or None,  instance = qr)

        if request.method == "POST"  :
            if form.is_valid():
                qr = form.save(commit = False)
                qr.teacher = teacher
                qr.save()
                for form_v in form_var :
                    if form_v.is_valid():
                        var = form_v.save()
                    try :
                        files = request.FILES.getlist("images-"+var.name)
                        for file in files :
                            VariableImage.objects.create(variable = var , image = file)
                    except :
                        pass
 
                return redirect('admin_qrandom' , knowledge.level.id)

        context = {  "form" : form , "form_var" : form_var ,'teacher' : teacher,'qrandom' : None , 'knowledge' : knowledge }
        return render(request, 'tool/form_qrandom_admin.html', context)

    else :
        return redirect('index')


def show_qrandom_admin(request,id):
    
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "QFlash"
    qrandom = Qrandom.objects.get(pk = id)
 
    return render(request, 'tool/show_qr.html', {'qrandom': qrandom      })


#####################################################################################################################################
#####################################################################################################################################
####    admin_question_ia
#####################################################################################################################################
#####################################################################################################################################

def this_level(level_id):
    if 1<level_id <13 :
        level_id = level_id - 1
    elif level_id == 14 :
        level_id = 14
    elif level_id == 1 :
        level_id = 14
    else :
        level_id = 12
    return level_id




@login_required(login_url= 'index')
def admin_question_ia(request,id_level):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    if request.user.is_superuser :
 
        id_level = this_level(id_level)
        level = Level.objects.get(pk = id_level)
        data = all_datas_qia(level)
        return render(request, 'tool/list_questions_ia.html', {'data': data ,'level': level   })
    else :
        return redirect('index')


@login_required(login_url= 'index')
def admin_create_question_ia(request,idk,qtype):


    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    knowledge = Knowledge.objects.get(pk=idk)
    form = QuestionKForm(request.POST or None, request.FILES or None, knowledge = knowledge)

    formSetvar = inlineformset_factory( Question , Variableq , fields=('name','question', 'is_integer','is_notnull','minimum','maximum', 'words') , extra=0)
 

    qtypes = Qtype.objects.filter(is_online=1).order_by("ranking") 

    if qtype > 0 :   
        qt = Qtype.objects.get(pk=qtype)
    else :
        qt = None

    if qtype == 3 or  qtype == 4  or  qtype == 7  or qtype == 12 :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct','retroaction') , extra=2)
        form_ans = formSet(request.POST or None,  request.FILES or None)

    elif  qtype == 13 :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct','retroaction') , extra=1)
        form_ans = formSet(request.POST or None,  request.FILES or None)

    elif qtype == 5 or qtype == 11  or qtype == 15  :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','answerbis','imageanswerbis','is_correct','retroaction') , extra=2)
        form_ans = formSet(request.POST or None,  request.FILES or None)

    elif qtype == 18  :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','answerbis','imageanswerbis','is_correct','retroaction') , extra=1)
        form_ans = formSet(request.POST or None,  request.FILES or None)

    elif qtype == 6 or qtype == 8 or qtype == 10 or qtype == 14   :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct','retroaction') , extra=2)
        form_ans = formSet(request.POST or None,  request.FILES or None)
        formSubset   = inlineformset_factory( Choice , Subchoice , fields=('answer','imageanswer','is_correct','retroaction') , extra=2)
        form_sub_ans = formSubset(request.POST or None,  request.FILES or None)


    if request.method == "POST"  :
        if form.is_valid():
            nf           = form.save(commit=False) 
            nf.teacher   = request.user.teacher
            nf.qtype     = qtype
            nf.knowledge = knowledge            
            nf.is_ia     = 1
            nf.save()
            form_var = formSetvar(request.POST or None,  instance = nf) 
            for form_v in form_var :
                if form_v.is_valid():
                    var = form_v.save()
                else :
                    print(form_v.errors)
                # files = request.FILES.getlist("images-"+var.name)
                # for file in files :
                #     VariableqImage.objects.create(variable = var , image = file)


            form.save_m2m() 
            if qtype == 3 or qtype == 4 or qtype == 5 or qtype == 10  or  qtype == 8 or qtype == 11 or qtype == 12 or qtype == 13 or qtype == 15 or qtype == 18 :
                form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
                for form_answer in form_ans :
                    if form_answer.is_valid():
                        form_answer.save()
            elif qtype == 6 or qtype == 14  :
                form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
                for form_answer in form_ans :
                    if form_answer.is_valid():
                        fa = form_answer.save()
                        form_sub_ans = formSubset(request.POST or None,  request.FILES or None, instance = fa)
                        for form_sub in form_sub_ans :
                            if form_sub.is_valid():
                                form_sub.save()


            id_level = this_level( knowledge.level.id + 2 )

            return redirect('admin_question_ia' , id_level )

        else :
            print(form.errors)

 
    bgcolors = ["bgcolorRed", "bgcolorBlue","bgcolorOrange", "bgcolorGreen"] 
    context = { 'bgcolors' : bgcolors  ,    'knowledge': knowledge , 'form' : form, 'qtype' : qtype , "question" : None , 
                "quizz" : None , 'qtypes' : qtypes ,  'qt' : qt , "class_quizz_box" : False ,  'form_var' : formSetvar}

    if qtype == 0 :
        context.update( {  'title_type_of_question' : "Choisir un type de question"   })
        template = 'tool/choice_type_of_question.html'

    elif   qtype == 6 or qtype == 14  :
        context.update( {  'form_ans' : form_ans,'form_sub_ans' : form_sub_ans, 'title_type_of_question' : qt.title , })
        template = 'tool/'+qt.template+'.html'
    
    elif   qtype == 7 or qtype == 9  :
        context.update( {  'title_type_of_question' : qt.title , })
        template = 'tool/'+qt.template+'.html'
    
    
    else : 
        if qtype > 2 :
            context.update( { 'form_ans' : form_ans ,   })  
        context.update( {  'title_type_of_question' : qt.title , })
        template = 'tool/'+qt.template+'.html'


    return render(request, template , context)


@login_required(login_url= 'index')
def admin_update_question_ia(request,idk,idq):

    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    question = Question.objects.get(pk=idq) 
    qt  = Qtype.objects.get(pk=question.qtype)

    knowledge = Knowledge.objects.get(pk=idk)
    form = QuestionKForm(request.POST or None, request.FILES or None, instance = question, knowledge = knowledge)

    formSetvar = inlineformset_factory( Question , Variableq , fields=('name','question', 'is_integer','is_notnull','minimum','maximum', 'words') , extra=0)
    formset_var = formSetvar(request.POST or None,  instance = question)


    qtypes = Qtype.objects.filter(is_online=1).order_by("ranking") 
   
    qtype = question.qtype
 
    if qtype == 3 or  qtype == 4  or  qtype == 7   or qtype == 12  or qtype == 13 :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct','retroaction') , extra=0)
        form_ans = formSet(request.POST or None,  request.FILES or None, instance = question)

    elif qtype == 5 or qtype == 11  or qtype == 15 or qtype == 18  :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','answerbis','imageanswerbis','is_correct','retroaction') , extra=0)
        form_ans = formSet(request.POST or None,  request.FILES or None, instance = question)
 
    elif qtype == 6 or qtype == 8 or qtype == 10 or qtype == 14   :
        formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct','retroaction') , extra=0)
        form_ans = formSet(request.POST or None,  request.FILES or None, instance = question)
        formSubset   = inlineformset_factory( Choice , Subchoice , fields=('answer','imageanswer','is_correct','retroaction') , extra=0)
        form_sub_ans = formSubset(request.POST or None,  request.FILES or None)


    if request.method == "POST"  :
        if form.is_valid():
            nf           = form.save(commit=False) 
            nf.teacher   = request.user.teacher
            nf.qtype     = qtype
            nf.knowledge = knowledge
            nf.is_ia     = 1
            nf.save()
            form.save_m2m()
            for form_v in formset_var :
                if form_v.is_valid():
                    var = form_v.save()
                else :
                    print(form_v.errors)
                # files = request.FILES.getlist("images-"+var.name)
                # for file in files :
                #     VariableqImage.objects.create(variable = var , image = file)

            if qtype == 3 or qtype == 4 or qtype == 5 or qtype == 10  or  qtype == 8 or qtype == 11 or qtype == 12 or qtype == 13 or qtype == 15 or qtype == 18 :
                for form_answer in form_ans :
                    if form_answer.is_valid():
                        form_answer.save()

            elif qtype == 6 or qtype == 14  :
                form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
                for form_answer in form_ans :
                    if form_answer.is_valid():
                        fa = form_answer.save()
                        form_sub_ans = formSubset(request.POST or None,  request.FILES or None, instance = fa)
                        for form_sub in form_sub_ans :
                            if form_sub.is_valid():
                                form_sub.save()

            id_level = this_level( knowledge.level.id + 2 )

            return redirect('admin_question_ia' , id_level )

        else :
            print(form.errors)

 
    bgcolors = ["bgcolorRed", "bgcolorBlue","bgcolorOrange", "bgcolorGreen"] 
    context = { 'bgcolors' : bgcolors  , 'knowledge': knowledge , 'form' : form, 'qtype' : qtype ,  "question" : question , 
                'form_var' : form_var  , "quizz" : None , 'qtypes' : qtypes ,  'qt' : qtype , "class_quizz_box" : False ,  }

    if qtype == 0 :
        context.update( { 'title_type_of_question' : qt.title , })
        template = 'tool/choice_type_of_question.html'

    elif   qtype == 6 or qtype == 14  :
        context.update( { 'form_ans' : form_ans,'form_sub_ans' : form_sub_ans, 'title_type_of_question' : qt.title , })
        template = 'tool/'+qt.template+'.html'
    
    elif   qtype == 7 or qtype == 9  :
        context.update( { 'title_type_of_question' : qt.title ,   }) 
        template = 'tool/'+qt.template+'.html'
    
    else : 
        if qtype > 2 :
            context.update( { 'form_ans' : form_ans   })  
        context.update( { 'title_type_of_question' : qt.title ,   }) 
        template = 'tool/'+qt.template+'.html'

    return render(request, template , context)



@login_required(login_url= 'index')
def admin_delete_question_ia(request,idk,idq):


    if request.user.is_superuser :
        knowledge = Knowledge.objects.get(pk=idk)
        question  = Question.objects.get(pk=idq)
        qtype = question.qtype
        qt = Qtype.objects.get(pk=qtype)
        question.delete()

        request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
        data = all_datas_qia( knowledge.level )
        return render(request, 'tool/list_questions_ia.html', {'data': data ,'level': knowledge.level   })
    else :
        return redirect('index')




@login_required(login_url= 'index')
def admin_duplicate_question_ia(request,idk,idq):

    if request.user.is_superuser :
        knowledge = Knowledge.objects.get(pk=idk)
        question  = Question.objects.get(pk=idq)
        choices = question.choices.all()        
        question.pk = None
        question.save()
        for c in choices:
            subchoices = c.subchoices.all()
            c.pk = None
            c.question = question
            c.save()            
            for subchoice in subchoices : 
                subchoice.pk = None
                subchoice.choice = c
                subchoice.save()

        request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
        data = all_datas_qia( knowledge.level )
        return render(request, 'tool/list_questions_ia.html', {'data': data ,'level': knowledge.level   })
    else :
        return redirect('index')



@login_required(login_url= 'index')
def admin_show_question_ia(request,idk,idq):
    pass




@csrf_exempt 
def ajax_is_ia(request): 

    idq =  request.POST.get("idq")
    data = {}
    question = Question.objects.get(pk = idq)
    if question.is_ia : question.is_ia = 0
    else :  question.is_ia =1
    question.save()

    return JsonResponse(data)

#####################################################################################################################################
#####################################################################################################################################
####    Question flash
#####################################################################################################################################
#####################################################################################################################################
 

@login_required(login_url= 'index')
def admin_mentals(request,idl):
    request.session["parcours_id"] = False 
    request.session["admin_create_qf_level_id"] = idl 
    level = Level.objects.get(pk=idl)
    mentals = Mental.objects.filter(Q(levels=level)|Q(levels=None)).order_by("mentaltitle","ranking")#filter(levels=level)
    return render(request, 'tool/admin_list_mental.html', { 'mentals': mentals ,'level' : level   })


@login_required(login_url= 'index')
def admin_create_update_mental(request,idm):
    levels = Level.objects.exclude(pk=13).order_by("ranking")
    idl    = request.session.get("admin_create_qf_level_id",1)
    level = Level.objects.get(pk=idl)
    if idm :
        mental = Mental.objects.get(pk=idm)
        form  = MentalForm(request.POST or None,instance = mental)
    else :
        form  = MentalForm(request.POST or None)
        mental = None
    if request.method == "POST" :
        if form.is_valid():
            form.save() 
            return redirect('admin_mentals', level.id )
    return render(request, 'tool/admin_form_mental.html', {  'form': form , 'mental' : mental , 'levels' : levels, 'idl' : idl , 'level' : level })



@login_required(login_url= 'index')
def admin_create_update_mentaltitle(request,idm):
    levels = Level.objects.exclude(pk=13).order_by("ranking")    
    idl    = request.session.get("admin_create_qf_level_id",1)    
    level = Level.objects.get(pk=idl)
    mentaltitles = Mentaltitle.objects.order_by("ranking")
    if idm :
        mentaltitle = Mentaltitle.objects.get(pk=idm)
        form  = MentaltitleForm(request.POST or None,instance = mentaltitle)
    else :
        mentaltitle = None
        form  = MentaltitleForm(request.POST or None )    
    if request.method == "POST" :
        if form.is_valid():
            form.save()
    return render(request, 'tool/admin_form_mentaltitle.html', {  'form': form , 'mentaltitle' : mentaltitle , 'levels' : levels, 'idl' : idl  , 'level' : level , 'mentaltitles' : mentaltitles })



@login_required(login_url= 'index')
def admin_delete_mental(request,idm):
    idl   = request.session.get("admin_create_qf_level_id",1)
    level = Level.objects.get(pk=idl)
    Mental.objects.filter(pk=idm).delete() 
    return redirect('admin_mentals', level.id )


@login_required(login_url= 'index')
def admin_delete_mentaltitle(request,idm):
    idl    = request.session.get("admin_create_qf_level_id",1)
    level = Level.objects.get(pk=idl)
    Mentaltitle.objects.filter(pk=idm).delete() 
    return redirect('admin_mentals', level.id )



@login_required(login_url= 'index')
def admin_duplicate_mental(request,idm):
    idl    = request.session.get("admin_create_qf_level_id",1)
    level = Level.objects.get(pk=idl)
    mental      = Mental.objects.get(pk=idm)
    mental.pk   = None
    mental.save()
    return redirect('admin_mentals', level.id )






@login_required(login_url= 'index')
def list_questions_flash(request):

    request.session["parcours_id"] = False
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "QFlash"


    teacher = request.user.teacher 
    quizzes = teacher.teacher_quizz.filter(is_archive=0 , is_random=1, folders=None).order_by("levels","-id") # non inclus dans un dossier, 
    delete_session_key(request, "quizz_id")

    grps = teacher.groups.filter(is_hidden=0)
    shared_grps_id = teacher.teacher_sharingteacher.values_list("group_id", flat=True) 
    sgps    = Group.objects.filter(pk__in=shared_grps_id,is_hidden=0)
    groupes =  grps | sgps
    groups  = groupes.order_by("level__ranking") 
    return render(request, 'tool/list_questions_flash.html', { 'quizzes': quizzes , 'teacher': teacher , 'groups': groups })




@login_required(login_url= 'index')
def list_questions_flash_student(request):

    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "QFlash"
    student = request.user.student
    tracker_execute_exercise(False, request.user)
    delete_session_key(request, "quizz_id")
    quizzes = set()
    for g in student.students_to_group.all() : 
        teacher_user = g.teacher.user
        today = time_zone_user(teacher_user)
        quizzes.update(g.quizz.filter(Q(is_publish = 1)| Q(start__lte= today, start__gte= today) ,is_random=1))

    context = { 'quizzes' : quizzes , }
    return render(request, 'tool/list_questions_flash_student.html', context)





@login_required(login_url= 'index')
def create_questions_flash(request,id):
    teacher = request.user.teacher
    form = QFlashForm(request.POST or None, request.FILES or None , teacher = teacher )
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "QFlash"

    if request.method == "POST":
        if form.is_valid():
            nf = form.save(commit = False)
            nf.teacher = teacher
            nf.is_questions = 1
            nf.is_random = 1
            nf.is_archive = 0
            nf.save()
            form.save_m2m()

            for group_id in request.POST.getlist("groups") :
                group = Group.objects.get(pk=group_id)
                nf.students.set(group.students.all())

            mental_ids = request.POST.getlist("mental_ids",None)
            if len(mental_ids) :
                mentaltitles = create_questions_flash_random_variable(mental_ids, nf, nf.nb_slide)
                nf.mentaltitles.set( mentaltitles )  

            return redirect('list_questions_flash')
        else:
            print(form.errors)


    mentals = Mental.objects.filter(mentaltitle__subject__id = 1 ).order_by("mentaltitle")
    context = {'form': form, 'teacher': teacher,  'mentals' : mentals   }

    return render(request, 'tool/form_question_flash.html', context)



@login_required(login_url= 'index')
def update_questions_flash(request,id):
    teacher = request.user.teacher
    quizz   = Quizz.objects.get(pk=id)

    form = QFlashForm(request.POST or None, request.FILES or None , teacher = teacher , instance = quizz)
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "QFlash"

    if request.method == "POST":
        if form.is_valid():
            nf = form.save(commit = False)
            nf.teacher = teacher
            nf.is_questions = 1
            nf.is_random = 1
            if nf.is_video == 0 : nf.is_numeric = 1
            nf.is_archive = 0
            nf.save()
            form.save_m2m()
            for group_id in request.POST.getlist("groups") :
                group = Group.objects.get(pk=group_id)
                nf.students.set(group.students.all())

            mental_ids = request.POST.getlist("mental_ids",None)
            if len(mental_ids) :
                mentaltitles = create_questions_flash_random_variable(mental_ids, nf, nf.nb_slide)
                nf.mentaltitles.set( mentaltitles )  
                    
            return redirect('list_questions_flash')
        else:
            print(form.errors)


    mentals = Mental.objects.filter(mentaltitle__subject__id = 1 ).order_by("mentaltitle")
    context = {'form': form, 'teacher': teacher,  'mentals' : mentals   }

    return render(request, 'tool/form_question_flash.html', context)



@login_required(login_url= 'index')
def duplicate_questions_flash(request,id):
    quizz      = Quizz.objects.get(pk=id)
    mental_ids = quizz.questions.values_list("mental_id",flat=True).distinct()
    quizz.pk   = None
    quizz.code = str(uuid.uuid4())[:8]
    quizz.save()
    if len(mental_ids) :
        mentaltitles = create_questions_flash_random_variable(mental_ids, quizz, quizz.nb_slide)
        quizz.mentaltitles.set( mentaltitles ) 

    return redirect('list_questions_flash')


@login_required(login_url= 'index') 
def show_questions_flash(request,id):
    """ permet à un prof de voir son quizz """
    
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "QFlash"
    quizz = Quizz.objects.get(pk= id)
    questions = quizz.questions.filter(is_publish=1).order_by("ranking")
    try :
        level = quizz.levels.first()
    except :
        level = None
    context = {  "quizz" : quizz , "questions" : questions , "is_test_admin" : False , 'level' : level }

    return render(request, 'tool/show_question_flash.html', context)


@login_required(login_url= 'index')
def goto_questions_flash(request,id):
    pass

@login_required(login_url= 'index')
def delete_questions_flash(request,id):
    quizz = Quizz.objects.get(pk = id)
    questions = quizz.questions.all()
    for question in questions :
        if question.quizz.count()==1:
            question.delete()
    quizz.delete()
    messages.success(request,'Questions flash Supprimée.')
    return redirect('list_questions_flash')



@login_required(login_url= 'index')
def delete_all_questions_flash(request):

    selected_checkboxes = request.POST.getlist('selected_checkbox',[])
    teacher = request.user.teacher
    for selected_checkbox in selected_checkboxes :
        quizz = Quizz.objects.get(pk = selected_checkbox, teacher = teacher)
        questions = quizz.questions.all()
        for question in questions :
            if question.quizz.count()==1:
                question.delete()
        quizz.delete()
    messages.success(request,'Questions flash Supprimée.')
    return redirect('list_questions_flash')




@login_required(login_url= 'index')
def admin_test_mental(request,id):

    teacher = request.user.teacher
    form = QFlashForm(request.POST or None, request.FILES or None , teacher = teacher )
    request.session["tdb"] = "Documents"
    request.session["subtdb"] = "QFlash"
    mental = Mental.objects.get(pk=id)
 
    quizz = Quizz.objects.create(title = "Question_Flash_Admin", teacher = teacher, color = '#5d4391', subject = mental.mentaltitle.subject ,
                                 is_questions = 1, is_random = 1,nb_slide = 10,is_result =1 , is_result_final = 1,is_archive = 0,interslide = 10)

    quizz.levels.set(mental.levels.all())
    quizz.mentaltitles.add(mental.mentaltitle)
    create_questions_flash_random_variable([id], quizz, 10)

    questions = quizz.questions.filter(is_publish=1).order_by("ranking")
    context = {  "quizz" : quizz , "questions" : questions , "is_test_admin" : True }

    return render(request, 'tool/show_question_flash.html', context)
 


def admin_test_mental_print(request,id):

    mental = Mental.objects.get(pk=id)
    quizz = Quizz.objects.create(title = "Question_Flash_Admin", teacher = teacher, color = '#5d4391', subject = mental.mentaltitle.subject ,
                                 is_questions = 1, is_random = 1,nb_slide = 10,is_result =1 , is_result_final = 1,is_archive = 0,interslide = 10)
    quizz.levels.set(mental.levels.all())
    quizz.mentaltitles.add(mental.mentaltitle)
    create_questions_flash_random_variable([id], quizz, 10)

    preamb = settings.TEX_PREAMBULE_PDF_QCM
    entetes=open(preamb,"r")
    elements=entetes.read()
    entetes.close()

    elements +=r"\begin{document}"+"\n"
    today = datetime.now()

    question_ids =  list(quizz.questions.values_list("id",flat=True).filter(is_publish=1).order_by("ranking"))
    elements += r"\\"

    if len(question_ids) < 6 : nb_loop  = 3 
    if len(question_ids) < 8 : nb_loop  = 2 
    else :  nb_loop  = 1 

    for n in range(nb_loop):
        for k in range(2):
            elements +=r"\begin{minipage}{0.5\linewidth}"

            if len(question_ids)<8 : start, stop = 0, len(question_ids)
            else : 
                quotient , reste  = len(question_ids)//2 , len(question_ids)%2
                if reste == 0 : start, stop = 0, quotient+1
                else : 
                    if k == 0 : start, stop = 0, quotient + 1
                    else : start, stop = quotient + 1, len(question_ids)

            elements += r" \includegraphics[scale=0.4]{/var/www/sacado/static/img/sacadologoqf.png}"
            elements += r" Nom : \ldots\ldots\ldots\ldots\ldots Date \ldots\ldots\ldots"
            elements += r"\framebox{ \ldots / \ldots} \\ \vspace{0.1cm}"

            elements +=r"\begin{tabular}{|>{\centering\arraybackslash}p{0.5cm}|p{7.5cm}|}\hline"

            for i in range(start ,stop) :
                question = Question.objects.get(pk=question_ids[i])

                elements += r" \textbf{"+ str(i+1) + r".} & " +question.title
                if question.imagefile :
                    elements += r" \includegraphics[scale=0.5]{"+question.imagefile.url+r"}"
                elements += r"\\"
                if 'complète' in question.title or 'compléte' in question.title : elements += r" \hline"
                else : elements += r" & {\scriptsize Écris ta réponse :} \vspace{1.2cm} \\ \hline"
            elements += r"\end{tabular}\end{minipage}"

        elements += r"\\ \noindent\raisebox{-2.8pt}[0pt][0.75\baselineskip]{\small\ding{34}}\unskip{\tiny\dotfill}"
        elements += r"\\"

    elements += r"\end{document}"
    elements += settings.DIR_TMP_TEX    

    ################################################################# 
    ################################################################# Attention ERREUR si non modif
    # pour windows
    #file = settings.DIR_TMP_TEX+r"\\quizz_pdf_"+str(quizz.id)
    # pour Linux
    file = settings.DIR_TMP_TEX+"/quizz_pdf_"+str(quizz.id)
    ################################################################# 
    ################################################################# 
    f_tex = open(file+".tex","w")
    f_tex.write(elements)
    f_tex.close()

    result = subprocess.run(["pdflatex", "-interaction","nonstopmode",  "-output-directory", settings.DIR_TMP_TEX ,  file ])
    return FileResponse(open(file+".pdf", 'rb'),  as_attachment=True, content_type='application/pdf')




@login_required(login_url= 'index')
def admin_delete_test_mental(request):
    idl   = request.session.get("admin_create_qf_level_id",1)
    teacher = request.user.teacher
    Quizz.objects.filter(title__contains = "Question_Flash_Admin").delete()
    return redirect('admin_mentals', idl)




def ajax_select_style_questions(request):

    subject_id = request.POST.get('subject_id',None)
    level_ids  = request.POST.getlist('level_ids',[])
    is_questions_quizz = request.POST.get('is_questions_quizz',None)
    teacher = request.user.teacher
    data = {}
 
    if is_questions_quizz and level_ids and is_questions_quizz == "true" :
        is_quizz = True
        quizzes = set()
        for level_id in level_ids :
            level = Level.objects.get(pk=level_id)
            quizzes.update( teacher.teacher_quizz.filter(subject_id = subject_id, levels = level,is_random=0) )
        all_questions = set()
        for quizz in quizzes:
            if quizz.questions.count() :
                all_questions.update(quizz.questions.all())
        data['html'] = render_to_string('tool/ajax_questions_flash.html', {'all_questions' : all_questions , 'is_quizz' : is_quizz , 'teacher' :  teacher })
    else :
        is_quizz = False
        all_mentals = list()
        mentaltitles = Mentaltitle.objects.filter(subject__id = subject_id, is_display=1).order_by("ranking")
        for level_id in level_ids :
            level_dict = dict()
            level = Level.objects.get(pk=level_id)
            level_dict["level"] = level 
            list_mentals = list()
            for mentaltitle in mentaltitles :
                dict_mentals = dict()
                mentals = Mental.objects.filter(mentaltitle  = mentaltitle, levels = level, is_display=1 ).order_by("ranking")
                is_mentals = False 
                if mentals :
                    dict_mentals["mentaltitle"] = mentaltitle 
                    dict_mentals["mentals"] = mentals
                    list_mentals.append(dict_mentals)
                    is_mentals = True
                    level_dict["sub"] = list_mentals
        all_mentals.append(level_dict)


        data['html'] = render_to_string('tool/ajax_questions_flash.html', {'all_mentals' : all_mentals , 'is_quizz' : is_quizz  , 'teacher' :  teacher  })

    return JsonResponse(data)


#####################################################################################################################################
#####################################################################################################################################
####    Visiocopie
#####################################################################################################################################
#####################################################################################################################################

 
@login_required(login_url= 'index')
def list_visiocopie(request):
    
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "VisioCopies"

    teacher = request.user.teacher

    if request.user.school :
        videocopies = Videocopy.objects.filter(teacher = teacher).order_by("-timestamp")
    else :
        messages.error(request,"Vous devez adhérer à l'association pour prétendre à cette fonctionnalité.")
        return redirect("index")

    form = VideocopyForm(request.POST or None, request.FILES or None   )
 
 
    if request.method == "POST" :
        if form.is_valid():
            nf = form.save(commit=False)
            nf.teacher = request.user.teacher
            nf.save()

            return redirect('list_visiocopie')
        else:
            print(form.errors)


    return render(request, 'tool/list_visiocopie.html', {'form': form , 'videocopies' : videocopies })


@login_required(login_url= 'index')
def create_visiocopie(request,code):
    
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "VisioCopies"
    form = VideocopyForm(request.POST or None, request.FILES or None,   )
 
    if request.method == "POST" :
        if form.is_valid():
            nf = form.save(commit=False)
            nf.teacher = request.user.teacher
            nf.save()

            return redirect('list_visiocopie')
        else:
            print(form.errors)

    context = {'form': form, 'code':code}

    return render(request, 'tool/form_visiocopie.html', context)

 
@login_required(login_url= 'index')
def delete_visiocopie(request, id):
    
    request.session["tdb"] = "Tools"
    request.session["subtdb"] = "VisioCopies"
    videocopy = Videocopy.objects.get(id=id)

    if request.user == videocopy.teacher.user :
        videocopy.delete()
    else :
        messages.error(request,"Vous ne pouvez pas supprimer cette image.")
        return redirect("index")

    return redirect('list_visiocopie')
    

 
