from qcm.models import Parcours, Course, Relationship,Customexercise
from account.models import Teacher, Student
from django.core.exceptions import PermissionDenied
from group.models import Sharing_group
from django.contrib import messages


def user_is_parcours_teacher(function):
	# def wrap(request, *args, **kwargs):

	# 	print("====================================") 
	# 	print("====================================")   
	# 	print(request.user) 
	# 	print("====================================")   
	# 	print("====================================") 	

	# 	kid = kwargs['id']
	# 	if kid > 0 :
	# 		parcours = Parcours.objects.get(pk=kid)
	# 		teacher = Teacher.objects.get(user= request.user)

	# 		students_parcours = parcours.students.all()
	# 		groups = []
	# 		for st in students_parcours :
	# 			for g in st.students_to_group.all() :
	# 				if not g in groups :
	# 					groups.append(g)

	# 		sharing_group_nb = Sharing_group.objects.filter(group__in = groups, teacher = teacher ).count()

	# 		if parcours.teacher == teacher or parcours.author == teacher or sharing_group_nb > 0:
	# 			return function(request, *args, **kwargs)
	# 		else:
	# 			#raise PermissionDenied
	# 			return function(request, *args, **kwargs)

	# 	else :
	# 		return function(request, *args, **kwargs)

	# return wrap
	pass

 

def user_can_modify_this_course(function):
	# def wrap(request, *args, **kwargs):
	# 	parcours = Parcours.objects.get(pk=kwargs['id'])
	# 	course = Course.objects.get(pk=kwargs['idc'])
	# 	print("====================================") 
	# 	print("====================================")   
	# 	print(request.user) 
	# 	print("====================================")   
	# 	print("====================================") 
	# 	if request.user.user_type == 2 : 
	# 		teacher = Teacher.objects.get(user= request.user)
	# 		if parcours.teacher == teacher or parcours.author == teacher :
	# 			return function(request, *args, **kwargs)
	# 		else:
	# 			raise PermissionDenied

	# 	elif request.user.user_type == 0 :  
	# 		student = Student.objects.get(user= request.user)
	# 		if student in parcours.students.all() and course.is_paired :
	# 			return function(request, *args, **kwargs)
	# 		else:
	# 			#raise PermissionDenied
	# 			return function(request, *args, **kwargs)

	# return wrap
	pass


def student_can_show_this_course(function):
	# def wrap(request, *args, **kwargs):
	# 	parcours = Parcours.objects.get(pk=kwargs['id'])

	# 	print("====================================") 
	# 	print("====================================")   
	# 	print(request.user) 
	# 	print("====================================")   
	# 	print("====================================") 
	# 	if request.user.user_type == 0 :  
	# 		student = Student.objects.get(user= request.user)
	# 		if student in parcours.students.all() :
	# 			return function(request, *args, **kwargs)
	# 		else:
	# 			#raise PermissionDenied
	# 			return function(request, *args, **kwargs)

	# return wrap 
	pass


def user_is_relationship_teacher(function):
	# def wrap(request, *args, **kwargs):
	# 	relationship = Relationship.objects.get(pk=kwargs['id'])

	# 	print("====================================") 
	# 	print("====================================")   
	# 	print(request.user) 
	# 	print("====================================")   
	# 	print("====================================") 	
	# 	teacher = Teacher.objects.get(user= request.user)
	# 	if relationship.parcours.teacher == teacher   :
	# 		return function(request, *args, **kwargs)
	# 	else:
	# 		#raise PermissionDenied
	# 		return function(request, *args, **kwargs)

	# return wrap
	pass

def user_is_customexercice_teacher(function):
	# def wrap(request, *args, **kwargs):
	# 	customexercise = Customexercise.objects.get(pk=kwargs['id'])
	# 	print("====================================") 
	# 	print("====================================")   
	# 	print(request.user) 
	# 	print("====================================")   
	# 	print("====================================") 
	# 	teacher = Teacher.objects.get(user= request.user)
	# 	if customexercise.teacher == teacher   :
	# 		return function(request, *args, **kwargs)
	# 	else:
	# 		#raise PermissionDenied
	# 		return function(request, *args, **kwargs)

	# return wrap
	pass
 
