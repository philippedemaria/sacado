from django import http
import json
from django.utils import timezone
from django.shortcuts import render, redirect
from schedule.models import Calendar, Event, Automatic
from schedule.forms import CalendarForm, EventForm
from group.models import Group
from account.models import User, Teacher , Student
from datetime import datetime,timedelta
from django.template.loader import render_to_string
from django.http import JsonResponse 
from django.core import serializers
from django.core.mail import send_mail
from qcm.models import  Relationship, Parcours, Studentanswer
from django.db.models import Count, Q
from sendmail.models import Communication
 

from group.decorators import  user_is_group_teacher
from general_fonctions import *

import pytz
import re
import html




def insert_in_calendar(user,title,start,end,comment, type_of_event,link):
    # Ajout de l'evenement dans le calendrier par défaut #######################################################
    calendars = Calendar.objects.filter(user = user).filter(default = 1)
    if type_of_event == 1 :
        color= "#FF0000"
    elif type_of_event == 2 : 
        color= "#006DA2"
    elif type_of_event == 3 : 
        color= "007F00"
    elif type_of_event == 4 : 
        color= "#FF8900"
    else  : 
        color= "#00819F"


    event = Event.objects.create(title=title, start=start, end=end, color=color, comment = comment, type_of_event=type_of_event, link=link) 
    for c in calendars.all() :
        c.event_set.add(event)
     #############################################################################################################


def update_in_calendar(user,type_of_event,link,title,start,end,comment): 
    # Ajout de l'evenement dans le calendrier par défaut #######################################################
    events = Event.objects.filter(type_of_event=type_of_event).filter(link=link).filter(calendar__user = user)
    for event in events : 
        Event.objects.filter(pk=event.id).update(title=title)
        Event.objects.filter(pk=event.id).update(start=start)
        Event.objects.filter(pk=event.id).update(end=end)
        Event.objects.filter(pk=event.id).update(comment=comment)   
    #############################################################################################################

def delete_in_calendar(user,type_of_event,link):

    event = Event.objects.filter(type_of_event = type_of_event).filter(calendar__user = user).filter(link = link) 
    event.delete()


##################################################################################################################################
##################################################################################################################################
##                     Affichage du calendrier des taches via calendar_initialize
##################################################################################################################################
##################################################################################################################################


def events_json(request):
    # Get all events - Pas encore terminé
    user = User.objects.get(pk=request.user.id)
    today = time_zone_user(request.user)

    if request.user.is_teacher:
        teacher = Teacher.objects.get(user=user)
        relationships = Relationship.objects.filter(is_publish=1, parcours__teacher=teacher).exclude(date_limit=None, students=None)

    else:
        student = Student.objects.get(user=request.user.id)
        relationships = Relationship.objects.filter(Q(is_publish=1) | Q(start__lte=today), is_evaluation=0, students=student).exclude(date_limit=None)

    # Create the fullcalendar json events list
    event_list = []

    for relationship in relationships:
        # On récupère les dates dans le bon fuseau horaire
        try :  
            relationship_start = dt_naive_to_timezone(relationship.date_limit, user.time_zone)            
            if relationship.exercise.supportfile.annoncement :
                title =  cleanhtml(unescape_html(relationship.exercise.supportfile.annoncement ))
            else :
                title =  unescape_html(relationship.exercise.knowledge.name)

            event_list.append({
                        'id': relationship.id,
                        'start': relationship_start.strftime('%Y-%m-%d %H:%M:%S'),
                        'end': relationship_start.strftime('%Y-%m-%d %H:%M:%S'),
                        'title': title,
                        'allDay': True,
                        'description': title,
                        'color' : relationship.parcours.color,
                        })
        except : 
            pass

    return http.HttpResponse(json.dumps(event_list), content_type='application/json')


def calendar_initialize(request):
 
    today = time_zone_user(request.user)
    if request.user.is_teacher:
        teacher = Teacher.objects.get(user=request.user)
        relationships = Relationship.objects.filter(parcours__teacher=teacher, date_limit__gte=today).exclude(date_limit=None)
        parcourses = Parcours.objects.filter(teacher=teacher)
        calendars = Calendar.objects.filter(user=request.user)
        form = EventForm(request.user, request.POST or None)        
        nb_teacher_level = teacher.levels.count()
        communications = Communication.objects.values('id', 'subject', 'texte').filter(active=1)
        context = {'form': form, 'relationships': relationships, 'parcourses': parcourses, 'calendars': calendars,'nb_teacher_level' :nb_teacher_level , 'communications' :  communications ,
                   'teacher': teacher}

    else:
        student = Student.objects.get(user=request.user.id)

 
        relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), students=student, date_limit__gte=today).order_by("date_limit")
        exercise_tab = []
        for r in relationships:
            if r not in exercise_tab:
                exercise_tab.append(r.exercise)
        num = 0
        for e in exercise_tab :
            if Studentanswer.objects.filter(student=student, exercise = e).count() > 0 :
                num += 1

        exercises = []
        studentanswers = Studentanswer.objects.filter(student = student)
        for studentanswer in studentanswers:
            if not studentanswer.exercise in exercises:
                exercises.append(studentanswer.exercise)
      
        relationships_in_late = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), students=student, is_evaluation=0, date_limit__lt=today).exclude(exercise__in=exercises).order_by("date_limit")

        nb_relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), students=student,  date_limit__gte=today).count()


        try :
            ratio = int(num/nb_relationships*100)
        except :
            ratio = 0

        ratiowidth = int(0.9*ratio)
        student = Student.objects.get(user=request.user)
        parcours = Parcours.objects.filter(students = student)
        context = {'student' : student ,    'relationships' : relationships ,    'ratio' : ratio ,  'ratiowidth' : ratiowidth ,       'relationships_in_late' : relationships_in_late ,    } 

    return render(request, "schedule/base.html" , context )


