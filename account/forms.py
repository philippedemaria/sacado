from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Teacher, User , Student , Parent
from django.db import transaction


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name','email',   'username','password1','password2')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)

        

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ('email' ,) 


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'



class TeacherForm(forms.ModelForm):

    class Meta :
        model = Teacher
        fields = '__all__'



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'user_type', 'password', 'is_manager','school']



class ManagerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'user_type', 'password']


class NewUserTForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'user_type']


class NewUserSForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'user_type']




class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
 

class ParentUpdateForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'user_type', 'password']


