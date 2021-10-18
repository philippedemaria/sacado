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
from django.http import JsonResponse 
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages

from qcm.views import get_teacher_id_by_subject_id
from group.models import Group , Sharing_group
from socle.models import  Knowledge , Level , Skill , Waiting , Subject
from bibliotex.models import  Bibliotex , Exotex , Relationtex , Blacklistex
from bibliotex.forms import  BibliotexForm , ExotexForm
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
    return render(request, 'bibliotex/list_exotexs.html', {'exos': exos,  })




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
        messages.success(request, "L'exercice a été créé avec succès !")
        return redirect('admin_exotexs', knowledge.level.id)
    else:
        print(form.errors)

    context = {'form': form, 'knowledge': knowledge , 'exotex': None }

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
        messages.success(request, "L'exercice a été créé avec succès !")
        return redirect('admin_exotexs', nf.knowledge.level.id)
    else:
        print(form.errors)

    context = {'form': form, 'exotex': None  }

    return render(request, 'bibliotex/form_exotex.html', context)


 
def update_exotex(request, id):

    exotex = Exotex.objects.get(id=id)
    teacher = request.user.teacher
    form = ExotexForm(request.POST or None, request.FILES or None, instance=exotex , teacher = teacher , knowledge = None )
    if request.method == "POST" :
        if form.is_valid():
            nf = form.save(commit = False) 
            nf.author = teacher
            nf.teacher = teacher
            nf.save()
            form.save_m2m()   
            messages.success(request, "L'exercice a été créé avec succès !")
            return redirect('admin_exotexs', exotex.knowledge.level.id)
        else:
            print(form.errors)

    context = {'form': form,  'exotex': exotex,   }

    return render(request, 'bibliotex/form_exotex.html', context )


 
def delete_exotex(request, id):
    exotex = Exotex.objects.get(id=id)
    level_id = exotex.knowledge.level.id
    if request.user == exotex.author.user :
        exotex.delete()

    return redirect('admin_exotexs', level_id)


 

def ajax_action_exotex(request, id):
    pass
 
 






#########################################################################################################################################
#########################################################################################################################################
######## Bibliotex
#########################################################################################################################################
#########################################################################################################################################
def bibliotexs(request):
 
    bibliotexs = Bibliotex.objects.all()
    return render(request, 'bibliotex/list_bibliotexs.html', {'bibliotexs': bibliotexs,  })


 
def my_bibliotexs(request):

    request.session["folder_id"] = None
    request.session["group_id"] = None

    teacher = request.user.teacher
    dataset = list()

    sbj = set()



    for s in teacher.subjects.all() :
        data = {}   
        lvl = set()
        bibliotexs = Bibliotex.objects.filter( Q(author=teacher)|Q(teacher=teacher)|Q(coteachers=teacher)  , subjects = s  ).order_by("subjects","levels")
 
        for bibliotex in bibliotexs :
            lvl.update( bibliotex.levels.order_by("ranking") )
 
        data['subject'] = s
        data['levels']  = lvl
 
        dataset.append(data)
        data = {}  


 
    return render(request, 'bibliotex/list_bibliotexs.html', {'bibliotexs': bibliotexs, 'dataset': dataset ,  })


 

 
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

 

@user_passes_test(user_is_creator)
def create_bibliotex(request,idf=0):


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
    
    form = BibliotexForm(request.POST or None,request.FILES or None, teacher = teacher, folder = folder, initial = { 'folders'  : [folder] ,  'groups'  : [group] } )

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

    bibliotex = Bibliotex.objects.get(id=id)
    teacher = request.user.teacher
    form = BibliotexForm(request.POST or None, request.FILES or None, instance=bibliotex, teacher = teacher, folder = None)
    if request.method == "POST" :
        if form.is_valid():
            form.save()
            messages.success(request, "L'exercice a été créé avec succès !")
            return redirect('bibliotexs')
        else:
            print(form.errors)

    context = {'form': form,  'bibliotex': bibliotex,   }

    return render(request, 'bibliotex/form_bibliotex.html', context )


def delete_bibliotex(request, id):
    bibliotex = Bibliotex.objects.get(id=id)
    if request.user == bibliotex.author.user :
        bibliotex.delete()

    return redirect('bibliotexs')



