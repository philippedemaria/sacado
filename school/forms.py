from django import forms
from .models import School, Country , Stage
from group.models import Group
from account.models import User, Teacher



class SchoolForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all().order_by("name") )


    class Meta:
    	model = School
    	fields = '__all__'

 

class SchoolUpdateForm(forms.ModelForm):
 
    class Meta:
    	model = School
    	fields = 'gar', 'logo', 'nbstudents'



class CountryForm(forms.ModelForm):


    class Meta:
    	model = Country
    	fields = '__all__'
        


class GroupForm(forms.ModelForm):


	class Meta:
		model = Group
		fields = '__all__'
		exclude = ('students','teachers')

	def __init__(self, *args, school, **kwargs):
		self.school = school
		super().__init__(*args, **kwargs)
		if school:
			users = User.objects.filter(user_type = 2, school = school)
			teachers = Teacher.objects.filter(user__in = users).order_by("user__last_name") 
			self.fields['teacher']	 = forms.ModelChoiceField(queryset= teachers) 
 
class StageForm(forms.ModelForm):

	class Meta:
		model = Stage
		fields = '__all__'        
