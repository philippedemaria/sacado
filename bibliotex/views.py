#################################
#### Auteur : philipe Demaria 
#### pour SACADO
#################################

from django.conf import settings # récupération de variables globales du settings.py
from django.shortcuts import render, redirect
from account.models import  Student, Teacher, User,Resultknowledge, Resultskill, Resultlastskill
from account.forms import StudentForm, TeacherForm, UserForm
from django.contrib.auth.forms import  AuthenticationForm
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import  permission_required,user_passes_test, login_required
from django.http import JsonResponse , FileResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from qcm.models import Folder , Parcours , Relationship
from qcm.views import get_teacher_id_by_subject_id, all_levels
from group.models import Group , Sharing_group
from socle.models import  Knowledge , Level , Skill , Waiting , Subject , Theme
from bibliotex.models import  Bibliotex , Exotex , Relationtex , Blacklistex
from bibliotex.forms import  BibliotexForm , ExotexForm , RelationtexForm , SetExotexForm
from django.views.decorators.csrf import csrf_exempt
from tool.consumers import *

import uuid
import time
import math
import json
import random
from datetime import datetime , timedelta
from django.db.models import Q
from django.core.mail import send_mail
from group.decorators import user_is_group_teacher 
from qcm.decorators import user_is_parcours_teacher, user_can_modify_this_course, student_can_show_this_course , user_is_relationship_teacher, user_is_customexercice_teacher , parcours_exists , folder_exists
from account.decorators import user_can_create, user_is_superuser, user_is_creator , user_is_testeur
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
import subprocess


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
def affectation_students_folders_groups(nf,group_ids,folder_ids):

    all_students = set()
    all_levels, all_subjects = [] , []
    for group_id in group_ids :    
        group = Group.objects.get(pk = group_id)
        group_students = group.students.all()
        all_students.update( group_students )   
        all_levels.append(group.level)
        all_subjects.append(group.subject)

    nf.levels.set(all_levels)
    nf.students.set(all_students) 
    nf.subjects.set(all_subjects) 

    for folder_id in folder_ids:
        folder = Folder.objects.get(pk=folder_id)
        folder.groups.set(group_ids)

    return all_students



def escape_multido(ctnt) : 
    ctnt = ctnt.replace(r"\point{1}","")
    ctnt = ctnt.replace(r"\point{2}","")
    ctnt = ctnt.replace(r"\point{3}","")
    ctnt = ctnt.replace(r"\point{4}","")
    ctnt = ctnt.replace(r"\point{5}","")
    ctnt = ctnt.replace(r"\point{6}","")
    ctnt = ctnt.replace(r"\point{7}","")
    ctnt = ctnt.replace(r"\point{8}","")
    ctnt = ctnt.replace(r"\point{9}","")
    ctnt = ctnt.replace(r"\point{10}","")
    ctnt = ctnt.replace(r"\point{11}","")
    return ctnt


def printer(request, relationtex_id, collection,output , obj):
    """affiche un exo ou une collection d'exercices, soit en pdf (output="pdf")
    soit en html (output="html") """

    # ouverture du texte dans le fichier tex
    landscape = request.POST.get("landscape",None)
    if output=="pdf" :
        if landscape :
            preamb = settings.TEX_PREAMBULE_PDF_FILE_LANDSCAPE
        else :
            preamb = settings.TEX_PREAMBULE_PDF_FILE

    elif output == "html" or output == "html_cor" :
        preamb = settings.TEX_PREAMBULE_FILE

    entetes=open(preamb,"r")
    elements=entetes.read()
    entetes.close()
    if relationtex_id == 0 : elements +=r"\setlength{\columnseprule}{1pt}\setlength{\columnseprule}{1pt}"
    elements +=r"\begin{document}"+"\n"

    print_title        = request.POST.get("print_title",None)  
    new_title          = request.POST.get("new_title",None) 
    texte_supplement   = request.POST.get("texte_supplement",None)
    linked_exercises   = request.POST.get("linked_exercises",None)
    multido            = request.POST.get("multido",None)

    columns   = request.POST.get("columns",None)
    correction = request.POST.get("correction",None) 

    ## Création du texte dans le fichier tex   
    if relationtex_id == 0 : # 0 pour la méthode POST
        if collection : 
            bibliotex_id = request.POST.get("print_bibliotex_id",None)  
            bibliotex    = Bibliotex.objects.get(pk = bibliotex_id)
            document     = "bibliotex" + str(bibliotex_id)
            if bibliotex.folders.count() and  bibliotex.parcours.count() : this_folder  =  bibliotex.folders.first().title + " > "+ bibliotex.parcours.first().title
            elif bibliotex.folders.count() and  not bibliotex.parcours.count() : this_folder  =  bibliotex.folders.first().title + " > "
            elif not bibliotex.folders.count() and  bibliotex.parcours.count() : this_folder  = " > "+ bibliotex.parcours.first().title
            else : this_folder = ""
            if new_title : title  = new_title
            else : title  = bibliotex.title
            author       = bibliotex.teacher.user.civilite+" "+bibliotex.teacher.user.last_name
        else :
            relationtex_id = request.POST.get("print_exotex_id",None)  
            relationtex    =  Relationtex.objects.get(pk = relationtex_id) 
            document       = "relationtex" + str(relationtex_id)
            title          =  relationtex.exotex.title
            author         = "Équipe SACADO"
 
            if relationtex.bibliotex.folders.count() and  relationtex.bibliotex.parcours.count() : this_folder  =  relationtex.bibliotex.folders.first().title + " > "+ relationtex.bibliotex.parcours.first().title
            elif relationtex.bibliotex.folders.count() and  not relationtex.bibliotex.parcours.count() : this_folder  =  relationtex.bibliotex.folders.first().title + " > "
            elif not relationtex.bibliotex.folders.count() and  relationtex.bibliotex.parcours.count() : this_folder  = " > "+ relationtex.bibliotex.parcours.first().title
            else : this_folder = ""

        if print_title : elements +=r"\titreFiche{"+title+r"}{"+author+r"}{"+this_folder+r"}"

        skills_printer     = request.POST.get("skills",None)  
        knowledges_printer = request.POST.get("knowledges",None)  
        relationtex_ids    = request.POST.getlist("relationtexs",None)
        sf_skills_first_printer = request.POST.get("sf_skills_first",None) 


        
        today = datetime.now()
        if collection and relationtex_ids :
            relationtex_ids = relationtex_ids[1:]
            relationtexs = bibliotex.relationtexs.filter(pk__in=relationtex_ids).order_by("ranking")
        elif collection : 
            relationtexs = bibliotex.relationtexs.filter(Q( is_publish = 1 )|Q(start__lte=today , stop__gte= today)).order_by("ranking")
            i = 1
        else: relationtexs=[relationtex]


        if texte_supplement : 
            elements +=  r"\\  "
            elements +=  texte_supplement 
            elements +=  r"\\  "


        if columns : elements += r"\begin{multicols}{2}"
        
        j = 1

        if sf_skills_first_printer :
            elements +=r"\begin{tabular}{|p{14cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|}" 
            elements +=r" \hline "  
            elements += r" SAVOIR FAIRE & MF & ECA & BM & TBM  \\"
            elements +=r" \hline "
            if knowledges_printer :
                k_ids = []
                k_string = ""
                # impression des savoir faire
                for relationtex in relationtexs :
                    k_id_display = relationtex.exotex.knowledge.id
                    if not k_id_display in k_ids :
                        elements += r" \raggedright " + relationtex.exotex.knowledge.name+r"  &   &   & & \\" 
                        elements +=r" \hline "   
                        k_ids.append(k_id_display)
                    if relationtex.knowledges.count()          : kws =  relationtex.knowledges.distinct()
                    elif  relationtex.exotex.knowledges.count(): kws =  relationtex.exotex.knowledges.distinct()
                    else : kws = []
                    for k in kws : 
                        elements += r"\raggedright " + k.name+r"  &   &   & & \\" 
                        elements +=r" \hline "   
                elements +=r"\end{tabular}  "


            if skills_printer : 
                elements +=r"\\"
                elements +=r"\begin{tabular}{|p{14cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|}" 
                elements +=r"\hline"  
                elements +=r" COMPETENCES & MF & ECA & BM & TBM \\"  
                elements +=r"\hline"

                if relationtex.skills.count():
                    sks =  relationtex.skills.all()
                else :
                    sks =  relationtex.exotex.skills.all()
                for s in sks :
                    elements += r"\raggedright " + s.name+r"  &   &   & & \\" 
                    elements +=r" \hline " 
                elements +=r"\end{tabular}"
 
        for relationtex in relationtexs :
        
            skills_display = ""
            if not sf_skills_first_printer and skills_printer :  
                if relationtex.skills.count():
                    sks =  relationtex.skills.all()
                else :
                    sks =  relationtex.exotex.skills.all()
                for s in sks :
                    skills_display +=  s.name+". "
                skill_dpl = r"\competence{" +skills_display+r"}"
            else : skill_dpl = ""

            pref_image = '/var/www/sacado/static/img/'

            if relationtex.exotex.calculator : calculator = pref_image + 'calculator.png'
            else : calculator = pref_image + 'no_calculator.png'   

            details = r'\includegraphics[scale=0.6]{'+calculator+r'}'

            if relationtex.exotex.is_python : 
                img_python = pref_image +'is_python.png'
                details += r'\includegraphics[scale=0.4]{'+img_python+r'}'

            if relationtex.exotex.is_scratch : 
                img_scratch = pref_image +'is_scratch.png'
                details += r'\includegraphics[scale=0.4]{'+img_scratch+r'}'

            if relationtex.exotex.is_tableur : 
                img_tableur = pref_image + 'is_tableur.png'
                details += r'\includegraphics[scale=0.4]{'+img_tableur+r'}'

            details_skills = details +  skill_dpl

            if request.POST.get("print_frame",None) :
                str_elements = ""
                # impression des savoir faire
                if not sf_skills_first_printer and knowledges_printer :  
                    k_display = relationtex.exotex.knowledge.name
                    str_elements = r"\savoirs{  \item " +  k_display 
                    if relationtex.knowledges.count()          : kws =  relationtex.knowledges.all()
                    elif  relationtex.exotex.knowledges.count(): kws =  relationtex.exotex.knowledges.all()
                    else : kws = []
                    for k in kws : 
                        str_elements += r" \item " +  k.name  
                    str_elements += r"}"

                if output == "html_cor" :
                    ctnt =  relationtex.exotex.correction
                elif output == "html" :
                    ctnt =  relationtex.exotex.content
                else :
                    ctnt =  relationtex.exotex.content

                    if not multido : ctnt = escape_multido(ctnt) 

                elements += r"\begin{GeneriqueT}{Exercice }{\;}"+str_elements +r" \\"+ctnt+r"\end{GeneriqueT}"

            else :
                try :
                    if request.POST.get("all_titles",None)   :
                        elements += r"\\ \exercice{Exercice "+ str(j) + r"} {\bf " +  relationtex.exotex.title  +  r" } " + details_skills
                    else :
                        elements += r"\\ \exercice{Exercice "+ str(j) + r"} "+ details_skills
                except :
                    elements += r"\\ \exercice{Exercice "+ str(j) + r"} "+ details_skills
                j+=1

                # impression des savoir faire
                if not sf_skills_first_printer and knowledges_printer :  
                    k_display = relationtex.exotex.knowledge.name
                    elements += r"\savoirs{  \item " +  k_display 
                    if relationtex.knowledges.count()          : kws =  relationtex.knowledges.all()
                    elif  relationtex.exotex.knowledges.count(): kws =  relationtex.exotex.knowledges.all()
                    else : kws = []
                    for k in kws : 
                        elements += r" \item " +  k.name  
                    elements += r"}"

                elements += r"\vspace{0.2cm}"
                
                if output == "html_cor" :
                    ctnt =  relationtex.exotex.correction
                elif output == "html" :
                    ctnt =  relationtex.exotex.content
                else :
                    ctnt =  relationtex.exotex.content
                    if not multido : ctnt = escape_multido(ctnt) 
                elements += ctnt


            if linked_exercises :

                exs = relationtex.exercises.order_by("ranking")
                if exs.count() > 0 :             
                    text_linked = "Compléments : "
                    for exercise in exs :
                        text_linked += str(exercise.supportfile.code ) + " | "
                    elements +=  text_linked 

                # exercises =  relationtex.exotex.exercises.order_by("ranking")
                # for e in exercises :
                #     elements +=  "exe : "+e.supportfile.code +" | "




            elements +=  r"\\ "


        if correction : 
            elements += r"\newpage"
            elements += r"\centerline{ \fbox{Corrigé} }"
            k=1
            for relationtex in relationtexs :
                if  relationtex.exotex.correction :
                    elements += r" \\ \vspace{0.1cm} \exercice{Exercice "+ str(k) + r"} \\"
                    elements += relationtex.exotex.correction
                    elements += r" \vspace{0.1cm}"
                else :
                    elements += r"\\ \vspace{0.1cm} \exercice{Exercice "+ str(k) + r"} - Non corrigé \\"
                    elements += r" \vspace{0.1cm}"
                k+=1
       
    else : #pour la création d'un exercise ou son update*

        try :
            if obj == "R" : 
                relationtex = Relationtex.objects.get(pk = relationtex_id)
                title       =  relationtex.exotex.title
                if output == "html_cor" :
                    ctnt =  relationtex.exotex.correction
                elif output == "html" :
                    ctnt =  relationtex.exotex.content 
                else :
                    ctnt =  relationtex.exotex.content 
                    if not multido : ctnt = escape_multido(ctnt) 

            else : 
                exotex = Exotex.objects.get(pk = relationtex_id)
                title  = exotex.title
                 
                if output == "html_cor" :
                    ctnt =  exotex.correction
                elif output == "html" :
                    ctnt =  exotex.content 
                else :
                    ctnt =  exotex.content 
                if not multido : ctnt = escape_multido(ctnt) 
        except :
            exotex = Exotex.objects.get(pk = relationtex_id)
            title  =  exotex.title
            if output == "html_cor" :
                ctnt =  exotex.correction
            elif output == "html" :
                ctnt =  exotex.content
            else :
                ctnt =  exotex.content 

        ctnt = ctnt.replace(r"\mathcal","")
        if not multido : ctnt = escape_multido(ctnt) 
        document       = "relationtex" + str(relationtex_id)
        author         = "Équipe SACADO"

        elements += ctnt
        elements += r" \vspace{0,1cm}"
    # Fermeture du texte dans le fichier tex
    if columns : elements +=r"\end{multicols}"
    elements +=  r"\end{document}"


    ################################################################# 
    ################################################################# Attention ERREUR si non modif
    # pour windows
    #file = settings.DIR_TMP_TEX+r"\\"+document
    # pour le serveur Linux
    file = settings.DIR_TMP_TEX+ str(request.user.id)+"_"+document
    ################################################################# 
    ################################################################# 

    f_tex = open(file+".tex","w")
    f_tex.write(elements)
    f_tex.close()


    if output=="pdf" :
        result = subprocess.run(["pdflatex", "-interaction","nonstopmode",  "-output-directory", settings.DIR_TMP_TEX  ,  file ])

        try :
            return FileResponse(open(file+".pdf", 'rb'),  as_attachment=True, content_type='application/pdf')
        except :
            return FileResponse(open(file+".log", 'rb'),  as_attachment=True, content_type='application/pdf')

    elif output == "html" or output== "html_cor" :
        #result = subprocess.run(["make4ht" ,  "-u" ,  file+".tex" , "mathml"] , cwd = settings.DIR_TMP_TEX )
        os.chdir(settings.DIR_TMP_TEX)
        os.system("make4ht -u "+document+".tex mathml")
        fhtml  = open(file+".html","r", errors='ignore')
        out    = ""
        recopie=False
        i=0
        for ligne in fhtml :
            ligne = ligne.replace('src="','src="https://sacado.xyz/ressources/tex/tmp_tex/')
            if "</body>" in ligne : recopie=False
            if recopie : out+=ligne
            if i  ==  9 : recopie=True
            i+=1
        return out


    else : 
        print("format output non reconnu")
        return 


