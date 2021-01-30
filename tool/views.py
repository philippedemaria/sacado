from django.shortcuts import render, redirect, get_object_or_404
from tool.models import Tool , Question  , Choice  , Quizz
from tool.forms import ToolForm ,  QuestionForm ,  ChoiceForm , QuizzForm  
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
from html import escape
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

    if request.user.is_superuser :
        tools = Tool.objects.all()
    else :
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
    if tool.url != "" :
        url = tool.url
    else :
        url = 'tool/show_tool.html'
    context = {  'tool': tool,   }

    return render(request, url , context )


def get_this_tool(request):

    data = {} 
    tool_id = int(request.POST.get("tool_id"))

    tool = Tool.objects.get(pk=tool_id) 
    tool.teachers.add(request.user.teacher)

    data['html'] =  "<div class='row' id='this_this_tool'  ><div class='col-lg-12 col-xs-12'><a href= /tool/show/"+str(tool.id)+" >"+str(tool.title)+"</a></div></div>"
 
 
    return JsonResponse(data)


def delete_my_tool(request):

    data = {} 
    tool_id = int(request.POST.get("tool_id"))

    tool = Tool.objects.get(pk=tool_id) 
    tool.teachers.remove(request.user.teacher)
 
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
        form.save_m2m()
        return redirect('create_question' , nf.pk )
    else:
        print(form.errors)


    context = {'form': form, 'form_question' : form_question  }

    return render(request, 'tool/form_quizz.html', context)


 
def update_quizz(request,id):
    
    teacher = request.user.teacher 
    quizz = Quizz.objects.get(pk= id)
    form = QuizzForm(request.POST or None, request.FILES or None , instance = quizz , teacher = teacher  )
 
    if form.is_valid():
        nf = form.save(commit = False)
        nf.teacher = teacher
        nf.save()
        form.save_m2m()

        return redirect('list_quizzes' )
    else:
        print(form.errors)

    context = {'form': form,   }

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


def play_quizz_teacher(request,id):
 
    quizz = Quizz.objects.get(pk= id)
    questions = quizz.questions.order_by("ranking")
    context = {  "quizz" : quizz , "questions" : questions }

    return render(request, 'tool/play_quizz_teacher.html', context)









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
    question_id =  request.POST.get("question_id",None)
    if question_id: # Pour l'update
        question_id = int(question_id)
        question = Question.objects.get(pk= question_id)
    else :
        question = None

    quizz_id =  request.POST.get("quizz_id",None)
    quizz = Quizz.objects.get(pk= quizz_id)


    datas = []
    if len(quizz.themes.all()) > 0 :
        waitings = Waiting.objects.filter(theme__in = quizz.themes)
    elif len(quizz.levels.all()) > 0 :
        waitings = Waiting.objects.filter(level_in = quizz.levels)
    elif  quizz.subject :
        waitings = Waiting.objects.filter(theme__subject = quizz.subject)
    else   :
        waitings = Waiting.objects.all()

    for w in waitings :
        data = {}
        data["waiting"] = w.name
        k_tab = []
        for k in  w.knowledges.all() :
            kw_k = {'id' : k.id , 'name' : k.name }
            k_tab.append(kw_k)
        data["knowledges"] = k_tab
        datas.append(data)

        


    # les type commencent à 1 donc garder une object occurence vide en début de liste
    type_tab = ["","Vrai/Faux","Réponse rédigée",'QCM',"QCS"]

    bgcolors = ["bgcolorRed","bgcolorBlue","bgcolorOrange","bgcolorGreen"] 

    classes = []

    if kind == 1 : # VF
        classes = [ {"bgcolor" : bgcolors[1] ,"answer" : "VRAI"   } , { "bgcolor" : bgcolors[0] ,"answer" : "FAUX"  } ]

    # Pour le kind = 2 il n'y a pas de bgcolor car question rédigée
    elif kind > 2 : # QCM/QCS
           
        if question_id: # Pour l'update
            i = 0
            for choice in question.choices.all() :
                classes.append({"labelcolor" : bgcolors[i]  , "bgcolor" : bgcolors[i]  ,"answer" : choice, "is_correct" : choice.is_correct })
                i +=1

        else : # création
            for i in range(4) : 
                classes.append({"labelcolor" : bgcolors[i]  ,  "bgcolor" : None  ,"answer" : None, "is_correct" : None })


    context = { 'kind' : kind , 'question' : question  , 'classes' : classes , 'datas' : datas }

    data['html'] = render_to_string('tool/type_of_question.html', context)

    data['title'] = type_tab[kind]

    return JsonResponse(data)

 


