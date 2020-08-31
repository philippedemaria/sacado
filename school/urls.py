
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
    

    path('new_student/<slug:slug>', new_student , name='new_student'),

    path('new_group', new_group , name='new_group'),
    path('update_group_school/<int:id>', update_group_school , name='update_group_school'),
    path('new_group_many', new_group_many, name='new_group_many'),

    path('send_account/<int:id>', send_account, name='send_account'),
    path('pdf_account/<int:id>', pdf_account, name='pdf_account'),    

    path('delete_student_group/<int:id>/<int:ids>', delete_student_group , name='delete_student_group'),
    path('delete_all_students_group/<int:id>', delete_all_students_group , name='delete_all_students_group'),
    path('delete_school_students', delete_school_students , name='delete_school_students'),
    path('delete_selected_students', delete_selected_students , name='delete_selected_students'),

    path('get_school_students', get_school_students , name='get_school_students'),
    path('manage_stage', manage_stage, name='manage_stage'),

]