def printer_bibliotex_by_student(request, bibliotex):
    """affiche un exo ou une collection d'exercices, en pdf (output="pdf") """

    # ouverture du texte dans le fichier tex

    preamb = settings.TEX_PREAMBULE_PDF_FILE

    entetes=open(preamb,"r")
    elements=entetes.read()
    entetes.close()

    elements +=r"\begin{document}"+"\n"   

    ## Création du texte dans le fichier tex   

 
    document     = "bibliotex" + str(bibliotex.id)
    title        = bibliotex.title
    author       = bibliotex.teacher.user.civilite+" "+bibliotex.teacher.user.last_name

    elements +=r"\titreFiche{"+title+r"}{"+author+r"}"

    today = datetime.now()
 
    relationtexs = bibliotex.relationtexs.filter(Q( is_publish = 1 )|Q(start__lte=today , stop__gte= today)).order_by("ranking")
 

    j = 1
    for relationtex in relationtexs :
    
        skills_display = ""
        if relationtex.skills.count():
            sks =  relationtex.skills.all()
        else :
            sks =  relationtex.exotex.skills.all()
        for s in sks :
            skills_display +=  s.name+". "
            

        elements += r"\exo {\bf " +  relationtex.exotex.title  +  r" }    \competence{" +skills_display+r"}"
        
        j+=1

        ctnt =  relationtex.exotex.content
        
        elements += r"\vspace{0,2cm}\\"
        elements += ctnt
        elements += r"\vspace{0,2cm}\\"

        if  relationtex.is_publish_cor  :
            elements += r"\textbf{ Correction :} \\"
            elements += relationtex.exotex.correction
            elements += r"\vspace{0,2cm}\\"
 


    # Fermeture du texte dans le fichier tex
    elements +=  r"\end{document}"

    #elements +=  settings.DIR_TMP_TEX    

    ################################################################# 
    ################################################################# Attention ERREUR si non modif
    # pour windows
    #file = settings.DIR_TMP_TEX+r"\\"+document
    # pour le serveur Linux
    file = settings.DIR_TMP_TEX+ str(request.user.id)+"_"+document
    ################################################################# 
    ################################################################# 
    f_tex = open(file+".tex","w")
    f_tex.write(elements)
    f_tex.close()
    result = subprocess.run(["pdflatex", "-interaction","nonstopmode",  "-output-directory", settings.DIR_TMP_TEX  ,  file ])

    if os.path.isfile(file+".out"):os.remove(file+".out")
    if os.path.isfile(file+".aux"):os.remove(file+".aux")    
    if os.path.isfile(file+".log"):os.remove(file+".log")

    return FileResponse(open(file+".pdf", 'rb'),  as_attachment=True, content_type='application/pdf')

 


#########################################################################################################################################
#########################################################################################################################################
######## Exotex
#########################################################################################################################################
#########################################################################################################################################

def admin_exotexs(request,idl):

    if request.user.is_superuser or request.user.is_extra :  # admin and more
        teacher = request.user.teacher
        level = Level.objects.get(pk=idl)
        exos = Exotex.objects.all()
        waitings = level.waitings.filter(theme__subject__in= teacher.subjects.all()).order_by("theme__subject" , "theme")

    return render(request, 'bibliotex/list_exotexs.html', { 'waitings': waitings, 'teacher':teacher , 'level':level   })


 
def my_exotexs(request):

    teacher = request.user.teacher 
    exos = Exotex.objects.filter( Q(author=teacher)|Q(teachers=teacher) )
    return render(request, 'bibliotex/list_exotexs.html', {'exos': exos,  'teacher':teacher , })


def compile_html(request,nf):

    save_html = False
    if r'\ps' in nf.content or r'\ps' in nf.correction :
        messages.error(request,'Votre contenu contient du pstricks. Il ne peut pas être compilé correctement.')
    else :
        
        try :
            if nf.content_html == "" :
                Exotex.objects.filter(pk= nf.id).update( content_html = printer(request, nf.id, False , "html" , "E" )   )
            if nf.correction_html == "" :
                Exotex.objects.filter(pk= nf.id).update( correction_html = printer(request, nf.id, False , "html_cor" , "E" )   )
            save_html = True    
        except :
            save_html = False

    return save_html 


