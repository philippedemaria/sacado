from django import forms
from .models import Exotex , Bibliotex 
from socle.models import Knowledge , Skill


class ExotexForm(forms.ModelForm):
	class Meta:
		model = Exotex 
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		knowledge = kwargs.pop('knowledge')

		super(ExotexForm, self).__init__(*args, **kwargs)
		if teacher:

 
			levels = teacher.levels.all()
			if knowledge :
				skills = knowledge.theme.subject.skill.all()
				knowledges = Knowledge.objects.filter(level = knowledge.level )
			else :
				skills = Skill.objects.all()
				knowledges = Knowledge.objects.all()
 
			self.fields['level']	  = forms.ModelChoiceField(queryset=levels,  required=True)         
			self.fields['skills']	  = forms.ModelMultipleChoiceField(queryset=skills,  required=True)   
			self.fields['knowledges'] = forms.ModelMultipleChoiceField(queryset=knowledges,  required=False) 



class BibliotexForm(forms.ModelForm):
	class Meta:
		model = Bibliotex 
		fields = '__all__'


	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		folder  = kwargs.pop('folder')
		super(BibliotexForm, self).__init__(*args, **kwargs)
		levels = teacher.levels.all()     
		if teacher and folder : 
			groups        = teacher.groups.filter(level = folder.level , subject = folder.subject)
			shared_groups = teacher.teacher_group.filter(level = folder.level , subject = folder.subject)
			these_groups  = groups|shared_groups
			all_groups    = these_groups.order_by("teachers","level")
			all_folders   = teacher.teacher_folders.filter(level = folder.level , subject = folder.subject , is_trash = 0 )
			all_parcours  = teacher.teacher_parcours.filter(level = folder.level , subject = folder.subject, is_trash = 0)

		elif teacher :
			groups        = teacher.groups.all()
			shared_groups = teacher.teacher_group.all()
			these_groups  = groups|shared_groups
			all_groups    = these_groups.order_by("teachers","level")
			all_folders   = teacher.teacher_folders.filter(is_trash = 0)
			all_parcours  = teacher.teacher_parcours.filter(is_trash = 0)

		self.fields['groups']   = forms.ModelMultipleChoiceField(queryset=all_groups, widget=forms.CheckboxSelectMultiple, required=True)
		self.fields['folders']  = forms.ModelMultipleChoiceField(queryset=all_folders, widget=forms.CheckboxSelectMultiple, required=False)
		self.fields['parcours'] = forms.ModelMultipleChoiceField(queryset=all_parcours, widget=forms.CheckboxSelectMultiple, required=False)