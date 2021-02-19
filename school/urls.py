
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


    path('teachers', school_teachers, name='school_teachers'),
    path('students', school_students , name='school_students'),
    path('groups', school_groups, name='school_groups'),
    path('level_groups', school_level_groups, name='school_level_groups'),
    

    path('get_school', get_school, name='get_school'),


    path('new_student/<slug:slug>', new_student , name='new_student'),
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

    path('get_school_students', get_school_students , name='get_school_students'),
    path('manage_stage', manage_stage, name='manage_stage'),


    path('ajax_subject_teacher', ajax_subject_teacher, name='ajax_subject_teacher'),
    path('ajax_get_this_school_in_session', ajax_get_this_school_in_session, name='ajax_get_this_school_in_session'),

]
