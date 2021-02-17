from django import forms
from .models import Group 



class GroupForm(forms.ModelForm):
    class Meta:
        model = Group 
        fields = ('name','color','level','assign','suiviparent','lock','subject','studentprofile') 




class GroupTeacherForm(forms.ModelForm):
	class Meta:
		model = Group 
		fields = ('name','color','level','assign','suiviparent','lock','subject','studentprofile')


	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		super(GroupTeacherForm, self).__init__(*args, **kwargs)
		print(teacher)
		if teacher:

			subjects = teacher.subjects.all()
			levels = teacher.levels.all()
			print(subjects)
			print(levels)
			self.fields['subject']	 = forms.ModelChoiceField(queryset=subjects,  required=True)    
			self.fields['level']	 = forms.ModelChoiceField(queryset=levels,  required=True)         
      