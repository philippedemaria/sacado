from qcm.models import Parcours, Course, Relationship
from account.models import Teacher, Student
from django.core.exceptions import PermissionDenied




def user_is_parcours_teacher(function):
    def wrap(request, *args, **kwargs):
        parcours = Parcours.objects.get(pk=kwargs['id'])
        teacher = Teacher.objects.get(user= request.user)
        if parcours.teacher == teacher or parcours.author == teacher :
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


 

def user_can_modify_this_course(function):
	def wrap(request, *args, **kwargs):
		parcours = Parcours.objects.get(pk=kwargs['id'])
		course = Course.objects.get(pk=kwargs['idc'])
		if request.user.user_type == 2 : 
			teacher = Teacher.objects.get(user= request.user)
			if parcours.teacher == teacher or parcours.author == teacher :
				return function(request, *args, **kwargs)
			else:
				raise PermissionDenied

		elif request.user.user_type == 0 :  
			student = Student.objects.get(user= request.user)
			if student in parcours.students.all() and course.is_paired :
				return function(request, *args, **kwargs)
			else:
				raise PermissionDenied

	return wrap



def student_can_show_this_course(function):
	def wrap(request, *args, **kwargs):
		parcours = Parcours.objects.get(pk=kwargs['id'])

		
		if request.user.user_type == 0 :  
			student = Student.objects.get(user= request.user)
			if student in parcours.students.all() :
				return function(request, *args, **kwargs)
			else:
				raise PermissionDenied

	return wrap 



def user_is_relationship_teacher(function):
	def wrap(request, *args, **kwargs):
		relationship = Relationship.objects.get(pk=kwargs['id'])
		teacher = Teacher.objects.get(user= request.user)
		if relationship.parcours.teacher == teacher   :
			return function(request, *args, **kwargs)
		else:
			raise PermissionDenied

	return wrap



 
