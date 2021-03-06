from django.shortcuts import render, redirect, get_object_or_404
from tool.models import Tool , Question  , Choice  , Quizz , Diaporama  , Slide ,Qrandom ,Variable , VariableImage , Generate_quizz , Generate_qr , Answerplayer , Display_question ,  Videocopy
from tool.forms import ToolForm ,  QuestionForm ,  ChoiceForm , QuizzForm,  DiaporamaForm , SlideForm,QrandomForm, VariableForm , AnswerplayerForm,  VideocopyForm
from group.models import Group 
from socle.models import Level, Waiting
from account.decorators import  user_is_testeur
from sacado.settings import MEDIA_ROOT
from socle.models import Knowledge, Waiting
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
import uuid
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.forms import inlineformset_factory
from templated_email import send_templated_mail
from django.db.models import Q
from random import  randint
import math
import json
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
 




#####################################################################################################################################
#####################################################################################################################################
####    tool
#####################################################################################################################################
#####################################################################################################################################

 
 
def list_tools(request):
    teacher = request.user.teacher
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche
    if request.user.is_superuser :
        tools = Tool.objects.all()
    else :
        tools = Tool.objects.filter(is_publish=1).exclude(teachers = teacher)
    form = ToolForm(request.POST or None, request.FILES or None   )
    return render(request, 'tool/list_tools.html', {'form': form , 'tools' : tools })



def create_tool(request):

    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche
    form = ToolForm(request.POST or None, request.FILES or None,   )
 

    if form.is_valid():
        form.save()

        return redirect('list_tools')
    else:
        print(form.errors)

    context = {'form': form, }

    return render(request, 'tool/form_tool.html', context)


def update_tool(request, id):

    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
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
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche
    tool = Tool.objects.get(id=id)
    tool.delete()
    return redirect('tool_index')
    

 
def show_tool(request, id ):
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche
    tool = Tool.objects.get(id=id)
    if tool.url != "" :
        url = tool.url
    else :
        url = 'tool/show_tool.html'
    context = {  'tool': tool,   }

    return render(request, url , context )


def get_this_tool(request):

    data = {} 
    tool_id = int(request.POST.get("tool_id"))
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche
    tool = Tool.objects.get(pk=tool_id) 
    tool.teachers.add(request.user.teacher)

    data['html'] =  "<div class='row' id='this_this_tool'  ><div class='col-lg-12 col-xs-12'><a href= /tool/show/"+str(tool.id)+" >"+str(tool.title)+"</a></div></div>"
 
 
    return JsonResponse(data)


def delete_my_tool(request):

    data = {} 
    tool_id = int(request.POST.get("tool_id"))
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche
    tool = Tool.objects.get(pk=tool_id) 
    tool.teachers.remove(request.user.teacher)
 
    return JsonResponse(data)


############################################################################################################
############################################################################################################
########## Quizz
############################################################################################################
############################################################################################################

def list_quizzes(request):

    teacher = request.user.teacher 
    quizzes = Quizz.objects.filter(teacher =teacher )
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche
    form = QuizzForm(request.POST or None, request.FILES or None ,teacher = teacher)
    return render(request, 'tool/list_quizzes.html', {'quizzes': quizzes , 'form': form,   })


 
def create_quizz(request):
    
    teacher = request.user.teacher 
    form = QuizzForm(request.POST or None, request.FILES or None , teacher = teacher  )
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche

    if form.is_valid():
        nf = form.save(commit = False)
        nf.teacher = teacher
        nf.is_questions = 1
        nf.save()
        form.save_m2m()
        print(nf.pk)
        return redirect('create_question' , nf.pk , 0 )
    else:
        print(form.errors)
        print("ici")

    context = {'form': form,  }

    return render(request, 'tool/form_quizz.html', context)


 
def update_quizz(request,id):
    
    teacher = request.user.teacher 
    quizz = Quizz.objects.get(pk= id)
    form = QuizzForm(request.POST or None, request.FILES or None , instance = quizz , teacher = teacher  )
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche
    if form.is_valid():
        nf = form.save(commit = False)
        nf.teacher = teacher
        nf.is_questions = 1
        nf.save()
        form.save_m2m()

        return redirect('list_quizzes' )
    else:
        print(form.errors)

    context = {'form': form,   }

    return render(request, 'tool/form_quizz.html', context)



