
from django.urls import path, re_path
from .views import *

urlpatterns = [

    re_path(r'^$', index, name='index'),
    re_path('get_cookie', get_cookie , name='get_cookie'),


    re_path('send_message', send_message, name='send_message'),

    path('ajax/change_color_account', ajax_changecoloraccount , name='ajax_changecoloraccount'), 
    path('admin_tdb', admin_tdb, name='admin_tdb'),  
    path('tutos_video_sacado', tutos_video_sacado, name='tutos_video_sacado'),



    path('gestion_files', gestion_files, name='gestion_files'),

    path('school_adhesion', school_adhesion, name='school_adhesion'),
    path('ajax_get_price', ajax_get_price , name='ajax_get_price'), 
    path('payment_school_adhesion', payment_school_adhesion , name='payment_school_adhesion'), 
    path('delete_school_adhesion', delete_school_adhesion , name='delete_school_adhesion'), 
    path('print_proformat_school', print_proformat_school, name='print_proformat_school'),  


    path('iban_asking/<int:school_id>/<int:user_id>', iban_asking, name='iban_asking'),  


    path('res/ressource/sacado', ressource_sacado , name='ressource_sacado'),

    ############################################################################################
    #######  SACADO Cahier de vacances payant
    ############################################################################################
    path('student_to_association', student_to_association, name='student_to_association'),     
    path('choice_menu/<slug:name>', choice_menu, name='choice_menu'), 
    path('details_of_adhesion', details_of_adhesion, name='details_of_adhesion'), 
    path('commit_adhesion', commit_adhesion, name='commit_adhesion'), 
    path('save_adhesion', save_adhesion, name='save_adhesion'), 
    path('adhesions', adhesions, name='adhesions'), 
    path('delete_adhesion', delete_adhesion, name='delete_adhesion'), 
    path('ajax_remboursement', ajax_remboursement, name='ajax_remboursement'), 
    ############################################################################################
    #######  SACADO Cahier de vacances 
    ############################################################################################

    path('play_quizz', play_quizz, name='play_quizz'), 
    path('play_quizz_login', play_quizz_login, name='play_quizz_login'), 
    path('play_quizz_start', play_quizz_start, name='play_quizz_start'), 

    path('ajax_get_subject/', ajax_get_subject, name='ajax_get_subject'),#gère les div des subjects sur la page d'accuril des exercices.
]


 