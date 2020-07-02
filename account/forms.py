from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Teacher, User, Student, Parent

class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name','email',   'username','password1','password2')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)



class UserFormAllAuth(UserForm):
    user_type = forms.IntegerField(widget=forms.HiddenInput(), initial=User.STUDENT)


    def save(self, request):
        user = super(UserFormAllAuth, self).save(request)
        user.user_type = self.cleaned_data['user_type']
        user.save()

        return user



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ( 'code',)


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
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined',  'username', 'user_type','time_zone', 'password']


 

class NewUserSForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined',   'username','user_type','is_manager','time_zone', 'password']




class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
 

class ParentUpdateForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
        exclude = ['user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'user_type', 'password']


