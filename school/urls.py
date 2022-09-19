
from django.urls import path, re_path
from .views import *

urlpatterns = [


    path('', list_schools, name='schools'),
    path('new', create_school, name='create_school'),
    path('update/<int:id>', update_school, name='update_school'),
    path('delete/<int:id>', delete_school, name='delete_school'),

    path('countries', list_countries, name='countries'),
    path('new_country', create_country , name='create_country'),
    path('update_country/<int:id>', update_country, name='update_country'),
    path('delete_country/<int:id>', delete_country, name='delete_country'),

    path('manager_teachers', manager_teachers, name='manager_teachers'),

    path('teachers', school_teachers, name='school_teachers'),
    path('students', school_students , name='school_students'),
    path('groups', school_groups, name='school_groups'),
    path('level_groups', school_level_groups, name='school_level_groups'),
    
    path('get_the_teacher_profile/<int:idt>', get_the_teacher_profile, name='get_the_teacher_profile'),
    path('get_reverse_the_teacher_profile', get_reverse_the_teacher_profile, name='get_reverse_the_teacher_profile'),


    path('get_school', get_school, name='get_school'),
    path('school_accounting', school_accounting, name='school_accounting'),
    path('get_first_adhesion', get_first_adhesion, name='get_first_adhesion'),

    path('print_bill_school/<int:a_id>', print_bill_school, name='print_bill_school'),  

    path('new_student/<slug:slug>', new_student , name='new_student'),
    path('create_new_student', create_new_student , name='create_new_student'),

    
    path('new_student_list/<slug:slug>', new_student_list , name='new_student_list'),
    path('push_student_group', push_student_group , name='push_student_group'),

    path('new_group', new_group , name='new_group'),
    path('update_group_school/<int:id>', update_group_school , name='update_group_school'),
    path('new_group_many', new_group_many, name='new_group_many'),

    path('send_account/<int:id>', send_account, name='send_account'),
    path('pdf_account/<int:id>', pdf_account, name='pdf_account'),   


    path('group_to_teacher',  group_to_teacher, name='group_to_teacher'),
    path('csv_full_group', csv_full_group, name='csv_full_group'), 

    path('delete_student_group/<int:id>/<int:ids>', delete_student_group , name='delete_student_group'),
    path('delete_all_students_group/<int:id>', delete_all_students_group , name='delete_all_students_group'),
    path('delete_school_students', delete_school_students , name='delete_school_students'),
    path('delete_selected_students', delete_selected_students , name='delete_selected_students'),

    path('delete_school_group_and_students', delete_school_group_and_students , name='delete_school_group_and_students'),



    path('get_school_students', get_school_students , name='get_school_students'),
    path('manage_stage', manage_stage, name='manage_stage'),
    path('choose_managing_school', choose_managing_school, name='choose_managing_school'), # choix du mode d'administration de l'établissement

    path('renew_school_adhesion', renew_school_adhesion , name='renew_school_adhesion'), 
    path('delete_renewal_school_adhesion', delete_renewal_school_adhesion, name='delete_renewal_school_adhesion'), 

    path('ajax_subject_teacher', ajax_subject_teacher, name='ajax_subject_teacher'),
    path('ajax_get_this_school_in_session', ajax_get_this_school_in_session, name='ajax_get_this_school_in_session'),

    ##### export from a school
    path('export_csv_all_students_school', export_csv_all_students_school, name='export_csv_all_students_school'),
    path('export_pdf_all_students_school', export_pdf_all_students_school, name='export_pdf_all_students_school'),
    path('reset_all_students_school', reset_all_students_school, name='reset_all_students_school'),
    path('reset_all_groups_school', reset_all_groups_school, name='reset_all_groups_school'),

    path('register_school_new', register_school_new, name='register_school_new'),

    path('chargeschools', chargeschools, name='chargeschools'),

    path('ask_school_adhesion', ask_school_adhesion, name='ask_school_adhesion'),
    #path('csv_new_school', csv_new_school, name='csv_new_school'),
    # Enregistrement d'un enseignant avec son enseignant
    path('ajax_charge_town'  , ajax_charge_town, name='ajax_charge_town'),
    path('ajax_charge_school', ajax_charge_school, name='ajax_charge_school'),
    path('ajax_charge_school_by_rne', ajax_charge_school_by_rne, name='ajax_charge_school_by_rne'),



]
