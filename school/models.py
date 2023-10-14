from django.db import models
from django.utils import timezone
from django.apps import apps
from datetime import datetime , timedelta
from django.db.models import Q



def image_directory_path(instance, filename):
    return "schools/{}".format(filename)


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom") 
 
    def __str__(self):
        return self.name


class Town(models.Model):
    name     = models.CharField(max_length=255, verbose_name="Nom") 
    country  = models.ForeignKey(Country, default='', blank=True, related_name='towns', related_query_name="towns", on_delete=models.PROTECT, verbose_name="Pays")
    zip_code = models.CharField(max_length=255, default='99999', blank=True, verbose_name="Code postal")

    def __str__(self):
        return "{} - {} ".format(self.name,  self.country.name)



class School(models.Model):

    NB_STUDENTS = (
        (150, "moins de 150 - Version gratuite"),
        (500, "Entre 150 et 500 : 100 €"),
        (1000, "Entre 500 et 1000 : 200 €"),
        (1500, "Entre 1000 et 1500 : 300 €"),
        (2000, "Entre 1500 et 2000 : 400 €"),
        (2500, "Entre 2000 et 2500 : 500 €"),
        (3000, "Entre 2500 et 3000 : 600 €"),
        (3500, "Entre 3000 et 3500 : 700 €"),
        (4000, "Entre 3500 et 4000 : 800 €"),
        (4500, "Entre 4000 et 4500 : 900 €"),
        (10000, "+ de 4500 : 1000 €"),
    )

  
    name                = models.CharField(max_length=255, verbose_name="nom")
    country             = models.ForeignKey(Country, default='', blank=True, related_name='school', related_query_name="school", on_delete=models.PROTECT, verbose_name="Pays")
    town                = models.CharField(max_length=255, default='', verbose_name="ville")
    code_acad           = models.CharField(max_length=255, default='999efe',   verbose_name="Code UAI")
    address             = models.CharField(max_length=255, blank=True, verbose_name="Adresse")
    complement          = models.CharField(max_length=255, blank=True, verbose_name="Complément d'adresse")
    zip_code            = models.CharField(max_length=255, default='99999', blank=True, verbose_name="Code postal")
    get_seconde_to_comp = models.BooleanField(default=0,   editable=False)# L'établissement a récupéré le groupe prépa math comp
    nbstudents          = models.PositiveIntegerField(default=150, choices=NB_STUDENTS, verbose_name="Nombre d'élèves")
    rythme              = models.BooleanField(default=1, verbose_name="Rythme")# Nord ou Sud
    is_active           = models.BooleanField(default=0,   editable=False)
    gar                 = models.BooleanField(default=0, verbose_name="Connexion via le GAR souhaitée")
    logo                = models.ImageField(upload_to=image_directory_path, verbose_name="Logo de l'établissement", blank=True, default="")
    comment             = models.TextField( verbose_name="Commentaire", blank=True, default="")
    resiliation         = models.TextField( verbose_name="Motif de Résiliation", blank=True, default="")
    tiers               = models.PositiveIntegerField(default=411 ,  editable=False)
    is_primaire         = models.BooleanField(default=1 ,   editable=False)
    is_managing         = models.PositiveIntegerField(default=1 ,   editable=False)

    def __str__(self):
        return "{} - {} - {}".format(self.name, self.town, self.country.name)

    def student_and_teacher(self):
        nbt, nbs = 0, 0
        for u in self.users.all():
            if u.is_teacher:
                nbt += 1
            elif u.is_student:
                nbs += 1
        nb = {"nbt": nbt, "nbs": nbs}
        return nb



    def admin(self):
        users = self.users.filter(is_manager = 1).order_by("last_name")
        return users


    def teachers(self):
        users = self.users.filter(user_type = 2).order_by("last_name")
        return users


    def teachers_exclude_myself(self,user):
        listing = list()
        users = self.users.filter(user_type = 2).exclude(pk=user.id).order_by("last_name")
        for u in users :
            try : 
                if u.edt.is_share : listing.append(u)
            except : pass
        return listing



    def get_data(self) :

        Group = apps.get_model('group', 'Group')
        nbg = Group.objects.filter(Q(teacher__user__school=self)|Q(teacher__user__schools=self)).count()
        try:
            stage = self.aptitude.first()
            if stage:
                eca, ac, dep , low , medium , up  = stage.medium - stage.low, stage.up - stage.medium, 100 - stage.up , stage.low , stage.medium , stage.up 
            else:
                eca, ac, dep , low , medium , up   = 20, 15, 15 , 50 , 70, 85 
        except:
            eca, ac, dep , low , medium , up  = 20, 15, 15 , 50 , 70, 85


        nbt, nbs = 0, 0
        for u in self.users.exclude(username__contains="_e-test"):
            if u.is_teacher:
                nbt += 1
            elif u.is_student:
                nbs += 1
        data_nb = {"nbt": nbt, "nbs": nbs}

        data_nb.update({"nbg": nbg , "low": low , "eca": eca, "ac": ac , "dep": dep, "medium": medium , "up": up , "nbs_max": self.nbstudents  })
 
        return data_nb



    def fee(self):
        """ cotisation pour un établissement suivant le nombre de ses élèves"""
        if self.nbstudents < 150 : f = 0
        elif self.nbstudents < 500 : f = 100
        elif self.nbstudents < 1000 : f = 200
        elif self.nbstudents < 1500 : f = 300
        elif self.nbstudents < 2000 : f = 400
        elif self.nbstudents < 2500 : f = 500
        elif self.nbstudents < 3000 : f = 600
        elif self.nbstudents < 4000 : f = 700
        elif self.nbstudents < 4500 : f = 800
        else : f = 900
        return f


    def adhesion(self) : 
        today = datetime.now()
        return self.abonnement.filter( date_start__lte=today , date_stop__gte=today ).count()


    def active_accounting(self) :
        today = datetime.now()
        try :
            abonnement  = self.abonnement.filter( date_start__lte = today , date_stop__gte = today ).last()
            account = abonnement.accounting
        except :
            account  = False
        return account
 
class Stage(models.Model):
    """" Niveau d'aquisition """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='aptitude', editable=False)
    low = models.PositiveIntegerField(default=50, verbose_name="Seuil 1 : NA à ECA")
    medium = models.PositiveIntegerField(default=70, verbose_name="Seuil 2 : ACE à acquis")
    up = models.PositiveIntegerField(default=85, verbose_name="Seuil 3 : acquis à dépassé")

    def __str__(self):
        return "seuils d'aquisition {}".format(self.school.name)

 

 