from django.urls import path 
from django.views.generic import TemplateView
from schedule.views import *
from django.views.decorators.csrf import csrf_exempt 


urlpatterns = [
    path('', calendar_initialize, name='calendar_initialize'),
    path('events_json', events_json_, name='events_json_'),

    path('schedule_task_group/<int:id>/', schedule_task_group, name='schedule_task_group'),
    path('events_json_group', events_json_group, name='events_json_group'),
   
    path('config_edt/<int:ide>', config_edt, name='config_edt'), 
    path('my_edt', my_edt, name='my_edt'),  
    path('my_edt_group_attribution', my_edt_group_attribution, name='my_edt_group_attribution'),  

    

    path('progressions', progressions, name='progressions'),
    path('config_progression', config_progression, name='config_progression'),


 ]