
from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('association_index', association_index, name='association_index'),
    path('update_activeyear', update_activeyear, name='update_activeyear'),


    path('accountings', accountings, name='accountings'),
    path('list_paypal', list_paypal, name='list_paypal'),
    path('bank_activities', bank_activities, name='bank_activities'),
    path('bank_bilan', bank_bilan, name='bank_bilan'),
    path('adhesions', adhesions, name='adhesions'),


    path('list_accountings/<int:tp>/', list_accountings, name='list_accountings'),
    path('new/<int:tp>/', create_accounting, name='create_accounting'),
    path('update/<int:id>/', update_accounting, name='update_accounting'),
    path('delete/<int:id>/', delete_accounting, name='delete_accounting'),
    path('show/<int:id>/', show_accounting, name='show_accounting'), 
    path('print/<int:id>/', print_accounting, name='print_accounting'), 
    path('renew/<int:ids>/', renew_accounting, name='renew_accounting'),



    path('new_voting/<int:id>/', create_voting, name='create_voting'),
 
 
    path('list_associate', list_associate, name='list_associate'),
    path('new_associate', create_associate, name='create_associate'),
    path('update_associate/<int:id>/', update_associate, name='update_associate'),
    path('delete_associate/<int:id>/', delete_associate, name='delete_associate'),
    path('accept_associate/<int:id>/', accept_associate, name='accept_associate'), 

 
    path('create_section', create_section, name='create_section'),
    path('update_section/<int:id>/', update_section, name='update_section'),
    path('delete_section/<int:id>/', delete_section, name='delete_section'),



    path('list_documents', list_documents, name='list_documents'),
    path('create_document', create_document, name='create_document'),
    path('update_document/<int:id>/', update_document, name='update_document'),
    path('delete_document/<int:id>/', delete_document, name='delete_document'),
 
    path('ajax_shower_document', ajax_shower_document, name='ajax_shower_document'),

    path('print_bilan', print_bilan, name='print_bilan'),
    path('export_bilan', export_bilan, name='export_bilan'),

    path('list_rates', list_rates, name='list_rates'),
    path('create_rate', create_rate, name='create_rate'),
    path('update_rate/<int:id>/', update_rate, name='update_rate'),
    path('delete_rate/<int:id>/', delete_rate, name='delete_rate'),
    path('show_rate', show_rate, name='show_rate'),


    path('payment_complete', payment_complete, name='payment_complete'),  

    path('ajax_total_month', ajax_total_month, name='ajax_total_month'),  
    path('ajax_total_period', ajax_total_period, name='ajax_total_period'),      

    path('reset_all_students_sacado', reset_all_students_sacado, name='reset_all_students_sacado'),


    path('display_holidaybook', display_holidaybook, name='display_holidaybook'),  
    path('update_formule/<int:id>/', update_formule, name='update_formule'),
    path('delete_formule/<int:id>/', delete_formule, name='delete_formule'),


    path('all_schools', all_schools, name='all_schools'),


]
 