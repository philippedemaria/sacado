from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime, time

class Calendar(models.Model):
    name = models.CharField(_('name'), null=True, blank = True,  max_length=50)
    color = models.CharField(_('color'), default='', max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank = True, on_delete=models.CASCADE, editable=False)


    def __str__(self):
        return "{}:{}".format(self.user,self.name)  


    class Meta:
        verbose_name = _('calendar')
        ordering = ['name']



class Event(models.Model):
    title = models.CharField(_('title'), max_length=100)
    start = models.DateTimeField(_('start'))
    end = models.DateTimeField(_('end'))
    is_allday = models.BooleanField(_('is_allday?'), default=False, blank=True)
    notification = models.BooleanField(_('Notification?'), default=False, blank=True)
    notification_day = models.PositiveIntegerField(default=False, blank=True)
    place = models.CharField(_('Place'), null=True, blank=True,   default='',  max_length=100)      
    comment =  models.TextField( null=True, blank=True, verbose_name="Commentaire")      
    display = models.BooleanField(default=0, verbose_name='Publication' ) 
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, default='',  blank=True, related_name='event_with', related_query_name="event_with",   verbose_name="Partagée avec")
    calendar = models.ManyToManyField(Calendar,   blank=True , verbose_name="Calendrier" )
    color = models.CharField(_('color'), default='#00819F', max_length=50)
    type_of_event = models.PositiveIntegerField(default=0, editable=False) # 0 sans type, 1 tache, 2 visite de classe, 3 animation, 4 stage
    link = models.PositiveIntegerField(default=0, editable=False) # id du type
    
    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = _('event')
        ordering = ['start', 'end']




class Automatic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, related_name='user_automatic', on_delete=models.CASCADE) # La liaison OneToOne vers le modèle User2
    module = models.CharField(max_length=255, blank=True, editable=False)
    insert = models.BooleanField(default=1, blank=True, editable=False) # Affichage par défaut
 
  
    def __str__(self):
        return "{} : {}".format(self.user, self.module) 
