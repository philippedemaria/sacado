from django.urls import path, re_path
from socle.views import *
 

urlpatterns = [
 
 
 
    path('knowledges', list_knowledges, name='knowledges'),
    path('create_knowledge', create_knowledge, name='create_knowledge'),
    path('create_multi_knowledge', create_multi_knowledge, name='create_multi_knowledge'),
    path('update_knowledge/<int:id>/', update_knowledge, name='update_knowledge'),
    path('delete_knowledge/<int:id>/', delete_knowledge, name='delete_knowledge'),


    path('skills', list_skills, name='skills'),
    path('create_multi_skill', create_multi_skill, name='create_multi_skill'),
    path('update_skill/<int:id>/', update_skill, name='update_skill'),
    path('delete_skill/<int:id>/', delete_skill, name='delete_skill'),

 
    path('themes', list_themes, name='themes'),
    path('create_theme', create_theme, name='create_theme'),
    path('update_theme/<int:id>/', update_theme, name='update_theme'),
    path('delete_theme/<int:id>/', delete_theme, name='delete_theme'),

    path('levels', list_levels, name='levels'),
    path('create_level', create_level, name='create_level'),
    path('update_level/<int:id>/', update_level, name='update_level'),
    path('delete_level/<int:id>/', delete_level, name='delete_level'),


    path('waitings', list_waitings, name='waitings'),
    path('create_waiting', create_waiting, name='create_waiting'),
    path('update_waiting/<int:id>/', update_waiting, name='update_waiting'),
    path('delete_waiting/<int:id>/', delete_waiting, name='delete_waiting'),
    path('create_multi_waiting', create_multi_waiting, name='create_multi_waiting'),
    path('association_knowledge/waitings/', association_knowledge, name='association_knowledge'),

 
    path('ajax/chargewaitings', ajax_chargewaitings, name='ajax_chargewaitings'),

 
]
