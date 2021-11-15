from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('flashpacks', list_flashpacks, name='flashpacks'),
    path('my_flashpacks', list_my_flashpacks, name='my_flashpacks'),
    path('create/<int:idf>', create_flashpack , name='create_flashpack'),
    path('update/<int:id>', update_flashpack, name='update_flashpack'),
    path('delete/<int:id>', delete_flashpack, name='delete_flashpack'),
    path('show_flashpack/<int:id>', show_flashpack, name='show_flashpack'), 
    path('clone_flashpack/<int:id>', clone_flashpack, name='clone_flashpack'),
    path('my_flashpack_archives', my_flashpack_archives, name='my_flashpack_archives'),
    
    path('flashpack_peuplate/<int:id>', flashpack_peuplate, name='flashpack_peuplate'),

    path('set_flashcards_to_flashpack/<int:id>', set_flashcards_to_flashpack, name='set_flashcards_to_flashpack'),   
 
    path('create_flashcard/new', create_flashcard, name='create_flashcard'),
    path('update_flashcard/<int:id>', update_flashcard, name='update_flashcard'),
    path('delete_flashcard/<int:id>', delete_flashcard, name='delete_flashcard'),
    path('show_flashcard/<int:id>', show_flashcard, name='show_flashcard'), 
    path('ajax_attribute_this_flashcard', ajax_attribute_this_flashcard, name='ajax_attribute_this_flashcard'),
    path('clone_flashcard/<int:idf>/<int:id>', clone_flashcard, name='clone_flashcard'),



    path('ajax_chargethemes', ajax_chargethemes, name='ajax_chargethemes'),
    path('ajax_chargeknowledges', ajax_chargeknowledges, name='ajax_chargeknowledges'),
    path('ajax_chargewaitings', ajax_chargewaitings, name='ajax_chargewaitings'),
    path('ajax_charge_groups', ajax_charge_groups, name='ajax_charge_groups'),
    path('ajax_charge_folders', ajax_charge_folders, name='ajax_charge_folders'),
    path('ajax_charge_parcours', ajax_charge_parcours, name='ajax_charge_parcours'),
    path('ajax_charge_parcours_without_folder', ajax_charge_parcours_without_folder, name='ajax_charge_parcours_without_folder'),
    path('ajax_charge_groups_level', ajax_charge_groups_level, name='ajax_charge_groups_level'),

    path('ajax_search_flashcard', ajax_search_flashcard, name='ajax_search_flashcard'),   

    path('ajax_set_flashcard_in_flashpack', ajax_set_flashcard_in_flashpack, name='ajax_set_flashcard_in_flashpack'),  

    path('ajax_level_flashcard', ajax_level_flashcard, name='ajax_level_flashcard'),   

    path('ajax_sharer_parcours', ajax_sharer_parcours, name='ajax_sharer_parcours'),
    path('ajax_publish_list_flashpack', ajax_publish_list_flashpack, name='ajax_publish_list_flashpack'),
    path('ajax_affectation_to_group', ajax_affectation_to_group, name='ajax_affectation_to_group'),
    path('ajax_is_favorite', ajax_is_favorite, name='ajax_is_favorite'),

     
] 