from django import forms
from .models import Exotex , Bibliotex , Relationtex
from qcm.models import Exercise 
from socle.models import Knowledge , Skill
from django.db.models import Q 

class ExotexForm(forms.ModelForm):
	class Meta:
		model = Exotex 
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		knowledge = kwargs.pop('knowledge')

		super(ExotexForm, self).__init__(*args, **kwargs)
		if teacher:
			subjects = teacher.subjects.all()
			levels   = teacher.levels.order_by("ranking")
			if knowledge :
				skills = knowledge.theme.subject.skill.all()
				knowledges = Knowledge.objects.filter(Q(level_id = knowledge.level.id )|Q(level_id = knowledge.level.id-1 ))
				self.fields['knowledges'] = forms.ModelMultipleChoiceField(queryset=knowledges,  required=True)  
				self.fields['knowledges'].required = False

				self.fields['subject']	     = forms.ModelChoiceField(queryset=subjects,  required=True) 
				self.fields['subject'].initial =  knowledge.theme.subject
				self.fields['level']	     = forms.ModelChoiceField(queryset=levels,  required=True)  
				self.fields['level'].initial =  knowledge.level.id
				self.fields['theme'].initial =  knowledge.theme.id
				exercises = Exercise.objects.filter( knowledge__level = knowledge.level)
				self.fields['exercises']     = forms.ModelMultipleChoiceField(queryset=exercises,  required=False)
			else :
				skills = Skill.objects.all()
			
				self.fields['subject']	  = forms.ModelChoiceField(queryset=subjects,  required=True) 
				self.fields['level']	  = forms.ModelChoiceField(queryset=levels,  required=True)         
				exercises = Exercise.objects.filter( knowledge__level__in = levels)
				self.fields['exercises']     = forms.ModelMultipleChoiceField(queryset=exercises,  required=False)
			self.fields['skills']	  = forms.ModelMultipleChoiceField(queryset=skills,  required=True)   
			   	 




class SetExotexForm(forms.ModelForm):
	class Meta:
		model = Exotex 
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		knowledge = kwargs.pop('knowledge')

		super(SetExotexForm, self).__init__(*args, **kwargs)
		if teacher:
			subjects = teacher.subjects.all()
			levels   = teacher.levels.order_by("ranking")
			if knowledge :
				skills = knowledge.theme.subject.skill.all()
				knowledges = Knowledge.objects.filter(Q(level_id = knowledge.level.id )|Q(level_id = knowledge.level.id-1 ))
				self.fields['knowledges'] = forms.ModelMultipleChoiceField(queryset=knowledges,  required=False)  
				exercises = Exercise.objects.filter( knowledge = knowledge)
				self.fields['exercises']  = forms.ModelMultipleChoiceField(queryset=exercises,  required=False)
			else :
				skills = Skill.objects.all()

			self.fields['knowledge'].required = False
			self.fields['subject']	  = forms.ModelChoiceField(queryset=subjects,  required=True) 
			self.fields['level']	  = forms.ModelChoiceField(queryset=levels,  required=True)         
			self.fields['skills']	  = forms.ModelMultipleChoiceField(queryset=skills,  required=True)   
			 


class BibliotexForm(forms.ModelForm):
	class Meta:
		model = Bibliotex 
		fields = '__all__'
		exclude = ('folders','parcours')

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		group   = kwargs.pop('group')
		super(BibliotexForm, self).__init__(*args, **kwargs)
 
 
		if group : all_folders = group.group_folders.filter(is_archive=0,is_trash=0)
		else : all_folders = teacher.teacher_folders.filter(is_archive=0,is_trash=0) 

		groups =  teacher.groups.filter(is_hidden = 0) 
		teacher_groups = teacher.teacher_group.filter(is_hidden = 0) 
		all_groups = groups|teacher_groups
 
		self.fields['groups']   = forms.ModelMultipleChoiceField(queryset = all_groups.order_by("teachers","level"), widget=forms.CheckboxSelectMultiple, required=True)



class RelationtexForm(forms.ModelForm):
	class Meta:
		model = Relationtex 
		fields = ('calculator','duration','skills','knowledges','is_python','is_scratch','is_tableur','start','stop','is_publish_cor','point','exercises')

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
 
		super(RelationtexForm, self).__init__(*args, **kwargs)
		if teacher:
			subjects = teacher.subjects.all()
			levels   = teacher.levels.order_by("ranking")
			skills = Skill.objects.filter(subject__in=subjects)
			knowledges = Knowledge.objects.filter(theme__subject__in=subjects,level__in=levels )  
			exercises  = Exercise.objects.filter(knowledge__in=knowledges) 
			self.fields['skills']	  = forms.ModelMultipleChoiceField(queryset=skills,  required=True)   
			self.fields['knowledges'] = forms.ModelMultipleChoiceField(queryset=knowledges,  required=False) 
			self.fields['exercises']  = forms.ModelMultipleChoiceField(queryset=exercises,  required=False) 

 