import html
import random
import re
import csv
import pytz
from datetime import datetime 
from django.utils import timezone


def time_zone_user(user):
    if user.time_zone :
        time_zome = user.time_zone
        timezone.activate(pytz.timezone(time_zome))
        today = timezone.localtime(timezone.now())
    else:
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
    naive_dt = datetime.combine(naive_date, datetime.min.time())
    tz = pytz.timezone(timezone_user)
    utc_dt = tz.localize(naive_dt, is_dst=None).astimezone(pytz.utc)
    return utc_dt
 
