from django.shortcuts import render, redirect
from django.db.models import Q
from account.models import User, Teacher, Student
from qcm.models import Studentanswer, Relationship
from group.models import Group
from sendmail.models import Email, Communication
from sendmail.forms import EmailForm, CommunicationForm
from django.http import JsonResponse
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sendmail.decorators import user_is_email_teacher
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import re
import html
import pytz
from general_fonctions import *
 



def list_emails(request):
 
    user = request.user
    users = []

    if user.is_teacher:
        today = time_zone_user(request.user)
        teacher = user.teacher
        groups = teacher.groups.all()
        for group in groups:
            for student in group.students.filter():
                users.append(student.user)

        studentanswers = Studentanswer.objects.filter(student__user__in =  users).order_by("-date")[:50]
        tasks = Relationship.objects.filter(parcours__teacher = teacher,  exercise__supportfile__is_title=0).exclude(date_limit=None).order_by("-date_limit")[:50] 

        #import pdb;pdb.set_trace()
        sent_emails = Email.objects.distinct().filter(author=user).order_by("-today")
        emails = Email.objects.distinct().filter(receivers=user).order_by("-today")
        form = EmailForm(request.POST or None, request.FILES or None)

        return render(request,
                      'sendmail/list.html',
                      {'emails': emails, 'sent_emails': sent_emails, 'form': form, 'users': users, 'groups': groups,  'today': today, 'communications': [], 
                       'studentanswers': studentanswers, 'tasks': tasks})

    elif user.is_student:
        student = Student.objects.get(user=user)
        groups = student.students_to_group.all()
        today = time_zone_user(request.user)
        for group in groups:
            users.append(group.teacher.user)

        sent_emails = Email.objects.distinct().filter(author=user).order_by("-today")
        emails = Email.objects.distinct().filter(receivers=user).order_by("-today")
        form = EmailForm(request.POST or None, request.FILES or None)

        return render(request,
                      'sendmail/list.html',
                      {'emails': emails, 'sent_emails': sent_emails, 'form': form, 'users': users, 'groups': groups, 'today': today, 'communications': [], 'student' : student , 
                       'studentanswers': [], 'tasks': []})
    else:
        raise PermissionDenied



def create_email(request):
 
	form = EmailForm(request.POST or None,request.FILES or None)
	user = request.user
	today = time_zone_user(user)

	if form.is_valid():		
		new_f = form.save(commit=False)
		new_f.author = user
		new_f.save()
		form.save_m2m()

		subject = request.POST.get('subject')
		texte = request.POST.get('texte')
		receivers = request.POST.getlist('receivers')
		groups = request.POST.getlist('groups')
		rcv = []
 
		for receiver  in receivers :
			u = User.objects.get(pk = int(receiver))
			new_f.receivers.add(u)
			rcv.append(str(u.email))

		for group_id  in groups :
			group = Group.objects.get(pk = int(group_id))
			for s in group.students.all():
				if s.user.email :
					new_f.receivers.add(s.user)	
					rcv.append(str(s.user.email)) 


		send_mail(subject, cleanhtml(unescape_html(texte)) , "info@sacado.xyz", rcv )
		send_mail(subject, cleanhtml(unescape_html(texte)) , "info@sacado.xyz", [str(request.user.email)] )

	else:
		print(form.errors)
		messages.errors(request, "Le corps de message est obligatoire !")

	return redirect('emails')


 




@user_is_email_teacher
def delete_email(request,id):
    email = Email.objects.get(id=id)
    email.receivers.clear()
    email.delete()
    return redirect('emails')



def show_email(request):
	email_id = int(request.POST.get("email_id"))
	email = Email.objects.get(id=email_id)
	form = EmailForm(request.POST or None,request.FILES or None)
	data = {} 

	html = render_to_string('sendmail/show.html',{ 'email' : email  , 'form' : form  , 'communications': [],  })
	data['html'] = html 		

	return JsonResponse(data)




def list_communications(request):
	communications = Communication.objects.all()
	form = CommunicationForm(request.POST or  None)
	context = {'form': form,  'communications': communications,  } 
	return render(request, 'sendmail/list_communications.html', context)


@csrf_exempt
def create_communication(request): # id du concours
	form = CommunicationForm(request.POST or  None)

	if request.method == "POST":
		if form.is_valid():
			new_f = form.save(commit=False)
			new_f.teacher = request.user
			new_f.save()

			try :
				users = User.objects.filter(user_type=2)
				rcv = []
				for u in users : 
					rcv.append(u.email)
				send_mail(new_f.subject, cleanhtml(unescape_html(new_f.texte)), "info@sacado.xyz", rcv )
			except :
				pass


		else :
			print(form.errors)
 


	return redirect('communications')







def update_communication(request,id): # update

	communication = Communication.objects.get(id= id)
	form = CommunicationForm(request.POST or  None, instance = communication)

	if request.method == "POST":
		if form.is_valid():
			new_f = form.save(commit=False)
			new_f.teacher = request.user
			new_f.save()
			return redirect('communications')
		else :
			print(form.errors)

	return render(request,'sendmail/form_update_communication.html', {'form':form,'communication':communication,   })







def delete_communication(request, id):
    communication = Communication.objects.get(id=id)
    communication.delete()
    return redirect('communications')


 



def show_communication(request):
	communication_id = int(request.POST.get("communication_id"))
	communication = Communication.objects.get(id=communication_id)
	form = CommunicationForm(request.POST or None)
	data = {} 

	html = render_to_string('sendmail/show_communication.html',{ 'communication' : communication  , 'form' : form  ,   })
	data['html'] = html 		

	return JsonResponse(data)




def reader_communication(request):
	
	data = {} 
	teacher = Teacher.objects.get(user = request.user)  
	communications = Communication.objects.exclude(teachers = teacher)
	for c in communications:
		c.teachers.add(teacher)
	
	return JsonResponse(data)