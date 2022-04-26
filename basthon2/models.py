from django.db import models
from qcm.models import Parcours,Criterion
from account.models import Student, Teacher, ModelWithCode, generate_code, User
from ckeditor_uploader.fields import RichTextUploadingField
from socle.models import  Knowledge, Level , Theme, Skill , Subject
import os.path

def vignette_directory_path(instance, filename):
    return "vignettes/{}/{}".format(instance.teacher.user.id, filename)

class ExoPython(models.Model):
    title  = models.CharField(max_length=255,null=True,blank=True, verbose_name="titre")
    instruction = RichTextUploadingField( verbose_name="Consigne*") 
    preambule_cache =  models.TextField(null=True,blank=True,verbose_name="preambule caché")
    preambule_visible =  models.TextField(null=True,blank=True,verbose_name="preambule visible")
    prog_cor = models.TextField(  blank=True, null=True,  verbose_name="Corrigé (programme)")
    # test avec réponse fournie
    test_rep_entree=models.TextField(null=True,blank=True,verbose_name="entree test avec reponse")
    test_rep_sortie=models.TextField(null=True,blank=True,verbose_name="sortie test avec reponse")
    #  auto test : les reponses sont celles que donnera les programmes du champs 'prog_cor'
    autotest = models.TextField(null=True,blank=True,verbose_name="entree autotest")
    #-----------
    teacher = models.ForeignKey(Teacher, related_name="teacherexoPython", blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    #### pour donner une date de remise - Tache     
    start = models.DateTimeField(null=True, blank=True, verbose_name="A partir de")
    date_limit = models.DateTimeField(null=True, blank=True, verbose_name="Date limite du rendu")
    lock = models.DateTimeField(null=True, blank=True, verbose_name="Verrouillé dès le")

    imagefile = models.ImageField(upload_to=vignette_directory_path, blank=True, verbose_name="Vignette d'accueil", default="")

    duration = models.PositiveIntegerField(default=15, blank=True, verbose_name="Durée (min.)")
    
    skills = models.ManyToManyField(Skill, blank=True, related_name='skillexoPython', verbose_name="Compétences évaluées")
    knowledges = models.ManyToManyField(Knowledge, blank=True, related_name='knowledgeexoPython', verbose_name="Savoir faire évalués")
    parcourses = models.ManyToManyField(Parcours, blank=True, related_name='parcoursexoPython', verbose_name="Parcours attachés")
    students = models.ManyToManyField(Student, blank=True, related_name='studentsexoPython' )   
    
    is_share = models.BooleanField(default=0, verbose_name="Mutualisé ?")
    is_realtime = models.BooleanField(default=0, verbose_name="Temps réel ?")

    is_mark = models.BooleanField(default=0, verbose_name="Notation ?")
    is_collaborative = models.BooleanField(default=0, verbose_name="Collaboratif ?")

    is_autocorrection = models.BooleanField(default=0, verbose_name="Autocorrection ?")
    criterions = models.ManyToManyField(Criterion, blank=True, related_name='criteres' )    

    mark = models.PositiveIntegerField(default=0, verbose_name="Sur ?")
    is_publish = models.BooleanField(default=0, verbose_name="Publié ?")
    ranking = models.PositiveIntegerField(  default=0,  blank=True, null=True, editable=False)

    text_cor = RichTextUploadingField(  blank=True, null=True,  verbose_name="Correction écrite") 
    file_cor = models.ImageField(upload_to=vignette_directory_path, blank=True, verbose_name="Fichier de correction", default="")
    video_cor = models.CharField(max_length = 100, blank=True, verbose_name="Code de la vidéo Youtube", default="")
    is_publish_cor = models.BooleanField(default=0, verbose_name="Publié ?")    
    def __str__(self):
        return self.title
	
