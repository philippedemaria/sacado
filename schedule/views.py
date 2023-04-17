from django import http
import json
from django.utils import timezone
from django.shortcuts import render, redirect

from schedule.models import Calendar, Event, Automatic , Edt , Slotedt , Template_edt
from schedule.forms import CalendarForm, EventForm , EdtForm , ContentslotForm

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

##################################################################################################################################
##################################################################################################################################
##                     Def annexe
##################################################################################################################################
##################################################################################################################################








##################################################################################################################################
##################################################################################################################################
##                     Progessions
##################################################################################################################################
##################################################################################################################################


def progressions(request):
    
    teacher =   request.user.teacher
    groups = teacher.groups.all()

    if teacher.user.edt :
        context = {  'groups': groups,   }
        return render(request, 'schedule/progressions.html', context )
    else :
        return redirect("config_edt",0)


def config_progression(request,idc):
    
    teacher =   request.user.teacher
    groups = teacher.groups.all()

    context = {  'groups': groups,   }

    return render(request, 'schedule/progressions.html', context )


def progression_group(request,idg):

    user = request.user
    teacher = request.user.teacher
    group   = teacher.groups.get(pk=idg) 
    groups = teacher.groups.all()

    sloters = [1,2,3,4,5,6,7,8,9,10,11,12]
    my_edt = user.edt
    days   = my_edt.days_on.split("-")
    days   = days[:-1] 
    start , stop  = my_edt.start , my_edt.stop
    all_slots = my_edt.slots.filter(groups=group).order_by("start")
    slots_edt = my_edt.slots.filter(start__gte=start, start__lt=start+timedelta(days=7))
    today = time_zone_user(user)
    list_all_slot_ids  = all_slots.values_list("id",flat=True)
    list_this_slot_ids = list_all_slot_ids.filter(start__gte=today, start__lt=today+timedelta(days=7))
    if not list_all_slot_ids : list_this_slot_ids = list_all_slot_ids.filter(start__gte=today, start__lt=today+timedelta(days=20))
    
    if len(list_this_slot_ids) : nb_px = list(list_all_slot_ids).index(list_this_slot_ids[0])*100
    else : nb_px = 10 

    today = time_zone_user(request.user)
    this_first_day_week = today +   timedelta(days=  int(my_edt.first_day) - today.weekday() )
    this_last_day_week  = this_first_day_week +   timedelta(days= len(my_edt.days_on.split("-"))-2 )
    form = ContentslotForm(request.POST or None)


    bibliotexs = group.bibliotexs.all()
    flashpacks = group.flashpacks.all()
    quizzes    = group.quizz.all()

    parcourses = group.group_parcours.filter( is_publish=1 ,is_trash=0)

    list_relationships , list_courses  = list() ,  list()
    for parcours in parcourses :
        dico_list_relationships = {'parcours' : parcours  , 'relationships' : parcours.parcours_relationship.all()  }
        dico_list_courses  = {'parcours' : parcours  , 'courses' : parcours.course.all() }
        list_relationships.append(dico_list_relationships)
        list_courses.append(dico_list_courses)

    waitings = group.level.waitings.filter(theme__subject= group.subject).order_by("theme__subject" , "theme")

    context = { 'bibliotexs' : bibliotexs , 'flashpacks' : flashpacks , 'quizzes' : quizzes , 'list_relationships' : list_relationships , 'list_courses' : list_courses ,  'waitings' : waitings ,  
                'groups': groups , 'group': group, 'teacher': teacher, 'sloters': sloters, 'slots_edt':slots_edt  , 'all_slots' : all_slots ,   'nb_px' : nb_px , 'today_slot' : today.date() ,
                'my_edt':my_edt  , 'days':days , 'this_first_day_week':this_first_day_week  , 'this_last_day_week':this_last_day_week  , 'form':form  }

    return render(request, 'schedule/progression_group.html', context )



def insert_content_into_slot(request,idg):

    user = request.user
    teacher = request.user.teacher
    group   = teacher.groups.get(pk=idg) 
    groups = teacher.groups.all()

    slot       = request.POST.get("slot")
    slot_start = request.POST.get("start")
    slot_start = datetime.strptime(slot_start, '%Y-%m-%d').date()
    slotedt = Slotedt.objects.get(users=user, start__startswith = slot_start, slot = slot , groups = group)
    content = slotedt.content
    form = ContentslotForm(request.POST or None,instance =slotedt)
    if form.is_valid() :
        nf = form.save(commit=True)
        nf.content = nf.content + content
        nf.save()
        nf.users.add(user)
        nf.groups.add(group)

    return redirect('progression_group',  idg )