@user_passes_test(user_is_creator)
def create_exotex_knowledge(request,idk):

    knowledge = Knowledge.objects.get(id = idk)
    teacher = request.user.teacher
    form = ExotexForm(request.POST or None,request.FILES or None, teacher = teacher , knowledge = knowledge , initial={'author':teacher,'teachers':teacher,'knowledge':knowledge} )


    if form.is_valid():
        nf = form.save(commit = False) 
        nf.author = teacher
        nf.teacher = teacher
        nf.save()
        form.save_m2m()
        save_html = compile_html(request,nf)

        if save_html :
            messages.success(request, "L'exercice a été créé avec succès !")
        else :
            messages.error(request,"Le contenu html ne s'est pas enregistré. Modifier l'exercice et changer l'encodage.")

        return redirect('admin_exotexs', knowledge.level.id)
    else:
        print(form.errors)

    context = {'form': form, 'knowledge': knowledge , 'exotex': None }

    return render(request, 'bibliotex/form_exotex.html', context)



def set_exotex_in_bibliotex(request,id):

    bibliotex = Bibliotex.objects.get(id=id)
    teacher = request.user.teacher
    form = SetExotexForm(request.POST or None,request.FILES or None, teacher = teacher , knowledge = None )

    if form.is_valid():
        nf = form.save(commit = False) 
        nf.author = teacher
        nf.teacher = teacher
        nf.is_share = 0
        nf.is_read = 0
        knowledges = request.POST.getlist("knowledgess")
        try :
            nf.knowledges.set(knowledges)
        except :
            pass

        nf.save()
        form.save_m2m() 
        
        try :
            save_html = compile_html(request,nf)
        except : save_html = False

        try :bibliotex.exotexs.add(nf)
        except : pass
        try :
            msg = "Salut Bruno, Philippe, \n\nUn exercice Latex vient d'être posté. Vous devriez aller y jeter quand même un oeil.\n\n ===> https://savado.xyz/bibliotex/exercise_exotex_update/"+str(nf.pk)
        except : msg = "Erreur dans le message d'envoi."

        send_mail('SACADO : Exercice Latex', msg ,settings.DEFAULT_FROM_EMAIL,['brunoserres33@gmail.com', 'philippe.demaria83@gmail.com'])

        if save_html :
            messages.success(request, "L'exercice a été créé avec succès !")
        else :
            messages.error(request,"Le contenu html ne s'est pas enregistré. Modifier l'exercice et changer l'encodage.")


        return redirect('my_bibliotexs')
    else:
        print(form.errors)

    context = {'form': form, 'exotex': "init" , 'knowledge': None  }

    return render(request, 'bibliotex/form_exotex.html', context)


 
def create_exotex(request):

    teacher = request.user.teacher
    form = ExotexForm(request.POST or None,request.FILES or None, teacher = teacher , knowledge = None )

    if form.is_valid():
        nf = form.save(commit = False) 
        nf.author = teacher
        nf.teacher = teacher
        nf.is_share = 1
        nf.save()
        form.save_m2m() 
        save_html = compile_html(request,nf)

        if save_html :
            msg = "Bonjour l'équipe,\n\n Un exercice Tex vient d'être posté par "+ request.user.get_full_name() +".\n\nPour le visualiser : https://sacado.xyz/bibliotex/exercise_exotex_update/"+str(nf.id)+" .\n\nCet exercice n'est pas encore mutualisé.\n\nCeci est un mail automatique. Merci de ne pas répondre."
            sending_mail("SACADO : Exercice TEX ",  msg  , settings.DEFAULT_FROM_EMAIL , ["sacado.asso@gmail.com"])    
            messages.success(request, "L'exercice a été créé avec succès !")
        else :
            messages.error(request,"Le contenu html ne s'est pas enregistré. Modifier l'exercice et changer l'encodage.")

        return redirect('admin_exotexs', nf.knowledge.level.id)
    else:
        print(form.errors)

    context = {'form': form, 'exotex': None  }

    return render(request, 'bibliotex/form_exotex.html', context)


 
def update_exotex(request, id):

    exotex = Exotex.objects.get(id=id)
    teacher = request.user.teacher
    form = ExotexForm(request.POST or None, request.FILES or None, instance=exotex , teacher = teacher , knowledge = exotex.knowledge )
    if request.method == "POST" :
        if form.is_valid():
            nf = form.save(commit = False) 
            nf.author = teacher
            nf.teacher = teacher
            nf.save()
            form.save_m2m()  
            save_html = compile_html(request,nf)

            if save_html :
                msg = "Bonjour l'équipe,\n\n Un exercice Tex vient d'être modifié avec succès par "+ request.user.get_full_name() +".\n\nPour le visualiser : https://sacado.xyz/bibliotex/exercise_exotex_update/"+str(nf.id)+" .\n\nCet exercice n'est pas encore mutualisé.\n\nCeci est un mail automatique. Merci de ne pas répondre."
                sending_mail("SACADO : Exercice TEX modifié",  msg  , settings.DEFAULT_FROM_EMAIL , ["sacado.asso@gmail.com"]) 

                messages.success(request, "L'exercice a été créé avec succès !")
            else :
                messages.error(request,"Le contenu html ne s'est pas enregistré. Modifier l'exercice et changer l'encodage.")
            
            return redirect('admin_exotexs', exotex.knowledge.level.id)
        else:
            print(form.errors)

    context = {'form': form,  'exotex': exotex, 'knowledge': exotex.knowledge ,   }

    return render(request, 'bibliotex/form_exotex.html', context )


 
def delete_exotex(request, id):
    exotex = Exotex.objects.get(id=id)
    level_id = exotex.knowledge.level.id
    if request.user == exotex.author.user or request.user.is_superuser :
        messages.success(request,"Exercice en Tex supprimé")
        exotex.delete()
    else :
        messages.error(request,"Errue de suppression")

    return redirect('admin_exotexs', level_id)


  
def show_exotex(request, id):
    exotex = Exotex.objects.get(id=id)
  
    context = { 'exotex': exotex,   }

    return render(request, 'bibliotex/show_exotex.html', context )




def ajax_action_exotex(request, id):
    pass
 


def div_to_display_latex(request):

    this_text = request.POST.get('this_text')
    this_correction = request.POST.get('this_correction',None)

    preamb = settings.TEX_PREAMBULE_PDF_FILE

    entetes=open(preamb,"r")
    elements=entetes.read()
    entetes.close()

    elements +=r" \begin{document} " 
    elements += this_text
    elements += r" \newpage "
    if  this_correction : 
        elements += r" \centerline{ \fbox{Corrigé} } "
        elements += this_correction

    elements +=  r" \end{document}"
    ################################################################# 
    ################################################################# Attention ERREUR si non modif
    file_path = settings.DIR_TMP_TEX + str(request.user.id)+"_exotex_display"
    ################################################################# 
    ################################################################# 
    with open(file_path+".tex", 'w') as file:
        file.write(elements)
        file.close()

    result = subprocess.run(["pdflatex", "-interaction","nonstopmode",  "-output-directory", settings.DIR_TMP_TEX  ,  file_path ])

    #return FileResponse(open(file_path+".pdf", 'rb'),  as_attachment=True, content_type='application/pdf')
    data={}
    if os.path.isfile(file_path+".out"):os.remove(file_path+".out")
    if os.path.isfile(file_path+".aux"):os.remove(file_path+".aux")   
    if result.returncode : 
        data['test'] = False
        data['html'] = "https://sacado.xyz/ressources/tex/tmp_tex/"+str(request.user.id)+"_exotex_display.log"
    else : 
        if os.path.isfile(file_path+".log"):os.remove(file_path+".log") 
        data['test'] = True
        data['html'] = "https://sacado.xyz/ressources/tex/tmp_tex/"+str(request.user.id)+"_exotex_display.pdf"

    return JsonResponse(data)
 
def update_relationtex(request, id):

    relationtex = Relationtex.objects.get(id=id)
    bibliotex_id = relationtex.bibliotex.id

    content = relationtex.exotex.content
    correction = relationtex.exotex.correction

    teacher = request.user.teacher
    form = RelationtexForm(request.POST or None, request.FILES or None, instance = relationtex , teacher = teacher , initial = { 'content' : content , 'correction' : correction } )
    if request.method == "POST" :
        if form.is_valid():
            nf = form.save(commit = False) 
            nf.teacher = teacher
            nf.save()
            form.save_m2m()  

            Relationtex.objects.filter(pk= nf.id).update( content_html = printer(request, nf.id, False , "html" , "R" )   )
            if nf.correction :  
                Relationtex.objects.filter(pk= nf.id).update( correction_html = printer(request, nf.id, False , "html_cor" , "R" )   )

            messages.success(request, "L'exercice a été modifié avec succès !")
            return redirect('show_bibliotex', bibliotex_id )
        else:
            print(form.errors)

    context = {'form': form,  'relationtex': relationtex,   }

    return render(request, 'bibliotex/form_relationtex.html', context )


def delete_relationtex(request, id):
    relationtex  = Relationtex.objects.get(id=id)
    bibliotex_id = relationtex.bibliotex.id
 
    if request.user == relationtex.teacher.user :
        relationtex.delete()

    return redirect('show_bibliotex', bibliotex_id)




