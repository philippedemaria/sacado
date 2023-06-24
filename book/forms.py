from django import forms
from django.conf import settings 
from django.template.defaultfilters import filesizeformat
from django.forms.models import inlineformset_factory, BaseInlineFormSet , ModelChoiceIterator, ModelChoiceField, ModelMultipleChoiceField

from .models import  *
from tool.models import Quizz
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
from itertools import groupby
from general_fonctions import *

import datetime
# def validation_file(content):
#     if content :
# 	    content_type = content.content_type.split('/')[0]
# 	    if content_type in settings.CONTENT_TYPES:
# 	        if content._size > settings.MAX_UPLOAD_SIZE: 
# 	            raise forms.ValidationError("Taille max : {}. Taille trop volumineuse {}".format(filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
# 	    else:
# 	        raise forms.ValidationError("Type de fichier non accepté")
# 	    return content


 
class BookForm(forms.ModelForm):

	class Meta:
		model = Book
		exclude = ("groups",)



class NewChapterForm(forms.ModelForm):

	class Meta:
		model = Chapter
		fields = ("title",)



class ChapterForm(forms.ModelForm):

	class Meta:
		model = Chapter
		fields = '__all__'
 

 
class SectionForm(forms.ModelForm):

	class Meta:
		model = Section
		fields = ('title','color')
 

class DocumentForm(forms.ModelForm):

	class Meta:
		model = Document
		fields = ('title','content','file','url','is_publish','is_share',)
 


class PageForm(forms.ModelForm):

	class Meta:
		model = Page
		fields = '__all__'
 


class TypeblocForm(forms.ModelForm):

	class Meta:
		model = Typebloc
		fields = '__all__'


 
class ParagraphForm(forms.ModelForm):

	class Meta:
		model = Paragraph
		fields = '__all__'
 

class BlocForm(forms.ModelForm):

	class Meta:
		model = Bloc
		fields = '__all__'

	def __init__(self, *args, **kwargs):

		print(kwargs)

		book = kwargs.pop('book')
		page = kwargs.pop('page')

		super(BlocForm, self).__init__(*args, **kwargs)
		level   = book.level
		subject = book.subject
		paragraphs = page.paragraphs.order_by("ranking")


		thms       = level.themes.all()
		skills     = Skill.objects.filter(subject=subject) 
		knowledges = level.knowledges.filter(theme__subject=subject)
		exercises  = level.exercises.filter(theme__subject=subject)
		exotexs    = level.level_exotexs.filter(theme__subject=subject)

		self.fields['paragraph'] = forms.ModelChoiceField(queryset=paragraphs)  

		self.fields['knowledge']  = forms.ModelChoiceField(queryset=knowledges,  required=False)  
		self.fields['theme']      = forms.ModelChoiceField(queryset=thms,  required=False)
		self.fields['skills']     = forms.ModelMultipleChoiceField(queryset=skills, required=False)
		self.fields['knowledges'] = forms.ModelMultipleChoiceField(queryset=knowledges,  required=False)  

		self.fields['exercises']  = forms.ModelMultipleChoiceField(queryset=exercises,  required=False) 
		self.fields['exotexs']    = forms.ModelMultipleChoiceField(queryset=exotexs,  required=False)  




class QFlashBookForm(forms.ModelForm):
 
	class Meta:
		model = Quizz
		fields = ('title','nb_slide','is_result','is_publish','subject','levels')

	def __init__(self, *args, **kwargs):
		book = kwargs.pop('book')
		super(QFlashBookForm, self).__init__(*args, **kwargs)

		self.fields['subject'].initial  = book.subject 
		self.fields['levels'].initial  = book.level 


