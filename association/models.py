from django.db import models
from datetime import date
from ckeditor_uploader.fields import RichTextUploadingField
from account.models import User , ModelWithCode
from django.apps import apps
from django.utils import   timezone
from django.db.models import Q
from school.models import School , Country 
# Pour créer un superuser, il faut depuis le shell taper :
# from account.models import User
# User.objects.create_superuser("admin","admin@gmail.com","motdepasse", user_type=0).save()

QUALITIES = (
        ("actif", 'membre actif'),    
        ("honneur", "membre d'honneur"),
        ("bienfaiteur", 'membre bienfaiteur'),    
        ("bénéficiaire", "membre bénéficiaire"),
    )



YEARS = []


class Rate(models.Model):
    """
    Modèle représentant les tarifs.
    """
    amount    = models.DecimalField(default=0, blank=True , max_digits=10, decimal_places=2, verbose_name="Tarif")
    discount    = models.DecimalField(default=0, blank=True , max_digits=10, decimal_places=2, verbose_name="Réduction" )
    quantity  = models.PositiveIntegerField(default=0,  verbose_name="Nombre d'élèves")
    year      = models.CharField(max_length=255, default='',  verbose_name="Année")
    is_active = models.BooleanField(default=0,  verbose_name="Année active")

    def __str__(self):
        return "{} {}, {}".format(self.amount, self.quantity, self.year)






class Associate(models.Model):
    """
    Modèle représentant un associé.
    """
    user = models.ForeignKey(User, blank=True, default=True, null=True,   related_name="associated", verbose_name="Membre inscrit",  on_delete=models.CASCADE)
    quality = models.CharField(max_length=255, default='', choices=QUALITIES, verbose_name="Qualité")
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=0, editable=False)

    first_name   = models.CharField(max_length=255,  blank=True,default='', null=True,   verbose_name="Nom")
    last_name = models.CharField(max_length=255,  blank=True, default='' , null=True, verbose_name="Prénom")
    email = models.CharField(max_length=255,  blank=True, default='', null=True,  verbose_name="Email")
    observation = RichTextUploadingField( blank=True, default="", null=True, verbose_name="Remarque") 


    def __str__(self):
        lname = self.user.last_name.capitalize()
        fname = self.user.first_name.capitalize()

        return "{} {}, {}".format(lname, fname, quality)


    def has_vote(self, user) :
        my_vote = False
        if self.voting.filter(user = user) :
            my_vote = self.voting.get(user = user)
        return my_vote

    def ratio(self) :
        s = self.voting.count()
        v = 4
        r = self.voting.filter(choice=1).count()
        data = {}
        if s > 0 :
            rat = r / v * 100
            data["rate"] = str(r) +"/" +str(v)+ " = "  + str(rat) + "%"
        else :
            data["rate"] = "en attente"
        data["fin"] = ""
        if s == 4 :
            data["fin"] = " fin du scrutin"
        return data




class Voting(models.Model):
    """
    Modèle représentant un associé.
    """
    associate = models.ForeignKey(Associate, blank=True, related_name="voting", on_delete=models.CASCADE)
    choice = models.BooleanField(default=0, verbose_name="vote")
    justification = models.CharField(max_length=255, default='', blank=True ,  verbose_name="justification (facultatif)")
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, related_name="votant", on_delete=models.CASCADE, editable=False)

    def __str__(self):
        lname = self.associated.user.last_name.capitalize()
        fname = self.associated.user.first_name.capitalize()

        return "{} {}".format(choice)

    class Meta:
        unique_together = ('associate', 'user')

 
class Accounting(ModelWithCode):
    """ Accounting   """
 
    amount = models.DecimalField(default=0, blank=True , max_digits=10, decimal_places=2, editable=False)
    is_credit = models.BooleanField(default=0, )
    objet = models.CharField(max_length=255, verbose_name="Objet*")

    beneficiaire = models.CharField(max_length=255, blank=True, verbose_name="En faveur de")
    address = models.CharField(max_length=255, blank=True, verbose_name="Adresse")
    complement = models.CharField(max_length=255, blank=True, verbose_name="Complément d'adresse")
    town = models.CharField(max_length=255, blank=True, verbose_name="Complément d'adresse")
    country = models.ForeignKey(Country, related_name="accontings", blank=True,  null=True,  on_delete=models.SET_NULL, verbose_name="Pays")
    contact = models.CharField(max_length=255, blank=True ,  verbose_name="Contact")

    school = models.ForeignKey(School, related_name="accontings", blank=True, null=True,  on_delete=models.CASCADE, verbose_name="Etablissement")  

    observation = RichTextUploadingField( blank=True, default="", null=True, verbose_name="Observation")

    acting = models.DateTimeField(null=True, blank=True, verbose_name="Date d'effet")
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="accontings", null=True, blank=True,  on_delete=models.CASCADE, editable=False)
    is_active = models.BooleanField(default=0, verbose_name="Actif")


    def __str__(self):
        return self.beneficiaire


    def school_contact(self):
        cs = self.school.users.filter(is_extra=1)
        return  cs

 
class Detail(models.Model):
    """ detail d'un Accounting   """
 
    accounting  = models.ForeignKey(Accounting, related_name="details", on_delete=models.CASCADE, verbose_name="Pays")
    description = models.CharField(max_length=255, blank=True ,   verbose_name="Description")
    amount      = models.DecimalField(default=0, blank=True , max_digits=10, decimal_places=2)
 
    def __str__(self):
        return self.accounting








########################################################################################################################################### 
########################################################################################################################################### 
############################################################   Documents    ############################################################### 
########################################################################################################################################### 
########################################################################################################################################### 

class Section(models.Model): # pour l'asso' 

    title = models.CharField(max_length=255, default='',  blank=True, verbose_name="Titre")    
 
 
    def __str__(self):
        return self.title 


class Document(models.Model): # pour l'asso' 

 
    title = models.CharField(max_length=255, default='',  blank=True, verbose_name="Titre")    
    annoncement = RichTextUploadingField( blank=True, verbose_name="Texte*") 
    user = models.ForeignKey(User, related_name = "documents", on_delete=models.CASCADE, editable=False )
    section = models.ForeignKey(Section, related_name = "sections", on_delete=models.CASCADE, verbose_name="Section") 
    ranking = models.PositiveIntegerField(  default=0,  blank=True, null=True,  verbose_name="Ordre", editable=False )

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification") 
 
 
    def __str__(self):
        return self.title 






########################################################################################################################################### 
########################################################################################################################################### 
############################################################  Abonnement    ############################################################### 
########################################################################################################################################### 
########################################################################################################################################### 



class Abonnement(models.Model):

    school     = models.ForeignKey(School, on_delete=models.CASCADE, related_name='abonnement', editable=False)
    date_start = models.DateTimeField(verbose_name="Date de début", editable=False)
    date_stop  = models.DateTimeField(verbose_name="Date de fin", editable=False)
    accounting = models.ForeignKey(Accounting, on_delete=models.CASCADE, related_name='abonnement', editable=False)
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='abonnement', editable=False)
    gar_active = models.BooleanField(default=0, verbose_name="Actif au GAR")

    def __str__(self):
        return "{}".format(self.school.name)