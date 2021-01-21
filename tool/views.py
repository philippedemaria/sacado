from django.shortcuts import render, redirect, get_object_or_404
from tool.models import Tool , Question  , Choice  , Quizz
from tool.forms import ToolForm ,  QuestionForm ,  ChoiceForm , QuizzForm  
from account.decorators import  user_is_testeur
from sacado.settings import MEDIA_ROOT

from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
import uuid
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
 
from templated_email import send_templated_mail
from django.db.models import Q

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

 
 

#####################################################################################################################################
#####################################################################################################################################
####    tool
#####################################################################################################################################
#####################################################################################################################################

 
 
def list_tools(request):
    teacher = request.user.teacher
    tools = Tool.objects.filter(is_publish=1).exclude(teachers = teacher)
    form = ToolForm(request.POST or None, request.FILES or None   )
    return render(request, 'tool/list_tools.html', {'form': form , 'tools' : tools })



def create_tool(request):


    form = ToolForm(request.POST or None, request.FILES or None,   )
 

    if form.is_valid():
        form.save()

        return redirect('list_tools')
    else:
        print(form.errors)

    context = {'form': form, }

    return render(request, 'tool/form_tool.html', context)


def update_tool(request, id):

 
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

    tool = Tool.objects.get(id=id)
    tool.delete()
    return redirect('tool_index')
    

 
def show_tool(request, id ):

    tool = Tool.objects.get(id=id)
    context = {  'tool': tool,   }

    return render(request, 'tool/show_tool.html', context )

def get_this_tool(request):

    data = {} 
    tool_id = int(request.POST.get("tool_id"))

    tool = Tool.objects.get(pk=tool_id) 
    tool.teachers.add(request.user.teacher)

    data['html'] =  "<div class='row'><div class='col-lg-12 col-xs-12'><a href= /tool/show/"+tool.id+" >zsz</a></div></div>"
 
    return JsonResponse(data)


############################################################################################################
############################################################################################################
########## Quizz
############################################################################################################
############################################################################################################

def list_quizzes(request):

    quizzes = Quizz.objects.all()
    teacher = request.user.teacher 

    form = QuizzForm(request.POST or None, request.FILES or None ,teacher = teacher)
    return render(request, 'tool/list_quizzes.html', {'quizzes': quizzes , 'form': form,   })


 
def create_quizz(request):
    
    teacher = request.user.teacher 
    form = QuizzForm(request.POST or None, request.FILES or None , teacher = teacher  )
 

    if form.is_valid():
        nf = form.save(commit = False)
        nf.teacher = teacher
        nf.save()

        return redirect('create_question' , nf.pk )
    else:
        print(form.errors)


    context = {'form': form, 'form_question' : form_question  }

    return render(request, 'tool/form_quizz.html', context)

 
def delete_quizz(request,id):
 
 
    quizz = Quizz.objects.get(pk= id)
    if quizz.teacher == request.user.teacher :
        quizz.delete() 

    return redirect('list_quizzes')


 
def show_quizz(request,id):
 
    quizz = Quizz.objects.get(pk= id)
    questions = quizz.questions.order_by("ranking")
    context = {  "quizz" : quizz , "questions" : questions }

    return render(request, 'tool/show_quizz.html', context)


############################################################################################################
############################################################################################################
########## Question
############################################################################################################
############################################################################################################


def list_questions(request):
    questions = Question.objects.all()
    return render(request, 'tool/list_question.html', {'questions': questions  })


 
def create_question(request,id):
 
    quizz = Quizz.objects.get(pk = id)
    questions = quizz.questions.order_by("ranking")
    context = { 'quizz': quizz, 'questions': questions, }

    return render(request, 'tool/form_question.html', context)

 
def delete_question(request,id,idquizz):
 
    question = Question.objects.get(pk= id)
    question.delete() 
 
    return redirect ('create_question', idquizz)


 
