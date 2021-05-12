import html
import random
import re
import csv
import pytz
from datetime import datetime 
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import  redirect
from school.models import Stage

from operator import attrgetter
from django.core.mail import send_mail 


def sending_mail(ob , m , a ,r) :
    try : 
        send_mail(ob, m, a, r)
    except :
        pass


def time_zone_user(user):
    try :
        if user.time_zone :
            time_zome = user.time_zone
            timezone.activate(pytz.timezone(time_zome))
            today = timezone.localtime(timezone.now())
        else:
            today = timezone.now()
    except :
        today = timezone.now()

    return today


 
def attribute_all_documents_to_student(parcourses,student):
    """  assigner les documents et renvoie Vrai ou Faux suivant l'attribution """
    try :
        for p in parcourses:
            p.students.add(student)

            relationships = p.parcours_relationship.all()
            for r in relationships:
                r.students.add(student)

            customexercises = p.parcours_customexercises.all()
            for c in customexercises:
                c.students.add(student)

            courses = p.course.all()
            for course in courses:
                course.students.add(student)

        test = True
    except :
        test = False
    return test



def cleanhtml(raw_html): #nettoie le code des balises HTML
    cleantext = re.sub('<.*?>', '', raw_html)
    cleantext = re.sub('\n', '', cleantext)
    return cleantext

def unescape_html(string):
    '''HTML entity decode'''
    string = html.unescape(string)
    return string


def escape_chevron(string):
    '''HTML entity decode'''
    string = string.replace("<","&lt")
    string = string.replace(">","&gt")  
    return string



def cleantext(raw_html):
    """Renvoie à la ligne pour es paragraphe et les listes"""
    raw_less_p = raw_html.split('<p>')

    for rp in raw_less_p :
        r_less_li = rp.split('<li>')

        for rli in r_less_li :
            r_less_li = re.sub('<.*?>', '', rli)

        rp = re.sub('<.*?>', '', rp)

    return raw_less_p


def dt_naive_to_timezone(naive_date,timezone_user):

    try :
        naive_dt = datetime.combine(naive_date, datetime.min.time())
        tz = pytz.timezone(timezone_user)
        utc_dt = tz.localize(naive_dt, is_dst=None).astimezone(pytz.utc)
    except :
        naive_dt = datetime.combine(naive_date, datetime.min.time())
        tz = pytz.timezone("Europe/Paris")
        utc_dt = tz.localize(naive_dt, is_dst=None).astimezone(pytz.utc)        
    return utc_dt
 


def authorizing_access(teacher ,parcours_or_group, sharing_group): #sharing_group est un booléen

    try : 
        if  teacher == parcours_or_group.teacher or  sharing_group :
            return True
        else :
            return False
    except : 
            return False


def authorizing_access_student(student , parcours_or_group): 

    try :
        if student in parcours_or_group.students.all() :
            return True
        else :
            return False
    except : 
            return False



def group_has_parcourses(group,is_evaluation ,is_archive ):
    pses_tab = []

    for s in group.students.all() :
        pses = s.students_to_parcours.filter(is_evaluation=is_evaluation,is_archive=is_archive)
        for p in pses :
            if p not in  pses_tab :
                pses_tab.append(p)
 
    return pses_tab


def get_level_by_point(student, point):
    point = int(point)
    if student.user.school :
        school = student.user.school
        stage = Stage.objects.get(school = school)

        if point > stage.up :
            level = 4
        elif point > stage.medium :
            level = 3
        elif point > stage.low :
            level = 2
        else   :
            level = 1
 
    else : 
        stage = { "low" : 50 ,  "medium" : 70 ,  "up" : 85  }

        if point > stage["up"]  :
            level = 4
        elif point > stage["medium"]  :
            level = 3
        elif point > stage["low"]  :
            level = 2
        else :
            level = 1
    return level


def split_paragraph(paragraph,coupe) :

    name  = ""
    longueur = 0
    words = paragraph.split(" ")
    for word in words:
        if longueur + 1 + len(word) > coupe:
            name += "\n" + word
            longueur = 0
        else:
            name += " " + word
            longueur += len(word)

    return name 



def increment_chrono( obj , pattern , forme , flag  ):
    """ On incrémente le chrono selon le chrono qui arrive """
    if forme :
        last_accountings = obj.objects.filter(chrono__contains = pattern).order_by("date")
        if last_accountings.count() == 0 :
            new = "01"
        else :
            last_accounting = last_accountings.last()
            chrono = last_accounting.chrono.split("-")

            new = int(chrono[2])+1
            if new < 10 :
                new = "0" + str(new)
            else :
                new = str(new)

        ch = "F" +  str(pattern) + "-" + new
        if flag :
            ch = str(pattern) + "-" + new
        else : 
            if forme == "AVOIR" :
                ch = "A" + str(pattern) + "-" + new
            elif forme == "DEVIS" :
                ch = "D" +  str(pattern) + "-" + new
    else :
        ch = ""
 
    return ch



def create_chrono(obj,forme):

    today = datetime.now().strftime("%Y-%m")
    this_chrono = increment_chrono( obj , today , forme , False )     
    return this_chrono

 

def update_chrono(obj, accounting,forme):

    this_chrono = accounting.chrono
    if forme :
        if this_chrono[0] != forme[0] :
            today = datetime.now().strftime("%Y-%m")
            new_pattern = str(forme[0]) + str(today)
            this_chrono = increment_chrono( obj ,   new_pattern ,  forme , True )  

    return this_chrono