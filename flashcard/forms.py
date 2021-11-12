import datetime
from django import forms
from .models import Flashcard , Flashpack
from account.models import Student , Teacher
from socle.models import Knowledge, Skill
from group.models import Group
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
from django.forms import MultiWidget, TextInput , CheckboxInput
from django.template.defaultfilters import filesizeformat
from django.conf import settings

from itertools import groupby
from django.forms.models import ModelChoiceIterator, ModelChoiceField, ModelMultipleChoiceField

 
 

 

class FlashcardForm(forms.ModelForm):

	class Meta:
		model = Flashcard
		fields = '__all__'
		widgets = {
            'is_correct' : CheckboxInput(),  
        }


	def __init__(self, *args, **kwargs):
		flashpack = kwargs.pop('flashpack')
		super(FlashcardForm, self).__init__(*args, **kwargs)

		levels = flashpack.levels.all()
		themes = flashpack.themes.all()
		subject = flashpack.subject
		knowledges = []
		if len(levels) > 0 and len(themes) > 0  :
			knowledges = Knowledge.objects.filter(theme__subject = subject ,level__in=levels, theme__in=themes )
		elif len(levels) > 0 :
			knowledges = Knowledge.objects.filter(theme__subject = subject ,level__in=levels)
		elif len(themes) > 0 :
			knowledges = Knowledge.objects.filter(theme__subject = subject ,theme__in=themes)

		self.fields['knowledge'] = forms.ModelChoiceField(queryset=knowledges, required=False)


	def clean_content(self):
		content = self.cleaned_data['imagefile']
		validation_file(content)  
		audio_ = self.cleaned_data['audio']
		validation_file(audio_) 
		video_ = self.cleaned_data['video']
		validation_file(video_) 



class FlashpackForm(forms.ModelForm):
 
	class Meta:
		model = Flashpack
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		super(FlashpackForm, self).__init__(*args, **kwargs)
		parcours =  teacher.teacher_parcours.exclude(is_archive=1)
		all_folders = teacher.teacher_folders.all() 
		coteacher_parcours = teacher.coteacher_parcours.exclude(is_archive=1) 
		all_parcours = parcours|coteacher_parcours

		groups =  teacher.groups.all() 
		teacher_groups = teacher.teacher_group.all() 
		all_groups = groups|teacher_groups

		self.fields['levels']   = forms.ModelMultipleChoiceField(queryset=teacher.levels.all(), required=False)
		self.fields['subject']  = forms.ModelChoiceField(queryset=teacher.subjects.all(), required=False)	
		self.fields['groups']   = forms.ModelMultipleChoiceField(queryset=all_groups.order_by("teachers","level"), widget=forms.CheckboxSelectMultiple, required=True)
		self.fields['parcours'] = forms.ModelMultipleChoiceField(queryset = all_parcours.order_by("level"), widget=forms.CheckboxSelectMultiple,  required=False)
		self.fields['folders']  = forms.ModelMultipleChoiceField(queryset = all_folders.order_by("level"), widget=forms.CheckboxSelectMultiple,  required=False)
 

	def clean_content(self):
		content = self.cleaned_data['imagefile']
		validation_file(content) 
 
 