def clear_the_slot(request,ids,idg):
 
    slotedt = Slotedt.objects.get(pk=ids)
    slotedt.content = ""
    slotedt.save() 

    return redirect('progression_group',  idg )



def config_edt(request,ide):

    user = request.user 

    if user.edt  :  
        my_edt = user.edt
        form = EdtForm(request.POST or None , instance = my_edt  )
    else :  
        form    = EdtForm(request.POST or None  )
        my_edt = None
 

    if form.is_valid():
        nf = form.save(commit=False)
        first_day = nf.first_day

        dico_fist = {  "0":"Lundi","1":"Mardi","2":"Mercredi","3":"Jeudi","4":"Vendredi","5":"Samedi","6":"Dimanche",}
        days = request.POST.getlist("days") #liste
        first = days.index(dico_fist[first_day])
        days_on = ""
        for i in range(len(days)):
            days_on += days[(first+i)%len(days)]+"-"
        nf.days_on = days_on
        nf.user = user
        nf.save()
        return redirect('my_edt')
    else:
        print(form.errors)

    context = {  'form' : form , 'edt' : my_edt  }

    return render(request, 'schedule/edt_config.html', context )


def my_edt(request):

    user = request.user
    teacher = user.teacher
    groups = teacher.groups.all()
    sloters = [1,2,3,4,5,6,7,8,9,10,11,12]

    if user.edt  :  
        my_edt = user.edts
        days   = my_edt.days_on.split("-")
        days   = days[:-1] 
        start , stop  = my_edt.start , my_edt.stop
        try :
            slots_edt = my_edt.slots.filter(start__gte=start, start__lt=start+timedelta(days=7))
        except : 
            slots_edt = None

    else :  
        my_edt = None

    if my_edt and request.method == "POST" :
        annual_slots,slots = list(), list()

        for a_s in  request.POST.getlist('annual_slots') :
            if a_s != "" : annual_slots.append(a_s)
 

        for a_slot in annual_slots :
            group_id, slot , day , half , even  = a_slot.split("-")
            group = Group.objects.get(pk=group_id)

            template_edt,created = Template_edt.objects.update_or_create( edt= my_edt,slot=slot,day=day,is_half=half)
            if created : template_edt.groups.add(group)
            else : 
                template_edt.groups.clear()
                template_edt.groups.add(group)

            nextDay = start +   timedelta(days= int(day) - start.weekday() )
            if str(even) == "0"   : nextDay += timedelta(days= 7 )
            if half == 1 : hday = 14
            else  : hday = 7            
            while nextDay < stop :
                slt  = Slotedt.objects.create( start=nextDay,slot=slot )

                nextDay +=  timedelta(days=hday)
                slt.groups.add(group)
                slt.users.add(user)
                slots.append(slt)
        my_edt.slots.set(slots)

    context = {  'sloters' : sloters ,'days' : days , 'my_edt' : my_edt , 'teacher' : teacher ,'slots_edt' : slots_edt ,'groups' : groups  }

    return render(request, 'schedule/my_edt.html', context )

 

def my_edt_group_attribution(request):

    id_group = request.POST.get("id_group",None)
    data     = {}
    if id_group and int(id_group) > 0 :   
        group   =  Group.objects.get(pk = id_group)
        data['style']    = "background-color:"+group.color+";color:white"
        data['name']     =  group.name
        data['group_id'] =  group.id
    else :
        data['style']    = "background-color:white;color:white"
        data['name']     =  ""
        data['group_id'] =  ""
 
    return JsonResponse(data)





def get_progression(request,idg) :

    group = Group.objects.get(pk=idg)
    user_and_group_id  = request.POST.get("user_and_group_id")
    user_id , group_id = user_and_group_id.split("-")

    my_edt_id = request.POST.get("my_edt_id")
    my_edt = Edt.objects.get(pk=my_edt_id)
    my_edt_slots = my_edt.slots.filter(groups = group).order_by("start")
    # détails du donneur
    share_user  = User.objects.get(pk=user_id)
    share_group = Group.objects.get(pk=group_id) 
    share_slots = share_user.edt.slots.filter(groups = share_group).order_by("start")
    ################# 
    if share_slots :
        i=0
        for slot in my_edt_slots :
            try :
                slot.content = share_slots[i]["content"]
                slot.save()
                i+=1
            except :
                pass

        messages.success(request,"Mutualisation réussie.")
    else :
        messages.error(request,"Cet enseignant ne mutualise pas de progression sur ce niveau.")
 
    return redirect('progression' , idg)



