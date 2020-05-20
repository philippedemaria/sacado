
from django.urls import path, re_path
from .views import *

urlpatterns = [


    path('', list_groups, name='groups'),
    path('new', create_group, name='create_group'),
    path('update/<int:id>/', update_group, name='update_group'),
    path('delete/<int:id>/', delete_group, name='delete_group'),

    path('show/<int:id>/', show_group, name='show_group'), 
    path('result/<int:id>/', result_group, name='result_group'),
    path('result_group_exercise/<int:id>/', result_group_exercise, name='result_group_exercise'),
    path('result_group_skill/<int:id>/', result_group_skill, name='result_group_skill'),

    path('stats/<int:id>/', stat_group, name='stat_group'),
    path('print_statistiques/<int:group_id>/<int:student_id>/', print_statistiques, name='print_statistiques'),


    path('task_group/<int:id>/', task_group, name='task_group'),


    path('group_theme/<int:id>/<int:idt>/', result_group_theme, name='result_group_theme'),

    path('group_theme_exercise/<int:id>/<int:idt>/', result_group_theme_exercise, name='result_group_theme_exercise'),
    path('associate_exercise_by_parcours/<int:id>/<int:idt>/',  associate_exercise_by_parcours, name='associate_exercise_by_parcours'),


    path('ajax/chargelisting', chargelisting, name='chargelisting'),
    path('ajax/chargelistgroup', chargelistgroup, name='chargelistgroup'),

    path('ajax/select_exercise_by_knowledge',  select_exercise_by_knowledge, name='select_exercise_by_knowledge'),
    path('ajax/sending_message_student',  sending_message_student, name='sending_message_student'),    

    path('aggregate_group',  aggregate_group, name='aggregate_group'), 


    path('<slug:slug>', enroll , name='enroll'), 

]
 