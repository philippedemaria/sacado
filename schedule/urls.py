from django.urls import path 
from django.views.generic import TemplateView
from schedule.views import *
from django.views.decorators.csrf import csrf_exempt 


urlpatterns = [
    path('', calendar_initialize, name='calendar_initialize'),
    path('events_json', events_json, name='events_json'),

    path('schedule_task_group/<int:id>/', schedule_task_group, name='schedule_task_group'),
    path('events_json_group', events_json_group, name='events_json_group'),
     
    path('create_calendar', create_calendar, name='create_calendar'),
    path('update_calendar/<int:id>/', update_calendar, name='update_calendar'),
    path('delete_calendar/<int:id>/', delete_calendar, name='delete_calendar'),
    path('create_event', create_event, name='create_event'),
    path('update_event/<int:id>/', csrf_exempt(update_event), name='update_event'),
    path('show_event', show_event, name='show_event'),
    path('delete_event/<int:id>/', delete_event, name='delete_event'), 
    path('shift_event', csrf_exempt(shift_event), name='shift_event'), 
    path('calendar_show/<int:id>/', calendar_show, name='calendar_show'),
    path('events_show/<int:id>/', events_show, name='events_show'),

    path('add_automaticly_update', add_automaticly_update, name='add_automaticly_update'), 

    path('delete_content_from_event/<int:id>/', delete_content_from_event, name='delete_content_from_event'), 
    
 ]