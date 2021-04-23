from django.shortcuts import render

import sys
import urllib.parse
import requests
from account.models import User  
from association.models import Accounting , Abonnement 
from school.models import School 
from datetime import datetime  
import json
from django.core.mail import send_mail
from templated_email import send_templated_mail
from django.http import JsonResponse 


def verify_payment(buyer, accounting, school,new):
	""" vérifie que le paiement a été reçu par Payal et active l'abonnement"""

	accounting.is_active = False
 
	today = datetime.now()
	if school :

		if buyer.school.fee() == accounting.amount : # Vérification que le montant à payer est le bon.

			is_school = True
			accounting.is_active = True
			accounting.acting = today
			message_details =  school.name 

			if new :  # Nouvelle inscription établissement
				
				topic  = "Nouvelle adhésion à la version établissement"

			elif school :  # Ré inscription établissement
 
				topic = "Renouvellement d'adhésion à la version établissement"

 
			message = topic + " : " + message_details
			send_mail(topic,  message  ,  'info@sacado.xyz',  ['sacado.asso@gmail.com'])
			# send_templated_mail(
			# 	template_name="teacher_registration",
			# 	from_email="info@sacado.xyz",
			# 	recipient_list=[self.user.email, ],
			# 	context={"teacher": self.user, }, )
			accounting.save()
			accounting.abonnement.is_active=True
			accounting.abonnement.save()


	else :
		is_school = False
		message_details = "Famille"
		student_family_id = new
		########################################################
		######## Adhésion famille  ---> TODO
		########################################################
		if new  :  # Ré inscription Famille
			
			topic = "Nouvelle adhésion"
 

		else  : # Nouvelle inscription Famille
 
			topic = "Renouvellement d'adhésion"

	return accounting.is_active




def create_payment(request):

	today = datetime.now()
	body = json.loads(request.body)

	accounting_id = body["accounting_id"]
	accounting    = Accounting.objects.get(pk=accounting_id) 
	request.session["accounting_id"] = accounting_id

	school_id = body["school_id"]
	if school_id : 
		school    = School.objects.get(pk=school_id) 
		request.session["school_id"] = school.id

	user_id = body["user_id"]
	user  = User.objects.get(pk=user_id) 
	request.session["user_id"] = user_id

	if request.session.get("inscription_school_id", None) :
		new = request.session.get("inscription_school_id")
	

	elif request.session.get("student_family_id", None) :
		new = request.session.get("student_family_id")
		school = None
	else :
		new = False

	verify_payment(user, accounting, school, new)
	
	return JsonResponse('Payment en cours', safe = False)



def thanks_for_payment(request) :

	if request.session.get("school_id", None) :

		school_id = request.session.get("school_id")
		school    = School.objects.get(pk = school_id)

		accounting_id = request.session.get("accounting_id")
		accounting    = Accounting.objects.get(pk=accounting_id) 

		if request.session.get("inscription_school_id", None) :
			new      = True
			template = 'payment/new_school_payment.html'
			user_id = request.session["user_id"]
			user  = User.objects.get(pk=user_id)

		else :
			new      = False
			user_id = request.session["user_id"]
			user  = User.objects.get(pk=user_id)
			template = 'payment/school_payment.html'

		context = { 'school' : school , 'accounting' : accounting, 'user' : user }
		

	else :
		template   = 'payment/family_payment.html'
 


	return render(request, template , context)