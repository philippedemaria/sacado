from django import forms
from django.conf import settings 
from django.template.defaultfilters import filesizeformat
from django.forms.models import inlineformset_factory, BaseInlineFormSet , ModelChoiceIterator, ModelChoiceField, ModelMultipleChoiceField

from .models import  *
 
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
		fields = ('title',)
 

class DocumentForm(forms.ModelForm):

	class Meta:
		model = Document
		fields = ('title','content','file','url','is_publish','is_share',)
 
 