##################################################################################################################################
##################################################################################################################################
##                     AFichage du calendrier à partir d'un groupe
##################################################################################################################################
##################################################################################################################################

def events_json_group(request):
 
    user = User.objects.get(pk = request.user.id)
    teacher = Teacher.objects.get(user = user)
 
    idg = request.GET.get("group_id")
    group = Group.objects.get(pk = idg)
    students = group.students.all()


    ## Gestion des taches
    ### Détermine la liste des parcours du groupe
    parcours_tab , evaluation_tab = [] , []
    for student in students :
        parcours = Parcours.objects.filter(students = student, teacher = teacher,is_evaluation=0)
        for p in parcours:
            if p not in parcours_tab :
                parcours_tab.append(p) ### parcours_tab = liste des parcours du groupe


    relationships = Relationship.objects.filter(is_publish = 1, parcours__in=parcours_tab).exclude(date_limit=None, students=None) 
 
 
    event_list = []

    for relationship in relationships:
        # On récupère les dates dans le bon fuseau horaire
        try :       
            relationship_start = dt_naive_to_timezone(relationship.date_limit, user.time_zone) 
            if relationship.exercise.supportfile.annoncement :
                title =  cleanhtml(unescape_html(relationship.exercise.supportfile.annoncement ))
            else :
                title =  unescape_html(relationship.exercise.knowledge.name)

            event_list.append({
                        'id': relationship.id,
                        'start': relationship_start.strftime('%Y-%m-%d %H:%M:%S'),
                        'end': relationship_start.strftime('%Y-%m-%d %H:%M:%S'),
                        'title': title,
                        'allDay': True,
                        'description': title,
                        'color' : relationship.parcours.color,
                        })
        except : 
            pass

    ## Gestion des parcours d'évaluation
    for student in students :
        evaluations = Parcours.objects.filter(students = student, teacher = teacher,is_evaluation=1)
        for e in evaluations:
            if e not in evaluation_tab :
                evaluation_tab.append(e) ### evaluation_tab = liste des evaluations du groupe

    for evaluation in evaluation_tab : # evaluation est un parcours

 
        evaluation_start =  datetime.combine(evaluation.start,  evaluation.starter) 
        evaluation_stop =  datetime.combine(evaluation.stop,  evaluation.stopper)  


        event_list.append({
                    'id': evaluation.id,
                    'start': evaluation_start.strftime('%Y-%m-%d %H:%M:%S'),
                    'end': evaluation_stop.strftime('%Y-%m-%d %H:%M:%S'),
                    'title': evaluation.title,
                    'allDay': False,
                    'description': evaluation.title,
                    'color' : evaluation.color,
                    })        


    return http.HttpResponse(json.dumps(event_list), content_type='application/json')



#@user_is_group_teacher
def schedule_task_group(request, id):
    group = Group.objects.get(id=id)
    teacher =  Teacher.objects.get(user= request.user)
    request.session["group_id"] = group.id   

    relationships = Relationship.objects.filter(parcours__teacher = teacher).exclude(date_limit = None) 

    context = {  'group': group, 'relationships' : relationships ,   }

    return render(request, 'schedule/base_group.html', context )



##################################################################################################################################
##################################################################################################################################
##                    FIN 
##################################################################################################################################
##################################################################################################################################


def calendar_show(request,id):
    user_shown = User.objects.get(pk = id)
 
    template = "schedule/just_show.html"
    context = { 'user_shown' : user_shown ,   }  

    return render(request, template , context )


def events_show(request,id):

    user_shown = User.objects.get(pk = id)
    events = Event.objects.filter(calendar__user = user_shown)
    # Create the fullcalendar json events list
    event_list = []

    for event in events:
        # On récupère les dates dans le bon fuseau horaire
        event_start = event.start.astimezone(timezone.get_default_timezone())
        event_end = event.end.astimezone(timezone.get_default_timezone())
        # On décide que si l'événement commence à minuit c'est un
        # événement sur la journée
        if event.is_allday :
            allDay = True
        else:
            allDay = False

        event_list.append({
                    'id': event.id,
                    'start': event_start.strftime('%Y-%m-%d %H:%M:%S'),
                    'end': event_end.strftime('%Y-%m-%d %H:%M:%S'),
                    'title': event.title,
                    'allDay': allDay,
                    'color' : event.color,
                    })

    if len(event_list) == 0:
        raise http.Http404
    else:
        return http.HttpResponse(json.dumps(event_list),
                                 content_type='application/json')