# Pour envoyer les fichiers vers le dossier 
def handle_uploaded_file(f):
    with open( MEDIA_ROOT+str(f.name) , 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


 

@csrf_exempt  
def from_ajax_create_question(kind,  ranking, title, calculator, duration, point , knowledge_id ,  is_publish, imagefile, is_correct, is_correct_tab,imageanswer_tab,answers):

    if kind == 1 : # Vrai/Faux
        question = Question.objects.create(title=title, duration= duration , point= point , knowledge_id= knowledge_id ,  calculator = calculator  ,imagefile=imagefile ,  is_publish=is_publish , kind=kind , ranking=ranking , is_correct = is_correct )

    elif kind == 2 : # Réponse tapée

        question = Question.objects.create(title=title, duration= duration , point= point , calculator= calculator  ,  knowledge_id= knowledge_id ,imagefile=imagefile ,  is_publish=is_publish , kind=kind , ranking=ranking  )
        choice = Choice.objects.create(answer=answers[0], imageanswer = None , is_correct = 1)
        question.choices.add(choice)    

    else : # QCM
        question = Question.objects.create(title=title, duration= duration , point= point , calculator= calculator  ,  knowledge_id= knowledge_id ,imagefile=imagefile ,  is_publish=is_publish , kind=kind , ranking=ranking  )

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
                image_answer = ""
            choice = Choice.objects.create(answer=answer, imageanswer = image_answer , is_correct = is_correct)
            question.choices.add(choice)
            i+=1
    return question


@csrf_exempt  
def from_ajax_udate_question(kind,  ranking, question, title, calculator, duration, point ,  is_publish, imagefile, knowledge_id, is_correct, is_correct_tab,imageanswer_tab,answers):

    if kind == 1 : # Vrai/Faux
        Question.objects.filter(pk = question.id).update(title= title, duration= duration , point= point , calculator= calculator  , knowledge_id= knowledge_id ,   is_publish=is_publish ,  is_correct = is_correct )
        if imagefile :
            Question.objects.filter(pk = question.id).update(  imagefile= imagefile    ) 

    else :

        Question.objects.filter(pk = question.id).update(title=title, duration= duration , point= point , calculator= calculator  ,  knowledge_id = knowledge_id ,   is_publish=is_publish )
        if imagefile :
            Question.objects.filter(pk = question.id).update(  imagefile= imagefile    )  

        if kind == 2 : # Réponse tapée
            for choice in question.choice.all():
                Choice.objects.filter(pk = choice.id).update(answer=answers[0], imageanswer = None , is_correct = 1)
        else : # QCM
            i=1
            for choice in question.choices.all() :
                if str(i) in is_correct_tab:
                    is_correct = True
                else :
                    is_correct = False
                try :
                    image_answer = imageanswer_tab[i-1]
                    if image_answer : 
                        handle_uploaded_file(image_answer)
                except :
                    image_answer = ""
                Choice.objects.filter(pk = choice.id).update(answer=answers[i-1], imageanswer = image_answer , is_correct = is_correct)    
                i+=1
 
    return question



@csrf_exempt
def send_question(request):

    data_files = request.FILES
    data_posted = request.POST

    ### le type
    kind = int(data_posted.get("kind"))

    ### le quizz
    quizz_id =  data_posted.get("quizz_id",None) 
    quizz =  Quizz.objects.get(pk = quizz_id)

    ### titre ####################################
    title =  cleanhtml(unescape_html(data_posted.get("title")) )
    ### calculatrice ####################################
    calculator =  data_posted.get("calculator", None) 
    if calculator :
        calculator = 1
    else :
        calculator = 0
    ### durée ####################################
    duration =  data_posted.get("duration", None)
    if not duration :
        duration = 20
    ### point attribué ####################################
    point =  data_posted.get("point", None) 
    if not point :
        point = 1000
    ### publication ####################################
    is_publish =  data_posted.get("is_publish", None) 
    if is_publish :
        is_publish = True 
    else : 
        is_publish = False
    ### question imagée ####################################        
    imagefile =  data_files.get("imagefile", None) 
    if imagefile : 
        handle_uploaded_file(imagefile)

    ## Donne le rang du dernier slide et compte le nombre de slide pour ajouter 1 pour afficher le numéro de la suivante.
    list_questions = quizz.questions.order_by("ranking")
    if len(list_questions) > 0 :
        last_question = list_questions.last()
        ranking = int(last_question.ranking) + 1
    else :
        ranking =   1
    ## Nombre de questions dans le quizz    ####################################
    nbq = list_questions.count()  + 1

    is_correct = data_posted.get("is_correct",0) 
 

    answers =  data_posted.getlist("answers", [])
    is_correct_tab =  data_posted.getlist("is_corrects",[])
    imageanswer_tab =  data_files.getlist("image_answers",[])

    question_id =  data_posted.get("question_id",None)
    knowledge_id =  data_posted.get("knowledge_id",None)
    if question_id :
        question = Question.objects.get(pk = int(question_id))
        new = False
        from_ajax_udate_question(kind,ranking,  question , title, calculator, duration, point ,  is_publish, imagefile, knowledge_id , is_correct, is_correct_tab,imageanswer_tab,answers)
    else :
        question = from_ajax_create_question(kind, ranking,  title, calculator, duration, point ,  is_publish, imagefile, knowledge_id , is_correct, is_correct_tab,imageanswer_tab,answers)
        new = True

    question.quizzes.add(quizz)
   
    context = {  'kind' : 0 ,    }
    context_liste = {  'question' : question ,  'quizz' : quizz , 'from_ajax' : True , 'nbq' : nbq }

    data = {'new' : new}
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

 
def play_printing_teacher(request, id):

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