from django.urls import path, re_path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [


    path('parcours', list_parcours, name='parcours'),
    path('evaluations', list_evaluations, name='evaluations'),
    path('archives', list_archives, name='archives'),
    path('evaluations_archives', list_evaluations_archives, name='evaluations_archives'),

    path('parcours_create', create_parcours, name='create_parcours'),
    path('parcours_create_evaluation', create_evaluation, name='create_evaluation'),
    path('parcours_evaluation_update/<int:id>/<int:idg>/', update_evaluation, name='update_evaluation'),
    path('parcours_evaluation_show/<int:id>/', show_evaluation, name='show_evaluation'), 
 
    path('parcours_update/<int:id>/<int:idg>/', update_parcours, name='update_parcours'),
    path('parcours_delete/<int:id>/<int:idg>/', delete_parcours, name='delete_parcours'),  
    path('parcours_archive/<int:id>/<int:idg>/', archive_parcours, name='archive_parcours'),
    path('parcours_unarchive/<int:id>/<int:idg>/', unarchive_parcours, name='unarchive_parcours'), 
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


    path('remove_students_from_parcours', remove_students_from_parcours, name='remove_students_from_parcours'),


    path('parcours_peuplate_evaluation/<int:id>/', peuplate_parcours_evaluation, name='peuplate_parcours_evaluation'),

    path('parcours_stat_evaluation/<int:id>/', stat_evaluation, name='stat_evaluation'), 

    path('parcours_get_exercise_custom', ajax_parcours_get_exercise_custom, name='ajax_parcours_get_exercise_custom'),
    path('parcours_clone_exercise_custom', parcours_clone_exercise_custom, name='parcours_clone_exercise_custom'),

    path('parcours_clone_course', ajax_parcours_clone_course, name='ajax_parcours_clone_course'),
    path('parcours_shower_course', ajax_parcours_shower_course, name='ajax_parcours_shower_course'),
    path('parcours_get_course', ajax_parcours_get_course, name='ajax_parcours_get_course'),
 
    #####################################  Modifie les relations par parcours et exercices  ##############################################################  
    path('<int:idp>/<int:ide>/', execute_exercise, name='execute_exercise'),#modif idp en id pour la sécurité 
    path('delete_evaluation/<int:id>/', delete_evaluation, name='delete_evaluation'), 
    ######################################################################################################################################################

    path('associate_parcours/<int:id>/', associate_parcours, name='associate_parcours'),  # id est l'id du groupe auquel le parcours est associé
 
    path('parcours_aggregate',  aggregate_parcours, name='aggregate_parcours'), 
    path('ajax_parcoursinfo/', ajax_parcoursinfo, name='ajax_parcoursinfo'),    
    path('exercises', list_exercises, name='exercises'),
    
    path('ajax/chargethemes', ajax_chargethemes, name='ajax_chargethemes'),
    path('ajax/chargeknowledges', ajax_chargeknowledges, name='ajax_chargeknowledges'),


    path('admin_supportfiles/<int:id>', admin_list_supportfiles, name='admin_supportfiles'),
    path('admin_associations/<int:id>', admin_list_associations, name='admin_associations'),
    path('gestion_supportfiles', gestion_supportfiles, name='gestion_supportfiles'),


    
    path('ajax_update_association', ajax_update_association, name='ajax_update_association'),
    path('create_supportfile', create_supportfile, name='create_supportfile'),
    path('admin/<int:id>', create_supportfile_knowledge, name='create_supportfile_knowledge'),
    path('update_supportfile/<int:id>/', update_supportfile, name='update_supportfile'),
    path('delete_supportfile/<int:id>/', delete_supportfile, name='delete_supportfile'), 
    path('show_this_supportfile/<int:id>/', show_this_supportfile, name='show_this_supportfile'),  #from dashboard 

    path('create_exercise/<int:supportfile_id>/', create_exercise, name='create_exercise'), 
    path('correction_exercise/<int:id>/<int:idp>', correction_exercise, name='correction_exercise'),  #from details_card 

    path('show_this_exercise/<int:id>/', show_this_exercise, name='show_this_exercise'),  #from dashboard 

    path('parcours_show_write_exercise/<int:id>/', show_write_exercise, name='show_write_exercise'), 


    path('show_exercise/<int:id>/', show_exercise, name='show_exercise'),       #from index  
    path('exercises_level/<int:id>/', exercises_level , name='exercises_level'), 
    path('content_is_done/<int:id>/', content_is_done , name='content_is_done'), 
    path('relation_is_done/<int:id>/', relation_is_done , name='relation_is_done'), 

    path('delete_relationship/<int:idr>/', delete_relationship, name='delete_relationship'),
    path('delete_relationship_by_individualise/<int:idr>/<int:id>/', delete_relationship_by_individualise, name='delete_relationship_by_individualise'),#modif idp en id pour la sécurité

    path('create_remediation/<int:idr>/', create_remediation, name='create_remediation'),
    path('update_remediation/<int:idr>/<int:id>/', update_remediation, name='update_remediation'),
    path('delete_remediation/<int:id>/', delete_remediation, name='delete_remediation'),  

    ####################################### Export Pronote #####################################################
    path('export_note_custom/<int:id>/<int:idp>', export_note_custom, name='export_note_custom'),   
    path('export_knowledge/<int:idp>/', export_knowledge, name='export_knowledge'),  
    path('export_note/<int:idg>/<int:idp>/', export_note, name='export_note'),  
    path('export_skill/<int:idp>/', export_skill, name='export_skill'),  

    path('detail_task/<int:id>/<int:s>/', detail_task, name='detail_task'), #modif idp en id pour la sécurité
    path('tasks', all_my_tasks, name='all_my_tasks'),
    path('all_tasks', these_all_my_tasks, name='these_all_my_tasks'),    
    path('group_tasks/<int:id>', group_tasks, name='group_tasks'), #taches en cours du groupe
    path('group_tasks_all/<int:id>', group_tasks_all, name='group_tasks_all'), #taches du groupe
    #################################### Les cours dans les parcours ###########################################

    path('parcours_courses', list_courses, name='courses'),
    path('parcours_create_course/<int:idc>/<int:id>', create_course, name='create_course'), # id = id du parcours, idc = id du cours
    path('parcours_update_course/<int:idc>/<int:id>', update_course, name='update_course'),
    path('parcours_delete_course/<int:idc>/<int:id>', delete_course, name='delete_course'),
    path('parcours_show_course/<int:idc>/<int:id>', show_course, name='show_course'),
    path('parcours_show_course_student/<int:idc>/<int:id>', show_course_student, name='show_course_student'),
    path('course_custom_show_shared', course_custom_show_shared, name='course_custom_show_shared'),  

    ############################################################################################################  
    path('exercise_custom_show_shared', exercise_custom_show_shared, name='exercise_custom_show_shared'),  

    #################################### Mastering #############################################################

    path('parcours_create_mastering/<int:id>/', create_mastering, name='create_mastering'),
    path('parcours_mastering_delete/<int:id>/<int:idm>/', parcours_mastering_delete, name='parcours_mastering_delete'),
    path('ajax/sort_mastering', ajax_sort_mastering, name='ajax_sort_mastering'),

    path('parcours_mastering_student_show/<int:id>/', mastering_student_show, name='mastering_student_show'),
    path('ajax/mastering_modal_show', ajax_mastering_modal_show, name='ajax_mastering_modal_show'),    
    path('parcours_mastering_done', mastering_done, name='mastering_done'),    
    path('ajax_populate_mastering', ajax_populate_mastering, name='ajax_populate_mastering'),
    ############################################################################################################ 
    #################################### Mastering_custom ######################################################

    path('parcours_create_mastering_custom/<int:id>/<int:idp>', create_mastering_custom , name='create_mastering_custom'),
    path('parcours_mastering_custom_delete/<int:id>/<int:idm>/<int:idp>', parcours_mastering_custom_delete, name='parcours_mastering_custom_delete'),
    path('ajax/sort_mastering_custom', ajax_sort_mastering_custom, name='ajax_sort_mastering_custom'),

    path('parcours_mastering_student_show_custom/<int:id>/', mastering_custom_student_show, name='mastering_custom_student_show'),
    path('ajax/mastering_custom_modal_show', ajax_mastering_custom_modal_show, name='ajax_mastering_custom_modal_show'),    
    path('parcours_mastering_custom_done', mastering_custom_done, name='mastering_custom_done'),    
 

    ############################################################################################################ 
    ############################################################################################################  

    ####################################     Les demandes d'exercice  ##########################################

    path('parcours_demands', list_demands, name='demands'),
    path('parcours_create_demand', create_demand, name='create_demand'),  
    path('parcours_update_demand/<int:id>', update_demand, name='update_demand'),
    path('parcours_delete_demand/<int:id>', delete_demand, name='delete_demand'),
    path('parcours_show_demand/<int:id>', show_demand, name='show_demand'),

    ############################################################################################################  


 
    path('advises', advises, name='advises'),   

    path('ajax/exercise_error', ajax_exercise_error, name='exercise_error'),
    path('ajax_detail_parcours/', ajax_detail_parcours , name='ajax_detail_parcours'),
    path('add_exercice_in_a_parcours', add_exercice_in_a_parcours, name='add_exercice_in_a_parcours'),  
    path('show_remediation/<int:id>/', show_remediation, name='show_remediation'),       #from index   
    path('ajax_search_exercise', ajax_search_exercise, name='ajax_search_exercise'),
    path('store_the_score_relation_ajax/', store_the_score_relation_ajax, name='store_the_score_relation_ajax'),
    #path('store_the_score_ajax/', store_the_score_ajax, name='store_the_score_ajax'),
    path('ajax/demand_done', ajax_demand_done, name='ajax_demand_done'),

    path('ajax/create_title_parcours', ajax_create_title_parcours, name='ajax_create_title_parcours'),
    path('ajax/erase_title', ajax_erase_title, name='ajax_erase_title'),

    path('ajax/parcours_default', ajax_parcours_default , name='ajax_parcours_default'),
    path('get_parcours_default/', get_parcours_default , name='get_parcours_default'),

    path('ajax_is_favorite', ajax_is_favorite, name='ajax_is_favorite'),
    path('ajax/course_sorter', ajax_course_sorter, name='ajax_course_sorter'),
    path('ajax/parcours_sorter', ajax_parcours_sorter, name='ajax_parcours_sorter'),

    path('parcours_show_student/<int:id>/', show_parcours_student, name='show_parcours_student'),     
    
    path('ajax_search_exercise', ajax_search_exercise, name='ajax_search_exercise'),
    path('ajax_knowledge_exercise', ajax_knowledge_exercise, name='ajax_knowledge_exercise'),
    path('ajax_theme_exercice', ajax_theme_exercice, name='ajax_theme_exercice'),
    path('ajax_level_exercise', ajax_level_exercise, name='ajax_level_exercise'),
    path('ajax/sort_exercise', ajax_sort_exercise, name='ajax_sort_exercise'), 
    path('ajax/publish', ajax_publish, name='ajax_publish'),  
    path('ajax/publish_parcours', ajax_publish_parcours, name='ajax_publish_parcours'),  
    path('ajax/dates', ajax_dates, name='ajax_dates'), 
    path('ajax/skills', ajax_skills, name='ajax_skills'), 


    path('ajax/remediation', ajax_remediation, name='ajax_remediation'),

    path('ajax/remediation_viewer', ajax_remediation_viewer , name='ajax_remediation_viewer'),
    path('json_create_remediation/<int:idr>/<int:idp>/<int:typ>', json_create_remediation, name='json_create_remediation'),  # création via la modal sans rechargement de la page
    path('json_delete_remediation/<int:id>/<int:idp>/<int:typ>', json_delete_remediation, name='json_delete_remediation'),   # suppression via la modal sans rechargement de la page    
    path('audio_remediation', audio_remediation, name='audio_remediation'),   # suppression via la modal sans rechargement de la page 


    path('ajax/constraint_create', ajax_create_constraint, name='ajax_create_constraint'),
    path('ajax/constraint_delete', ajax_delete_constraint, name='ajax_delete_constraint'), 
    path('ajax/infoExo', ajax_infoExo, name='ajax_infoExo'),

    path('ajax/course_viewer', ajax_course_viewer, name='ajax_course_viewer'),

    # Evaluation des exercices non auto corrigé
    path('ajax_choose_student', ajax_choose_student, name='ajax_choose_student'),
    path('ajax_exercise_evaluate', ajax_exercise_evaluate, name='ajax_exercise_evaluate'),
    path('ajax_comment_all_exercise', ajax_comment_all_exercise, name='ajax_comment_all_exercise'),
    path('ajax_audio_comment_all_exercise', ajax_audio_comment_all_exercise, name='ajax_audio_comment_all_exercise'),
    path('write_exercise/<int:id>', write_exercise, name='write_exercise'), # page dans laquelle l'élève repond à l'exercice non auto-corrigé - l'id est celui de la relation.

    # page de création d'un exercice non auto-corrigé dans un parcours - l'id est celui du parcours.
    path('parcours_create_custom_exercise/<int:id>/<int:typ>', parcours_create_custom_exercise, name='parcours_create_custom_exercise'), 
    path('parcours_update_custom_exercise/<int:idcc>/<int:id>', parcours_update_custom_exercise, name='parcours_update_custom_exercise'), 
    path('parcours_delete_custom_exercise/<int:idcc>/<int:id>', parcours_delete_custom_exercise, name='parcours_delete_custom_exercise'), 
    path('parcours_show_custom_exercise/<int:id>/<int:idp>',  show_custom_exercise, name='show_custom_exercise'), # vue enseignant de l'exercice

    path('write_custom_exercise/<int:id>/<int:idp>', write_custom_exercise, name='write_custom_exercise'), 
    path('ajax_mark_evaluate', ajax_mark_evaluate, name='ajax_mark_evaluate'),
 ]
