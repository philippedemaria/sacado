from django.db import models

from django.db import models

from account.models import Teacher
from bibliotex.models import Bibliotex , Exotex
from flashcard.models import Flashpack , Flashcard
from group.models import Group
from qcm.models import Course, Exercise
from tool.models import Quizz, Question
from socle.models import Level , Subject , Skill , Knowledge , Theme
from ckeditor_uploader.fields import RichTextUploadingField
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

    color         = models.CharField(max_length=255, default="#5d4391" , verbose_name="Couleur")
    color_hover   = models.CharField(max_length=255, default="#9274C7" , verbose_name="Couleur hover")
 
    def __str__(self):
        return "{}".format(self.title)



class Chapter(models.Model):

    title         = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")

    author        = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='author_chapters', blank=True,null=True,  verbose_name="Enseignant")
    teacher       = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="teacher_chapters", blank=True,null=True,  verbose_name="Participants")

    is_publish    = models.BooleanField(default=0, verbose_name="Publié ?")
    is_share      = models.BooleanField(default=0, verbose_name="Mutualisé ?")
    
    ranking       = models.PositiveIntegerField( default=0,  blank=True, null=True, editable=False)

    date_created  = models.DateTimeField( auto_now_add= True)
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    book          = models.ForeignKey(Book, on_delete=models.CASCADE,  blank=True,   related_name='chapters', editable=False)


    def __str__(self):
        return "{}".format(self.title)


class Section(models.Model):

    title   = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")
    ranking = models.PositiveIntegerField( default=0)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,  blank=True, null=True,  related_name='sections', editable=False)

    def __str__(self):
        return "{}".format(self.title )

    class Meta:
        unique_together = ('title', 'chapter')

##################################     doctypes     ################################################    
##  doctypes  ["content","file","url","GGB","Quizz","Course","BiblioTex","Exotex","flashpack","QF"]
##  doc_id    [    0    ,   1  ,  2  ,  3  ,   4   ,   5    ,     6     ,   7    ,      8    ,  9 ]
##################################     doctypes     ################################################

class Document(models.Model):
 
    title    = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")
    section  = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True, related_name='documents', verbose_name="Section")

    author   = models.ForeignKey(Teacher, on_delete=models.CASCADE,  blank=True,null=True, related_name='author_documents', verbose_name="Auteur")
    teacher  = models.ForeignKey(Teacher, on_delete=models.CASCADE,  blank=True,null=True, related_name="documents", verbose_name="Participants")

    level    = models.ForeignKey(Level, on_delete=models.CASCADE,  blank=True,null=True,  related_name='documents', verbose_name="Niveau")
    subject  = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True, related_name='documents', verbose_name="Enseignement")
    ranking  = models.PositiveIntegerField( default=0,  blank=True, null=True, editable=False)

    content  = RichTextUploadingField( blank=True,  verbose_name="Texte")  
    file     = models.FileField(upload_to=document_path, blank=True,  verbose_name="Fichier", default="")
    url      = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Lien externe")

    doctype  = models.PositiveIntegerField( default=0,  blank=True, null=True, editable=False)#doctypes = ["content","file","url","exercise","quizz","question","bibliotex","exotex","flashcard","flashpack"]
    doc_id   = models.PositiveIntegerField( default=0,  blank=True, null=True, editable=False)

    is_publish   = models.BooleanField(default=0, verbose_name="Publié ?")
    is_share     = models.BooleanField(default=0, verbose_name="Mutualisé ?")

    def __str__(self):
        return "{} {}".format(self.title,self.level.name)

    def icon_doctype(self):

        if self.doctype == 0 : icon = '<i class="bi bi-file-earmark book_main_page_section_document_earmark"></i>'
        elif self.doctype == 1 : icon = '<i class="bi bi-file book_main_page_section_document_earmark"></i>'
        elif self.doctype == 2 : icon = '<i class="bi bi-link  book_main_page_section_document_earmark"></i>'
        elif self.doctype == 3 : icon = '<i class="bi bi-explicit  book_main_page_section_document_earmark"></i>'
        elif self.doctype == 4 : icon = '<i class="bi bi-file-aspect-ratio  book_main_page_section_document_earmark"></i>'
        elif self.doctype == 5 : icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-c-square" viewBox="0 0 16 16"><path d="M8.146 4.992c-1.212 0-1.927.92-1.927 2.502v1.06c0 1.571.703 2.462 1.927 2.462.979 0 1.641-.586 1.729-1.418h1.295v.093c-.1 1.448-1.354 2.467-3.03 2.467-2.091 0-3.269-1.336-3.269-3.603V7.482c0-2.261 1.201-3.638 3.27-3.638 1.681 0 2.935 1.054 3.029 2.572v.088H9.875c-.088-.879-.768-1.512-1.729-1.512Z"/><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2Zm15 0a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2Z"/></svg>'
        elif self.doctype == 6 : icon = '<i class="bi bi-bootstrap  book_main_page_section_document_earmark"></i>'
        elif self.doctype == 7 : icon = '<i class="bi bi-explicit-fill  book_main_page_section_document_earmark"></i>'
        elif self.doctype == 8 : icon = '<i class="bi bi-stack  book_main_page_section_document_earmark"></i>'
        elif self.doctype == 9 : icon = '<i class="bi bi-lightning  book_main_page_section_document_earmark"></i>'
        return icon



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