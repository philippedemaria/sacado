from django.urls import path, re_path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [


    path('parcours', list_parcours, name='parcours'),
    path('evaluations', list_evaluations, name='evaluations'),

    path('parcours_create', create_parcours, name='create_parcours'),
    path('parcours_create_evaluation', create_evaluation, name='create_evaluation'),
    path('parcours_evaluation_update/<int:id>/<int:idg>/', update_evaluation, name='update_evaluation'),

    path('parcours_update/<int:id>/<int:idg>/', update_parcours, name='update_parcours'),
    path('parcours_delete/<int:id>/<int:idg>/', delete_parcours, name='delete_parcours'),  
    path('parcours_show/<int:id>/', show_parcours, name='show_parcours'), 
    path('parcours_tasks_and_publishes/<int:id>/', parcours_tasks_and_publishes, name='parcours_tasks_and_publishes'), # gestion des taches
    path('show_parcours_visual/<int:id>/', show_parcours_visual, name='show_parcours_visual'), 


    # Résultats d'un parcours
    path('parcours_result/<int:id>/', result_parcours, name='result_parcours'), 
    path('parcours_result_theme/<int:id>/<int:idt>/', result_parcours_theme, name='result_parcours_theme'),  # Je ne sais pas si cette route est utilisée ?????
    path('parcours_result_knowledge/<int:id>/', result_parcours_knowledge, name='result_parcours_knowledge'), 
    path('parcours_stat/<int:id>/', stat_parcours, name='stat_parcours'), 
    path('parcours_detail_task/<int:id>/<int:s>/', detail_task_parcours, name='detail_task_parcours'), #modif idp en id pour la sécurité
    path('parcours_exercises/<int:id>/', parcours_exercises, name='parcours_exercises'),  # student_list_exercises
    path('parcourses_all/', all_parcourses, name='all_parcourses'),
    path('parcours_clone/<int:id>/', clone_parcours, name='clone_parcours'),
    path('parcours_group/<int:id>/', list_parcours_group, name='list_parcours_group'), # parcours d'un groupe

    path('parcours_peuplate/<int:id>/', peuplate_parcours, name='peuplate_parcours'),
    path('parcours_individualise/<int:id>/', individualise_parcours, name='individualise_parcours'),#modif idp en id pour la sécurité
    path('ajax_populate', ajax_populate, name='ajax_populate'),
    path('ajax_individualise', ajax_individualise , name='ajax_individualise'),

    path('result_parcours_exercise_students/<int:id>/', result_parcours_exercise_students, name='result_parcours_exercise_students'),#modif idp en id pour la sécurité

    #####################################  Modifie les relations par parcours et exercices  ##############################################################  
    path('<int:idp>/<int:ide>/', execute_exercise, name='execute_exercise'),#modif idp en id pour la sécurité 
    path('delete_evaluation/<int:id>/', delete_evaluation, name='delete_evaluation'), 
    ######################################################################################################################################################

    path('associate_parcours/<int:id>/', associate_parcours, name='associate_parcours'),  # id est l'id du groupe auquel le parcours est associé
 
    path('parcours_aggregate',  aggregate_parcours, name='aggregate_parcours'), 
    path('ajax_parcoursinfo/', ajax_parcoursinfo, name='ajax_parcoursinfo'),    
    path('exercises', list_exercises, name='exercises'),
    
    path('ajax/chargethemes', chargethemes, name='chargethemes'),

    path('admin_supportfiles', admin_list_supportfiles, name='admin_supportfiles'),
    path('admin_associations', admin_list_associations, name='admin_associations'),
    path('ajax_update_association', ajax_update_association, name='ajax_update_association'),
    path('create_supportfile', create_supportfile, name='create_supportfile'),
    path('admin/<int:id>', create_supportfile_knowledge, name='create_supportfile_knowledge'),
    path('update_supportfile/<int:id>/', update_supportfile, name='update_supportfile'),
    path('delete_supportfile/<int:id>/', delete_supportfile, name='delete_supportfile'), 
    path('show_this_supportfile/<int:id>/', show_this_supportfile, name='show_this_supportfile'),  #from dashboard 

    path('create_exercise/<int:supportfile_id>/', create_exercise, name='create_exercise'), 


    path('show_this_exercise/<int:id>/', show_this_exercise, name='show_this_exercise'),  #from dashboard 

    path('show_exercise/<int:id>/', show_exercise, name='show_exercise'),       #from index  
    path('exercises_level/<int:id>/', exercises_level , name='exercises_level'), 
    path('content_is_done/<int:id>/', content_is_done , name='content_is_done'), 
    path('relation_is_done/<int:id>/', relation_is_done , name='relation_is_done'), 

    path('delete_relationship/<int:idr>/', delete_relationship, name='delete_relationship'),
    path('delete_relationship_by_individualise/<int:idr>/<int:id>/', delete_relationship_by_individualise, name='delete_relationship_by_individualise'),#modif idp en id pour la sécurité

    path('create_remediation/<int:idr>/', create_remediation, name='create_remediation'),
    path('update_remediation/<int:idr>/<int:id>/', update_remediation, name='update_remediation'),
    path('delete_remediation/<int:id>/', delete_remediation, name='delete_remediation'),  
 
    path('export_knowledge/<int:idp>/', export_knowledge, name='export_knowledge'),  
    path('export_note/<int:idg>/<int:idp>/', export_note, name='export_note'),  


    path('detail_task/<int:id>/<int:s>/', detail_task, name='detail_task'), #modif idg en id pour la sécurité
    path('tasks', all_my_tasks, name='all_my_tasks'),


    #################################### Les cours dans les parcours ###########################################

    path('', list_courses, name='courses'),
    path('create_course/<int:idc>/<int:id>', create_course, name='create_course'),
    path('update_course/<int:idc>/<int:id>', update_course, name='update_course'),
    path('delete_course/<int:idc>/<int:id>', delete_course, name='delete_course'),
    path('show_course/<int:idc>/<int:id>', show_course, name='show_course'),

    ############################################################################################################  




 
    path('advises', advises, name='advises'),   

    path('ajax/exercise_error', ajax_exercise_error, name='exercise_error'),
    path('ajax_detail_parcours/', ajax_detail_parcours , name='ajax_detail_parcours'),
    path('add_exercice_in_a_parcours', add_exercice_in_a_parcours, name='add_exercice_in_a_parcours'),  
    path('show_remediation/<int:id>/', show_remediation, name='show_remediation'),       #from index   
    path('ajax_search_exercise', ajax_search_exercise, name='ajax_search_exercise'),
    path('store_the_score_relation_ajax/', store_the_score_relation_ajax, name='store_the_score_relation_ajax'),
    path('store_the_score_ajax/', store_the_score_ajax, name='store_the_score_ajax'),

    path('ajax/create_title_parcours', ajax_create_title_parcours, name='ajax_create_title_parcours'),
    path('ajax/erase_title', ajax_erase_title, name='ajax_erase_title'),


    path('parcours_show_student/<int:id>/', show_parcours_student, name='show_parcours_student'),     
    
    path('ajax_search_exercise', ajax_search_exercise, name='ajax_search_exercise'),
    path('ajax_knowledge_exercice', ajax_knowledge_exercice, name='ajax_knowledge_exercice'),
    path('ajax_theme_exercice', ajax_theme_exercice, name='ajax_theme_exercice'),
    path('ajax_level_exercise', ajax_level_exercise, name='ajax_level_exercise'),
    path('ajax/sort_exercise', ajax_sort_exercice, name='ajax_sort_exercice'), 
    path('ajax/publish', ajax_publish, name='ajax_publish'),  
    path('ajax/publish_parcours', ajax_publish_parcours, name='ajax_publish_parcours'),  
    path('ajax/dates', ajax_dates, name='ajax_dates'), 
    path('ajax/skills', ajax_skills, name='ajax_skills'), 
    path('ajax/remediation', ajax_remediation, name='ajax_remediation'),  
    path('ajax/remediation_viewer', ajax_remediation_viewer , name='ajax_remediation_viewer'),
    path('json_create_remediation/<int:idr>', json_create_remediation, name='json_create_remediation'),  # création via la modal sans rechargement de la page
    path('json_delete_remediation/<int:id>', json_delete_remediation, name='json_delete_remediation'),   # suppression via la modal sans rechargement de la page    


    path('ajax/constraint_create', ajax_create_constraint, name='ajax_create_constraint'),
    path('ajax/constraint_delete', ajax_delete_constraint, name='ajax_delete_constraint'), 
    path('ajax/infoExo', ajax_infoExo, name='ajax_infoExo'),
 ]
