#################################
#### Auteur : philipe Demaria 
#### pour SACADO
#################################
from django.urls import path, re_path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    path('admin_exotexs/<int:idl>', admin_exotexs, name='admin_exotexs'),
    path('my_exotexs', my_exotexs, name='my_exotexs'),


    path('create_exotex_knowledge/<int:idk>', create_exotex_knowledge , name='create_exotex_knowledge'),
    path('exercise_exotex_update/<int:id>', update_exotex, name='update_exotex'),
    path('exercise_exotex_delete/<int:id>', delete_exotex, name='delete_exotex'), 

    # path('exercise_exotex_archive/<int:id>', archive_exotex, name='archive_exotex'),
    # path('exercise_exotex_unarchive/<int:id>', unarchive_exotex, name='unarchive_exotex'), 
    # path('exercise_exotex_show/<int:id>', show_exotex, name='show_exotex'), 

    path('bibliotexs', bibliotexs, name='bibliotexs'),
    path('my_bibliotexs', my_bibliotexs, name='my_bibliotexs'),
    path('exercise_bibliotex_create/<int:idf>', create_bibliotex , name='create_bibliotex'),
    path('exercise_bibliotex_update/<int:id>', update_bibliotex, name='update_bibliotex'),
    path('exercise_bibliotex_delete/<int:id>', delete_bibliotex, name='delete_bibliotex'), 
    path('exercise_bibliotex_peuplate/<int:id>', exercise_bibliotex_peuplate, name='exercise_bibliotex_peuplate'),
    path('exercise_bibliotex_show/<int:id>', show_bibliotex, name='show_bibliotex'),
    # path('exercise_bibliotex_archive/<int:id>', archive_bibliotex, name='archive_bibliotex'),
    # path('exercise_bibliotex_unarchive/<int:id>', unarchive_bibliotex, name='unarchive_bibliotex'), 
    path('real_time_bibliotex/<int:id>', real_time_bibliotex, name='real_time_bibliotex'),  


    path('print_exotex', print_exotex, name='print_exotex'),      
    path('print_bibliotex', print_bibliotex, name='print_bibliotex'),  

 
    path('exercise_bibliotex_individualise/<int:id>', exercise_bibliotex_individualise, name='exercise_bibliotex_individualise'), 
    path('exercise_bibliotex_results/<int:id>', exercise_bibliotex_results, name='exercise_bibliotex_results'),

    path('ajax_chargethemes', ajax_chargethemes, name='ajax_chargethemes'),
    path('ajax_level_exotex', ajax_level_exotex, name='ajax_level_exotex'),
    path('ajax_charge_groups', ajax_charge_groups, name='ajax_charge_groups'),
    path('ajax_my_bibliotexs', ajax_my_bibliotexs, name='ajax_my_bibliotexs'),
    path('ajax_set_exotex_in_bibliotex', ajax_set_exotex_in_bibliotex, name='ajax_set_exotex_in_bibliotex'),


    path('ajax_results_exotex', ajax_results_exotex, name='ajax_results_exotex'),
    path('ajax_print_exotex', ajax_print_exotex, name='ajax_print_exotex'),
    path('ajax_print_bibliotex', ajax_print_bibliotex, name='ajax_print_bibliotex'),
    path('ajax_individualise_exotex', ajax_individualise_exotex, name='ajax_individualise_exotex'),
 ]
