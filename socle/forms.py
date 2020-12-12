from django import forms 
from socle.models import   Theme, Knowledge, Level, Skill, Waiting
 

 
 


class ThemeForm(forms.ModelForm):
	class Meta:
 		model = Theme  
 		fields = '__all__'


class KnowledgeForm(forms.ModelForm):
	class Meta:
 		model = Knowledge  
 		fields = '__all__'


class WaitingForm(forms.ModelForm):
	class Meta:
 		model = Waiting  
 		fields = '__all__' 



class SkillForm(forms.ModelForm):
	class Meta:
 		model = Skill  
 		fields = '__all__' 

class LevelForm(forms.ModelForm):
 
	class Meta:
 		model = Level  
 		fields = '__all__'


	def __init__(self, *args, **kwargs):
		super(LevelForm, self).__init__(*args, **kwargs)
		themes = Theme.objects.all()
 
		self.fields['themes'] = forms.ModelMultipleChoiceField(queryset=themes, widget=forms.CheckboxSelectMultiple, required=False)



class MultiWaitingForm(forms.ModelForm):

	name = forms.CharField( widget=forms.Textarea )
	class Meta:
 		model = Waiting  
 		fields = '__all__'


 		

class MultiKnowledgeForm(forms.ModelForm):

	name = forms.CharField( widget=forms.Textarea )
	class Meta:
 		model = Knowledge  
 		fields = '__all__'



class MultiSkillForm(forms.ModelForm):

	name = forms.CharField( widget=forms.Textarea )
	class Meta:
 		model = Skill  
 		fields = '__all__'