def print_progression(request,idg) :

    group = Group.objects.get(pk=idg)
    formatage = request.POST.get("format")
    my_edt_id = request.POST.get("my_edt_id")
    my_edt = Edt.objects.get(pk=my_edt_id)

    date_start = request.POST.get("date_start")
    date_stop  = request.POST.get("date_stop")
    all_progression = request.POST.get("all_progression")


    if all_progression : slots = my_edt.slots.filter(groups=group).order_by("start")
    else : slots = my_edt.slots.filter(groups=group, start__gte=date_start, start__lte=date_stop )

    if formatage == "pdf" :
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=progression_'+group.level.name+'.pdf'

        doc = SimpleDocTemplate(response,   pagesize=A4, 
                                            topMargin=0.3*inch,
                                            leftMargin=0.3*inch,
                                            rightMargin=0.3*inch,
                                            bottomMargin=0.3*inch     )

        title = ParagraphStyle('title',  fontSize=13, textColor=colors.HexColor("#000000"),)
        normal = ParagraphStyle('normal',  fontSize=11, textColor=colors.HexColor("#000000"),)                   

        logo = Image('https://sacado.xyz/static/img/sacadoA1.png')
        logo_tab = [[logo,  "Progression de "+group.level.name+"\nDocument généré par SACADO"  ]]
        logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5*inch])
        logo_tab_tab.setStyle(TableStyle([ ('TEXTCOLOR', (0,0), (-1,0), colors.Color(0,0.5,0.62))]))
        
        elements = list()
        elements.append(logo_tab_tab)
        elements.append(Spacer(0, 0.2*inch))
        i = 1
        for slot in slots :
            elements.append(Paragraph( i+". "+ slot.start , title ))
            elements.append(Paragraph( slot.content , normal ))
            elements.append(Spacer(0, 0.2*inch))
            i+=1

        doc.build(elements)
        return response

    elif  formatage == "csv" :
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=progression_'+group.level.name+'.pdf'
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        fieldnames = ("Créneau", "Date", "Contenu"  )
        writer.writerow(fieldnames)
        i = 1
        for slot in slots :
            writer.writerow( i, slot.start , slot.content )
            i +=1
        return response

    elif  formatage == "xls" :

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=progression_'+group.level.name+'.pdf'

        response.write(u'\ufeff'.encode('utf8'))
        wb = xlwt.Workbook(encoding='utf-8')
        font_style = xlwt.XFStyle()
        ws = wb.add_sheet("Progression"+group.level.name)

        # Sheet header, first row
        row_num = 0

        columns = ("Créneau", "Date", "Contenu"  ) 
        i = 1
        for col_num in range(len(columns)):
            ws.write(i, col_num, columns[col_num], font_style)
            i +=1

        return response

##################################################################################################################################
##################################################################################################################################
##                     Calendrier à partir d'un groupe
##################################################################################################################################
##################################################################################################################################


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


def events_json_(request):
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
        parcourses = Parcours.objects.filter(teacher=teacher,is_trash=0)
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
        parcours = Parcours.objects.filter(students = student,is_trash=0)
        context = {'student' : student ,    'relationships' : relationships ,    'ratio' : ratio ,  'ratiowidth' : ratiowidth ,       'relationships_in_late' : relationships_in_late ,    } 

    return render(request, "schedule/base.html" , context )


##################################################################################################################################
##################################################################################################################################
##                     Affichage du calendrier à partir d'un groupe
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
        parcours = Parcours.objects.filter(students = student, teacher = teacher,is_evaluation=0,is_trash=0)
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
        evaluations = Parcours.objects.filter(students = student, teacher = teacher,is_evaluation=1,is_trash=0)
        for e in evaluations:
            if e not in evaluation_tab :
                evaluation_tab.append(e) ### evaluation_tab = liste des evaluations du groupe

    for evaluation in evaluation_tab : # evaluation est un parcours

 
        evaluation_start =  evaluation.start
        evaluation_stop =  evaluation.stop


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
    teacher =   request.user.teacher
    request.session["group_id"] = group.id   

    relationships = Relationship.objects.filter(parcours__teacher = teacher).exclude(date_limit = None) 

    context = {  'group': group, 'relationships' : relationships , 'teacher' : teacher  }

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


