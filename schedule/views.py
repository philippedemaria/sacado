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

 
from django.contrib.auth.decorators import login_required 
from group.decorators import  user_is_group_teacher


import pytz
import re
import html


def time_zone_user(user):
    if user.time_zone :
        time_zome = user.time_zone
        timezone.activate(pytz.timezone(time_zome))
        current_tz = timezone.get_current_timezone()
        today = timezone.localtime(timezone.now())
        
    else :
        today = timezone.now()
    return today


def unescape_html(string):
        '''HTML entity decode'''
        string = html.unescape(string)
        return string 


def cleanhtml(raw_html): # nettoie le code des balises HTML
    cleantext = re.sub('<.*?>', '', raw_html)
    cleantext = re.sub('\n', '', cleantext)
    cleantext = re.sub('\t', '', cleantext)
    return cleantext
 


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
        relationship_start = relationship.date_limit
        if relationship.exercise.supportfile.annoncement :
            title =  cleanhtml(unescape_html(relationship.exercise.supportfile.annoncement ))
        else :
            title =  unescape_html(relationship.exercise.knowledge.name)
        event_list.append({
                    'id': relationship.id,
                    'start': relationship_start.strftime('%Y-%m-%d %H:%M:%S'),
                    'end': relationship_start.strftime('%Y-%m-%d %H:%M:%S'),
                    'title': title,
                    'allDay': False,
                    'description': title,
                    'color' : relationship.parcours.color,
                    })

    return http.HttpResponse(json.dumps(event_list), content_type='application/json')


