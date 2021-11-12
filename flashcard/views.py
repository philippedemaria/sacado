from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail

from flashcard.models import Flashcard, Flashpack
from flashcard.forms import FlashcardForm ,  FlashpackForm  
from qcm.models import  Parcours, Exercise , Folder
from account.decorators import  user_is_testeur
from sacado.settings import MEDIA_ROOT
from qcm.views import  get_teacher_id_by_subject_id
from group.models import Group 
from socle.models import Level, Waiting , Knowledge

import uuid
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.forms import inlineformset_factory
from templated_email import send_templated_mail
from django.db.models import Q
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





def list_flashpacks(request):
 
    flashpacks = Flashpack.objects.all()
    return render(request, 'flashcard/list_flashpacks.html', {'flashpacks': flashpacks, 'communications' : [] , })


 
def list_my_flashpacks(request):

	teacher = request.user.teacher
	flashpacks = Flashpack.objects.filter(teacher = teacher)
	return render(request, 'flashcard/list_flashpacks.html', {'flashpacks': flashpacks, 'communications' : [] , })

 

def create_flashpack(request):

    teacher = request.user.teacher
    form = FlashpackForm(request.POST or None ,request.FILES or None , teacher = teacher  )

    if form.is_valid():
        nf = form.save(commit=False)
        nf.teacher  = teacher
        nf.save()
        form.save_m2m()

        for l_id in request.POST.getlist("levels") :
            level = Level.objects.get(pk=l_id)
            level.flashpacks.add(nf)
        messages.success(request, 'Le thème a été créé avec succès !')
        return redirect('my_flashpacks')
    else:
        print(form.errors)

    context = {'form': form, 'communications' : [] , 'flashpack': None  }

    return render(request, 'flashcard/form_flashpack.html', context)



 
def update_flashpack(request, id):

    flashpack = Flashpack.objects.get(id=id)
    flashpack_form = FlashpackForm(request.POST or None, instance=flashpack )
    if request.method == "POST" :
        if flashpack_form.is_valid():
            flashpack_form.save()
            for l_id in request.POST.getlist("levels") :
                level = Level.objects.get(pk=l_id)
                level.flashpacks.add(flashpack)
            messages.success(request, 'Le thème a été modifié avec succès !')
            return redirect('my_flashpacks')
        else:
            print(flashpack_form.errors)

    context = {'form': flashpack_form, 'communications' : [] , 'flashpack': flashpack,   }

    return render(request, 'flashcard/form_flashpack.html', context )


 
def delete_flashpack(request, id):
    flashpack = Flashpack.objects.get(id=id)
    levels = Level.objects.filter(flashpacks=flashpack)
    for l in levels :
        l.flashpacks.remove(flashpack)
    flashpack.delete()

    return redirect('my_flashpacks')



 
def show_flashpack(request, id):
    flashpack = Flashpack.objects.get(id=id)
    context = {'flashpack': flashpack,   }
    return render(request, 'flashcard/show_flashpack.html', context )




def clone_flashpack(request, id):
    flashpack = Flashpack.objects.get(id=id)
    context = {'flashpack': flashpack,   }
    return render(request, 'flashcard/show_flashpack.html', context )   

######################################################################################
######################################################################################
#           Flashcard
######################################################################################
######################################################################################


def list_flashcards(request):
 
    flashcards = Flashcard.objects.all()
    return render(request, 'flashcard/list_flashcards.html', {'flashcards': flashcards, 'communications' : [] , })



 
def create_flashcard(request):

    form = FlashcardForm(request.POST or None  )

    if form.is_valid():
        nf = form.save()
        for l_id in request.POST.getlist("levels") :
            level = Level.objects.get(pk=l_id)
            level.flashcards.add(nf)
        messages.success(request, 'Le thème a été créé avec succès !')
        return redirect('flashcards')
    else:
        print(form.errors)

    context = {'form': form, 'communications' : [] , 'flashcard': None  }

    return render(request, 'flashcard/form_flashcard.html', context)



 
def update_flashcard(request, id):

    flashcard = Flashcard.objects.get(id=id)
    flashcard_form = FlashcardForm(request.POST or None, instance=flashcard )
    if request.method == "POST" :
        if flashcard_form.is_valid():
            flashcard_form.save()
            for l_id in request.POST.getlist("levels") :
                level = Level.objects.get(pk=l_id)
                level.flashcards.add(flashcard)
            messages.success(request, 'Le thème a été modifié avec succès !')
            return redirect('flashcards')
        else:
            print(flashcard_form.errors)

    context = {'form': flashcard_form, 'communications' : [] , 'flashcard': flashcard,   }

    return render(request, 'flashcard/form_flashcard.html', context )


 
def delete_flashcard(request, id):
    flashcard = Flashcard.objects.get(id=id)
    levels = Level.objects.filter(flashcards=flashcard)
    for l in levels :
        l.flashcards.remove(flashcard)
    flashcard.delete()

    return redirect('flashcards')




 
def show_flashcard(request, id):
    flashcard = Flashcard.objects.get(id=id)
    context = {'flashcard': flashcard,   }
    return render(request, 'flashcard/show_flashcard.html', context )








######################################################################################
######################################################################################
#           AJAX 
######################################################################################
######################################################################################



@csrf_exempt 
def ajax_attribute_this_flashcard(request):  

    id_level =  request.POST.get("id_level")
    id_theme =  request.POST.get("id_theme")
    data = {}

    level =  Level.objects.get(pk = id_level)

    waitings = level.waitings.values_list('id', 'name').filter(theme_id=id_theme) 
    data['waitings'] = list(waitings)
 
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



def ajax_charge_groups(request):  # utilisé par form_quizz et form_folder aussi

    teacher = request.user.teacher
    data = {} 
    subject_id = request.POST.get('id_subject', None)
    groups = Group.objects.values_list("id","name").filter(Q(teacher=teacher)|Q(teachers=teacher),subject_id =  subject_id)

    data["groups"] = list(groups)

    return JsonResponse(data)


def ajax_charge_groups_level(request):  # utilisé par form_folder aussi

    teacher = request.user.teacher
    data = {} 
    subject_id = request.POST.get('id_subject', None)
    level_id   = request.POST.get('id_level', None)
    groups     = Group.objects.values_list("id","name").filter(Q(teacher=teacher)|Q(teachers=teacher),subject_id =  subject_id, level_id =  level_id)

    data["groups"] = list(groups)

    # gère les propositions d'image d'accueil    
    level =  Level.objects.get(pk = level_id)
    data['imagefiles'] = None
    imagefiles = level.level_folders.values_list("vignette", flat = True).filter(subject_id=subject_id).exclude(vignette=" ").distinct()
    if imagefiles.count() > 0 :
        data['imagefiles'] = list(imagefiles)

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
            fldrs.update(group.group_folders.values_list("id","title").filter(is_trash=0))
            prcs.update(group.group_parcours.values_list("id","title").filter(is_trash=0,folders=None))
        data['folders'] =  list( fldrs )
        data['parcours'] =  list( prcs )
    else :
        data['folders'] =  []
        data['parcours'] =  []
    return JsonResponse(data)


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
