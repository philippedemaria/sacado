from django import http
import json
from django.utils import timezone
from django.shortcuts import render, redirect
from lesson.models import Event
from lesson.forms import EventForm
from account.models import User, Student , Teacher, Parent
from school.models import School

from datetime import datetime,timedelta
from django.template.loader import render_to_string
from django.http import JsonResponse 
from django.core import serializers
from django.core.mail import send_mail
from general_fonctions import *


def get_hours():
    hours = []
    hour, minute = 8,0
    for i in range(14) :
        for j in range(4) :
            minute = 15*j
            if minute == 0:
                minute = "00"
            time = str(hour)+":"+str(minute)
            hours.append(time)
        hour=hour+1
    return hours




def events_json(request):

    user =  request.user 
    events = user.events.all()
    event_list = []

    for event in events:
        # On récupère les dates dans le bon fuseau horaire
        event_start = event.start.astimezone(timezone.get_default_timezone())
        event_end = event.end.astimezone(timezone.get_default_timezone())
 
        event_list.append({
                    'id': event.id,
                    'start': event_start.strftime('%Y-%m-%d %H:%M:%S'),
                    'end': event_end.strftime('%Y-%m-%d %H:%M:%S'),
                    'title': event.title,
                    'color' : event.color,
                    })

    if len(event_list) == 0:
        raise http.Http404
    else:
        return http.HttpResponse(json.dumps(event_list), content_type='application/json')
 


def calendar_show(request,id=0):
    user  = request.user
    form = EventForm(user, request.POST or None)
    hours = get_hours()
    students = user.teacher.students.all()
    context = { 'user_shown' : user , 'form' : form , 'hours' : hours , 'students' : students ,  }  

    return render(request, "lesson/calendar_show.html" , context )
 


def create_event(request):

    user =  request.user  
    form = EventForm(user, request.POST or None)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        date_of_event = new_form.start 
        start_hour = request.POST.get("start_hour")
        tabs = start_hour.split(":")
        new_form.start = date_of_event + timedelta(hours=int(tabs[0]),minutes=int(tabs[1]))

        end_hour = request.POST.get("end_hour")
        tabe = end_hour.split(":")
 
        new_form.end = date_of_event + timedelta(hours=int(tabe[0]),minutes=int(tabe[1]))
        new_form.save()


        start_hour = request.POST.get("start_hour")
        end_hour = request.POST.get("end_hour")

        send_list = []
        for s in request.POST.getlist("students") :
            if s.user.email :
                send_list.append(s.user.email)
        send_list.append(request.user.email)  
              
        send_mail("SACADO : Création de leçon par visio",  str(user) +" vient de créer une nouvelle leçon : '"+ str(new_form.title) +"' qui se déroulera le "+ str(date_of_event) +" de "+str(start_hour)+" à "+str(end_hour)+". \n Cette leçon sera retransmise par visio à l'adresse : "+ new_form.title +". \nCordialement.", str(user.email), send_list) #send_list )

    else:
        print(form.errors)
        
    return redirect('calendar_show' , 0)


 
 


def update_event(request,id):
    user = User.objects.get(pk=request.user.id)
    event = Event.objects.get(pk=id)
    form = EventForm(user, request.POST or None, instance = event)

    if form.is_valid():
        new_form = form.save(commit=False)
        start_hour = request.POST.get("start_hour")
        tabs = start_hour.split(":")
        new_form.start = new_form.start + timedelta(hours=int(tabs[0]),minutes=int(tabs[1]))

        #new_form.type_of_event = request.POST.get("type_of_event")

        end_hour = request.POST.get("end_hour")
        tabe = end_hour.split(":")
        new_form.end = new_form.end + timedelta(hours=int(tabe[0]),minutes=int(tabe[1]))
        new_form.user = user 
        new_form.save()

    else :
        print(form.errors)
        
    return redirect('calendar_show' , 0)


def shift_event(request):
 
    event_id = request.POST.get('event_id')
    new_start_event = request.POST.get('start_event')
    event = Event.objects.filter(pk=event_id).update(start=new_start_event)
 
    data = {} 
    return JsonResponse(data)

def show_event(request):
    event_id = request.POST.get('event_id')
    event = Event.objects.get(pk=event_id)   
    user = User.objects.get(pk=request.user.id) 
    form = EventForm(user, request.POST or None, instance = event) 

    delta = event.end - event.start
 
    same_day = False
    if delta <= timedelta(days=1) :
        same_day = True

    data = {}

    hs = ['8','9','10','11','12','13','14','16','16','17','18','19'] 
    ms = ['00','15','30','45'] 
    hours = []
    for h in hs :
        for m in ms :
            hours.append(h+":"+m)
 
    html = render_to_string('lesson/show.html',{ 'event' : event  , 'same_day': same_day ,  'form' : form  , 'hours' : hours  ,  })
    data['html'] = html       

    return JsonResponse(data)




def delete_event(request,id):
 
    event = Event.objects.get(pk=id)    
    event.delete()
    return redirect('calendar_show' , 0)



def add_students_to_my_lesson_group(request):
 
    user = request.user
    if request.method == "POST":
        students = request.POST.getlist('students')

        for s in students :
            print(s)
            user.teacher.students.add(s)
        return redirect('calendar_show' , 0)

    today   = time_zone_user(user)
    students = Student.objects.filter(user__school_id = 50,user__user_type=0, user__closure__lte= today  ).order_by("level__ranking", "user__last_name")
    
    context = { 'user' : user , 'students' : students , 'teacher' : user.teacher   }   
    return render(request, "lesson/add_students_to_my_lesson_group.html" , context )



def delete_student_to_my_lesson_group(request,id):
 
    user = request.user  
    s= Student.objects.get(user_id=id) 
    user.teacher.students.remove(s)
    return redirect('calendar_show' , 0)





def dashboard_parent(request):
 
    parent = Parent.objects.get(user=request.user)
    students = parent.students.order_by("user__first_name")
    index_tdb = False  # Permet l'affichage des tutos Youtube dans le dashboard
    today = time_zone_user(request.user)
    context = {'parent': parent, 'students': students, 'today' : today , 'index_tdb' : index_tdb, }
    template = 'lesson/dashboard_lesson_parent.html'
      
    return render(request, template , context )




def detail_student_lesson(request,id):
 
    user = request.user
    student = Student.objects.get(user_id=id)
    lessons = student.user.these_events.all()
    
    context = { 'user' : user , 'student' : student , 'lessons' : lessons   }   
    return render(request, "lesson/list_lessons.html" , context )





def ask_lesson(request,id):
 
    user = request.user
    student = Student.objects.get(user_id=id)
    teachers = Teacher.objects.filter(user__school_id=50,is_lesson=1).order_by("user__last_name")
    
    context = { 'user' : user , 'student' : student , 'teachers' : teachers   }   
    return render(request, "lesson/ask_lesson.html" , context )
