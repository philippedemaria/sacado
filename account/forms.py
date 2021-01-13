from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Teacher, User, Student, Parent

from django.core.exceptions import ValidationError
from django.forms import BaseFormSet

from django.db import transaction
from django.contrib.auth.hashers import make_password


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'cgu')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà utilisé. Merci d'en choisir un autre.", code='invalid')
        return username

 


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ('code',)


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
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'user_type', 'is_extra', 'password','school','cgu','schools','is_testeur']



class ManagerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'username',   'user_type', 'password','cgu']


class ManagerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined',  'user_type', 'password','cgu']


class NewUserTForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined',  'username', 'is_extra','user_type','time_zone', 'password']


  

class NewUserSForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined',   'username', 'user_type', 'is_manager',  'is_extra',  'time_zone', 'password' ,'cgu','schools']




class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
 

class ParentUpdateForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'user_type', 'password' , 'cgu','schools']




class BaseUserFormSet(BaseFormSet):
    def clean(self):
        """Checks that no two articles have the same title."""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        titles = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            username = form.cleaned_data.get('username')
            if User.objects.filter(username = username):
                raise ValidationError("Deux utilisateurs doivent avoir des identifiants différents.")