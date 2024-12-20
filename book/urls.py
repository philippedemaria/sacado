#################################
#### Auteur : philipe Demaria 
#### pour SACADO
#################################
from django.urls import path, re_path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [


    #################################################################
    # book
    #################################################################

    path('books', books, name='books'),
    path('mybooks', mybooks, name='mybooks'),
    path('get_mybook/<int:idb>/<int:idg>', get_mybook, name='get_mybook'),

    path('show_mybook/<int:idb>/<int:n>', show_mybook, name='show_mybook'),
    path('show_mybook_two_pages/<int:idb>/<int:n>', show_mybook_two_pages, name='show_mybook_two_pages'),


    path('show_mybook_student/<int:idb>/<int:n>', show_mybook_student, name='show_mybook_student'),

    path('create_book/0', create_book, name='create_book'),
    path('update_book/<int:idb>', update_book, name='update_book'),
    path('delete_book/<int:idb>', delete_book, name='delete_book'), 
    path('show_book/<int:idb>/<int:idch>', show_book, name='show_book'),
    path('conception_book/<int:idb>/<int:idch>', conception_book, name='conception_book'),

    #################################################################
    # chapter
    #################################################################
    path('create_chapter/<int:idb>/<int:idch>', create_chapter, name='create_chapter'),
    path('update_chapter/<int:idb>/<int:idch>', update_chapter, name='update_chapter'),
    path('delete_chapter/<int:idb>/<int:idch>', delete_chapter, name='delete_chapter'),

    path('update_student_book_chapter/<int:idb>/<int:idch>', update_student_book_chapter, name='update_student_book_chapter'),
    path('delete_student_book_chapter/<int:idb>/<int:idch>', delete_student_book_chapter, name='delete_student_book_chapter'),

    path('sorter_chapter', sorter_chapter, name='sorter_chapter'),

    path('reset_all_chapters/<int:idb>', reset_all_chapters, name='reset_all_chapters'),

    path('chapter_chrono_show_document/<int:idb>/<int:idch>', chapter_chrono_show_document, name='chapter_chrono_show_document'),
    path('chapter_chrono_concept_document/<int:idb>/<int:idch>', chapter_chrono_concept_document, name='chapter_chrono_concept_document'),

    path('print_latex_to_pdf/<int:idch>/<int:idp>', print_latex_to_pdf , name='print_latex_to_pdf'), 
    path('print_latex_to_tex/<int:idch>/<int:idp>', print_latex_to_tex , name='print_latex_to_tex'), 
    path('print_latex_to_book/<int:idch>/<int:idp>', print_latex_to_book , name='print_latex_to_book'), 
    path('print_latex_to_tex_avec_cor/<int:idch>/<int:idp>', print_latex_to_tex_avec_cor , name='print_latex_to_tex_avec_cor'),
    #################################################################
    # document
    #################################################################

    path('update_book_document/<int:idb>/<int:idch>/<int:idd>', update_book_document, name='update_book_document'),
    path('duplicate_book_document/<int:idb>/<int:idch>/<int:idd>', duplicate_book_document, name='duplicate_book_document'),
    path('delete_book_document', delete_book_document, name='delete_book_document'),
    path('show_book_document', show_book_document, name='show_book_document'),
    path('sorter_book_document', sorter_book_document, name='sorter_book_document'),
    path('sorter_book_chrono_document', sorter_book_chrono_document, name='sorter_book_chrono_document'),

    path('publish_book_document', publish_book_document, name='publish_book_document'),
    path('book_document_is_done', book_document_is_done, name='book_document_is_done'),


    path('get_type_book_document', get_type_book_document, name='get_type_book_document'),
 
    path('book_chapter_show_document/<int:idb>/<int:idch>/<int:idd>', book_chapter_show_document, name='book_chapter_show_document'),

    path('create_book_section', create_book_section, name='create_book_section'),
    path('update_book_section', update_book_section, name='update_book_section'),
    path('delete_book_section', delete_book_section, name='delete_book_section'),
    path('sorter_book_section', sorter_book_section, name='sorter_book_section'),
    path('publish_book_section', publish_book_section, name='publish_book_section'),

    path('sorter_book_pages', sorter_book_pages, name='sorter_book_pages'),
 
    ##################################################################################################################################
    ##################################################################################################################################
    ################### Student book
    ##################################################################################################################################
    ##################################################################################################################################

    path('show_student_book/<int:idb>/<int:n>', show_student_book, name='show_student_book'),
    path('show_student_book_one_page/<int:idb>/<int:n>', show_student_book_one_page, name='show_student_book_one_page'),

    path('student_book_builder/<int:idb>/<int:n>', student_book_builder, name='student_book_builder'),

    path('create_page/<int:idb>/<int:idch>', create_page, name='create_page'),
    path('update_page/<int:idb>/<int:idp>', update_page, name='update_page'),
    path('goto_update_page/<int:idb>/<int:n>', goto_update_page, name='goto_update_page'),
    
    path('delete_page/<int:idb>/<int:idp>', delete_page, name='delete_page'),
    path('add_page/<int:idb>/<int:idch>', add_page, name='add_page'),

    path('create_paragraph/<int:idb>/0', create_paragraph, name='create_paragraph'),
    path('update_paragraph/<int:idb>/<int:idp>/<int:idpa>', update_paragraph, name='update_paragraph'),
    path('delete_paragraph/<int:idb>/<int:idp>/<int:idpa>', delete_paragraph, name='delete_paragraph'),


    path('typeblocs/0', typeblocs, name='typeblocs'),
    path('create_typebloc/0', create_typebloc, name='create_typebloc'),
    path('update_typebloc/<int:idb>/<int:idp>/<int:idt>', update_typebloc, name='update_typebloc'),
    path('delete_typebloc', delete_typebloc, name='delete_typebloc'),

 

    path('create_bloc/<int:idb>/<int:idp>', create_bloc, name='create_bloc'),
    path('update_bloc/<int:idb>/<int:idp>/<int:idbl>', update_bloc, name='update_bloc'),
    path('delete_bloc/<int:idb>/<int:idp>/<int:idbl>', delete_bloc, name='delete_bloc'),

 
    path('sorter_book_page_bloc', sorter_book_page_bloc, name='sorter_book_page_bloc'),
 
    ##################################################################################################################################
    ##################################################################################################################################
    ################### 
    ##################################################################################################################################
    ##################################################################################################################################
    path('type_de_page', type_de_page, name='type_de_page'),
    path('insert_document_into_section', insert_document_into_section, name='insert_document_into_section'),
    ##################################################################################################################################
    ##################################################################################################################################
    ################### 
    ##################################################################################################################################
    ##################################################################################################################################
    path('list_appliquettes/<int:idl>', list_appliquettes, name='list_appliquettes'),
    path('create_appliquette/<int:idl>', create_appliquette, name='create_appliquette'),
    path('update_appliquette/<int:ida>', update_appliquette, name='update_appliquette'),
    path('delete_appliquette/<int:ida>', delete_appliquette, name='delete_appliquette'),
    path('show_appliquette/<int:ida>', show_appliquette, name='show_appliquette'),


    path('display_details_bloc_by_qr/<int:idbl>', display_details_bloc_by_qr, name='display_details_bloc_by_qr'),
    path('display_details_bloc_correction/<int:idbl>', display_details_bloc_correction, name='display_details_bloc_correction'),

    

    path('ajax_display_correction_bloc', ajax_display_correction_bloc, name='ajax_display_correction_bloc'),
    path('ajax_create_exercise_from_scratch', ajax_create_exercise_from_scratch, name='ajax_create_exercise_from_scratch'),
    path('ajax_insidebloc', ajax_insidebloc, name='ajax_insidebloc'),
    path('ajax_knowledge_inbloc', ajax_knowledge_inbloc, name='ajax_knowledge_inbloc'),

    
    path('group_can_get_the_book', group_can_get_the_book, name='group_can_get_the_book'),
    path('goto_direct_page', goto_direct_page, name='goto_direct_page'),
    path('goto_direct_page_student', goto_direct_page_student, name='goto_direct_page_student'),


    
 ]
