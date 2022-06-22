
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

    ############################################################################################
    #######  Interface Python
    ############################################################################################
    path('python', python, name='python'),

    ############################################################################################
    #######  GAR
    ############################################################################################
    path('sacado', ressource_sacado , name='ressource_sacado'),

    path('saml/SingleLogout', singleLogoutGar , name='saml/SingleLogout'),


    path('rgpd', rgpd, name='rgpd'), 
    path('gar_rgpd', gar_rgpd, name='gar_rgpd'), 
    path('cgv', cgv, name='cgv'), 
    path('cgu', cgu, name='cgu'), 
    path('mentions', mentions, name='mentions'), 
    path('mentions_academy', mentions_academy, name='mentions_academy'), 

    ############################################################################################
    #######  SACADO Académie
    ############################################################################################
    path('academy', academy, name='academy'), 
    path('student_to_association', student_to_association, name='student_to_association'),     
    path('choice_menu/<slug:name>', choice_menu, name='choice_menu'), 
    path('details_of_adhesion', details_of_adhesion, name='details_of_adhesion'), 
    path('commit_adhesion', commit_adhesion, name='commit_adhesion'), 
    path('save_adhesion', save_adhesion, name='save_adhesion'), 
    path('adhesions_academy', adhesions_academy, name='adhesions_academy'), 
    path('delete_adhesion', delete_adhesion, name='delete_adhesion'), 
    path('ajax_remboursement', ajax_remboursement, name='ajax_remboursement'),
    path('add_adhesion', add_adhesion, name='add_adhesion'),
    path('save_renewal_adhesion', save_renewal_adhesion, name='save_renewal_adhesion'),

    path('accept_renewal_adhesion', accept_renewal_adhesion, name='accept_renewal_adhesion'),

    path('renewal_adhesion', renewal_adhesion, name='renewal_adhesion'),

    path('list_exercises_academy/<int:id>', list_exercises_academy, name='academy_level'),

    path('logout_academy', logout_academy , name='logout_academy'), 

    path('renewal_adhesion', renewal_adhesion, name='renewal_adhesion'),
    ############################################################################################
    #######  SACADO Cahier de vacances 
    ############################################################################################

    path('play_quizz', play_quizz, name='play_quizz'), 
    path('play_quizz_login', play_quizz_login, name='play_quizz_login'), 
    path('play_quizz_start', play_quizz_start, name='play_quizz_start'), 

    path('ajax_get_subject/', ajax_get_subject, name='ajax_get_subject'),#gère les div des subjects sur la page d'accuril des exercices.

    ############################################################################################
    #######  WEBINAIRE
    ############################################################################################
    path('webinaire_list', webinaire_list, name='webinaires'), 
    path('webinaire_create', webinaire_create, name='webinaire_create'),
    path('webinaire_update/<int:id>/', webinaire_update, name='webinaire_update'),
    path('webinaire_delete/<int:id>/', webinaire_delete, name='webinaire_delete'), 
    path('webinaire_register', webinaire_register, name='webinaire_register'), 
    path('webinaire_registrar/<int:id>/<int:key>/', webinaire_registrar, name='webinaire_registrar'), 

    path('webinaire_show/<int:id>/', webinaire_show, name='webinaire_show'), 
    ############################################################################################
    #######  Tweeter
    ############################################################################################
    path('tweeters', tweeters, name='tweeters'), 
    path('tweeter_create/0', tweeter_create, name='tweeter_create'),
    path('tweeter_update/<int:id>', tweeter_update, name='tweeter_update'),
    path('tweeter_delete/<int:id>', tweeter_delete, name='tweeter_delete'), 
    path('tweeters_public', tweeters_public, name='tweeters_public'),


    path('scheduledTasks/send_reports/', send_reports ,name='send_reports'), 
    path('<slug:adresse>', all_routes , name='all_routes'), 
]


 