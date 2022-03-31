#################################
#### Auteur : philipe Demaria 
#### pour SACADO
#################################

from django.conf import settings # récupération de variables globales du settings.py
from django.shortcuts import render, redirect
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import  permission_required,user_passes_test, login_required
from django.http import JsonResponse 
from account.models import  Adhesion
from academy.models import  Autotest 
from academy.forms import  AutotestForm
from socle.models import  Level
from qcm.models import  Studentanswer
from bibliotex.models import  Exotex
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from tool.consumers import *

import json
##############bibliothèques pour les impressions pdf  #########################
import os
from pdf2image import convert_from_path # convertit un pdf en autant d'images que de pages du pdf
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
from html import escape
from operator import attrgetter
from itertools import chain
cm = 2.54
import os
import re
import pytz
import csv
import html
from general_fonctions import *








def printer_bibliotex_by_student(exotexs):
    """affiche un exo ou une collection d'exercices, soit en pdf (output="pdf")
    soit en html (output="html") """

    # ouverture du texte dans le fichier tex

    preamb = settings.TEX_PREAMBULE_PDF_FILE

    entetes=open(preamb,"r")
    elements=entetes.read()
    entetes.close()

    elements +=r"\begin{document}"+"\n"   

    ## Création du texte dans le fichier tex   

 
 

    elements +=r"\titreFiche{Auto test"+r"}{SACADO"+r"}"

    today = datetime.now()
 
     
 

    j = 1
    for exotex in exotexs :
    
        skills_display = ""
        if exotex.skills.count():
            sks =  exotex.skills.all()
        else :
            sks =  exotex.exotex.skills.all()
        for s in sks :
            skills_display +=  s.name+". "
            

        elements += r"\exo {\bf " +   exotex.title  +  r" }    \competence{" +skills_display+r"}"
        
        j+=1

  
        k_display =  exotex.knowledge.name
        elements += r"\savoirs{  \item " +  k_display 


        if exotex.knowledges.count() : kws =  exotex.knowledges.all()
        else : kws = []
        
        for k in kws : 
            elements += r" \item " +  k.name  

        elements += r"}"
 
    # Fermeture du texte dans le fichier tex
    elements +=  r"\end{document}"

    elements +=  settings.DIR_TMP_TEX    

    ################################################################# 
    ################################################################# Attention ERREUR si non modif
    # pour windows
    #file = settings.DIR_TMP_TEX+r"\\"+document
    # pour le serveur Linux
    file = settings.DIR_TMP_TEX+"/"+document
    ################################################################# 
    ################################################################# 
    f_tex = open(file+".tex","w")
    f_tex.write(elements)
    f_tex.close()
    result = subprocess.run(["pdflatex", "-interaction","nonstopmode",  "-output-directory", settings.DIR_TMP_TEX ,  file ])
    return FileResponse(open(file+".pdf", 'rb'),  as_attachment=True, content_type='application/pdf')

 








def academy_index(request):

	rq_user = request.user 

	if rq_user.is_board :
		levels = Level.objects.order_by("ranking")

		context = { 'levels' : levels   }

 
		return render(request, "academy/academy_index.html" , context)

	else:
		return redirect("index")



def details_adhesion(request,level_id):

	rq_user = request.user 

	if rq_user.is_board :
		today = time_zone_user(rq_user)
		level = Level.objects.get(pk=level_id)
		adhesions = Adhesion.objects.filter(levels=level,date_start__lte=today ,date_end__gte=today )

		context = { 'adhesions' : adhesions ,  'level' : level,   'historic' : False }

 
		return render(request, "academy/adhesions.html" , context)

	else:
		return redirect("index")



def historic_adhesions(request,level_id):

	rq_user = request.user 
	level = Level.objects.get(pk=level_id)
	if rq_user.is_board :
		adhesions = Adhesion.objects.filter(levels=level)

		context = { 'adhesions' : adhesions ,  'level' : level ,  'historic' : True   }

 
		return render(request, "academy/adhesions.html" , context)

	else:
		return redirect("index")



def autotests(request) :

	student   = request.user.student 
	autotests = Autotest.objects.filter(student=student )
	context   = { 'autotests' : autotests }

	return render(request, "academy/auto_tests.html" , context)




def create_autotest(request) :

	student  = request.user.student 
	form     = AutotestForm(request.POST or None, request.FILES or None )


	if request.method == "POST" :
		if form.is_valid():
			date = request.POST.get("date")

			studentanswers = Studentanswer.objects.filter(student=student, date__gte=date )

			knowledges , exotexs_exam = [] , []

			for studentanswer in studentanswers :
				if studentanswer.exercise.knowledge not in knowledges :
					knowledges.append(studentanswer.exercise.knowledge)

			exotexs = list( Exotex.objects.filter(knowledge__in=knowledges) )

			for i in range (5) :
				ind = random.randint(0,len(exotexs)-1)
				exotexs_exam.append(exotexs[ind])
				exotexs.remove(exotexs[ind])
 

			nf = form.save(commit=False)
			nf.file = printer_bibliotex_by_student(exotexs)
			nf.save()

	context   = { 'form' : form }
	return render(request, "academy/form_autotest.html" , context)





def delete_autotest(request,test_id) :

	student   = request.user.student 
	autotests = Autotest.objects.filter(student=student )
	context   = { 'autotests' : autotests }

	return render(request, "academy/auto_tests.html" , context)





def exemple_json(request):
    data = {}
    custom = request.POST.get("custom")
    image_id = request.POST.get("image_id")
    Customanswerimage.objects.get(pk = int(image_id)).delete()
    return JsonResponse(data)  


 