from django.db import models

from django.db import models

from account.models import Teacher
from bibliotex.models import Bibliotex , Exotex
from flashcard.models import Flashpack , Flashcard
from group.models import Group
from qcm.models import Course, Exercise
from tool.models import Quizz, Question
from socle.models import Level , Subject , Skill , Knowledge , Theme

from django.utils import formats, timezone
from datetime import datetime, timedelta       
import uuid

def image_book_path(instance,filename):
    return "book/{}/{}".format(instance.id,filename)


def document_path(author,filename):
    return "chapter/{}/{}".format(author.user.id,filename)



class Book(models.Model):

    title         = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")
    author        = models.ForeignKey(Teacher, on_delete=models.CASCADE,  blank=True,   related_name='author_books', verbose_name="Enseignant", editable= False)
    teachers      = models.ManyToManyField(Teacher, related_name="teacher_books", blank=True,  verbose_name="Participants", editable= False)
    level         = models.ForeignKey(Level, on_delete=models.CASCADE,  related_name='books', verbose_name="Niveau")
    subject       = models.ForeignKey(Subject, on_delete=models.CASCADE,  related_name='books', verbose_name="Enseignement")

    is_publish   = models.BooleanField(default=0, verbose_name="Publié ?")
    is_share     = models.BooleanField(default=0, verbose_name="Mutualisé ?")

    is_student    = models.BooleanField(default=0, verbose_name="Livre élève ?")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    texte         = models.TextField( null=True, blank=True,  verbose_name="Texte")      
    date_created  = models.DateTimeField( auto_now_add= True)
    groups        = models.ManyToManyField(Group, blank=True, related_name='books', verbose_name="Groupes")
    imagefile     = models.ImageField(upload_to=image_book_path, blank=True,  verbose_name="Fichier", default="")
    ranking       = models.PositiveIntegerField( default=0,  blank=True, null=True)
    price         = models.DecimalField( decimal_places=2, default=6, max_digits=4, blank=True, null=True) 
 
    def __str__(self):
        return "{}".format(self.title)




class Section(models.Model):

	title   = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")
	ranking = models.PositiveIntegerField( default=0)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default="2480" , related_name='sections', verbose_name="teacher")

	def __str__(self):
	    return "{}".format(self.title )





class Document(models.Model):
 
	title    = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")
	section  = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True,  related_name='documents', verbose_name="Type de document")

	author   = models.ForeignKey(Teacher, on_delete=models.CASCADE,  blank=True,null=True,  related_name='author_documents', verbose_name="Auteur")
	teachers = models.ManyToManyField(Teacher, related_name="documents", blank=True,  verbose_name="Participants")

	level    = models.ForeignKey(Level, on_delete=models.CASCADE,  blank=True,null=True,  related_name='documents', verbose_name="Niveau")
	subject  = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True, related_name='documents', verbose_name="Enseignement")
	ranking  = models.PositiveIntegerField( default=0,  blank=True, null=True, editable=False)

	doctype   = models.PositiveIntegerField( default=0,  blank=True, null=True, editable=False)
	content   = models.TextField( blank=True,  verbose_name="Texte")  
	file      = models.FileField(upload_to=document_path, blank=True,  verbose_name="Fichier", default="")
	url       = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Lien externe")
	exercise  = models.ForeignKey( Exercise,  on_delete=models.CASCADE,  related_name="chapters", blank=True,  null=True, verbose_name="Exercices" )
	quizz     = models.ForeignKey( Quizz,  on_delete=models.CASCADE,  related_name="chapters", blank=True,  null=True, verbose_name="Quizz")
	bibliotex = models.ForeignKey( Bibliotex,  on_delete=models.CASCADE,  related_name="chapters", blank=True,  null=True, verbose_name="Bibliotex")
	exotex    = models.ManyToManyField(Exotex,  through="Documentex",  related_name="chapters" ,   blank=True,  verbose_name="Exotex")
	flashpack = models.ForeignKey( Flashpack,  on_delete=models.CASCADE,  related_name="chapters", blank=True,  null=True, verbose_name="Flashpack")

	is_publish   = models.BooleanField(default=0, verbose_name="Publié ?")
	is_share     = models.BooleanField(default=0, verbose_name="Mutualisé ?")

	def __str__(self):
	    return "{} {}".format(self.title,self.level.name)


class Chapter(models.Model):

    title         = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")

    author        = models.ForeignKey(Teacher, on_delete=models.CASCADE,  related_name='author_chapters', verbose_name="Enseignant")
    teachers      = models.ManyToManyField(Teacher, related_name="teacher_chapters", blank=True,  verbose_name="Participants")

    is_publish    = models.BooleanField(default=0, verbose_name="Publié ?")
    is_share      = models.BooleanField(default=0, verbose_name="Mutualisé ?")

    documents     = models.ManyToManyField(Document, related_name="chapters", blank=True,  verbose_name="Documents") 

    ranking       = models.PositiveIntegerField( default=0,  blank=True, null=True, editable=False)

    date_created  = models.DateTimeField( auto_now_add= True)
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    book          = models.ForeignKey(Book, on_delete=models.CASCADE,  blank=True,   related_name='chapters', editable=False)

    def __str__(self):
        return "{}".format(self.title)






class Documentex(models.Model):

    exotex = models.ForeignKey(Exotex,  on_delete=models.CASCADE,   related_name='documentexs', editable= False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,  related_name='documentexs',  editable= False)
    content = models.TextField( null=True, blank=True, verbose_name="Enoncé en LaTeX")
    content_html = models.TextField( null=True, blank=True)    

    correction = models.TextField( blank=True, default="", null=True, verbose_name="Correction en LaTeX")
    correction_html = models.TextField( blank=True, default="", null=True) 
    is_publish_cor = models.BooleanField(default=0, verbose_name="Publié ?") 

    #### pour validation si le qcm est noté
    calculator = models.BooleanField(default=0, verbose_name="Calculatrice ?")
    #### pour donner une date de remise
 
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
 
    duration = models.PositiveIntegerField(default=15, blank=True, verbose_name="Durée estimée - en minutes")

    author  = models.ForeignKey(Teacher, on_delete=models.CASCADE,  related_name='author_chapterxtexs', verbose_name="Enseignant")
    teacher = models.ManyToManyField(Teacher, related_name="teacher_chapterxtexs", blank=True,  verbose_name="Participants")

    ###### Socle
    skills = models.ManyToManyField(Skill, blank=True, related_name='documentexs', verbose_name="Compétences ciblées")
    knowledges = models.ManyToManyField(Knowledge, related_name='documentexs', verbose_name="Savoir faire associés complémentaires")

    is_python = models.BooleanField(default=0, verbose_name="Python ?")
    is_scratch = models.BooleanField(default=0, verbose_name="Scratch ?")
    is_tableur = models.BooleanField(default=0, verbose_name="Tableur ?")
    is_print = models.BooleanField(default=0, verbose_name="Imprimé ?")
    is_publish = models.BooleanField(default=0, verbose_name="Publié ?")
    start = models.DateTimeField(null=True, blank=True, verbose_name="A partir de")
    stop = models.DateTimeField(null=True, blank=True, verbose_name="Date de verrouillage")

    ranking = models.PositiveIntegerField(  default=0,  blank=True, null=True, editable=False)
    point = models.PositiveIntegerField(  default=0,  blank=True, null=True ,  verbose_name="Points") 

    def __str__(self):       
        return "{} > {}".format(self.chapter.title,self.document.title)

    class Meta:
        unique_together = ('exotex', 'document')