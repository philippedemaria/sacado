import datetime
from django import forms
from .models import Parcours, Exercise, Remediation, Relationship, Supportfile, Course, Demand
from account.models import Student
from socle.models import Knowledge, Skill
from group.models import Group


class ParcoursForm(forms.ModelForm):

	class Meta:
		model = Parcours
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		super(ParcoursForm, self).__init__(*args, **kwargs)
		if teacher:
			groups = Group.objects.filter(teacher=teacher)
			students_tab = []
			for group in groups:
				for student in group.students.order_by("user__last_name"):
					students_tab.append(student.user)

			students = Student.objects.filter(user__in=students_tab).order_by("level", "user__last_name")
			self.fields['students']	 = forms.ModelMultipleChoiceField(queryset=students, widget=forms.CheckboxSelectMultiple, required=False)

	def clean(self):
		"""
		Vérifie que la fin de l'évaluation n'est pas avant son début
		"""
		cleaned_data = super().clean()

		start_date = cleaned_data.get("start")
		start_time = cleaned_data.get("starter")
		start = datetime.datetime.combine(start_date, start_time)

		stop_date = cleaned_data.get("stop")
		stop_time = cleaned_data.get("stopper")
		stop = datetime.datetime.combine(stop_date, stop_time)

		if stop <= start:
			raise forms.ValidationError("La fin de l'évaluation ne peut pas être antérieure à son début.")


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


class RemediationForm(forms.ModelForm):
	class Meta:
		model = Remediation
		fields = '__all__'


class SupportfileForm(forms.ModelForm):
	class Meta:
		model = Supportfile
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		super(SupportfileForm, self).__init__(*args, **kwargs)

		subjects = teacher.subjects.all()
		knowledges = Knowledge.objects.filter(theme__subject__in= subjects)
		self.fields['knowledge'] = forms.ModelChoiceField(queryset=knowledges) 
		skills  = forms.ModelMultipleChoiceField(queryset= Skill.objects.filter(subject__in= subjects), widget=forms.CheckboxSelectMultiple, required=False)


class SupportfileKForm(forms.ModelForm):
	class Meta:
		model = Supportfile
		fields = '__all__'
		exclude = ('knowledge',)

	def __init__(self, *args, **kwargs):
		knowledge = kwargs.pop('knowledge')
		super(SupportfileKForm, self).__init__(*args, **kwargs)
		subject = knowledge.theme.subject 
		knowledges = Knowledge.objects.filter(theme__subject= subject)
		skills  = forms.ModelMultipleChoiceField(queryset= Skill.objects.filter(subject= subject), widget=forms.CheckboxSelectMultiple, required=False)


class UpdateSupportfileForm(forms.ModelForm):

	class Meta:
		model = Supportfile 
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		knowledge = kwargs.pop('knowledge')
		subject = knowledge.theme.subject	
		super(UpdateSupportfileForm, self).__init__(*args, **kwargs)
		instance = kwargs.pop('instance')
		knowledges = Knowledge.objects.filter(theme__subject=subject)
		skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.filter(subject=subject), widget=forms.CheckboxSelectMultiple, required=False)


class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = '__all__'


class DemandForm(forms.ModelForm):
	class Meta:
		model = Demand
		fields = '__all__'
