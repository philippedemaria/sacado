import datetime
from django import forms
from .models import Flashcard , Flashpack , Commentflashcard
from account.models import Student , Teacher
from socle.models import Waiting, Skill
from group.models import Group
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
from django.forms import MultiWidget, TextInput , CheckboxInput
from django.template.defaultfilters import filesizeformat
from django.conf import settings

from itertools import groupby
from django.forms.models import ModelChoiceIterator, ModelChoiceField, ModelMultipleChoiceField

 
def validation_file(content):
	if content :
		content_type = content.content_type.split('/')[0]
		if content_type in settings.CONTENT_TYPES:
			if content._size > settings.MAX_UPLOAD_SIZE:
				raise forms.ValidationError("Taille max : {}. Taille trop volumineuse {}".format(filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
		else:
			raise forms.ValidationError("Type de fichier non accepté")
		return content

 

class FlashcardForm(forms.ModelForm):

	class Meta:
		model = Flashcard
		fields = '__all__'


	def __init__(self, *args, **kwargs):
		flashpack = kwargs.pop('flashpack')
		super(FlashcardForm, self).__init__(*args, **kwargs)
		if flashpack : 
			try :
				themes = flashpack.themes.all()
				waitings = []
				if  len(themes) > 0  :
					waitings = Waiting.objects.filter(theme__in = themes )
			except :
				waitings = Waiting.objects.all()
		else :
			waitings = Waiting.objects.all()
		try :
			self.fields['waiting'] = forms.ModelChoiceField(queryset=waitings )

		except :
			pass
		self.fields['waiting'].required = False

	def clean_content(self):
		content = self.cleaned_data['imagefile']
		validation_file(content)  
		audio_ = self.cleaned_data['audio']
		validation_file(audio_) 
		video_ = self.cleaned_data['video']
		validation_file(video_)

	def html(self) :
		context = { "obj" :self ,}
		return render_to_string("flashcard/form_flashcard_tag.html", context)



class FlashpackForm(forms.ModelForm):
 
	class Meta:
		model = Flashpack
		exclude = ('flashcards',)

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher')
		folder  = kwargs.pop('folder')
		group   = kwargs.pop('group')

		super(FlashpackForm, self).__init__(*args, **kwargs)
		

		if group : all_folders = group.group_folders.filter(is_archive=0,is_trash=0)
		else : all_folders = teacher.teacher_folders.filter(is_archive=0,is_trash=0) 
		
		

		if folder : parcours = folder.parcours.filter(is_archive=0,is_trash=0)
		else : parcours =  teacher.teacher_parcours.filter(is_archive=0,is_trash=0)

		coteacher_parcours = teacher.coteacher_parcours.filter(is_archive=0,is_trash=0) 
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
 


class FlashpackAcademyForm(forms.ModelForm):


	class Meta:
		model = Flashpack
		exclude = ('flashcards',)
 

 

	def clean_content(self):
		content = self.cleaned_data['imagefile']
		validation_file(content) 







class CommentflashcardForm(forms.ModelForm):

	class Meta:
		model = Commentflashcard
		fields = ('comment',)


