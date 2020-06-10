
from django.urls import path, re_path
from .views import *

urlpatterns = [


    path('', list_schools, name='schools'),
    path('new', create_school, name='create_school'),
    path('update/<int:id>/', update_school, name='update_school'),
    path('delete/<int:id>/', delete_school, name='delete_school'),

    path('countries', list_countries, name='countries'),
    path('new_country', create_country , name='create_country'),
    path('update_country/<int:id>/', update_country, name='update_country'),
    path('delete_country/<int:id>/', delete_country, name='delete_country'),


    path('teachers', school_teachers, name='school_teachers'),
    path('students', school_students , name='school_students'),
    path('groups', school_groups, name='school_groups'),
 

    path('csv_teachers', csv_teachers, name='csv_teachers'),
    path('csv_students', csv_students , name='csv_students'),
    path('csv_groups', csv_groups, name='csv_groups'),
]
