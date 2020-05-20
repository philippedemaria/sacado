from django import forms
from socle.models import Skill, Waiting, Knowledge  
 

class SkillForm(forms.ModelForm):

 
	class Meta:
		model = Skill 
		fields = '__all__'


class WaitingForm(forms.ModelForm):

    class Meta:
        model = Waiting 
        fields = '__all__'
 

 

 

class KnowledgeForm(forms.ModelForm):

    
    class Meta:
        model = Knowledge 
        fields = '__all__'


 