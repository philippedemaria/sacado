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
    path('my_edt_delete', my_edt_delete, name='my_edt_delete'),
    

    path('progressions', progressions, name='progressions'),
    path('progression/<int:idg>', progression_group, name='progression_group'),     
    path('config_progression', config_progression, name='config_progression'),
    path('insert_content_into_slot/<int:idg>', insert_content_into_slot, name='insert_content_into_slot'),

    path('clear_the_slot/<int:ids>/<int:idg>', clear_the_slot, name='clear_the_slot'),

    path('print_progression/<int:idg>', print_progression, name='print_progression'),  
    path('get_progression/<int:idg>', get_progression, name='get_progression'),  
 ]