def show_bibliotex(request, id):

    bibliotex = Bibliotex.objects.get(id=id)
    relationtexs = Relationtex.objects.filter(bibliotex_id=id).order_by("ranking")
 
    context = { 'bibliotex': bibliotex, 'relationtexs': relationtexs,   }

    return render(request, 'bibliotex/show_bibliotex.html', context )




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

    bibliotex    = Bibliotex.objects.get(id=id)
    relationtexs = Relationtex.objects.filter(bibliotex_id=id)
    students     = bibliotex.students.exclude(user__username__contains="_e-test").order_by('user__last_name')
 
    context = { 'bibliotex': bibliotex, 'relationtexs': relationtexs, 'students' : students  }

    return render(request, 'bibliotex/bibliotex_results.html', context )










def exercise_bibliotex_peuplate(request, id):

    teacher   = request.user.teacher
    bibliotex = Bibliotex.objects.get(id=id)
    skills    = Skill.objects.filter(subject__in=teacher.subjects.all())
    relationtexs = bibliotex.relationtexs.order_by("ranking")

 
    context   = { 'bibliotex': bibliotex, 'relationtexs': relationtexs , 'teacher': teacher, 'skills' : skills  }

    return render(request, 'bibliotex/form_peuplate_bibliotex.html', context )
 
 

def  exercise_bibliotex_individualise(request, id):

    teacher   = request.user.teacher
    bibliotex = Bibliotex.objects.get(id=id)

    context   = { 'bibliotex': bibliotex,    'group':None }

    return render(request, 'bibliotex/form_individualise_bibliotex.html', context )
 


def real_time_bibliotex(request, id):
    pass
 


def  ajax_chargethemes(request):
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


    teacher = Teacher.objects.get(user= request.user)
    data = {} 
 
    theme_ids    = request.POST.getlist('theme_id', None)
    level_id     = request.POST.get("level_id",None)
    subject_id   = request.POST.get("subject_id",None)
    skill_id     = request.POST.get("skill_id",None)
    keyword      = request.POST.get("keyword",None)
    bibliotex_id = request.POST.get("bibliotex_id",None)

    bibliotex = Bibliotex.objects.get(pk=bibliotex_id)
    teacher = request.user.teacher 
    data = {}



    base = Exotex.objects.filter(Q(author__user__school = teacher.user.school)| Q(author__user_id=teacher.user.id), is_share = 1).exclude(bibliotexs=bibliotex) 

    if theme_ids :  

        if level_id and theme_ids[0] != "" and skill_id  : 
            skill = Skill.objects.get(pk=skill_id)
            exotexs = base.filter( level_id = level_id , theme_id__in= theme_ids, skills = skill, ).order_by("theme","knowledge__waiting","knowledge","ranking")

     
        elif level_id and theme_ids[0] != ""  : 
            exotexs = base.filter( level_id = level_id , theme_id__in= theme_ids ).order_by("theme","knowledge__waiting","knowledge","ranking")


        elif theme_ids[0] != ""    : 
            exotexs = base.filter(  theme_id__in= theme_ids).order_by("theme","knowledge__waiting","knowledge","ranking")

     
        elif keyword and theme_ids[0] != ""   : 
            exotexs =  base.filter(theme_id__in= theme_ids,  title__contains= keyword ).order_by("theme","knowledge__waiting","knowledge","ranking")
        else :
            exotexs = base
    else :

        if level_id and  skill_id  : 
            skill = Skill.objects.get(pk=skill_id)
            exotexs = base.filter(level_id = level_id ,  skills = skill, ).order_by("theme","knowledge__waiting","knowledge","ranking")

        elif level_id and keyword  : 
            exotexs = base.filter( level_id = level_id ,  title__contains= keyword ).order_by("theme","knowledge__waiting","knowledge","ranking")


        elif keyword and skill_id  : 
            skill = Skill.objects.get(pk=skill_id)
            exotexs =  base.filter(skills = skill, title__contains= keyword ).order_by("theme","knowledge__waiting","knowledge","ranking")

 

        else :
            exotexs = base

    data['html'] = render_to_string('bibliotex/ajax_list_exercises.html', { 'bibliotex_id': bibliotex_id , 'exotexs': exotexs , "teacher" : teacher  })

    return JsonResponse(data)