def exotex_display_pdf(request,ide):

    preamb = settings.TEX_PREAMBULE_PDF_FILE

    entetes=open(preamb,"r")
    elements=entetes.read()
    entetes.close()

    exotex = Exotex.objects.get(pk=ide)

    elements +=r"\begin{document}"+"\n"  
    elements += exotex.content
    elements += r"\newpage"
    elements += r"\centerline{ \fbox{Corrigé} }"
    elements += exotex.correction

    elements +=  r"\end{document}"
    ################################################################# 
    ################################################################# Attention ERREUR si non modif
    # pour windows
    # file_path = settings.DIR_TMP_TEX+r"\\doc" 
    # pour le serveur Linux
    file_path = settings.DIR_TMP_TEX + str(request.user.id)+"_bibliotex_display"
    ################################################################# 
    ################################################################# 
    with open(file_path+".tex", 'w') as file:
        file.write(elements)
        file.close()

    result = subprocess.run(["pdflatex", "-interaction","nonstopmode",  "-output-directory", settings.DIR_TMP_TEX  ,  file_path ])

    if result.returncode :  
        return FileResponse(open(file_path+".log", 'rb'))
    else : 
        if os.path.isfile(file_path+".out"):os.remove(file_path+".out")
        if os.path.isfile(file_path+".aux"):os.remove(file_path+".aux")    
        if os.path.isfile(file_path+".log"):os.remove(file_path+".log") 
        return FileResponse(open(file_path+".pdf", 'rb'))


def print_exotex_by_student(request,ide):

    preamb = settings.TEX_PREAMBULE_PDF_FILE

    entetes=open(preamb,"r")
    elements=entetes.read()
    entetes.close()

    relationtex = Relationtex.objects.get(pk=ide)

    elements +=r"\begin{document}"+"\n"
    elements += relationtex.exotex.content
    elements +=  r"\end{document}"
    ################################################################# 
    ################################################################# Attention ERREUR si non modif
    # pour windows
    # file_path = settings.DIR_TMP_TEX+r"\\doc" 
    # pour le serveur Linux
    file_path = settings.DIR_TMP_TEX + str(request.user.id)+"_exotex_display"
    ################################################################# 
    ################################################################# 
    with open(file_path+".tex", 'w') as file:
        file.write(elements)
        file.close()

    result = subprocess.run(["pdflatex", "-interaction","nonstopmode",  "-output-directory", settings.DIR_TMP_TEX  ,  file_path ])

    if result.returncode :  
        return FileResponse(open(file_path+".log", 'rb'))
    else : 
        if os.path.isfile(file_path+".out"):os.remove(file_path+".out")
        if os.path.isfile(file_path+".aux"):os.remove(file_path+".aux")    
        if os.path.isfile(file_path+".log"):os.remove(file_path+".log") 
        return FileResponse(open(file_path+".pdf", 'rb'))

#########################################################################################################################################
#########################################################################################################################################
######## Bibliotex
#########################################################################################################################################
#########################################################################################################################################
def bibliotexs(request):

    group_id = request.session.get("group_id",None)
    folder_id = request.session.get("folder_id",None)
    parcours_id = request.session.get("parcours_id",None)

    group, folder, parcours = None, None, None

    if group_id : group = Group.objects.get(pk=group_id)
    if folder_id : folder = Folder.objects.get(pk=folder_id)
    if parcours_id : parcours = Parcours.objects.get(pk=parcours_id)


    bibliotexs = Bibliotex.objects.all()
    teacher = request.user.teacher

    return render(request, 'bibliotex/all_bibliotexs.html', {'bibliotexs': bibliotexs,'teacher': teacher,'group': group,'folder': folder,'parcours': parcours })


 
def my_bibliotexs(request):

    request.session["folder_id"] = None
    request.session["group_id"] = None    
    request.session["parcours_id"] = False
    teacher = request.user.teacher

    dataset_user = teacher.teacher_bibliotexs
    dataset      = dataset_user.filter(is_archive=0)

    bibliotexs = dataset.filter(folders=None)
    bibliotexs_folders = dataset.values_list("folders", flat=True).exclude(folders=None).distinct().order_by("folders")

    request.session["tdb"] = "Documents"  
    request.session["subtdb"] = "Bibliotex"

    list_folders, list_details = list(), list()
    for folder in bibliotexs_folders :
        bibtexs_folders = dict()
        fld = Folder.objects.get(pk=folder)
        bibtexs_folders["folder"] = fld
        bibtexs_folders["bibliotexs"] = dataset.filter(folders=folder).order_by("levels")  

        these_details = (fld.title, fld.level, fld.subject)
        if not these_details in list_details : 
            list_details.append(these_details)
            list_folders.append(bibtexs_folders)


    groups = teacher.has_groups() # pour ouvrir le choix de la fenetre modale pop-up
 
 
    nb_archive = dataset_user.filter(  is_archive=1).count()
    return render(request, 'bibliotex/list_bibliotexs.html', { 'list_folders': list_folders , 'bibliotexs': bibliotexs , 'teacher': teacher,  'groups': groups,   'nb_archive' : nb_archive  })



def my_bibliotex_archives(request):

    request.session["folder_id"] = None
    request.session["group_id"] = None
    teacher = request.user.teacher
 
    dataset = teacher.teacher_bibliotexs.filter(is_archive=1)

    bibliotexs = dataset.filter(folders=None)
    bibliotexs_folders = dataset.values_list("folders", flat=True).exclude(folders=None).distinct().order_by("folders")

    request.session["tdb"] = "Documents"  
    request.session["subtdb"] = "Bibliotex"

 
    list_folders, list_details = list(), list()
    for folder in bibliotexs_folders :
        bibtexs_folders = dict()
        fld = Folder.objects.get(pk=folder)
        bibtexs_folders["folder"] = fld
        bibtexs_folders["bibliotexs"] = dataset.filter(folders=folder).order_by("levels")  

        these_details = (fld.title, fld.level, fld.subject)
        if not these_details in list_details : 
            list_details.append(these_details)
            list_folders.append(bibtexs_folders)

    groups = teacher.has_groups() # pour ouvrir le choix de la fenetre modale pop-up
 
    return render(request, 'bibliotex/list_bibliotexs_archives.html', { 'list_folders': list_folders , 'bibliotexs': bibliotexs , 'teacher': teacher,  'groups': groups  })



def ajax_my_bibliotexs(request):

    level_id = request.POST.get("level_id")
    subject_id = request.POST.get("subject_id")

    teacher = request.user.teacher 
    data = {}
    level =  Level.objects.get(pk = level_id)
    subject =  Subject.objects.get(pk = subject_id)
    bibliotexs = Bibliotex.objects.filter( Q(author=teacher)|Q(teacher=teacher)|Q(coteachers=teacher)  ,  subjects = subject   ,  levels = level ).distinct()

    data['html'] = render_to_string('bibliotex/ajax_list_bibliotexs.html', {'bibliotexs' : bibliotexs , })

    return JsonResponse(data)



def create_bibliotex_sequence(request,id):

    teacher = request.user.teacher
    folder_id = request.session.get("folder_id",None)
    group_id = request.session.get("group_id",None)
    if group_id :group = Group.objects.get(id=group_id)
    else : group = None
    if folder_id : folder = Folder.objects.get(id=folder_id)
    else : folder = None

    request.session["tdb"] = "Documents"  
    request.session["subtdb"] = "Bibliotex"


    parcours = Parcours.objects.get(id=id)

    form = BibliotexForm(request.POST or None,request.FILES or None, teacher = teacher, group = group,  folder = folder,  initial = { 'folders'  : [folder] ,  'groups'  : [group] ,  'parcours'  : [parcours]  } )

    if form.is_valid():
        nf = form.save(commit = False) 
        nf.author = teacher
        nf.teacher = teacher
        nf.save()
        form.save_m2m() 

        group_ids = request.POST.getlist("groups",[])
        folder_ids = request.POST.getlist("folders",[])
        nf.groups.set(group_ids)
        nf.folders.set(folder_ids)
        all_students = affectation_students_folders_groups(nf,group_ids,folder_ids)

        relation = Relationship.objects.create(parcours = parcours , exercise_id = None , document_id = nf.id  , type_id = 5 , ranking =  200 , is_publish= 1 , start= None , date_limit= None, duration= 10, situation= 0 ) 
        students = parcours.students.all()
        relation.students.set(students)
 
        return redirect('exercise_bibliotex_peuplate', nf.id)

    else:
        print(form.errors)

    context = {'form': form, 'bibliotex': None, 'folder': folder, 'group': group, 'parcours': parcours   }

    return render(request, 'bibliotex/form_bibliotex.html', context)





def ajax_find_peuplate_sequence(request):

    id_parcours = request.POST.get("id_parcours",0)
    subject_id  = request.POST.get("id_subject",0) 
    level_id    = request.POST.get("id_level",None) 
    keyword     = request.POST.get("keyword",None) 

    level       = Level.objects.get(pk=level_id)
    subject     = Subject.objects.get(pk=subject_id)

    if keyword :
        bibliotexs  = Bibliotex.objects.filter(  Q(teacher__user=request.user)|Q(is_share =  1) , title__icontains=keyword,     subjects=subject,levels=level ) #teacher__user__school = request.user.school ,
    else :
        bibliotexs  = Bibliotex.objects.filter( Q(teacher__user=request.user)|Q(is_share =  1) , subjects=subject,levels=level ) #teacher__user__school = request.user.school ,
 

    if keyword and level_id :
        level = Level.objects.get(pk=level_id)
        bibliotexs  = Bibliotex.objects.filter(  Q(teacher__user=request.user)|Q(is_share =  1) , title__icontains=keyword,   subjects=subject,levels=level  ) #teacher__user__school = request.user.school ,
    elif keyword :
        bibliotexs  = Bibliotex.objects.filter(  Q(teacher__user=request.user)|Q(is_share =  1) , title__icontains=keyword,   subjects=subject  ) #teacher__user__school = request.user.school ,
    else :
        level = Level.objects.get(pk=level_id)
        bibliotexs  = Bibliotex.objects.filter( Q(teacher__user=request.user)|Q(is_share =  1) ,   subjects=subject ,levels=level ) #teacher__user__school = request.user.school ,



    context = { "bibliotexs" : bibliotexs }

    data = {}
    data['html']    = render_to_string( 'bibliotex/ajax_bibliotex_peuplate_sequence.html' , context)

    return JsonResponse(data)  