def delete_quizz(request,id):

    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    quizz = Quizz.objects.get(pk= id)
    if quizz.teacher == request.user.teacher :
        quizz.delete() 

    return redirect('list_quizzes')


 
def show_quizz(request,id):
    """ permet à un prof de voir son quizz """
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    quizz = Quizz.objects.get(pk= id)
    questions = quizz.questions.filter(is_publish=1).order_by("ranking")
    context = {  "quizz" : quizz , "questions" : questions }

    return render(request, 'tool/show_quizz.html', context)




 


def result_quizz(request,id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    g_quizz = Generate_quizz.objects.get(pk= id, quizz__teacher = request.user.teacher)
    context = {  "g_quizz" : g_quizz }

    return render(request, 'tool/result_quizz.html', context)





def delete_historic_quizz(request,id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    g_quizz = Generate_quizz.objects.get(pk= id)

    if g_quizz.quizz.teacher == request.user.teacher :
        g_quizz.delete()

    return redirect("list_quizzes")



def ajax_show_generated(request):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    gq_id = request.POST.get("gq_id")
    data = {}  
    g_quizz = Generate_quizz.objects.get(pk= gq_id, quizz__teacher = request.user.teacher) 
    context = { "g_quizz" : g_quizz   }

    data['html'] = render_to_string('tool/ajax_show_generated.html', context)

    return JsonResponse(data)  





def get_save_new_gquizz(quizz) :
    """ permet un enregistrement d'un nouveau quizz généré toutes les hours = 1 """
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    save = True
    remainig_time = datetime.now() - timedelta(hours = 0.15) # 0.25 pour 1/4 d'heure , 0.5 pour 1/2 heure
    if Generate_quizz.objects.filter(date_created__gt= remainig_time, quizz__teacher = quizz.teacher ).count() > 0 :
        save = False
    return save




def get_qr(quizz_id,group_id,mode) :

    """ fonction qui génére un historique de questions aléatoires à partir du modèle du quizz"""
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
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
        qrandoms.shuffle()
    
 
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




def get_date_play(quizz_id,group_id,mode) : # pour les questionnaires non randomisés

    """ fonction qui génére un quizz à partir du modèle du quizz"""
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    quizz = Quizz.objects.get(pk= quizz_id)
    save = get_save_new_gquizz(quizz)
    if save :
        gquizz = Generate_quizz.objects.create(quizz_id = quizz_id ,  group_id = group_id ,is_game=mode)
    else :
        gquizz   = Generate_quizz.objects.filter(quizz_id = quizz_id ,  group_id = group_id ,is_game=mode).last()
    questions = quizz.questions.order_by("ranking")
    return quizz , gquizz , questions , save
  


 
def show_quizz_group(request,id,idg):

    """ show quizz d'un groupe classe """
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    quizz , gquizz , questions , save = get_date_play(id,idg,0)
    questions = quizz.questions.filter(is_publish=1).order_by("ranking")
    group = Group.objects.get(pk = idg)
    context = {  "quizz" : quizz , "questions" : questions , "group" : group , "save" : save }

    return render(request, 'tool/show_quizz.html', context)



############################################################################################################
############################################################################################################
########## Play quizz
############################################################################################################
############################################################################################################

def play_quizz_teacher(request,id,idg):
    """ Lancer d'un play quizz """
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
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
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
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
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    can_play = False
    groups = gquizz.quizz.groups.all()
    group_set = set()
    for group in groups :
        group_set.update(group.students.all())
    if student in group_set :
        can_play = True
    return can_play


 

def play_quizz_student(request):
    """ Lancer le play quizz élève """
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
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
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    all_results = request.POST.get("all",None)
    question_id = request.POST.get("question_id",None)
    random = int(request.POST.get("random",0))
    data = {}

    if random == 0 :
        answers = Answerplayer.objects.filter(question_id = question_id, is_correct = 1 ).order_by("-score")
        no_answers = Answerplayer.objects.filter(question_id = question_id, is_correct = 0 ).order_by("-score")
    else :
        answers = Answerplayer.objects.filter(qrandom_id = question_id, is_correct = 1 ).order_by("id")
        no_answers = Answerplayer.objects.filter(qrandom_id = question_id, is_correct = 0 ).order_by("-score")

    no_answers_display = True
    if all_results == "0" :
        answers = answers[:3]
        no_answers_display = False
 

    context = { "answers" : answers , "no_answers" : no_answers , "no_answers_display" : no_answers_display   }

    print(context)

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
def ajax_display_question_to_student(request):  
    """ Affichage de la question aux élèves par envoie du timestamp
        Appel Ajax de la vue élève
    """
    gquizz_id = request.POST.get("gquizz_id",None)
    student   = request.user.student
    form      = AnswerplayerForm(request.POST or None)
    time_zone = time_zone_user(request.user)
    timestamp = time_zone.timestamp()
    data      = {}
    data['is_valid'] = "False"
    if gquizz_id :
        gquizz = Generate_quizz.objects.get(pk = gquizz_id)
        dq     = Display_question.objects.filter(gquizz=gquizz).last()

        if not student in dq.students.all() : #Si l'élève n'a pas chargé la question et que le temps est inférieur à 2 minutes
            if gquizz.quizz.is_random :
                generate_qr = Generate_qr.objects.get(pk = dq.question_id)
                question    =  { "qtype" : generate_qr.qrandom.qtype , "title" : generate_qr.qr_text , "id" : generate_qr.id, "duration" : generate_qr.qrandom.duration  }
                timer       = int(generate_qr.qrandom.duration)*1000 + 5000
            else :
                question = Question.objects.get(pk = dq.question_id)
                timer    = int(question.duration)*1000 + 5000

            context = { "question" : question , "form" : form ,  "gquizz_id" : gquizz_id ,  "timestamp" : timestamp   }  

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
        gquizz_id = request.POST.get("gquizz_id")
        gquizz    = Generate_quizz.objects.get(pk = gquizz_id)
        if form.is_valid() :
            if gquizz.quizz.is_random :
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
            Answerplayer.objects.get_or_create(gquizz = gquizz , student = request.user.student , question = question , qrandom_id = qrandom_id , defaults = {"answer": answer , "score" :score , "timer" : timer , "is_correct" : answer_is_correct} )

        else :
            print(form.errors)
    else :
        messages.error(request,"Erreur d'enregistrement")
 

    context = { 'student' : request.user.student , 'gquizz' : gquizz , 'starter' : False }
    return render(request, 'tool/play_quizz_start.html', context)

############################################################################################################
############################################################################################################
########## Question
############################################################################################################
############################################################################################################


def list_questions(request):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    questions = Question.objects.all()
    return render(request, 'tool/list_question.html', {'questions': questions  })


 
def create_question(request,idq,qtype):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    quizz = Quizz.objects.get(pk = idq)
    questions = quizz.questions.order_by("ranking")

    form = QuestionForm(request.POST or None, request.FILES or None, quizz = quizz)

    
    if qtype > 2 :
        formSet = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct') , extra=4)
        form_ans = formSet(request.POST or None,  request.FILES or None)
    if request.method == "POST"  :
        if form.is_valid():
            nf         = form.save(commit=False) 
            nf.teacher = request.user.teacher
            nf.qtype   = qtype
            nf.save()
            form.save_m2m() 
            quizz.questions.add(nf)
            if qtype > 2 :
                form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
                for form_answer in form_ans :
                    if form_answer.is_valid():
                        form_answer.save()

            return redirect('create_question' , idq,0)

 
    bgcolors = ["bgcolorRed", "bgcolorBlue","bgcolorOrange", "bgcolorGreen"] 
    context = { 'quizz': quizz, 'questions': questions,  'form' : form, 'qtype' : qtype  }


    if quizz.is_random :
        knowledges = Knowledge.objects.filter(theme__subject=quizz.subject ,theme__in=quizz.themes.all() , level__in =quizz.levels.all())
        context.update( {  'title_type_of_question' : "Questions aléatoires" , "knowledges" : knowledges  })
        template = 'tool/quizz_random.html'
 
    #Choix des questions
    elif qtype == 0 :
        context.update( {  'title_type_of_question' : "Choisir un type de question"   })
        template = 'tool/choice_type_of_question.html'

    #Vrai/Faux
    elif qtype == 1 :
        context.update( {   'title_type_of_question' : "Vrai / faux"   })
        template = 'tool/question_vf.html'

    #Réponse rédigée
    elif qtype == 2 :
        context.update( {    'title_type_of_question' : "Réponse rédigée"   })
        template = 'tool/form_question.html'

    #QCM ou QCS
    elif qtype == 3 or qtype == 4  :
 
        context.update( {  'bgcolors' : bgcolors  ,  'title_type_of_question' : "QCM" , 'form_ans' : form_ans   , 'question' : None  })
        template = 'tool/question_qcm.html'


    return render(request, template , context)




 
def update_question(request,id,idq,qtype):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    quizz = Quizz.objects.get(pk = idq)
    questions = quizz.questions.order_by("ranking")

    question = Question.objects.get(pk = id)
    form = QuestionForm(request.POST or None, request.FILES or None, instance = question,  quizz = quizz)

    
    if qtype > 2 :
        formSet = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct') , extra=0)
        form_ans = formSet(request.POST or None,  request.FILES or None, instance = question)

    if request.method == "POST"  :  
        if form.is_valid():
            nf         = form.save(commit=False) 
            nf.teacher = request.user.teacher
            nf.qtype   = qtype
            nf.save()
            form.save_m2m() 
            if qtype > 2 :
                for form_answer in form_ans :
                    if form_answer.is_valid():
                        form_answer.save()

            return redirect('create_question' , idq,0)

 
    bgcolors = ["bgcolorRed","bgcolorBlue","bgcolorOrange","bgcolorGreen"] 
    context = { 'quizz': quizz, 'questions': questions,  'form' : form, 'qtype' : qtype  }

    #Choix des questions
    if qtype == 0 :
        context.update( {  'title_type_of_question' : "Choisir un type de question"   })
        template = 'tool/choice_type_of_question.html'

    #Vrai/Faux
    elif qtype == 1 :
        context.update( {   'title_type_of_question' : "Vrai / faux"   })
        template = 'tool/question_vf.html'

    #Réponse rédigée
    elif qtype == 2 :
        context.update( {    'title_type_of_question' : "Réponse rédigée"   })
        template = 'tool/form_question.html'

    #QCM ou QCS
    elif qtype == 3 or qtype == 4  :
 
        context.update( {  'bgcolors' : bgcolors  ,  'title_type_of_question' : "QCM" , 'form_ans' : form_ans , 'question' : question    })
        template = 'tool/question_qcm.html' 


    return render(request, template , context)




 
def delete_question(request,id,idq):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    question = Question.objects.get(pk= id)
    if question.quizz.count() == 0 :
        question.delete()
    else :
        messages.error(request, "  !!!  Cette question est utiolisée dans un quizz  !!! Suppression interdite.")
    return redirect ('create_question', idq, 0)

 
def remove_question(request,id,idq):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    quizz = Quizz.objects.get(pk = idq)
    if quizz.teacher == request.user.teacher :
        question = Question.objects.get(pk = id)
        quizz.questions.remove(question)
    return redirect ('create_question', idq, 0)



 
def show_question(request,id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche  
    question = Question.objects.get(pk= id)
    context = {'form': form, "question" : question }

    return render(request, 'tool/form_question.html', context)

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

    p.setFont("Helvetica", 16)
    p.drawString(75, 800, quizz.title +"                                    "+quizz.title )    

    p.setFont("Helvetica", 12)
    p.drawString(75, 770, "Classe  : ________________________           Classe  : _______________________ " )  
    p.drawString(75, 740, "Nom :  _________________________            Nom :  _________________________" )  

    for i in range(1,quizz.questions.count()+1) :
        p.setFont("Helvetica", 12)  
        string0 = str(i)+". _____________________________          " + str(i)+". _____________________________" 
        p.drawString(75, 740-30*i, string0)


    p.line(75, 740-30*(i+1) ,550,740-30*(i+1) )

    p.setFont("Helvetica", 16)
    p.drawString(75, 740-30*(i+2), quizz.title +"                                    "+quizz.title )    

    p.setFont("Helvetica", 12)
    p.drawString(75, 740-30*(i+3), "Classe  : ________________________           Classe  : _______________________ " )  
    p.drawString(75, 740-30*(i+4), "Nom :  _________________________            Nom :  _________________________" )  

    for j in range(1,quizz.questions.count()+1) :
        p.setFont("Helvetica", 12)  
        string0 = str(j)+". _____________________________          " + str(i)+". _____________________________" 
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

def list_diaporama(request):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    teacher = request.user.teacher 
    diaporamas = Diaporama.objects.filter(teacher =teacher )


    form = DiaporamaForm(request.POST or None, request.FILES or None ,teacher = teacher)
    return render(request, 'tool/list_diaporama.html', {'diaporamas': diaporamas , 'form': form,   })


 
def create_diaporama(request):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche     
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


 
def update_diaporama(request,id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche     
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
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche  
    diaporama = Diaporama.objects.get(pk= id)
    slides = diaporama.slides.order_by("ranking")
 
    context = {  "diaporama" : diaporama ,'slides' : slides }

    return render(request, 'tool/show_diaporama.html', context)


def delete_diaporama(request,id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche  
    diaporama = Diaporama.objects.get(pk= id)
    if diaporama.teacher == request.user.teacher :
        diaporama.delete() 
 
    return redirect ('list_diaporama')
############################################################################################################
############################################################################################################
########## Slides
############################################################################################################
############################################################################################################
 

 
def create_slide(request,id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche  
    diaporama = Diaporama.objects.get(pk = id)
    teacher = request.user.teacher
    form = SlideForm(request.POST or None)

    slides = diaporama.slides.order_by("ranking")
    context = { 'diaporama': diaporama, 'slides': slides, 'form': form, }

    return render(request, 'tool/form_slide.html', context)

 
def delete_slide(request,id,idp):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    slide = Slide.objects.get(pk= id)
    if slide.diapositive.count() == 0 :
        slide.delete()
    else :
        messages.error(request, "  !!!  Cette question est utiolisée dans un quizz  !!! Suppression interdite.")
 
    return redirect ('create_slide', idp)


 
def remove_slide(request,id,idq):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    diaporama = Diaporama.objects.get(pk = idq)
    if diaporama.teacher == request.user.teacher :
        slide = Slide.objects.get(pk= id)
        diaporama.slides.remove(question)
    return redirect ('create_question', idq, 0)


 
def update_slide(request,id,idp):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche  
    diaporama = Diaporama.objects.get(pk = idp)

    slide= Slide.objects.get(pk = id)
    teacher = request.user.teacher
    form = SlideForm(request.POST or None , instance = slide  )
    if form.is_valid():
        form.save()     
        return redirect ('create_slide', idp)

    slides = diaporama.slides.order_by("ranking")
    context = { 'diaporama': diaporama, 'slides': slides, 'form': form, 'slide': slide, }

    return render(request, 'tool/form_slide.html', context)




@csrf_exempt
def send_slide(request):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    ### le quizz
    diaporama_id =  request.POST.get("diaporama_id",None)    
    diaporama =  Diaporama.objects.get(pk = diaporama_id)

    list_slides = diaporama.slides.order_by("ranking")
    if len(list_slides) > 0 :
        last_slide = list_slides.last()
        ranking = int(last_slide.ranking) + 1
    else :
        ranking =   1
    ## Nombre de questions dans le quizz    ####################################
    nbq = list_slides.count()  + 1

    form = SlideForm(request.POST or None   )
    if form.is_valid():
        slide = form.save(commit=False)
        slide.ranking = ranking
        slide.save()  
        form.save_m2m()      
        diaporama.slides.add(slide)
    else :
        slide = None

    context = {    }
    context_liste = {  'slide' : slide ,  'diaporama' : diaporama , 'from_ajax' : True , 'nbq' : nbq }

    data = {'new' : True}
    data['html'] = render_to_string('tool/type_of_slide.html', context)
    data['slide'] = render_to_string('tool/list_of_slide.html', context_liste)
 
    return JsonResponse(data)



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



def show_quizz_random(request,id):
    """ Vue pour l'enseignant """
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    quizz , gquizz , qrandoms , save = get_qr(id, None,0)  
 
    context = {  "quizz" : quizz , "gquizz" : gquizz , "qrandoms" : qrandoms  , "save" : save }

 
    return render(request, 'tool/show_quizz_random.html', context)



def show_quizz_random_group(request,id,idg):
    """ Vue pour le groupe en vidéo projection """
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    group = Group.objects.get(id = idg)
    quizz ,  gquizz , qrandoms , save = get_qr(id,idg,0)

    context = {   "quizz" : quizz , "gquizz" : gquizz , "qrandoms" : qrandoms , "group" : group  , "save" : save }
 
    return render(request, 'tool/show_quizz_random.html', context)




def create_quizz_random(request,id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    quizz = Quizz.objects.get(pk= id)
    noq = int(request.POST.get('noq',1)) 
    knowledge_ids = request.POST.getlist('knowledges')
    qrandoms_list = list(Qrandom.objects.filter(knowledge_id__in = knowledge_ids))
    lenq = len(qrandoms_list) 
    for i in range(lenq) :
        quizz.qrandoms.add(qrandoms_list[i])
    Quizz.objects.filter(pk=quizz.id).update(nb_slide = noq )
 
    return redirect('list_quizzes' )
 


def list_qrandom(request):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    if request.user.is_superuser :
        qrandoms = Qrandom.objects.all()
        context = {  "qrandoms" : qrandoms  }
        return render(request, 'tool/list_qrandom.html', context)
    else :
        return redirect('index')



def create_qrandom(request):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
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

    
 


def update_qrandom(request,id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
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



def delete_qrandom(request,id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    if request.user.is_superuser :
        qr = Qrandom.objects.get(pk= id)
        qr.delete()
    else :
        return redirect('index')
 
    return redirect("list_qrandom")

 
 

 
def admin_qrandom(request,id_level):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    if request.user.is_superuser :
        level = Level.objects.get(pk = id_level)
        data = all_datas(level)
        return render(request, 'tool/list_qr.html', {'data': data ,'level': level   })
    else :
        return redirect('index')




def create_qrandom_admin(request,id_knowledge):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
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





def update_qrandom_admin(request,id_knowledge,id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
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
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    qrandom = Qrandom.objects.get(pk = id)
 
    return render(request, 'tool/show_qr.html', {'qrandom': qrandom      })


#####################################################################################################################################
#####################################################################################################################################
####    Videocopy
#####################################################################################################################################
#####################################################################################################################################

 
 
def list_videocopy(request):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
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

            return redirect('list_videocopy')
        else:
            print(form.errors)


    return render(request, 'tool/list_videocopy.html', {'form': form , 'videocopies' : videocopies })



def create_videocopy(request):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    form = VideocopyForm(request.POST or None, request.FILES or None,   )
 
    if request.method == "POST" :
        if form.is_valid():
            nf = form.save(commit=False)
            nf.teacher = request.user.teacher
            nf.save()

            return redirect('list_videocopy')
        else:
            print(form.errors)

    context = {'form': form, }

    return render(request, 'tool/form_videocopy.html', context)

 

def delete_videocopy(request, id):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    videocopy = Videocopy.objects.get(id=id)

    if request.user == videocopy.teacher.user :
        videocopy.delete()
    else :
        messages.error(request,"Vous ne pouvez pas supprimer cette image.")
        return redirect("index")

    return redirect('list_videocopy')
    

 
