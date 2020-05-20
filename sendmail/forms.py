from django import forms
from sendmail.models import Email, Communication
from account.models import User
from django.forms import models
from django.forms.fields import MultipleChoiceField
 

class EmailForm(forms.ModelForm):

	class Meta:
		model = Email
		fields = ('subject','texte'  )
    


class CommunicationForm(forms.ModelForm):

	class Meta:
		model = Communication
		fields = '__all__'