from django.shortcuts import render,redirect
from account.forms import  UserForm, TeacherForm, StudentForm
from django.contrib.auth import   logout
from account.models import  User, Teacher, Student  ,Parent
from basthon2.models import ExoPython 
 
 

def basthon(request):
     context = { 'relationship' : False , 'communications' : []}
     return render(request, 'index.html', context )


def pyodide(request):
	context=dict()
	exo=ExoPython.objects.get(title="essai4")
	context['instruction']=exo.instruction
	context['preambule_cache']=exo.preambule_cache
	context['preambule_visible']=exo.preambule_visible
	context['autotest']=exo.autotest
	context['prog_cor']=exo.prog_cor
	
	return render(request,'indexPyodide.html',context)


