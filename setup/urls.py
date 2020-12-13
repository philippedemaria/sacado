
from django.urls import path, re_path
from .views import *

urlpatterns = [

    re_path(r'^$', index, name='index'),

    re_path('get_cookie', get_cookie , name='get_cookie'),


    re_path('send_message', send_message, name='send_message'),

    path('ajax/change_color_account', ajax_changecoloraccount , name='ajax_changecoloraccount'), 
    path('admin_tdb', admin_tdb, name='admin_tdb'),  

    path('gestion_files', gestion_files, name='gestion_files'),  


    path('student_to_association', student_to_association, name='student_to_association'),     


    path('choice_menu/<slug:name>', choice_menu, name='choice_menu'), 



]