def ajax_charge_groups(request):

    teacher = Teacher.objects.get(user= request.user)
    data = {} 
    group_ids = request.POST.getlist('group_ids', None)

    if len(group_ids) :
        grps = set()
        for group_id in group_ids :
            group = Group.objects.get(pk=group_id)
            grps.update(group.group_folders.values_list("id","title").filter(is_trash=0))

        data['folders'] =  list( grps )
    else :
        data['folders'] =  []

    return JsonResponse(data)



def ajax_set_exotex_in_bibliotex(request):

    data = {} 
    exotex_id    = request.POST.get('exotex_id', None)
    bibliotex_id = request.POST.get('bibliotex_id', None)

    bibliotex   = Bibliotex.objects.get(pk = bibliotex_id) 
    exotex      = Exotex.objects.get(pk = exotex_id)
    skills      = exotex.skills.all()
    knowledges  = exotex.knowledges.all()

    statut = request.POST.get("statut") 
    data = {}    
    stds     = bibliotex.students.all()

    if statut=="true" or statut == "True":

        r = Relationtex.objects.get(bibliotex_id=bibliotex_id , exotex_id = exotex_id )  
        students = list(stds)
        r.students.remove(*students)

        data["statut"] = "False"
        data["class"] = "btn btn-danger"
        data["noclass"] = "btn btn-success"


    else:

        relationtex = Relationtex.objects.create(   bibliotex_id=bibliotex_id, exotex_id = exotex_id, ranking = 100,  
                                                    teacher = request.user.teacher, calculator = exotex.calculator,  duration =exotex.duration , 
                                                    is_python = exotex.is_python,is_scratch =exotex.is_scratch,is_print = 0,
                                                    is_publish = 1,  correction=exotex.correction ,is_publish_cor = 0 )
        relationtex.skills.set(skills)
        relationtex.knowledges.set(knowledges)
        relationtex.students.set(stds)


        data["statut"]  = "True"
        data["class"]   = "btn btn-success"
        data["noclass"] = "btn btn-danger"


    data["nb"] = bibliotex.exotexs.count()


    return JsonResponse(data)



def unset_exotex_in_bibliotex(request,idr):
    bibliotex_id = Relationtex.objects.get(pk = idr).bibliotex.id
    Relationtex.objects.filter(pk = idr).delete()
    return redirect("show_bibliotex" , bibliotex_id)
############################################################################################################
############################################################################################################
#################  Résultats
############################################################################################################
############################################################################################################

def ajax_results_exotex(request):

    data = {}
    relationtex_id = request.POST.get('relationtex_id', None)
    relationtex = Relationtex.objects.get(pk=relationtex_id)
    students = relationtex.bibliotex.students.exclude(user__username__contains="_e-test").order_by("user__last_name")
    std_r = relationtex.students.all()
    if std_r.count() :
        students = std_b.intersection(std_r).order_by("user__last_name")

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
                        for s in parcours.students.all() :
                            exercise = Exercise.objects.get(pk = exercise_id )
                            if Studentanswer.objects.filter(student = s , exercise = exercise, parcours = relationship.parcours).count() == 0 :
                                relationship.students.remove(s)
                                somme +=1
                            Blacklist.objects.get_or_create(customexercise=None, student = s ,relationship = relationship   )
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
                    relationship.students.set(parcours.students.all())
                    for s in parcours.students.all():
                        if Blacklist.objects.filter(relationship=relationship, student = s ).count() > 0 :
                            Blacklist.objects.get(relationship=relationship, student = s ).delete()   
                    data["statut"] = "True"
                    data["class"] = "btn btn-success"
                    data["noclass"] = "btn btn-default"
                    data["alert"] = False

            else :
                student = Student.objects.get(pk = student_id)  

                if statut=="true" or statut == "True":

                    if Studentanswer.objects.filter(student = student , relationtex = relationtex ).count() == 0 :
                        relationship.students.remove(student)
                        Blacklist.objects.get_or_create(relationtex=relationtex, student = student  )
                        data["statut"] = "False"
                        data["class"] = "btn btn-default"
                        data["noclass"] = "btn btn-success"
                        data["alert"] = False

                    else :
                        data["statut"] = "True"
                        data["class"] = "btn btn-success"
                        data["noclass"] = "btn btn-default"
                        data["alert"] = True

                else:
                    relationship.students.add(student)
                    if Blacklist.objects.filter(relationtex=relationtex, student = student  ).count()  > 0 :
                        Blacklist.objects.get(relationtex=relationtex, student = student ).delete()
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
    students = relationtex.bibliotex.students.exclude(user__username__contains="_e-test").order_by("user__last_name")
    std_r = relationtex.students.all()
    if std_r.count() :
        students = std_b.intersection(std_r).order_by("user__last_name")
    context = { 'students': students ,  "relationtex" : relationtex }
    data["html"] = render_to_string('bibliotex/ajax_individualise_exercise.html',context)
    data["title"] = "Individualiser l'exercice "+relationtex.exotex.title

    return JsonResponse(data)
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
    bibliotex = Bibliotex.objects.get(pk=relationtex_id)
    students =  bibliotex.students.exclude(user__username__contains="_e-test").order_by("user__last_name")
    context = { 'students': students , 'bibliotex':  bibliotex   }
    data["html"] = render_to_string('bibliotex/ajax_print_bibliotex.html', context)
    data["title"] = "Imprimer la Bibliotex "+bibliotex.title

    return JsonResponse(data)



