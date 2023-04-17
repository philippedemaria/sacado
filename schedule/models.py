from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime, time
from group.models import Group

class Calendar(models.Model):
    name         = models.CharField(_('name'), null=True, blank = True,  max_length=50)
    color        = models.CharField(_('color'), default='', max_length=50)
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank = True, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return "{}:{}".format(self.user,self.name)  


    class Meta:
        verbose_name = _('calendar')
        ordering = ['name']

class Event(models.Model):

    title         = models.CharField(_('title'), max_length=100)
    start         = models.DateTimeField(_('start'))
    end           = models.DateTimeField(_('end'))
    place         = models.CharField(_('Place'), null=True, blank=True,   default='',  max_length=100)      
    comment       = models.TextField( null=True, blank=True, verbose_name="Commentaire")      
    display       = models.BooleanField(default=0, verbose_name='Publication' ) 
    users         = models.ManyToManyField(settings.AUTH_USER_MODEL, default='',  blank=True, related_name='event_with', related_query_name="event_with",   verbose_name="Partagée avec")
    calendar      = models.ManyToManyField(Calendar,   blank=True , verbose_name="Calendrier" )
    color         = models.CharField(_('color'), default='#00819F', max_length=50)
    link          = models.PositiveIntegerField(default=0, editable=False) # id du type
    
    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = _('event')
        ordering = ['start', 'end']

class Automatic(models.Model):
    user   = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, related_name='user_automatic', on_delete=models.CASCADE) 
    module = models.CharField(max_length=255, blank=True, editable=False)
    insert = models.BooleanField(default=1, blank=True, editable=False) # Affichage par défaut
 
  
    def __str__(self):
        return "{} : {}".format(self.user, self.module) 



class Slotedt(models.Model):
    users   = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='my_slots_edt' )  
    start   = models.DateField(_('start'))
    slot    = models.PositiveIntegerField(default=1, editable=False) # id du type
    content = models.TextField( null=True, blank=True, verbose_name="Contenu")   
    groups  = models.ManyToManyField(Group, blank = True, related_name='slots_edt', editable=False)  
 
  
    def __str__(self):
        return "{} : {}".format(self.start,self.slot) 



  
class Edt(models.Model):

    DAYS = (("0","Lundi"),("1","Mardi"),("2","Mercredi"),("3","Jeudi"),("4","Vendredi"),("5","Samedi"),("6","Dimanche"))
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='edt', null=True, blank = True, on_delete=models.CASCADE, editable=False)
    is_slot     = models.BooleanField(default=0) 
    start_class = models.CharField( default="8:00" ,blank = True, max_length=5)
    slots       = models.ManyToManyField(Slotedt, blank = True, related_name='edts', editable=False) 
    start       = models.DateTimeField(_('start'))
    stop        = models.DateTimeField(_('stop'))
    days_on     = models.CharField( default="Lundi-Mardi-Mercredi-Jeudi-Vendredi-Samedi" ,max_length=250,editable=False)
    first_day   = models.CharField( default="0",choices=DAYS ,max_length=250)
    is_share    = models.BooleanField(default=1) # Mutualiser les progressions

    def __str__(self):
        return "Edt:{}".format(self.user)  


    def this_day_slot(self,slot,day):
        template_edts = self.template_edts.filter(slot=slot,day=day)
        data = {}
        if template_edts :
            boolean = True
            tedt = template_edts.first() 
            group = tedt.groups.first() 
            if tedt.is_half : data["group_name"] = "1sem/2 : "+ group.name
            else : data["group_name"] =  group.name
            data["group_id"] =  group.id
            data["style"] = "background-color:"+group.color+";color:white;text-align:center"
             
        else :
            boolean = False

        data["boolean"] = boolean
        return data

class Template_edt(models.Model):

    edt     = models.ForeignKey(Edt, related_name='template_edts',   blank = True, on_delete=models.CASCADE, editable=False)
    slot    = models.PositiveIntegerField(default=1, editable=False)
    day     = models.PositiveIntegerField(default=1, editable=False)
    groups  = models.ManyToManyField(Group, blank = True, related_name='template_edts', editable=False)  
    is_half = models.BooleanField(default=0)

    def __str__(self):
        g_str=""
        for g in self.groups.all():
            g_str += g.name+" "
        return "slot:{}, day:{}, groupes :{}".format(self.slot,self.day,g_str)

 