from django.shortcuts import render

import sys
import urllib.parse
import requests
from association.models import Accounting  
from school.models import School 
from datetime import datetime  


def traite_notif(request):

	template = "school/renew_school_adhesion.html"
    context = {   }

    return render(request, template , context)




def traite_notif____(request):

    param_str = request.body
    params = urllib.parse.parse_qsl(param_str)
    VERIFY_URL = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'
    ###### for live : https://ipnpb.paypal.com/cgi-bin/webscr

    # Add '_notify-validate' parameter                                                                                                                                    
    params.append(('cmd', '_notify-validate'))
    # Post back to PayPal for validation                                                                                                                                  
    headers = {'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'Python-IPN-Verification-Script'}

    r = requests.post(VERIFY_URL, params=params, headers=headers, verify=True)
    r.raise_for_status()
    # Check return message and take action as needed

                                                                                                                      
    if r.text == 'VERIFIED':
        # Paiement validé
        done                  = True
        inscription_school_id = request.session.get("inscription_school_id", None)
        accounting_id         = request.session.get("accounting_id", None)
        school                = request.user.school  
        student_family_id     = request.session.get("student_family_id", None)
        today                 = datetime.now()

        if accounting_id : # récupération de la facture
            Accounting.ojects.filter(pk=accounting_id).update(is_valide=1, acting = today)
            accounting = Accounting.ojects.get(pk=accounting_id)

            if inscription_school_id :  # Nouvelle inscription établissement
                school          = School.ojects.get(pk=inscription_school_id) 
                topic           = "Nouvelle adhésion à la version établissement"
                message_details =  school.name 
                template        = 'school/thanks_for_payment.html'

            elif school :  # Ré inscription établissement

                topic           = "Renouvellement d'adhésion à la version établissement"
                message_details =  school.name 
                template        = 'school/thanks_for_payment.html'

            ########################################################
            ######## Adhésion famille  ---> TODO
            ########################################################
            elif student_family_id  :  # Ré inscription Famille

                topic = "Nouvelle adhésion"
                message_details = "Famille"
                template        = 'setup/thanks_for_payment.html'

            else  : # Nouvelle inscription Famille

                topic           = "Renouvellement d'adhésion"
                message_details = "Famille"
                template        = 'setup/thanks_for_payment.html'


        message +=  message_details
        send_mail(topic,  message  ,  'info@sacado.xyz',  ['sacado.asso@gmail.com'])

    else:
        done       = False  
        accounting = None
        school     = None
        family     = None
        template  = 'home.html'

    context = { 'accounting' : accounting ,  "done" : done,  "school" : school,  "family" : family  }

    return render(request, template , context)