def calendar_initialize(request):
 
    today = time_zone_user(request.user)
    if request.user.is_teacher:
        teacher = Teacher.objects.get(user=request.user)
        relationships = Relationship.objects.filter(parcours__teacher=teacher, date_limit__gte=today).exclude(date_limit=None)
        parcourses = Parcours.objects.filter(teacher=teacher)
        calendars = Calendar.objects.filter(user=request.user)
        form = EventForm(request.user, request.POST or None)
        context = {'form': form, 'relationships': relationships, 'parcourses': parcourses, 'calendars': calendars,
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
        context = {'student' : student ,     'relationships' : relationships ,    'ratio' : ratio ,  'ratiowidth' : ratiowidth ,       'relationships_in_late' : relationships_in_late ,    } 

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
        relationship_start = relationship.date_limit 
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


 
@login_required
@user_is_group_teacher
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



def create_calendar(request):

    user = User.objects.get(pk=request.user.id)
    calendars = Calendar.objects.filter(user = user)
    form = CalendarForm(request.POST or None)
    if request.method =='POST' :    
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
 
            if request.POST.get("from_dashboard") ==  "1"  :
                return redirect("index")
            else :
                return redirect('calendar_initialize')   

    return render(request,'schedule/new_calendar.html', { 'form' : form , 'calendars' : calendars , })


def update_calendar(request,id):

    if request.method =='POST' : 

        calendar = Calendar.objects.get(pk=id)
        if request.POST.get("calendar_public") :           
            calendar.status = 1
        else :
            calendar.status = 0
        if request.POST.get("calendar_type") :  
            calendar.default = 1
        else :
            calendar.default = 0
        if request.POST.get("calendar_color")  : 
            calendar.color= request.POST.get("calendar_color")
        calendar.save() 

    return redirect('preferences')  


def delete_calendar(request,id):

    form = CalendarForm(request.POST or None)
    calendar = Calendar.objects.get(pk=id)
    calendar.delete() 
    return render(request,'schedule/new_calendar.html', { 'form' : form , })


def create_event(request):

    user = User.objects.get(pk=request.user.id)
    form = EventForm(user, request.POST or None)
    if form.is_valid():
        new_form = form.save(commit=False)
        date_of_event = new_form.start 
        if not new_form.is_allday :
            start_hour = request.POST.get("start_hour")
            tabs = start_hour.split(":")
            date_of_event = new_form.start 
            new_form.start = new_form.start + timedelta(hours=int(tabs[0]),minutes=int(tabs[1]))

            end_hour = request.POST.get("end_hour")
            tabe = end_hour.split(":")
            new_form.end = new_form.end + timedelta(hours=int(tabe[0]),minutes=int(tabe[1]))
 
        new_form.save()
        cals = Calendar.objects.filter(default=1).filter(user=user)
        for cal in cals :
            new_form.calendar.add(cal)

        send_list = []
        tab_users_id = []

        for other_id in request.POST.getlist("users") :
            user_dest = User.objects.get(pk = other_id)
            new_form.pk = None
            calendars = Calendar.objects.filter(user=other_id).filter(default=1)
            for cal in calendars :
                calendar = cal
            new_form.save()
            new_form.calendar.add(calendar)
            new_form.notification = 1
            new_form.comment += " Ajouté directement par " + str(user)
            new_form.save()
            tab_users_id.append(user_dest.id)
            send_list.append(str(user_dest.email))

        try :
            start_hour = request.POST.get("start_hour")
            end_hour = request.POST.get("end_hour")
        except :
            start_hour = "8h30"
            end_hour = "15h30"

        if len(send_list) > 0 :
            send_mail("Création d'événement",  str(user) +" vient de créer un nouvel événement : '"+ str(new_form.title) +"' qui se déroulera le "+ str(date_of_event) +" à "+str(start_hour)+". Il a souhaité vous y associer. \n Cet événement est donc déjà enregistré dans votre agenda par défaut, connectez-vous à votre espace MEM https://mem.erlm.tn. \n Si vous ne souhaitez pas y être associé, vous pourrez supprimer cet événement. Cordialement.", str(user.email), send_list) #send_list )

        if request.POST.get("type_of_event") == "1" :
            Task.objects.create(note=new_form.title,issue=date_of_event,done=0, owner=user,comment=new_form.comment,ranking=0)
 
        elif request.POST.get("type_of_event") == "2" : # Visite de classe
            neo = Teacher.objects.get(user_id = int(request.POST.get("neo")))
            place = request.POST.get("schools")
            former = Former.objects.get(pk = request.user.id)


            Suivineo.objects.create(dateVisite=date_of_event,heureVisite=start_hour , neo=neo, former=former,place=place )                
 

            directors = Director.objects.filter(user__school_id = int(place) )
            for director in directors :
                send_mail("INFO : Visite  croisée  MEM le"+ str(date_of_event), "Une visite de classe est programmée dans votre établissement le "+ str(date_of_event)+" à "+str(start_hour)+" entre "+str(neo)+" et "+str(former)+".", "info@sacado.xyz", [str(director.user.email)]) # CE
            send_mail("Visite croisée  MEM le"+ str(date_of_event), "Une visite de classe est programmée le "+ str(date_of_event)+" à "+str(start_hour)+" entre vous et "+str(former)+". Connectez-vous à votre espace MEM https://mem.erlm.tn", "info@sacado.xyz", [str(neo.user.email)]) # neo
            send_mail("Visite croisée  MEM le"+ str(date_of_event), "Une visite de classe est programmée le "+ str(date_of_event)+" à "+str(start_hour)+" entre vous et "+str(former)+". Connectez-vous à votre espace MEM https://mem.erlm.tn", "info@sacado.xyz", [str(former.user.email)]) # neo

        for user_id in tab_users_id :
            receiver = User.objects.get(pk = user_id)
            insert_in_calendar(receiver,new_form.title,date_of_event,date_of_event,new_form.comment, request.POST.get("type_of_event"),0)

    else:
        print(form.errors)
        
    return redirect('calendar_initialize')


 
 


def update_event(request,id):
    user = User.objects.get(pk=request.user.id)
    event = Event.objects.get(pk=id)
    form = EventForm(user, request.POST or None, instance = event)

    if form.is_valid():
        new_form = form.save(commit=False)
        if not new_form.is_allday :
            start_hour = request.POST.get("start_hour")
            tabs = start_hour.split(":")
            new_form.start = new_form.start + timedelta(hours=int(tabs[0]),minutes=int(tabs[1]))

            #new_form.type_of_event = request.POST.get("type_of_event")

            end_hour = request.POST.get("end_hour")
            tabe = end_hour.split(":")
            new_form.end = new_form.end + timedelta(hours=int(tabe[0]),minutes=int(tabe[1]))
        new_form.save()
        user = User.objects.get(pk = request.user.id)
        cals = Calendar.objects.filter(default=1).filter(user=user)
        for cal in cals :
            new_form.calendar.add(cal)
    else :
        print(form.errors)
 

    return redirect('calendar_initialize') 


def shift_event(request):
 
    event_id = request.POST.get('event_id')
    new_start_event = request.POST.get('start_event')
    event = Event.objects.filter(pk=event_id).update(start=new_start_event)
    
 
    data = {} 
    return JsonResponse(data)

def show_event(request):
    event_id = request.POST.get('event_id')
    user = User.objects.get(pk=request.user.id)  
    relationship = Relationship.objects.get(pk=event_id)   
    same_day = False
    data = {}

    hs = ['8','9','10','11','12','13','14','16','16','17','18','19'] 
    ms = ['00','15','30','45'] 
    hours = []
    for h in hs :
        for m in ms :
            hours.append(h+":"+m)

    
    html = render_to_string('schedule/show_content_cal.html',{ 'relationship' : relationship  })
 
    
    data['html'] = html       

    return JsonResponse(data)




def delete_event(request,id):
 
    event = Event.objects.get(pk=id)    
    event.delete()
    return redirect('calendar_initialize') 




def add_automaticly_update(request):
 
    user = User.objects.get(pk=request.user.id)
    if request.POST.get("publish_now1") : 
        value = 1
    else:
        value = 0
    if request.POST.get("publish_now2") : 
        val  = 1
    else:
        val  = 0
    if request.POST.get("publish_now3") : 
        v  = 1
    else:
        v  = 0
    Automatic.objects.update_or_create(user=user,module='visit',defaults = {"insert": value,})
    Automatic.objects.update_or_create(user=user,module='stage',defaults = {"insert": val,})
    Automatic.objects.update_or_create(user=user,module='animation',defaults = {"insert": v, })  

    return redirect('preferences') 


def delete_content_from_event(request,id):

    Content.objects.filter(pk = id).update(is_task=0)
    return redirect('calendar_initialize') 