def show_question(request,id):
 
    question = Question.objects.get(pk= id)
    context = {'form': form, "question" : question }

    return render(request, 'tool/form_question.html', context)

#######################################################################################################################
############################ Ajax  ####################################################################################
#######################################################################################################################
def get_question_type(request):

    data = {} 
    kind = int(request.POST.get("kind"))

    print(kind)

    type_tab = ["","Vrai/Faux","Réponse rédigée",'QCM',"QCS"]

    classes = []
    if kind == 1 :
        classes = [ {"bgcolor" : "bgcolorBlue" ,"texte" : "VRAI" } , { "bgcolor" :"bgcolorRed","texte" : "FAUX" } ]

    elif kind > 2 :
        classes = ["bgcolorRed","bgcolorBlue","bgcolorOrange","bgcolorGreen"] 


    context = { 'kind' : kind , 'classes' : classes }

    data['html'] = render_to_string('tool/type_of_question.html', context)

    data['title'] = type_tab[kind]

    return JsonResponse(data)


def get_an_existing_question(request):

    data = {} 
    kind = int(request.POST.get("kind"))
    question_id = int(request.POST.get("question_id"))
    question = Question.objects.get(pk= question_id)
    type_tab = ["","Vrai/Faux","Réponse rédigée",'QCM',"QCS"]
    quizz_id = int(request.POST.get("quizz_id"))


    context = {  'kind' : kind ,  'question' : question ,    }

    data['html'] = render_to_string('tool/type_of_question.html', context)

    data['title'] = type_tab[kind]



    return JsonResponse(data)


# Pour envoyer les fichiers vers le dossier 
def handle_uploaded_file(f):
    with open( MEDIA_ROOT+str(f.name) , 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)



@csrf_exempt
def send_question(request):

    data_files = request.FILES
    print("data_files", data_files)

    data_posted = request.POST

    print("data_posted", data_posted)

    kind = int(data_posted.get("kind"))
    quizz_id = int(data_posted.get("quizz_id"))

    title =  cleanhtml(unescape_html(data_posted.get("title")) )
    calculator =  data_posted.get("calculator", None) 
    if calculator :
        calculator = 1
    else :
        calculator = 0
    duration =  data_posted.get("duration", None)
    if not duration :
        duration = 20
    point =  data_posted.get("point", None) 
    if not point :
        point = 1000
    is_publish =  data_posted.get("is_publish", None) 
    if is_publish :
        is_publish = True 
    else : 
        is_publish = False
    imagefile =  data_files.get("imagefile", None) 
    if imagefile : 
        handle_uploaded_file(imagefile)
    quizz =  Quizz.objects.get(pk = quizz_id)

    ##Donne le rang du dernier slide et compte le nombre de slide pour ajouter 1 pour afficher le numéro de la suivante.
    list_questions = quizz.questions.order_by("ranking")
    if len(list_questions) > 0 :
        last_question = list_questions.last()
        ranking = int(last_question.ranking) + 1
    else :
        ranking =   1

    nbq = list_questions.count()  + 1

    if kind == 1 : # Vrai/Faux
        is_correct = data_posted.get("is_correct",None)  
        if is_correct == 1 :
            is_correct = True
        else :
            is_correct = False
        question = Question.objects.create(title=title, duration= duration , point= point , calculator = calculator  ,imagefile=imagefile ,  is_publish=is_publish , kind=kind , ranking=ranking , is_correct = is_correct )


    elif kind == 2 : # Réponse tapée
        answer =  data_posted.get("answer") 
        question = Question.objects.create(title=title, duration= duration , point= point , calculator= calculator  ,imagefile=imagefile ,  is_publish=is_publish , kind=kind , ranking=ranking  )
        choice = Choice.objects.create(answer=answer, imageanswer = None , is_correct = 1)
        question.choices.add(choice)    

    else : # QCM
        answers =  data_posted.getlist("answers")
        question = Question.objects.create(title=title, duration= duration , point= point , calculator= calculator  ,imagefile=imagefile ,  is_publish=is_publish , kind=kind , ranking=ranking  )

        is_correct_tab =  data_posted.getlist("is_correct")
        imageanswer_tab =  data_files.getlist("image_answers")

        i=1
        for answer in answers :
            if str(i) in is_correct_tab:
                is_correct = True
            else :
                is_correct = False
            try :
                image_answer = imageanswer_tab[i-1]
                if image_answer : 
                    handle_uploaded_file(image_answer)
            except :
                imageanswer = ""
            choice = Choice.objects.create(answer=answer, imageanswer = image_answer , is_correct = is_correct)
            question.choices.add(choice)
            i+=1

    question.quizzes.add(quizz)
   
    context = {  'kind' : 0 ,    }
    context_liste = {  'question' : question ,  'quizz' : quizz , 'from_ajax' : True , 'nbq' : nbq }

    data = {}
    data['html'] = render_to_string('tool/type_of_question.html', context)
    data['question'] = render_to_string('tool/list_of_question.html', context_liste)
 
    return JsonResponse(data)




