from django.shortcuts import render,redirect
from account.forms import  UserForm, TeacherForm, StudentForm
from django.contrib.auth import   logout
from account.models import  User, Teacher, Student  ,Parent
 
 
 

def basthon(request):
 

    context = { 'relationship' : False , 'communications' : []}

    return render(request, 'index.html', context )

 