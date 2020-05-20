from django import forms 
from socle.models import   Theme, Knowledge, Level

 
class ThemeForm(forms.ModelForm):
	class Meta:
 		model = Theme  
 		fields = '__all__'


class KnowledgeForm(forms.ModelForm):
	class Meta:
 		model = Knowledge  
 		fields = '__all__'

 

class LevelForm(forms.ModelForm):
	class Meta:
 		model = Level  
 		fields = '__all__'


class MultiKnowledgeForm(forms.ModelForm):

	name = forms.CharField( widget=forms.Textarea )
	class Meta:
 		model = Knowledge  
 		fields = '__all__'