def clone_bibliotex_sequence(request, idb):
    """ cloner un parcours """

    teacher = request.user.teacher
    bibliotex = Bibliotex.objects.get(pk=idb) # parcours à cloner.pk = None
    relationtexs = bibliotex.relationtexs.all()
    bibliotex.pk = None
    bibliotex.teacher = teacher
    bibliotex.save()

    parcours_id = request.session.get("parcours_id",None) 
    if parcours_id :
        parcours = Parcours.objects.get(pk = parcours_id)
        relation = Relationship.objects.create(parcours = parcours , exercise_id = None , document_id = bibliotex.id  , type_id = 5 , ranking =  200 , is_publish= 1 , start= None , date_limit= None, duration= 10, situation= 0 ) 
        students = parcours.students.all()
        relation.students.set(students) 
                
    for r in relationtexs :
        r.pk = None
        r.teacher = teacher
        r.save()
        
        if parcours_id :
            r.students.set(students)



    return redirect('show_parcours' , 0, parcours_id )




def ajax_search_bibliotex_by_level(request):

    teacher = request.user.teacher
    data = {}
    level_id =  request.POST.get("id_level",None)
    subject_id =  request.POST.get("id_subject",None)  
    id_annale  = request.POST.get('is_annale',None)
    teacher_id = get_teacher_id_by_subject_id(subject_id) 
    base = Bibliotex.objects.filter(Q(teacher = teacher)|Q(teacher__user__school = teacher.user.school)| Q( teacher__user_id=teacher_id ) ,is_share = 1) 
    
    if subject_id :       
        subject = Subject.objects.get(pk=int(subject_id))
        base = base.filter( subjects = subject)

    if level_id :
        level = Level.objects.get(pk=int(level_id))
        thms  = level.themes.values_list('id', 'name').filter(subject_id=subject_id).order_by("name")
        data['themes'] = list(thms)
        base = base.filter(  levels = level )
    
    bibliotexs = base.order_by('teacher')

            
    if id_annale == "yes" :
        annales = set()
        for bibliotex in bibliotexs :
            if bibliotex.is_annale() :
                annales.add(bibliotex)
    else :
        annales=bibliotexs

    data['html'] = render_to_string('bibliotex/ajax_list_bibliotexs.html', {'bibliotexs' : annales, 'teacher' : teacher ,  })

    return JsonResponse(data)

 

def ajax_search_bibliotex(request):

    teacher = request.user.teacher
    data = {}

    level_id   = request.POST.get('level_id',None)
    subject_id = request.POST.get('subject_id',None)
    id_annale  = request.POST.get('is_annale',None)
    keywords = request.POST.get('keyword',None)   
    theme_ids = request.POST.getlist('theme_id',[])

    teacher_id = get_teacher_id_by_subject_id(subject_id)
    base = Bibliotex.objects.filter(Q(teacher = teacher)|Q(teacher__user__school = teacher.user.school)|Q(author__user_id=teacher_id),  is_share = 1)

    if subject_id :
        subject = Subject.objects.get(pk=subject_id)
        base = base.filter(subjects=subject)

    try :
        level = Level.objects.get(pk=int(level_id))
        base = base.filter( levels = level )
    except :pass

    if  keywords :
        #base = base.filter(Q(title__icontains = keywords) |  Q(exotexs__title__icontains = keywords) | Q(exotexs__content__icontains = keywords) |Q(teacher__user__first_name__icontains = keywords) |Q(teacher__user__last_name__icontains = keywords))
        base = base.filter(title__icontains= keywords)




    if len(theme_ids) > 0 and theme_ids[0] != '' :
        base = base.filter(exotexs__knowledge__theme_id__in = theme_ids )

    bibliotexs = base.order_by('teacher')

            
    if id_annale == "yes" :
        annales = set()
        for bibliotex in bibliotexs :
            if bibliotex.is_annale() :
                annales.add(bibliotex)
    else :
        annales=bibliotexs


    data['html'] = render_to_string('bibliotex/ajax_list_bibliotexs.html', {'bibliotexs' : annales, 'teacher' : teacher ,  })
 
    return JsonResponse(data)


 

def create_bibliotex(request,idf=0):

    request.session["tdb"] = "Documents"  
    request.session["subtdb"] = "Bibliotex"

    teacher = request.user.teacher
    folder_id = request.session.get("folder_id",idf)
    group_id = request.session.get("group_id",None)
    if group_id :
        group = Group.objects.get(id=group_id)
    else :
        group = None

    if folder_id :
        folder = Folder.objects.get(id=folder_id)
    else :
        folder = None

    form = BibliotexForm(request.POST or None,request.FILES or None, teacher = teacher,  group = group, folder = folder , initial = {  'groups'  : [group] , 'folders' : [folder] } )

    if form.is_valid():
        nf = form.save(commit = False) 
        nf.author = teacher
        nf.teacher = teacher
        nf.save()
        form.save_m2m() 

        group_ids = request.POST.getlist("groups",[])
        folder_ids = request.POST.getlist("folders",[])
        nf.groups.set(group_ids)
        nf.folders.set(folder_ids)
        all_students = affectation_students_folders_groups(nf,group_ids,folder_ids)

        return redirect('exercise_bibliotex_peuplate', nf.id)

    else:
        print(form.errors)

    context = {'form': form, 'bibliotex': None, 'folder': folder, 'group': group  }

    return render(request, 'bibliotex/form_bibliotex.html', context)




def update_bibliotex(request, id):

    request.session["tdb"] = "Documents"  
    request.session["subtdb"] = "Bibliotex"
    teacher = request.user.teacher
    bibliotex = Bibliotex.objects.get(id=id)
    folder_id = request.session.get("folder_id",None)
    group_id = request.session.get("group_id",None)
    if group_id :
        group = Group.objects.get(id=group_id)
    else :
        group = None

    if folder_id :
        folder = Folder.objects.get(id=folder_id)
    else :
        folder = None


    form = BibliotexForm(request.POST or None, request.FILES or None, instance=bibliotex, teacher = teacher ,group = group , folder = folder    )

    if form.is_valid():
        nf = form.save(commit = False) 
        nf.author = teacher
        nf.teacher = teacher
        nf.save()
        form.save_m2m() 

        group_ids = request.POST.getlist("groups",[])
        folder_ids = request.POST.getlist("folders",[])
        parcours_ids = request.POST.getlist("parcours",[])

        nf.groups.set(group_ids)
        nf.folders.set(folder_ids)
        nf.parcours.set(parcours_ids)

        all_students = affectation_students_folders_groups(nf,group_ids,folder_ids)
        
        save_form = request.POST.get("save_form",None)

        if group_id and folder_id :
            return redirect('list_sub_parcours_group', group_id,folder_id)
        elif group_id :
            return redirect('list_parcours_group', group_id)
        elif save_form : return redirect('my_bibliotexs')
        else : return redirect('exercise_bibliotex_peuplate', nf.id)

    else:
        print(form.errors)

    context = {'form': form, 'bibliotex': bibliotex, 'group' : group , 'folder' : folder  }

    return render(request, 'bibliotex/form_bibliotex.html', context)




def create_bibliotex_from_parcours(request,idp=0):

    request.session["tdb"] = "Documents"  
    request.session["subtdb"] = "Bibliotex"

    teacher = request.user.teacher
    folder_id = request.session.get("folder_id",None)
    group_id = request.session.get("group_id",None)
    if group_id :group = Group.objects.get(id=group_id)
    else : group = None
    if folder_id : folder = Folder.objects.get(id=folder_id)
    else : folder = None

    parcours = Parcours.objects.get(id=idp)

    form = BibliotexForm(request.POST or None,request.FILES or None, teacher = teacher, group = group,  folder = folder,  initial = { 'folders'  : [folder] ,  'groups'  : [group] ,  'parcours'  : [parcours] } )
    
    if form.is_valid():
        nf = form.save(commit = False) 
        nf.author = teacher
        nf.teacher = teacher
        nf.save()
        form.save_m2m() 

        group_ids = request.POST.getlist("groups",[])
        folder_ids = request.POST.getlist("folders",[])
        nf.groups.set(group_ids)
        nf.folders.set(folder_ids)
        all_students = affectation_students_folders_groups(nf,group_ids,folder_ids)
 

        return redirect('exercise_bibliotex_peuplate', nf.id)

    else:
        print(form.errors)

    context = {'form': form, 'bibliotex': None, 'folder': folder, 'group': group, 'parcours': parcours  }

    return render(request, 'bibliotex/form_bibliotex.html', context)



def peuplate_bibliotex_parcours(request,idp):

    teacher = request.user.teacher
    parcours = Parcours.objects.get(id=idp)
    bibliotexs = Bibliotex.objects.filter(parcours=parcours)


    context = {'parcours': parcours, 'teacher': teacher , 'bibliotexs' : bibliotexs , 'type_of_document' : 5 }

    return render(request, 'bibliotex/form_peuplate_bibliotex_parcours.html', context)



def delete_bibliotex(request, id):
    group_id  = request.session.get('group_id',None)
    folder_id = request.session.get('folder_id',None)

    bibliotex = Bibliotex.objects.get(id=id)
    if request.user == bibliotex.author.user :
        bibliotex.delete()
    
    if folder_id :
        return redirect('list_sub_parcours_group' , group_id , folder_id)

    elif group_id :
        return redirect('list_parcours_group' , group_id )

    else :
        return redirect('my_bibliotexs')



def show_bibliotex(request, id):

    request.session["tdb"] = "Documents"  
    request.session["subtdb"] = "Bibliotex"
    
    try :
        teacher = request.user.teacher
    except :
        messages.error(request,"Vous n'êtes pas enseignant ou pas connecté.")
        return redirect('index')

    group_id = request.session.get('group_id',None)
    group = None
    if group_id :
        group = Group.objects.get(pk=group_id)


    folder_id = request.session.get('folder_id',None)
    folder = None
    if folder_id :
        folder = Folder.objects.get(pk=folder_id)


    bibliotex = Bibliotex.objects.get(id=id)
    relationtexs = Relationtex.objects.filter(bibliotex_id=id).order_by("ranking")

    context = { 'bibliotex': bibliotex, 'relationtexs': relationtexs, 'teacher' : teacher , 'group' : group, 'folder' : folder }

    return render(request, 'bibliotex/show_bibliotex.html', context )






