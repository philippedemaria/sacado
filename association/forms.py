from django import forms
from .models import Accounting , Voting , Associate, Document , Section



class AccountingForm(forms.ModelForm):
    class Meta:
        model = Accounting 
        fields = '__all__' 



class AssociateForm(forms.ModelForm):
    class Meta:
        model = Associate
        fields = '__all__' 


 
class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting 
        fields = '__all__' 

 
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document 
        fields = '__all__'  

 
class SectionForm(forms.ModelForm):
    class Meta:
        model = Section 
        fields = '__all__' 