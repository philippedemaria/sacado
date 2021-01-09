from django import forms
from .models import Accounting , Voting , Associate



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


  