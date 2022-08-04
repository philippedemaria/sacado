from django import forms
from .models import Group 
from socle.models import Subject,  Level 


class GroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        subjects = Subject.objects.filter(is_active=1)
        self.fields['subject']  = forms.ModelMultipleChoiceField(queryset=subjects)
        levels = Level.objects.order_by("ranking")
        self.fields['level']  = forms.ModelMultipleChoiceField(queryset=levels)

    class Meta:
        model = Group 
        fields = ('name','color','level','assign','suiviparent','lock','subject','studentprofile' ) 




class GroupTeacherForm(forms.ModelForm):
	class Meta:
		model = Group 
		fields = ('name','color','level','assign','suiviparent','lock','subject','studentprofile','recuperation') 


	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		super(GroupTeacherForm, self).__init__(*args, **kwargs)
		if teacher:

			subjects = teacher.subjects.all()
			levels = teacher.levels.order_by("ranking")
			self.fields['subject']	 = forms.ModelChoiceField(queryset=subjects,  required=True)    
			self.fields['level']	 = forms.ModelChoiceField(queryset=levels,  required=True)         
      