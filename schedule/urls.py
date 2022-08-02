from django.urls import path 
from django.views.generic import TemplateView
from schedule.views import *
from django.views.decorators.csrf import csrf_exempt 


urlpatterns = [
    path('', calendar_initialize, name='calendar_initialize'),
    path('events_json', events_json, name='events_json'),

    path('schedule_task_group/<int:id>/', schedule_task_group, name='schedule_task_group'),
    path('events_json_group', events_json_group, name='events_json_group'),
   
    
 ]