def show_bibliotex_student(request, id):

    request.session["tdb"] = "Documents"  
    request.session["subtdb"] = "Bibliotex"

    try : student = request.user.student
    except : return redirect('index')

    bibliotex = Bibliotex.objects.get(id=id)
    relationtexs = Relationtex.objects.filter(bibliotex=bibliotex).order_by("ranking")

    context = { 'bibliotex': bibliotex, 'relationtexs': relationtexs,    }

    return render(request, 'bibliotex/show_bibliotex.html', context )










def duplicate_bibliotex(request):

    bibliotex_id = request.POST.get("this_document_id",None)
    folders      = request.POST.getlist("folders",[])
    parcourses   = request.POST.getlist("parcourses",[])
    groups       = request.POST.getlist("groups",[])

    data = {}
    if bibliotex_id :
        bibliotex = Bibliotex.objects.get(id=bibliotex_id)
        relationtexs = bibliotex.relationtexs.all()
        levels   = bibliotex.levels.all()
        subjects = bibliotex.subjects.all()
        bibliotex.pk=None
        bibliotex.save()

        bibliotex.folders.set(folders)    
        bibliotex.parcours.set(parcourses)
        bibliotex.groups.set(groups)
        bibliotex.levels.set(levels)
        bibliotex.subjects.set(subjects)


        group_str = ""
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
            group_str += group.name+". "

        bibliotex.students.set(students)

        for relationtex in relationtexs :
            skills     = relationtex.skills.all()
            knowledges = relationtex.knowledges.all()
            courses    = relationtex.courses.all()
            relationtex.pk = None
            relationtex.bibliotex = bibliotex
            relationtex.save()
            relationtex.students.set(students)
            relationtex.skills.set(skills)
            relationtex.knowledges.set(knowledges)
            relationtex.courses.set(courses)


        data["validation"] = "Duplication réussie. Retrouvez la biblioTex dans "+group_str
    else :
        data["validation"] = "Duplication abandonnée. La BiblioTex n'est pas reconnue." 

    return JsonResponse(data)










def bibliotex_actioner(request):

    teacher = request.user.teacher 
    idbs = request.POST.getlist("selected_bibliotexs")
    if  request.POST.get("action") == "deleter" :  
        for idb in idbs :
            bibliotex = Bibliotex.objects.get(id=idb)
            bibliotex.coteachers.clear()
            bibliotex.folders.clear()
            bibliotex.groups.clear()
            bibliotex.parcours.clear()
            bibliotex.exotexs.clear()
            bibliotex.students.clear()
            bibliotex.levels.clear()
            bibliotex.subjects.clear() 
            bibliotex.delete()

    elif  request.POST.get("action") == "archiver" :  
        for idb in idbs :
            bibliotex = Bibliotex.objects.get(id=idb) 
            bibliotex.is_archive = 1
            bibliotex.is_favorite = 0
            bibliotex.save()

    else : 
        for idb in idbs :
            bibliotex = Bibliotex.objects.get(id=idb) 
            bibliotex.is_archive = 0
            bibliotex.is_favorite = 0
            bibliotex.save()
     
    return redirect('my_bibliotexs')



def ajax_publish_bibliotex(request):

    data = {} 
    bibliotex_id = request.POST.get('bibliotex_id', None)
    statut = request.POST.get("statut")

    if statut == "True":
        data["statut"] = "False"
        data["publish"] = " n'est pas "
        data["class"] = "legend-btn-danger"
        data["noclass"] = "legend-btn-success"
        data["legendclass"] = "text-danger"
        data["nolegendclass"] = "text-success"
        data["color"] = "background-color:#dd4b39"
        data["removedisc"] = "disc"
        data["adddisc"] = "disc_persistant"
        data["noget"] = ""
        data["get"] = "noget"
        status = 0

    else:
        data["statut"] = "True"
        data["publish"] = "est"
        data["class"] = "legend-btn-success"
        data["noclass"] = "legend-btn-danger"
        data["legendclass"] = "text-success"        
        data["nolegendclass"] = "text-danger"
        data["color"] = "background-color:#00a65a"
        data["removedisc"] = "disc_persistant"
        data["adddisc"] = "disc"
        data["get"] = "get"
        data["noget"] = ""
        status = 1
 
    Bibliotex.objects.filter(pk = int(bibliotex_id)).update(is_publish = status)    
    return JsonResponse(data) 




def exercise_bibliotex_results(request, id):

    request.session["tdb"] = "Documents"  
    request.session["subtdb"] = "Bibliotex"

    bibliotex    = Bibliotex.objects.get(id=id)
    relationtexs = Relationtex.objects.filter(bibliotex_id=id)
    students     = bibliotex.students.exclude(user__username__contains="_e-test").order_by('user__last_name')
 
    context = { 'bibliotex': bibliotex, 'relationtexs': relationtexs, 'students' : students  }

    return render(request, 'bibliotex/bibliotex_results.html', context )




def exercise_bibliotex_peuplate(request, id):

    request.session["tdb"] = "Documents"  
    request.session["subtdb"] = "Bibliotex"

    teacher   = request.user.teacher
    bibliotex = Bibliotex.objects.get(id=id)
    skills    = Skill.objects.filter(subject__in=teacher.subjects.all())
    relationtexs = bibliotex.relationtexs.order_by("ranking")

    levels = Level.objects.exclude(pk=13).order_by("ranking")

    try : 
        level  = bibliotex.levels.first()
        subject  = bibliotex.subjects.first()

    except : 
        try : 
            level = teacher.levels.first()
            level = teacher.subjects.first()
        except : 
            level   = Level.objects.get(pk=6)
            subject = Subject.objects.get(pk=1)
            
    waitings = level.waitings.filter(theme__subject = subject ).order_by("theme__subject" , "theme")

    group_id  = request.session.get("group_id",None)
    folder_id = request.session.get("folder_id",None)
    group , folder = None, None
    if group_id  : group  = Group.objects.get(pk=group_id)
    if folder_id : folder = Folder.objects.get(pk=folder_id)
    context   = { 'bibliotex': bibliotex, 'relationtexs': relationtexs , 'teacher': teacher, 'skills' : skills, 'levels' : levels ,'waitings' : waitings , 'level' : level , 'subject' : subject ,'folder' : folder  ,'group' : group   ,'folder_id' : folder_id  ,'group_id' : group_id   }

    return render(request, 'bibliotex/form_peuplate_bibliotex.html', context )
 
 

def ajax_list_exotex(request):

    level_id   =  request.POST.get("level_id")
    subject_id =  request.POST.get("subject_id")
    teacher    = request.user.teacher
    level      = Level.objects.get(pk=level_id)
    waitings   = level.waitings.filter(theme__subject_id = subject_id).order_by("theme") 
    data = dict()
    data['html'] = render_to_string('bibliotex/ajax_list_exotexs.html', {'waitings' : waitings , 'teacher' : teacher })

    return JsonResponse(data)





def  exercise_bibliotex_individualise(request, id):
    
    request.session["tdb"] = "Documents"  
    request.session["subtdb"] = "Bibliotex"

    teacher   = request.user.teacher
    bibliotex = Bibliotex.objects.get(id=id)

    context   = { 'bibliotex': bibliotex,    'group':None }

    return render(request, 'bibliotex/form_individualise_bibliotex.html', context )
 





def real_time_bibliotex(request, id):
    pass
 




def link_to_relationship(request,idr):

    relationtex = Relationtex.objects.get(pk=idr)
    parcourses  = relationtex.bibliotex.parcours.all()

    if request.method == "POST" :
        relationships = request.POST.getlist("relationships")
        relationtex.exercises.set(relationships)
        return redirect( 'show_bibliotex' , relationtex.bibliotex.id ) 


    context   = { 'relationtex': relationtex, 'parcourses': parcourses }

    return render(request, 'bibliotex/form_link_to_relationship.html', context )


def ajax_chargethemes(request):
    level_id =  request.POST.get("id_level")
    id_subject =  request.POST.get("id_subject")
    teacher = request.user.teacher

    teacher_id = get_teacher_id_by_subject_id(id_subject)

    data = {}
    level =  Level.objects.get(pk = level_id)

    thms = level.themes.values_list('id', 'name').filter(subject_id=id_subject).order_by("name")
    data['themes'] = list(thms)
    exotexs = Exotex.objects.filter(Q(author__user__school = teacher.user.school)| Q(author__user_id=teacher_id),  level_id = level_id ).order_by('author').distinct()

    data['html'] = render_to_string('qcm/ajax_list_parcours.html', {'exotexs' : exotexs , })

    return JsonResponse(data)



def ajax_level_exotex(request):

    data = {} 
 
    theme_ids    = request.POST.getlist('theme_id', None)
    level_id     = request.POST.get("level_id",None)
    subject_id   = request.POST.get("subject_id",None)
    skill_id     = request.POST.get("skill_id",None)
    keyword      = request.POST.get("keyword",None)
    bibliotex_id = request.POST.get("bibliotex_id",None)
    is_annale    = request.POST.get("is_annale",None)

    teacher = request.user.teacher 

    if int(level_id) > 0 and subject_id :
        level = Level.objects.get(pk=int(level_id))
        subject = Subject.objects.get(pk=int(subject_id))
        thms  = level.themes.values_list('id', 'name').filter(subject_id=subject_id).order_by("name")
        data['themes'] = list(thms) 


    if bibliotex_id :

        bibliotex = Bibliotex.objects.get(pk=bibliotex_id)
        teacher = request.user.teacher 
 
        data['knowledges']       =  None
        data['knowledges_level'] =  None

        base = Exotex.objects.filter(theme__subject_id = subject_id).exclude(bibliotexs=bibliotex)
        if is_annale == 'yes' : 
            base = base.filter(is_annals=1)


        if level_id  : 
            base = base.filter( level_id = level_id).order_by("theme","knowledge__waiting","knowledge","ranking")
        
        if skill_id  : 
            skill = Skill.objects.get(pk=skill_id)
            base = base.filter( skills = skill ).order_by("theme","knowledge__waiting","knowledge","ranking")


        if theme_ids : 
            knowledges = set()
            for theme_id in theme_ids :
                try :
                    theme = Theme.objects.get(pk=int(theme_id))
                    knowledges.update( theme.knowledges.values_list('id', 'name').filter(level_id = level_id ) )
                except :
                    knowledges = []
            data['knowledges']  =  list(knowledges)

            if theme_ids[0] != "" : 
                base = base.filter( theme_id__in= theme_ids ).order_by("theme","knowledge__waiting","knowledge","ranking")

        if keyword  : 
            base = base.filter(Q(title__icontains=keyword)| Q(content_html__icontains=keyword)).order_by("theme","knowledge__waiting","knowledge","ranking")

        exotexs = base
        data['html'] = render_to_string('bibliotex/ajax_list_exercises.html', { 'bibliotex_id': bibliotex_id , 'exotexs': exotexs , "teacher" : teacher  })

    else :
        knowledges = Knowledge.objects.values_list("id","name").filter(theme_id__in=theme_ids, level_id = level_id  ) 
        knowledges_level = Knowledge.objects.values_list("id","name").filter(theme__subject__id = subject_id,  level_id = level_id  ) 
        data['knowledges']       =  list( knowledges )
        data['knowledges_level'] =  list( knowledges_level )

    return JsonResponse(data)

 

