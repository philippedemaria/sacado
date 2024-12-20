
from django.urls import path, re_path
from .views import *

urlpatterns = [


    ############################################################################################
    #######  INSTALLER SACADO
    ############################################################################################
    path('all_set_up_sacado', all_set_up_sacado, name='all_set_up_sacado'),
    ############################################################################################
    ############################################################################################



    path('dashboard/<int:id>', dashboard_group, name='dashboard_group'),

    path('', list_groups, name='groups'),
    path('new', create_group, name='create_group'),
    path('update/<int:id>/', update_group, name='update_group'),
    path('delete/<int:id>/', delete_group, name='delete_group'),
    path('delete_group_and_his_documents/<int:id>/', delete_group_and_his_documents, name='delete_group_and_his_documents'),
    path('insert_students_to_this_group/<int:id>/', insert_students_to_this_group, name='insert_students_to_this_group'),
    
    path('ajax_group_sorter', ajax_group_sorter, name='ajax_group_sorter'),

    path('delete_all_groups', delete_all_groups , name='delete_all_groups'),

    path('get_this_group/<int:id>/', get_this_group, name='get_this_group'),
    path('get_out_this_group/<int:id>/', get_out_this_group, name='get_out_this_group'),  


    path('show/<int:id>/', show_group, name='show_group'), 
    path('result/<int:id>/', result_group, name='result_group'),
    path('result_group_exercise/<int:id>/', result_group_exercise, name='result_group_exercise'),
    path('result_group_skill/<int:id>/', result_group_skill, name='result_group_skill'),
    path('result_group_waiting/<int:id>/', result_group_waiting, name='result_group_waiting'),

    
    path('stats/<int:id>/', stat_group, name='stat_group'),
    path('print_statistiques/<int:group_id>/<int:student_id>/', print_statistiques, name='print_statistiques'),
    
    path('print_monthly_statistiques', print_monthly_statistiques, name='print_monthly_statistiques'),

    path('print_inscription_link/<int:id>', print_inscription_link, name='print_inscription_link'),
    path('print_ids/<int:id>/', print_ids, name='print_ids'),
    path('print_list_ids/<int:id>/', print_list_ids, name='print_list_ids'),
    path('print_list_tableur_ids/<int:id>/', print_list_tableur_ids, name='print_list_tableur_ids'),
    path('print_school_ids', print_school_ids, name='print_school_ids'),

    path('task_group/<int:id>/', task_group, name='task_group'),

    path('schedule_task_group/<int:id>/', schedule_task_group, name='schedule_task_group'),


    path('group_theme/<int:id>/<int:idt>/', result_group_theme, name='result_group_theme'),

    path('group_theme_exercise/<int:id>/<int:idt>/', result_group_theme_exercise, name='result_group_theme_exercise'),
    path('associate_exercise_by_parcours/<int:id>/<int:idt>/',  associate_exercise_by_parcours, name='associate_exercise_by_parcours'),

    path('ajax/student_select_to_school',  student_select_to_school, name='student_select_to_school'),
    path('ajax/student_remove_from_school',  student_remove_from_school, name='student_remove_from_school'),
    path('ajax/chargelisting', chargelisting, name='chargelisting'),
    path('ajax/chargelistgroup', chargelistgroup, name='chargelistgroup'),

    path('ajax_delete_student_profiles', ajax_delete_student_profiles, name='ajax_delete_student_profiles'),
    path('ajax_choose_parcours',  ajax_choose_parcours, name='ajax_choose_parcours'), 
    path('ajax/select_exercise_by_knowledge',  select_exercise_by_knowledge, name='select_exercise_by_knowledge'),

    path('aggregate_group',  aggregate_group, name='aggregate_group'), 

    path('export_skills',  export_skills, name='export_skills'), 
    path('envoieStatsEnMasse',envoieStatsEnMasse, name="envoieStatsEnMasse"),

    path('<slug:slug>', enroll , name='enroll'),



    path('book_bilan_group/<int:idg>', book_bilan_group , name='book_bilan_group'),


    path('homeless_group/<int:id>', homeless_group, name='homeless_group'),
    path('ajax_add_homeworkless/', ajax_add_homeworkless, name='ajax_add_homeworkless'),
    path('ajax_add_toolless/', ajax_add_toolless, name='ajax_add_toolless'),
    path('ajax_remove_homeworkless/', ajax_remove_homeworkless , name='ajax_remove_homeworkless'),
    path('ajax_remove_toolless/', ajax_remove_toolless, name='ajax_remove_toolless'),
 
    path('ajax_remove_homeworkless_mini/', ajax_remove_homeworkless_mini , name='ajax_remove_homeworkless_mini'),
    path('ajax_remove_toolless_mini/', ajax_remove_toolless_mini, name='ajax_remove_toolless_mini'),


]
 