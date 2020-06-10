from django import forms
from .models import School, Country 

 



class SchoolForm(forms.ModelForm):


    class Meta:
    	model = School
    	fields = '__all__'



class CountryForm(forms.ModelForm):


    class Meta:
    	model = Country
    	fields = '__all__'
        
