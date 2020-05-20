from django import forms
from .models import  Parcours, Exercise, Remediation,Relationship,Supportfile
from account.models import  Student
from socle.models import  Knowledge , Skill
from group.models import  Group 
from django.db.models import Q
from django.forms.models import modelformset_factory

class ParcoursForm(forms.ModelForm):

	class Meta:
	    model = Parcours 
	    fields = '__all__'

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		super(ParcoursForm, self).__init__(*args, **kwargs)
		if teacher:
			groups = Group.objects.filter(teacher  = teacher)
			students_tab = []
			for group in groups :
				for student in group.students.order_by("user__last_name"):
					students_tab.append(student.user)

			students = Student.objects.filter(user__in = students_tab).order_by("level","user__last_name") 
			self.fields['students']	 = forms.ModelMultipleChoiceField(queryset= students, widget=forms.CheckboxSelectMultiple, required=False) 


class UpdateParcoursForm(forms.ModelForm):

	class Meta:
	    model = Parcours 
	    fields = '__all__'
	    exclude = ("exercises",)

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		super(UpdateParcoursForm, self).__init__(*args, **kwargs)
		if teacher:
			groups = Group.objects.filter(teacher  = teacher)
			students_tab = []
			for group in groups :
				for student in group.students.order_by("user__last_name"):
					students_tab.append(student.user)

			students = Student.objects.filter(user__in = students_tab).order_by("user__last_name") 

			self.fields['students']	 = forms.ModelMultipleChoiceField(queryset= students, widget=forms.CheckboxSelectMultiple, required=False) 
 

class ExerciseForm(forms.ModelForm):
 
	class Meta:
		model = Exercise 
		fields = '__all__'



	def __init__(self, *args, **kwargs):
		super(ExerciseForm, self).__init__(*args, **kwargs)
		knowledges = Knowledge.objects.filter(id  = 0)
		self.fields['knowledge'] = forms.ModelChoiceField(queryset=knowledges) 


class ExerciseKForm(forms.ModelForm):
 
	class Meta:
		model = Exercise 
		fields = '__all__'
		exclude = ('knowledge',)
 



class UpdateExerciseForm(forms.ModelForm):
 
	class Meta:
		model = Exercise 
		fields = '__all__'



class RelationshipForm(forms.ModelForm):
 

	class Meta:
		model = Relationship 
		fields = '__all__' 
		exclude = ('exercise', 'parcours', 'order', 'skill')

  
 

#	def __init__(self, *args, **kwargs):
#		self.parcours = kwargs.pop('parcours')
#		super(RelationshipForm, self).__init__(*args, **kwargs)
 

# NON UTILISE MAIS A GARDER POUR PUS TARD
# BaseRelationshipSet = modelformset_factory(Relationship, form=RelationshipForm)

# class RelationshipFormSet(BaseRelationshipSet):



#     def __init__(self, *args, **kwargs):
#         #  create a user attribute and take it out from kwargs
#         # so it doesn't messes up with the other formset kwargs
#         self.parcours = kwargs.pop('parcours')
#         super(RelationshipFormSet, self).__init__(*args, **kwargs)
#         for form in self.forms:
#             form.empty_permitted = False

#     def _construct_form(self, *args, **kwargs):
#         # inject user in each form on the formset
#         kwargs['parcours'] = self.parcours
#         return super(RelationshipFormSet, self)._construct_form(*args, **kwargs)




class RemediationForm(forms.ModelForm):

    class Meta:
        model = Remediation 
        fields = '__all__' 




class SupportfileForm(forms.ModelForm):

	skills  = forms.ModelMultipleChoiceField(queryset= Skill.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)   
	class Meta:
		model = Supportfile 
		fields = '__all__'



	def __init__(self, *args, **kwargs):
		super(SupportfileForm, self).__init__(*args, **kwargs)
		knowledges = Knowledge.objects.filter(id  = 0)
		self.fields['knowledge'] = forms.ModelChoiceField(queryset=knowledges) 


class SupportfileKForm(forms.ModelForm):

	skills  = forms.ModelMultipleChoiceField(queryset= Skill.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)    
	class Meta:
		model = Supportfile 
		fields = '__all__'
		exclude = ('knowledge',)
 



class UpdateSupportfileForm(forms.ModelForm):
	skills  = forms.ModelMultipleChoiceField(queryset= Skill.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)    
	class Meta:
		model = Supportfile 
		fields = '__all__'
