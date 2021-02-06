from django.shortcuts import render, redirect, get_object_or_404
from tool.models import Tool , Question  , Choice  , Quizz , Diaporama  , Slide
from tool.forms import ToolForm ,  QuestionForm ,  ChoiceForm , QuizzForm,  DiaporamaForm , SlideForm    
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

    teacher = request.user.teacher 
    quizzes = Quizz.objects.filter(teacher =teacher )

    form = QuizzForm(request.POST or None, request.FILES or None ,teacher = teacher)
    return render(request, 'tool/list_quizzes.html', {'quizzes': quizzes , 'form': form,   })


 
def create_quizz(request):
    
    teacher = request.user.teacher 
    form = QuizzForm(request.POST or None, request.FILES or None , teacher = teacher  )
 

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


 
def create_question(request,idq,qtype):
 
    quizz = Quizz.objects.get(pk = idq)
    questions = quizz.questions.order_by("ranking")

    levels = quizz.levels.all()
    themes = quizz.themes.all()
    subject = quizz.subject
    waitings , knowledges = [] ,  []
    if len(levels) > 0 and len(themes) > 0  :
        waitings = Waiting.objects.filter(theme__subject = subject , level__in=levels, theme__in=themes )
        knowledges = Knowledge.objects.filter(theme__subject = subject ,level__in=levels, theme__in=themes )
    elif len(levels) > 0 :
        waitings = Waiting.objects.filter(theme__subject = subject ,level__in=levels)
        knowledges = Knowledge.objects.filter(theme__subject = subject ,level__in=levels)
    elif len(themes) > 0 :
        waitings = Waiting.objects.filter(theme__subject = subject ,theme__in=themes)
        knowledges = Knowledge.objects.filter(theme__subject = subject ,theme__in=themes)

    form = QuestionForm(request.POST or None, request.FILES or None)

    form_ans = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct') , extra=4)

    if request.method == "POST"  :
        print("create_question")  
        if form.is_valid():
            nf         = form.save(commit=False) 
            nf.teacher = request.user.teacher
            nf.qtype   = qtype
            nf.save()
            form.save_m2m() 
            quizz.questions.add(nf)
            if qtype > 2 :
                form_answers = form_ans(request.POST or None,  request.FILES or None, instance = nf)
                for form_answer in form_answers :
                    if form_answer.is_valid():
                        form_answer.save()

            return redirect('create_question' , idq,0)

 
    bgcolors = ["bgcolorRed","bgcolorBlue","bgcolorOrange","bgcolorGreen"] 
    context = { 'quizz': quizz, 'questions': questions,  'waitings': waitings, 'knowledges': knowledges, 'form' : form, 'qtype' : qtype  }

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
 
        context.update( {  'bgcolors' : bgcolors  ,  'title_type_of_question' : "QCM" , 'form_ans' : form_ans    })
        template = 'tool/question_qcm.html'


    return render(request, template , context)




 
def update_question(request,id,idq):
 
    question = Question.objects.get(pk= id)
  
    return redirect ('create_question', idq, 0)




 
def delete_question(request,id,idq):
 
    question = Question.objects.get(pk= id)
    question.delete() 
    return redirect ('create_question', idq, 0)


 
def show_question(request,id):
 
    question = Question.objects.get(pk= id)
    context = {'form': form, "question" : question }

    return render(request, 'tool/form_question.html', context)

#######################################################################################################################
############################ Ajax  ####################################################################################
#######################################################################################################################
 

 
# Pour envoyer les fichiers vers le dossier 
def handle_uploaded_file(f):
    with open( MEDIA_ROOT+str(f.name) , 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


 

 


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


############################################################################################################
############################################################################################################
########## diaporama
############################################################################################################
############################################################################################################

def list_diaporama(request):

    teacher = request.user.teacher 
    diaporamas = Diaporama.objects.filter(teacher =teacher )


    form = DiaporamaForm(request.POST or None, request.FILES or None ,teacher = teacher)
    return render(request, 'tool/list_diaporama.html', {'diaporamas': diaporamas , 'form': form,   })


 
def create_diaporama(request):
    
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
 
    diaporama = Diaporama.objects.get(pk= id)
    slides = diaporama.slides.order_by("ranking")
 
    context = {  "diaporama" : diaporama ,'slides' : slides }

    return render(request, 'tool/show_diaporama.html', context)


def delete_diaporama(request,id):
 
    diaporama = Diaporama.objects.get(pk= id)
    diaporama.delete() 
 
    return redirect ('list_diaporama')
############################################################################################################
############################################################################################################
########## Slides
############################################################################################################
############################################################################################################
 

 
def create_slide(request,id):
 
    diaporama = Diaporama.objects.get(pk = id)
    teacher = request.user.teacher
    form = SlideForm(request.POST or None)

    slides = diaporama.slides.order_by("ranking")
    context = { 'diaporama': diaporama, 'slides': slides, 'form': form, }

    return render(request, 'tool/form_slide.html', context)

 
def delete_slide(request,id,idp):
 
    slide = Slide.objects.get(pk= id)
    slide.delete() 
 
    return redirect ('create_slide', idp)

 

 
def update_slide(request,id,idp):
 
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
def ajax_chargeknowledges(request):  

    try :
        slide_ids = request.POST.get("valeurs")
        slide_tab = slide_ids.split("-") 

        for i in range(len(slide_tab)-1):
            Slide.objects.filter(  pk = slide_tab[i]).update(ranking = i)
    except :
        pass

    data = {}
    return JsonResponse(data)  

