from django.db import models
from django.utils import timezone
from django.apps import apps
from datetime import datetime , timedelta


 

class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom") 
 

    def __str__(self):
        return  self.name 



class School(models.Model):
    name = models.CharField(max_length=255, verbose_name="nom") 
     
    country = models.ForeignKey(Country, default='',  blank=True, related_name='school', related_query_name="school", on_delete=models.CASCADE ,  verbose_name="Pays") 
    town = models.CharField(max_length=255, default='',   verbose_name="ville")  
    
 

    
    def __str__(self):
        return "{0} - {1}".format(self.name, self.town)


 

 