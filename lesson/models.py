from account.models import User  
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime, time

 


class Event(models.Model):

    user = models.ForeignKey(User, null=True, blank = True, related_name='events' , on_delete=models.CASCADE, editable=False)    
    title = models.CharField(_('title'), max_length=100)
    start = models.DateTimeField(_('start'))
    end = models.DateTimeField(_('end'))
    notification = models.BooleanField(_('Notification?'), default=False, blank=True) 
    comment =  models.TextField( null=True, blank=True, verbose_name="Commentaire")      
    display = models.BooleanField(default=0, verbose_name='Publication' ) 
    users = models.ManyToManyField(User, default='',  blank=True, related_name='these_events', related_query_name="these_events",   verbose_name="Partagée avec")
    color = models.CharField(_('color'), default='#00819F', max_length=50)
    url = models.CharField(_('url'), null=True,  blank=True,  max_length=250)


    def __str__(self):
        return "{}".format(self.title)  

    class Meta:
        verbose_name = _('event')
        ordering = ['start', 'end']