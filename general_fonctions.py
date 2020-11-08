import html
import random
import re
import csv
import pytz
from datetime import datetime 
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import  redirect

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
 



def cleanhtml(raw_html): #nettoie le code des balises HTML
    cleantext = re.sub('<.*?>', '', raw_html)
    cleantext = re.sub('\n', '', cleantext)
    return cleantext


def unescape_html(string):
    '''HTML entity decode'''
    string = html.unescape(string)
    return string

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