def ajax_knowledges_exotex(request):

    data = {} 
 
    knowledge_ids = request.POST.getlist('knowledge_ids', None)
    skill_id      = request.POST.get("skill_id",None)
    keyword       = request.POST.get("keyword",None)
    bibliotex_id  = request.POST.get("bibliotex_id",None)
    teacher       = request.user.teacher

    exotexs_set = set()
    if knowledge_ids and knowledge_ids[0] != "" and skill_id  : 
        skill = Skill.objects.get(pk=skill_id)
        exotexs_set.update(Exotex.objects.filter( knowledge_id__in = knowledge_ids))
        for knowledge_id in knowledge_ids :
            knowledge = Knowledge.objects.get(pk=knowledge_id)
            exotexs_set.update( knowledge.other_knowledge_exotexs.order_by("name") )

    if skill_id :
        skill = Skill.objects.get(pk=skill_id)
        exotexs_set.update( skill.skills_exotexs.order_by("name") )

    if keyword :
        k_tab = keyword.split(" ")
        for kw in k_tab :
            exotexs_set.update( Exotex.objects.filter( Q(title__contains=kw)|Q(content__contains=kw) ) ) 



    data['html'] = render_to_string('bibliotex/ajax_list_exercises.html', { 'bibliotex_id': bibliotex_id , 'exotexs': exotexs_set , "teacher" : teacher  })
    

    return JsonResponse(data)







def ajax_charge_folders(request):  

    teacher = request.user.teacher
    data = {} 
    group_ids = request.POST.getlist('group_ids', None)

    if len(group_ids) :
        fldrs = set()
        prcs  = set()
        for group_id in group_ids :
            group = Group.objects.get(pk=group_id)
            fldrs.update(group.group_folders.values_list("id","title").filter(subject=group.subject, level=group.level, is_trash=0))
            prcs.update(group.group_parcours.values_list("id","title").filter(subject=group.subject, level=group.level,is_trash=0,folders=None))

            print(fldrs)
        data['folders'] =  list( fldrs )
        data['parcours'] =  list( prcs )
    else :
        data['folders'] =  []
        data['parcours'] =  []
    return JsonResponse(data)



def ajax_charge_parcours(request):

    teacher = request.user.teacher
    data = {} 
    folder_ids = request.POST.getlist('folder_ids', None)

    if len(folder_ids) :
        parcourses = set()
        for folder_id in folder_ids :
            folder = Folder.objects.get(pk=folder_id)
            parcourses.update(folder.parcours.values_list("id","title").filter(subject=folder.subject, level=folder.level,is_trash=0))

        data['parcours'] =  list( parcourses )
    else :
        data['parcours'] =  []

    return JsonResponse(data)



def ajax_set_exotex_in_bibliotex(request):

    data = {} 
    exotex_id    = request.POST.get('exotex_id', None)
    bibliotex_id = request.POST.get('bibliotex_id', None)

    bibliotex   = Bibliotex.objects.get(pk = bibliotex_id) 
    exotex      = Exotex.objects.get(pk = exotex_id)


    statut = request.POST.get("statut")

    data = {}    
    stds     = bibliotex.students.all()

    if statut=="true" or statut == "True":
        r = Relationtex.objects.get(bibliotex_id=bibliotex_id , exotex_id = exotex_id )  
        students = list(stds)
        r.students.remove(*students)
        r.delete()
        data["statut"]  = "False"
        data["class"]   = "btn btn-danger"
        data["noclass"] = "btn btn-success"
    else:
        skills      = exotex.skills.all()
        knowledges  = exotex.knowledges.all()
        exercises   = exotex.exercises.all()
        try :        
            relationtex = Relationtex.objects.create(   bibliotex_id=bibliotex_id, exotex_id = exotex_id, ranking = 100,  
                                                        teacher = request.user.teacher, calculator = exotex.calculator,  duration =exotex.duration , 
                                                        is_python = exotex.is_python,is_scratch =exotex.is_scratch,is_tableur =exotex.is_tableur,is_print = 0,
                                                        is_publish = 1)
            relationtex.skills.set(skills)
            relationtex.knowledges.set(knowledges)
            relationtex.students.set(stds)
            relationtex.exercises.set(exercises)
            data["statut"]  = "True"
            data["class"]   = "btn btn-success"
            data["noclass"] = "btn btn-danger"
        except :
            data["statut"]  = "False"
            data["class"]   = "btn btn-danger"
            data["noclass"] = "btn btn-success"

    data["nb"] = bibliotex.exotexs.count()
    context        = { 'exotex': exotex , 'bibliotex':  bibliotex  }
    data["html"]   = render_to_string('bibliotex/exotex_tag.html', context)

    return JsonResponse(data)



def unset_exotex_in_bibliotex(request,idr):
    bibliotex_id = Relationtex.objects.get(pk = idr).bibliotex.id
    Relationtex.objects.filter(pk = idr).delete()
    return redirect("show_bibliotex" , bibliotex_id)


@csrf_exempt # PublieDépublie un exercice depuis organize_parcours
def ajax_is_favorite(request):  

    target_id = int(request.POST.get("target_id",None))
    statut = int(request.POST.get("statut"))
    status = request.POST.get("status") 
    data = {}
 
    if statut :
        Bibliotex.objects.filter(pk = target_id).update(is_favorite = 0)
        data["statut"] = "<i class='fa fa-star text-default' ></i>"
        data["fav"] = 0
    else :
        Bibliotex.objects.filter(pk = target_id).update(is_favorite = 1)  
        data["statut"] = "<i class='fa fa-star   text-is_favorite' ></i>"
        data["fav"] = 1     

    return JsonResponse(data) 



def ajax_affectation_to_group(request):
    group_id    = request.POST.get('group_id') 
    status      = request.POST.get('status')
    target_id   = request.POST.get('target_id')
    checked     = request.POST.get('checked')

    group       = Group.objects.get(pk=group_id)
    folders     = group.group_folders.all()
    parcourses  = group.group_parcours.all()
    students    = group.students.all() 

    data        = {}
    html        = ""
    change_link = "no"
 
    bibliotex   = Bibliotex.objects.get(pk=target_id)

    if checked == "false" :
        bibliotex.groups.remove(group)
        for folder in folders :
            bibliotex.folders.remove(folder)
        for parcours in parcourses :
            bibliotex.parcours.remove(parcours)
        for student in students :
            bibliotex.students.remove(student) 
        change_link = "change"
    else :
        bibliotex.groups.add(group)
        bibliotex.students.set(students)  

    for g in bibliotex.groups.all():
        html += "<small>"+g.name +" (<small>"+ str(g.just_students_count())+"</small>)</small> "

    data['html']        = html
    data['change_link'] = change_link
    return JsonResponse(data)



@csrf_exempt   # PublieDépublie un parcours depuis form_group et show_group
def ajax_sharer_parcours(request):  

    parcours_id = request.POST.get("parcours_id")
    statut = request.POST.get("statut")
    is_folder = request.POST.get("is_folder")
 
    data = {}
    if statut=="true" or statut == "True":
        statut = 0
        data["statut"]  = "false"
        data["share"]   = "Privé"
        data["style"]   = "#dd4b39"
        data["class"]   = "legend-btn-danger"
        data["noclass"] = "legend-btn-success"
        data["label"]   = "Privé"
    else:
        statut = 1
        data["statut"]  = "true"
        data["share"]   = "Mutualisé"
        data["style"]   = "#00a65a"
        data["class"]   = "legend-btn-success"
        data["noclass"] = "legend-btn-danger"
        data["label"]   = "Mutualisé"

    Bibliotex.objects.filter(pk = int(parcours_id)).update(is_share = statut)
 
    return JsonResponse(data) 



@csrf_exempt   # PublieDépublie un parcours depuis form_group et show_group
def ajax_publish_list_bibliotex(request):  

    bibliotex_id = request.POST.get("bibliotex_id")
    statut = request.POST.get("statut")
    data = {}
    if statut=="true" or statut == "True":
        statut = 0
        data["statut"] = "false"
        data["style"] = "#dd4b39"
        data["class"] = "legend-btn-danger"
        data["noclass"] = "legend-btn-success"
        data["label"] = "Non publié"
    else:
        statut = 1
        data["statut"] = "true"
        data["style"] = "#00a65a"
        data["class"] = "legend-btn-success"
        data["noclass"] = "legend-btn-danger"
        data["label"] = "Publié"
 
    Bibliotex.objects.filter(pk = int(bibliotex_id)).update(is_publish = statut)

    return JsonResponse(data) 



############################################################################################################
############################################################################################################
#################  Résultats
############################################################################################################
############################################################################################################

