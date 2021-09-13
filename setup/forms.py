from django import forms
from socle.models import Skill, Waiting, Knowledge  
from .models import Formule , Webinaire 

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



class FormuleForm(forms.ModelForm):

    class Meta:
        model = Formule 
        fields = ('price',)


class WebinaireForm(forms.ModelForm):

    class Meta:
        model = Webinaire 
        fields = '__all__'
        exclude = ('users',)

