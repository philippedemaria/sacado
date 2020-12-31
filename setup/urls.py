
from django.urls import path, re_path
from .views import *

urlpatterns = [

    re_path(r'^$', index, name='index'),
    re_path('get_cookie', get_cookie , name='get_cookie'),


    re_path('send_message', send_message, name='send_message'),

    path('ajax/change_color_account', ajax_changecoloraccount , name='ajax_changecoloraccount'), 
    path('admin_tdb', admin_tdb, name='admin_tdb'),  

    path('gestion_files', gestion_files, name='gestion_files'),



    path('student_to_association__123526', student_to_association, name='student_to_association'),     
    path('choice_menu__123526/<slug:name>', choice_menu, name='choice_menu'), 
    path('details_of_adhesion__123526', details_of_adhesion, name='details_of_adhesion'), 
    path('commit_adhesion__123526', commit_adhesion, name='commit_adhesion'), 
    path('save_adhesion__123526', save_adhesion, name='save_adhesion'), 
    path('adhesions__123526', adhesions, name='adhesions'), 

    
    path('delete_adhesion__123526', delete_adhesion, name='delete_adhesion'), 

    path('ajax_remboursement__123526', ajax_remboursement, name='ajax_remboursement'),    
]
 