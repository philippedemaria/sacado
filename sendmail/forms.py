from django import forms
from sendmail.models import Email, Communication
from account.models import User
from django.forms import models
from django.forms.fields import MultipleChoiceField
 

class EmailForm(forms.ModelForm):

	class Meta:
		model = Email
		fields = ('subject','texte'  )
    
 
 
	def clean(self):
		cleaned_data = super().clean()

		texte = cleaned_data.get("texte")
		subject = cleaned_data.get("subject")

		if texte == "" or subject == ""  :
			msg = "Ces champs ne peuvent être vides"
			self.add_error('texte', msg)
			self.add_error('subject', msg)



class CommunicationForm(forms.ModelForm):

	class Meta:
		model = Communication
		fields = '__all__'