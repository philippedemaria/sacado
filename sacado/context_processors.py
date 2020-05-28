from django.conf import settings
from account.models import Teacher, Student , User
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from group.models import Group
from qcm.models import Parcours, Studentanswer, Exercise, Relationship
from django.db.models import Q
from datetime import datetime,timedelta 
import time
import pytz
from itertools import chain
from django.utils import timezone

 

 


def menu(request):


 
	if request.user.is_authenticated :


		if request.user.time_zone :
			time_zome = request.user.time_zone
			timezone.activate(pytz.timezone(time_zome))
			current_tz = timezone.get_current_timezone()
			today = timezone.localtime(timezone.now())

		else :
			today = timezone.now()
		one_week =  today +timedelta(days=7)
  

		if  request.user.user_type == 2 :  #teacher
			return {   'today' : today, }
 

		elif  request.user.user_type == 0 : #student

			student = Student.objects.get(user = request.user)
			last_exercises_done = Studentanswer.objects.filter(student=student).order_by("-date")[:10]
			nb_exercise = Exercise.objects.filter(level=student.level).count()  
			parcours = Parcours.objects.filter(is_publish = 1 , exercises__level=student.level).exclude(author=None)
			parcourses = Parcours.objects.filter(is_publish = 1 , is_evaluation = 0 , students=student) # tous les parcours attribués à cet élève
			studentanswers = Studentanswer.objects.filter(student=student) 
 
			return {   
			'student' : student ,  
			'parcourses' : parcourses,  
			'parcours' : parcours,  
			'last_exercises_done' : last_exercises_done,   
			}


		elif  request.user.user_type == 1 : #student
			this_user = User.objects.get(pk=request.user.id)
 
			return {   
			'this_user' : this_user , 
 
			}


	else:
		nb_teacher  = Teacher.objects.all().count()  
		nb_exercise  = Exercise.objects.all().count()  
		nb_student  = Student.objects.all().count() 
		nb_group = Group.objects.all().count() 
		contributeurs = User.objects.filter(is_superuser=1) 



		return { 
		'nb_teacher' : nb_teacher , 
		'nb_exercise' : nb_exercise ,  
		'nb_student' : nb_student ,
		'nb_group' : nb_group,    
		'contributeurs' : contributeurs, 
			}
