import datetime
from django import forms
from .models import Parcours, Exercise, Remediation, Relationship, Supportfile, Course, Demand, Mastering,Mastering_done, Writtenanswerbystudent, Customexercise,Customanswerbystudent, Masteringcustom, Masteringcustom_done
from account.models import Student
from socle.models import Knowledge, Skill
from group.models import Group
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput

class ParcoursForm(forms.ModelForm):

	class Meta:
		model = Parcours
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		super(ParcoursForm, self).__init__(*args, **kwargs)
		self.fields['stop'].required = False
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
		stop_date = cleaned_data.get("stop")
		try :
			if stop <= start:
				raise forms.ValidationError("La date de verrouillage ne peut pas être antérieure à son début.")
		except:
			pass


class UpdateParcoursForm(forms.ModelForm):

	class Meta:
		model = Parcours
		fields = '__all__'
		exclude = ("exercises",)

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		super(UpdateParcoursForm, self).__init__(*args, **kwargs)
		self.fields['stop'].required = False
		if teacher:
			groups = Group.objects.filter(teacher  = teacher)
			students_tab = []
			for group in groups :
				for student in group.students.order_by("user__last_name"):
					students_tab.append(student.user)

			students = Student.objects.filter(user__in = students_tab).order_by("user__last_name") 

			self.fields['students']	 = forms.ModelMultipleChoiceField(queryset= students, widget=forms.CheckboxSelectMultiple, required=False)
			

	def clean(self):
		"""
		Vérifie que la fin de l'évaluation n'est pas avant son début
		"""
		cleaned_data = super().clean()
		start_date = cleaned_data.get("start")
		stop_date = cleaned_data.get("stop")

		try :
			if stop <= start:
				raise forms.ValidationError("La date de verrouillage ne peut pas être antérieure à son début.")
		except:
			pass



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
		exclude = ('attach_file','is_subtitle')

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		super(SupportfileForm, self).__init__(*args, **kwargs)

		subjects = teacher.subjects.all()
		knowledges = Knowledge.objects.filter(theme__subject__in= subjects)
		self.fields['knowledge'] = forms.ModelChoiceField(queryset=knowledges) 
		self.fields['skills']  =  forms.ModelMultipleChoiceField(queryset= Skill.objects.filter(subject= subject), required=False)

class SupportfileKForm(forms.ModelForm):
	class Meta:
		model = Supportfile
		fields = '__all__'
		exclude = ('knowledge','attach_file','is_subtitle')

	def __init__(self, *args, **kwargs):
		knowledge = kwargs.pop('knowledge')
		super(SupportfileKForm, self).__init__(*args, **kwargs)
		subject = knowledge.theme.subject 
		knowledges = Knowledge.objects.filter(theme__subject= subject)
		self.fields['knowledge'] = forms.ModelChoiceField(queryset=knowledges) 
		self.fields['skills']  =  forms.ModelMultipleChoiceField(queryset= Skill.objects.filter(subject= subject), required=False)

class UpdateSupportfileForm(forms.ModelForm):

	class Meta:
		model = Supportfile 
		fields = '__all__'
		exclude = ('attach_file','is_subtitle')

	def __init__(self, *args, **kwargs):
		knowledge = kwargs.pop('knowledge')
		subject = knowledge.theme.subject	
		super(UpdateSupportfileForm, self).__init__(*args, **kwargs)
		instance = kwargs.pop('instance')
		knowledges = Knowledge.objects.filter(theme__subject= subject)
		self.fields['knowledge'] = forms.ModelChoiceField(queryset=knowledges) 
		self.fields['skills']  = forms.ModelMultipleChoiceField(queryset=Skill.objects.filter(subject=subject), required=False)

class AttachForm(forms.ModelForm):
	class Meta:
		model = Supportfile
		fields = ('attach_file','annoncement','is_subtitle')
		widgets = {
          'annoncement': forms.Textarea(attrs={'rows':1}),
        }




