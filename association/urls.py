
from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('association_index', association_index, name='association_index'),
    path('activeyears', activeyears, name='activeyears'),
    path('create_activeyear', create_activeyear, name='create_activeyear'),
    path('update_activeyear/<int:id>', update_activeyear, name='update_activeyear'),

    path('statistiques', statistiques, name='statistiques'),

    path('accountings', accountings, name='accountings'),
    path('list_paypal', list_paypal, name='list_paypal'),
    path('bank_activities', bank_activities, name='bank_activities'),
    path('bank_bilan', bank_bilan, name='bank_bilan'),
    path('adhesions', adhesions, name='adhesions'),

    path('list_accountings/<int:tp>/', list_accountings, name='list_accountings'),
    path('new/<int:tp>/<int:ids>', create_accounting, name='create_accounting'),
    path('update/<int:id>/<int:tp>', update_accounting, name='update_accounting'),
    path('create_avoir/<int:id>/', create_avoir, name='create_avoir'),
    path('show/<int:id>/', show_accounting, name='show_accounting'), 
    path('print/<int:id>/', print_accounting, name='print_accounting'), 
    path('renew/<int:ids>/', renew_accounting, name='renew_accounting'),
    path('relance_accounting/<int:id>', relance_accounting, name='relance_accounting'),


    path('accounting_to_accountancy', accounting_to_accountancy, name='accounting_to_accountancy'),
    path('create_accountancy', create_accountancy, name='create_accountancy'),
    path('list_accountancy', list_accountancy, name='list_accountancy'),
    path('print_balance', print_balance, name='print_balance'),
    path('print_big_book', print_big_book, name='print_big_book'),
    path('create_accountancy', create_accountancy, name='create_accountancy'),
    path('print_bank_bilan', print_bank_bilan, name='print_bank_bilan'),

    path('new_customer', new_customer, name='new_customer'),
    path('ajax_new_customer', ajax_new_customer, name='ajax_new_customer'),

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


    path('all_schools', all_schools, name='all_schools'),# all_customers
    path('update_school_admin/<int:id>/', update_school_admin, name='update_school_admin'),
    path('ajax_customer/', ajax_customer, name='ajax_customer'),

    path('customer_payment_from_modal/<int:idc>', customer_payment_from_modal, name='customer_payment_from_modal'),

    path('paiement_abonnement/<int:idc>', paiement_abonnement, name='paiement_abonnement'),

    path('mails_parents', mails_parents, name='mails_parents'),


    path('pending_adhesions', pending_adhesions, name='pending_adhesions'),
    path('prospec_schools', prospec_schools, name='prospec_schools'),
    path('prospec_to_adhesions', prospec_to_adhesions, name='prospec_to_adhesions'),


    path('contact_prosp', contact_prosp, name='contact_prosp'),

    path('customers_pending', customers_pending, name='customers_pending'),


    ### -------------------------  Bouton d'adhésion
    path('ajax_display_button', ajax_display_button, name='ajax_display_button'),
    path('ajax_display_all_buttons', ajax_display_all_buttons, name='ajax_display_all_buttons'),

    
    ### -------------------------  GAR
    path('abonnements_gar', abonnements_gar, name='abonnements_gar'),
    path('delete_abonnement_gar/<slug:idg>', delete_abonnement_gar, name='delete_abonnement_gar'),
    path('direct_update_abonnement_gar', direct_update_abonnement_gar, name='direct_update_abonnement_gar'),
    path('purge_gar/<int:user_type>', purge_gar, name='purge_gar'),


    ### -------------------------  to_clean_database
    path('to_clean_database/<int:idl>/<int:start>', to_clean_database, name='to_clean_database'),

    path('create_bibliotex_from_tex', create_bibliotex_from_tex, name='create_bibliotex_from_tex'),
    path('create_exotex_from_tex', create_exotex_from_tex, name='create_exotex_from_tex'),
    
    path('courbeLog', courbeLog, name='courbeLog'),

    path('erase_gar', erase_gar, name='erase_gar'),

]
 