from qcm.models import Parcours, Course, Relationship
from account.models import Teacher, Student
from django.core.exceptions import PermissionDenied
from django.contrib import messages




def user_is_superuser(function):
	# def wrap(request, *args, **kwargs):
	# 	print("====================================") 
	# 	print("====================================")   
	# 	print(request.user) 
	# 	print("====================================")   
	# 	print("====================================") 
	# 	if request.user.is_superuser :
	# 		return function(request, *args, **kwargs)
	# 	else:
	# 		#raise PermissionDenied
	# 		return function(request, *args, **kwargs)
	# return wrap
	pass

