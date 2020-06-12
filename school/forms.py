from django import forms
from .models import School, Country 

 



class SchoolForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all().order_by("name") )


    class Meta:
    	model = School
    	fields = '__all__'



class CountryForm(forms.ModelForm):


    class Meta:
    	model = Country
    	fields = '__all__'
        