class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = '__all__'


	def __init__(self, *args, **kwargs):
		parcours = kwargs.pop('parcours')
		print(parcours)
		super(CourseForm, self).__init__(*args, **kwargs)
		relations = Relationship.objects.filter(exercise__supportfile__is_title = 1, parcours=parcours)
		print(relations)
		self.fields['relationships'] = forms.ModelMultipleChoiceField(queryset=relations, required=False )


class DemandForm(forms.ModelForm):
	class Meta:
		model = Demand
		fields = '__all__'



class MasteringForm (forms.ModelForm):
	class Meta:
		model = Mastering
		fields = '__all__'


	def __init__(self, *args, **kwargs):
		relationship = kwargs.pop('relationship')
		super(MasteringForm, self).__init__(*args, **kwargs)
		relations = Relationship.objects.filter(exercise__supportfile__is_title = 0, parcours=relationship.parcours)
		courses = Course.objects.filter(parcours=relationship.parcours)
		self.fields['practices'] = forms.ModelMultipleChoiceField(queryset=relations, widget=forms.CheckboxSelectMultiple,   required=False )
 

class MasteringDoneForm (forms.ModelForm):
	class Meta:
		model = Mastering_done
		fields = ('writing',)

 

class MasteringcustomForm (forms.ModelForm):
	class Meta:
		model = Masteringcustom
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		customexercise = kwargs.pop('customexercise')
		super(MasteringcustomForm, self).__init__(*args, **kwargs)
		relations = Relationship.objects.filter(exercise__supportfile__is_title = 0, parcours__in=customexercise.parcourses.filter(is_publish=1))
		courses = Course.objects.filter(parcours__in=customexercise.parcourses.filter(is_publish=1))
		self.fields['practices'] = forms.ModelMultipleChoiceField(queryset=relations, widget=forms.CheckboxSelectMultiple,   required=False )
 
class MasteringcustomDoneForm (forms.ModelForm):
	class Meta:
		model = Masteringcustom_done
		fields = ('writing',)




class WrittenanswerbystudentForm (forms.ModelForm):
	class Meta:
		model = Writtenanswerbystudent
		fields = ('imagefile','answer')



class CustomanswerbystudentForm (forms.ModelForm):
	class Meta:
		model = Customanswerbystudent
		fields = ('imagefile','answer')

class CustomexerciseForm (forms.ModelForm):
	
	class Meta:
		model = Customexercise
		fields = '__all__'

				
	def __init__(self, *args, **kwargs):
		parcours = kwargs.pop('parcours')
		teacher = kwargs.pop('teacher')

		super(CustomexerciseForm, self).__init__(*args, **kwargs)
		skills = Skill.objects.filter(subject__in = teacher.subjects.all())
		knowledges = Knowledge.objects.filter(theme__subject__in = teacher.subjects.all(), level__in = teacher.levels.all())
		parcourses = teacher.author_parcours.exclude(pk=parcours.id)
		students = parcours.students.all()

		self.fields['skills'] = forms.ModelMultipleChoiceField(queryset=skills,    required=False )
		self.fields['knowledges'] = forms.ModelMultipleChoiceField(queryset=knowledges,  required=False ) 
		self.fields['parcourses'] = forms.ModelMultipleChoiceField(queryset=parcourses,  required=False )  
		self.fields['students'] = forms.ModelMultipleChoiceField(queryset=students, widget=forms.CheckboxSelectMultiple,   required=False )
 


class  CustomexerciseNPForm (forms.ModelForm):

	class Meta:
		model = Customexercise
		fields = '__all__'

				
	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		custom = kwargs.pop('custom')
		super(CustomexerciseNPForm, self).__init__(*args, **kwargs)
		skills = Skill.objects.filter(subject__in = teacher.subjects.all())
		knowledges = Knowledge.objects.filter(theme__subject__in = teacher.subjects.all(), level__in = teacher.levels.all())
		students = custom.students.all() 
		self.fields['skills'] = forms.ModelMultipleChoiceField(queryset=skills,    required=False )
		self.fields['knowledges'] = forms.ModelMultipleChoiceField(queryset=knowledges,  required=False ) 
		self.fields['students'] = forms.ModelMultipleChoiceField(queryset=students, widget=forms.CheckboxSelectMultiple,   required=False )
		