def ajax_sort_exotexs_in_bibliotex(request):

    data = {}
    bibliotex_id = request.POST.get('bibliotex_id', None)
    relationtexs = request.POST.getlist('relationtexs', None)
    i=0
    for relationtex in relationtexs :
        Relationtex.objects.filter(pk = relationtex ).update(ranking=i)
        i+=1
    return JsonResponse(data)


@csrf_exempt
def ajax_bibliotex_sorter(request):

    data = {}
    valeurs = request.POST.get('valeurs', None)
    i=0
    for val in valeurs.split("-") :
        try :Bibliotex.objects.filter(pk = val ).update(ranking=i)
        except :pass
        i+=1
    return JsonResponse(data)




@csrf_exempt
def ajax_class_exotex(request):

    data = {}
    exotex_id = request.POST.get('exotex_id', None)
    value = request.POST.get('value', None)

    print(exotex_id , value)
    Exotex.objects.filter(pk = exotex_id ).update(ranking=value)

    return JsonResponse(data)








@csrf_exempt
def ajax_display_exotex(request):

    data = {}
    relationtex_id = request.POST.get('relationtex_id', None)
    r = Relationtex.objects.get(pk = relationtex_id )
    if r.is_publish : r.is_publish = 0
    else :  r.is_publish = 1
    r.save()
    data["display"] = "true"
    return JsonResponse(data)


@csrf_exempt
def ajax_display_correction_exotex(request):

    data = {}
    relationtex_id = request.POST.get('relationtex_id', None)
    r = Relationtex.objects.get(pk = relationtex_id )
    if r.is_publish_cor : 
        r.is_publish_cor = 0
        data["addClass"]    = "fa-eye-slash text-danger"
        data["removeClass"] = "fa-eye text-success"
        data["title"]       = "Correction publiée"
    else :  
        r.is_publish_cor = 1
        data["addClass"]    = "fa-eye text-success"
        data["removeClass"] = "fa-eye-slash text-danger"
        data["title"]       = "Correction dépubliée"
    r.save()
    
    return JsonResponse(data)


def ajax_results_exotex(request):

    data = {}
    relationtex_id = request.POST.get('relationtex_id', None)
    relationtex = Relationtex.objects.get(pk=relationtex_id)
    students = relationtex.bibliotex.students.exclude(user__username__contains="_e-test").order_by("user__last_name")
    std_r = relationtex.students.order_by("user__last_name")
    if std_r.count() :
        students = [ s for s in std_r if s in students]



    context = { 'students': students , 'bibliotex': relationtex.bibliotex , "exotex" : relationtex.exotex  }
    data["html"] = render_to_string('bibliotex/ajax_results_exercise.html', context )
    data["title"] = "Résultats de l'exercice "+relationtex.exotex.title

    return JsonResponse(data)


############################################################################################################
############################################################################################################
#################  Individualisation
############################################################################################################
############################################################################################################


def ajax_individualise(request):
    """ A partir d'une bibliotex """    
    data = {}
    relationtex_id = request.POST.get('relationtex_id', None)
    student_id     = request.POST.get('student_id', None)
    statut         = request.POST.get('statut', None)
    is_checked     = request.POST.get('is_checked', None)

    relationtex    = Relationtex.objects.get(pk=relationtex_id)

    if is_checked == "true" : # Pour tous lex exercices à partir du premier
        for relationtex in relationtex.relationtexs.filter(is_publish=1 ) : 
            if student_id ==  "0"  :
                if statut=="true" or statut == "True" :
                    somme = 0
                    try :
                        for s in relationtex.bibliotex.parcours.students.all() :
                            relationtex.students.remove(s)
                            Blacklistex.objects.get_or_create( student = s ,relationtex = relationtex   )
                    except :
                        pass
   
                    data["statut"] = "False"
                    data["class"] = "btn btn-default"
                    data["noclass"] = "btn btn-success"
                    if somme == 0 :
                        data["alert"] = True
                    else :
                        data["alert"] = False

                else : 
                    relationtex.students.set(relationtex.bibliotex.parcours.students.all())
                    for s in relationtex.parcours.students.all():
                        if Blacklistex.objects.filter(relationtex=relationtex, student = s ).count() > 0 :
                            Blacklistex.objects.get(relationtex=relationtex, student = s ).delete()   
                    data["statut"] = "True"
                    data["class"] = "btn btn-success"
                    data["noclass"] = "btn btn-default"
                    data["alert"] = False

            else :
                student = Student.objects.get(pk = student_id)  

                if statut=="true" or statut == "True":


                    relationtex.students.remove(student)
                    Blacklistex.objects.get_or_create(relationtex=relationtex, student = student  )
                    data["statut"] = "False"
                    data["class"] = "btn btn-default"
                    data["noclass"] = "btn btn-success"
                    data["alert"] = False

 

                else:
                    relationtex.students.add(student)
                    if Blacklistex.objects.filter(relationtex=relationtex, student = student  ).count()  > 0 :
                        Blacklistex.objects.get(relationtex=relationtex, student = student ).delete()
                    data["statut"] = "True"
                    data["class"] = "btn btn-success"
                    data["noclass"] = "btn btn-default"
                    data["alert"] = False
    else :
        if student_id ==  "0"  :
            if statut=="true" or statut == "True" :
                somme = 0
                try :
                    for s in relationtex.students.all() :
                        Blacklistex.objects.get_or_create(student = s , relationtex = relationtex   )
                except :
                    pass

                data["statut"] = "False"
                data["class"] = "btn btn-default"
                data["noclass"] = "btn btn-success"
                if somme == 0 :
                    data["alert"] = True
                else :
                    data["alert"] = False

            else : 
                relationtex.students.set(relationtex.bibliotex.students.all())
                for s in relationtex.bibliotex.students.all():
                    if Blacklistex.objects.filter(relationtex=relationtex, student = s ).count() > 0 :
                        Blacklistex.objects.get(relationtex=relationtex, student = s ).delete()   
                data["statut"] = "True"
                data["class"] = "btn btn-success"
                data["noclass"] = "btn btn-default"
                data["alert"] = False

        else :
            student = Student.objects.get(pk = student_id)  

            if statut=="true" or statut == "True":

                relationtex.students.remove(student)
                Blacklistex.objects.get_or_create(relationtex=relationtex, student = student  )
                data["statut"] = "False"
                data["class"] = "btn btn-default"
                data["noclass"] = "btn btn-success"
                data["alert"] = False
 
            else:
                relationtex.students.add(student)
                if Blacklistex.objects.filter(relationtex=relationtex, student = student ).count()  > 0 :
                    Blacklistex.objects.get(relationtex=relationtex, student = student  ).delete()
                data["statut"] = "True"
                data["class"] = "btn btn-success"
                data["noclass"] = "btn btn-default"
                data["alert"] = False

    return JsonResponse(data)


        

def ajax_individualise_exotex(request):
    """ A partir d'un exotex """
    data = {}
    relationtex_id = request.POST.get('relationtex_id', None)
    relationtex = Relationtex.objects.get(pk=relationtex_id)
    std_r = relationtex.bibliotex.students.exclude(user__username__contains="_e-test").order_by("user__last_name")
    group_id = request.session.get("group_id",None)
    if group_id : 
        group = Group.objects.get(pk=group_id)
        std_g = group.students.order_by("user__last_name")
    if std_g.count() :
        students = [student for student in std_g if student   in std_r] 
    else :
        students = std_r

    context = { 'students': students ,  "relationtex" : relationtex }
    data["html"] = render_to_string('bibliotex/ajax_individualise_exercise.html',context)
    data["title"] = "Individualiser l'exercice "+relationtex.exotex.title

    return JsonResponse(data)


def change_publications_in_all_exotex(request,idf,idb):

    bibliotex = Bibliotex.objects.get(pk=idb)
    relationtexs = bibliotex.relationtexs.order_by("ranking")
 
    try :
        teacher = request.user.teacher
    except :
        messages.error(request,"Vous n'êtes pas enseignant ou pas connecté.")
        return redirect('index')


    if request.method == "POST" :
        global_publication = request.POST.get('global', 0)

        for r in relationtexs :
            Relationtex.objects.filter(pk=r.id).update(is_publish = global_publication)

        bibliotex_publication = request.POST.get('bibliotex', 0)
        # si tous les exercices sont dépubliés, on dépublie le parcours et si vous publiez tous 
        Bibliotex.objects.filter(pk=idb).update(is_publish = bibliotex_publication)

        return redirect('show_bibliotex' ,  idb )



    context = { 'bibliotex': bibliotex, 'relationtexs': relationtexs ,  'teacher': teacher   }

    return render(request, 'bibliotex/change_publications.html', context)


############################################################################################################
############################################################################################################
#################   IMPRESSION
############################################################################################################
############################################################################################################

def ajax_print_exotex(request):

    data = {}
    relationtex_id = request.POST.get('relationtex_id', None)
    relationtex = Relationtex.objects.get(pk=relationtex_id)
    context = { 'bibliotex': relationtex.bibliotex , "exotex" : relationtex.exotex  }
    data["html"] = render_to_string('bibliotex/ajax_print_exercise.html', context)
    data["title"] = "Imprimer l'exercice "+relationtex.exotex.title

    return JsonResponse(data)

def ajax_print_bibliotex(request):

    data = {}
    relationtex_id = request.POST.get('relationtex_id', None)
    bibliotex      = Bibliotex.objects.get(pk=relationtex_id)
    students       =  bibliotex.students.exclude(user__username__contains="_e-test").order_by("user__last_name")
    context        = { 'students': students , 'bibliotex':  bibliotex , 'relationtexs':  bibliotex.relationtexs.all()  }
    data["html"]   = render_to_string('bibliotex/ajax_print_bibliotex.html', context)
    data["title"]  = "Imprimer la Bibliotex "+bibliotex.title

    return JsonResponse(data)





 

def print_bibliotex(request ):

    return printer(request,0, True,"pdf" , "E")


def print_exotex(request):

    return printer(request,0, False,"pdf" , "E")



def print_bibliotex_by_student(request,id):

    data = {}
    bibliotex = Bibliotex.objects.get(pk=id)
    return printer_bibliotex_by_student(request,bibliotex) 

 