@csrf_exempt  
def ajax_update_question(request):

 
    data_posted = request.POST
    type_of_question = int(data_posted.get("type_of_question"))
    quizz_id = int(data_posted.get("quizz_id"))
    quizz =  Quizz.objects.get(pk = quizz_id)    
    question_id = int(data_posted.get("question_id"))
    question =  Question.objects.get(pk = question_id)


    title =  cleanhtml(unescape_html(data_posted.get("title")) )
    calculator =  data_posted.get("calculator", None) 
    if not calculator :
        calculator = 1
    duration =  data_posted.get("duration", None)
    if not duration :
        duration = 20
    point =  data_posted.get("point", None) 
    if not point :
        point = 1000
    is_publish =  data_posted.get("is_publish", None) 
    if not is_publish :
        is_publish = True
    else : 
        is_publish = False
    imagefile =  data_posted.get("imagefile") 


    ranking = quizz.questions.count() + 1

 
    if type_of_question == 1 : # Vrai/Faux
        is_correct = data_posted.get("is_correct",None)  
        if is_correct == 1 :
            is_correct = True
        else :
            is_correct = False

        question =  Question.objects.filter(pk = question.id).update(title= title, duration= duration , point= point , calculator= calculator  ,   is_publish=is_publish , kind=type_of_question,  is_correct = is_correct )
        if imagefile :
            Question.objects.filter(pk = question.id).update(  imagefile= imagefile    ) 


    elif type_of_question == 2 : # Réponse tapée
 

        question =  Question.objects.filter(pk = question.id).update(title=title, duration= duration , point= point , calculator= calculator  ,   is_publish=is_publish , kind=type_of_question )
        if imagefile :
            Question.objects.filter(pk = question.id).update(  imagefile= imagefile    ) 

        answer =  data_posted.get("answer")
        for choice in question.choice.all():
            Choice.objects.filter(pk = choice.id).update(answer=answer, imageanswer = None , is_correct = 1)


    else : # QCM


        answers =  data_posted.getlist("answers")
 
        Question.objects.filter(pk = question.id).update( title = title,  duration = duration , point = point ,  calculator = calculator  ,    is_publish =is_publish   )
        if imagefile :
            Question.objects.filter(pk = question.id).update(  imagefile= imagefile    )  


        is_correct_tab =  data_posted.getlist("is_correct")
        i=1

        for choice in question.choices.all() :
            if str(i) in is_correct_tab:
                is_correct = True
            else :
                is_correct = False
            Choice.objects.filter(pk = choice.id).update(answer=answers[i], imageanswer = None , is_correct = is_correct)    
            i+=1
 
    context = {  'kind' : 0 ,    }
    context_liste = {  'question' : question ,  'quizz' : quizz ,  }

    data = {}
    data['html'] = render_to_string('tool/type_of_question.html', context)
    data['question'] = render_to_string('tool/list_of_question.html', context_liste)
 
    return JsonResponse(data)





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