#def print_exotex(request):

    relationtex_id = request.POST.get("print_exotex_id",None)  
    skills         = request.POST.get("skills",None)  
    knowledges     = request.POST.get("knowledges",None)  
    relationtex    = Relationtex.objects.get(pk = relationtex_id) 
    elements    = []     

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+str(relationtex.exotex.title).replace(" ","_")+'.pdf"'

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

    style_cell = TableStyle(
            [
                ('SPAN', (0, 1), (1, 1)),
                ('TEXTCOLOR', (0, 1), (-1, -1),  colors.Color(0,0.7,0.7))
            ]
        )


    title = ParagraphStyle('title',  fontSize=16 )                   

    normal = ParagraphStyle(name='Normal',fontSize=12,)    
    red = ParagraphStyle(name='Normal',fontSize=12,  textColor=colors.HexColor("#cb2131"),) 
    yellow = ParagraphStyle(name='Normal',fontSize=12,  textColor=colors.HexColor("#ffb400"),)
    green = ParagraphStyle(name='Normal',fontSize=12,  textColor=colors.HexColor("#1bc074"),)
    blue = ParagraphStyle(name='Normal',fontSize=14,  textColor=colors.HexColor("#005e74"),)
    small = ParagraphStyle(name='Normal',fontSize=10,)    
    violet = ParagraphStyle(name='Normal',fontSize=14,  textColor=colors.HexColor("#5d4391"),)
    


    skills_display = ""
    if skills :   
        if relationtex.skills.count():
            sks =  relationtex.skills.all()
        else :
            sks =  relationtex.exotex.skills.all()
        for s in sks :
            skills_display +=  s.name+". "

    exo = Paragraph("Exercice. " +  relationtex.exotex.title + ".    " +skills_display, violet )
    elements.append(exo)



    if knowledges :  
        k_display = Paragraph( relationtex.exotex.knowledge.name , small )
        elements.append(k_display)
        if relationtex.knowledges.count():
            kws =  relationtex.knowledges.all()
        else :
            kws =  relationtex.exotex.knowledges.all()
        for k in kws :
            ks_display = Paragraph( k.name , small )
            elements.append(ks_display)

    if  relationtex.content :
        ctnt =  relationtex.content
    else :
        ctnt =  relationtex.exotex.content

    content = Paragraph(ctnt , normal )
    elements.append(content) 

    doc.build(elements)

    return response


