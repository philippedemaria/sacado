from django.urls import path 
from django.views.generic import TemplateView
from lesson.views import *
from django.views.decorators.csrf import csrf_exempt 


urlpatterns = [

    path('events_json', events_json, name='events_json'), 
    path('create_event', create_event, name='create_event'),
    path('update_event/<int:id>/', csrf_exempt(update_event), name='update_event'),
    path('show_event', show_event, name='show_event'),
    path('delete_event/<int:id>/', delete_event, name='delete_event'), 
    path('shift_event', csrf_exempt(shift_event), name='shift_event'), 
    path('calendar_show/<int:id>', calendar_show, name='calendar_show'),
 

 
 ]