def print_bibliotex(request ):

    bibliotex_id = request.POST.get("print_bibliotex_id",None)  
    skills       = request.POST.get("skills",None)  
    knowledges   = request.POST.get("knowledges",None)  
    bibliotex    = Bibliotex.objects.get(pk = bibliotex_id) 
    elements     = []     
   

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+str(bibliotex.title).replace(" ","_")+'.pdf"'

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

    style_cell = TableStyle(
            [
                ('SPAN', (0, 1), (1, 1)),
                ('TEXTCOLOR', (0, 1), (-1, -1),  colors.Color(0,0.7,0.7))
            ]
        )


    title = ParagraphStyle('title',  fontSize=16 )                   

    normal = ParagraphStyle(name='Normal',fontSize=12,)    
    red = ParagraphStyle(name='Normal',fontSize=12,  textColor=colors.HexColor("#cb2131"),) 
    yellow = ParagraphStyle(name='Normal',fontSize=12,  textColor=colors.HexColor("#ffb400"),)
    green = ParagraphStyle(name='Normal',fontSize=12,  textColor=colors.HexColor("#1bc074"),)
    blue = ParagraphStyle(name='Normal',fontSize=14,  textColor=colors.HexColor("#005e74"),)
    small = ParagraphStyle(name='Normal',fontSize=10,)    
    violet = ParagraphStyle(name='Normal',fontSize=14,  textColor=colors.HexColor("#5d4391"),)
    
    paragraph = Paragraph( bibliotex.title , title )
    elements.append(paragraph)

    today = datetime.now()

    relationtexs = bibliotex.relationtexs.filter(Q( is_publish = 1 )|Q(start__lte=today , stop__gte= today))
    i = 1
    for relationtex in relationtexs :
        
        exo = Paragraph( "Exercice "+str(i)+". " +relationtex.exotex.title, violet )
        elements.append(exo)

        if skills :   

            if relationtex.skills.count():
                sks =  relationtex.knowledges.all()
            else :
                sks =  relationtex.exotex.skills.all()
            for s in sks :
                skills_display +=  s.name+". "
                sk_display = Paragraph( skills_display , small )
                elements.append(sk_display)

        if knowledges :  
            k_display = Paragraph( relationtex.exotex.knowledge.name , small )
            elements.append(k_display)
            if relationtex.knowledges.count():
                kws =  relationtex.knowledges.all()
            else :
                kws =  relationtex.exotex.knowledges.all()
            for k in kws :
                ks_display = Paragraph( k.name , small )
                elements.append(sk_display)
 


        if  relationtex.content :
            ctnt =  relationtex.content
        else :
            ctnt =  relationtex.exotex.content

        content = Paragraph( ctnt , normal )        
        elements.append(content) 
        i+=1

    doc.build(elements)

    return response




def print_exotex(request):


    relationtex_id = request.POST.get("print_exotex_id",None)  
    skills         = request.POST.get("skills",None)  
    knowledges     = request.POST.get("knowledges",None)  
    relationtex    = Relationtex.objects.get(pk = relationtex_id) 
    elements       = [] 

    elements.append(r"""\documentclass[12pt]{article}
                        \input{"""+settings.DIR_PREAMBULE_TEX+r"""preambule} 
                        \input{"""+settings.DIR_PREAMBULE_TEX+r"""styleCoursLycee} 
                        \input{"""+settings.DIR_PREAMBULE_TEX+r"""styleExercices} 
                        \input{"""+settings.DIR_PREAMBULE_TEX+r"""algobox}
                        \begin{document}""")    



    skills_display = ""
    if skills :   
        if relationtex.skills.count():
            sks =  relationtex.skills.all()
        else :
            sks =  relationtex.exotex.skills.all()
        for s in sks :
            skills_display +=  s.name+". "

    exo = "Exercice. " +  relationtex.exotex.title + ".    " +skills_display
    elements.append(exo)



    if knowledges :  
        k_display = relationtex.exotex.knowledge.name
        elements.append(k_display)
        if relationtex.knowledges.count():
            kws =  relationtex.knowledges.all()
        else :
            kws =  relationtex.exotex.knowledges.all()
        for k in kws :
            elements.append(k.name)

    if  relationtex.content :
        ctnt =  relationtex.content
    else :
        ctnt =  relationtex.exotex.content

    elements.append(ctnt)
    elements.append(r"\end{document}")

    file = settings.DIR_TMP_TEX+"exotex"+str(relationtex.id)
    my_tex = ""
    for e in elements:
        my_tex +=str(e)

    f_tex = open(file+".tex","w")
    f_tex.write(my_tex)
    f_tex.close()

    ftex = open( file+".tex" , 'r')

    print(ftex)


    result = subprocess.run(["pdflatex", "-interaction","nonstopmode", file ])

    fpdf = open( file+".pdf" , 'r')
    response = HttpResponse(fpdf, mimetype='application/pdf')
    return response



