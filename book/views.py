from django.conf import settings # récupération de variables globales du settings.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import  permission_required,user_passes_test, login_required
from django.db.models import Q , Sum , Avg
from django.core.mail import send_mail
from django.http import JsonResponse  , FileResponse
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

 
from .models import Book, Chapter , Page ,  Bloc , Mybook , Mybloc
from .forms import *
from bibliotex.models import Bibliotex
from account.models import User
from qcm.models import Parcours, Docperso , Course
from tool.models import Mentaltitle, Quizz , Mental
from tool.views import create_questions_flash_random_variable
from socle.decorators import user_is_extra
from django.utils.html import escape
from datetime import datetime , timedelta ,date
import subprocess
import os




##################################     doctypes     ################################################    
##  doctypes  ["content","file","url","GGB","Quizz","Course","BiblioTex","Exotex","flashpack","QF"]
##  doc_id    [    0    ,   1  ,  2  ,  3  ,   4   ,   5    ,     6     ,   7    ,      8    ,  9 ]
##################################     doctypes     ################################################ 

################################################################################################
########################    FONCTIONS ANNEXE    ################################################
################################################################################################

@user_is_extra 
def books(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    teacher = request.user.teacher
    mybooks = Book.objects.filter(level__in=teacher.levels.all(), subject__in=teacher.subjects.all(),is_publish=1).order_by('subject','level')
    
    levels  = teacher.levels.order_by("ranking")
    subjects = teacher.subjects.all()

    if request.session.get('this_page_id_created',None) : 
        del request.session['this_page_id_created']

    # mybooks = list()
    # for subject in subjects :
    #     mylist = list()
    #     data   = dict()
    #     data["subject"] = subject
    #     for level in levels :
    #         datal = dict()            
    #         datal["level"] = level
    #         datal["books"] = Book.objects.filter(level = level, subject=subject,is_publish=1).order_by('ranking')
    #         mylist.append(datal)
    #     data["books"] = mylist
    #     mybooks.append(data)

    other_books = Book.objects.exclude(level__in=teacher.levels.all(), subject__in=teacher.subjects.all()).order_by('subject','level','ranking')
    return render(request, 'book/books.html', {'other_books': other_books , 'mybooks': mybooks })



def mybooks(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    teacher = request.user.teacher
    mybooks = Mybook.objects.filter(group__teacher=teacher)
    book= None
    if mybooks.count() == 0 :
        book =  Book.objects.get(pk=9)
    return render(request, 'book/configmybooks.html', {'mybooks': mybooks , 'book' : book })


@user_is_extra 
def create_book(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    
    form = BookForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        nf = form.save(commit=False)
        user = User.objects.get(id=2480)
        nf.author = user.teacher
        nf.teacher = user.teacher        
        nf.save()
        messages.success(request, 'Le livre a été créé avec succès !')
        return redirect('books')
    else:
        print(form.errors)

    context = {'form': form,  }
    return render(request, 'book/form_book.html', context)


@user_is_extra 
def update_book(request,idb):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    book = Book.objects.get(id=idb)
    form = BookForm(request.POST or None,request.FILES or None, instance=book )

    if form.is_valid():
        nf = form.save()
        messages.success(request, 'Le livre a été modifié avec succès !')
        return redirect('books')
    else:
        print(form.errors)

    context = {'form': form, 'book': book,  }
    return render(request, 'book/form_book.html', context)


def delete_book(request):

    if request.user.is_superuser :

        request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
        request.session["subtdb"] = "Chapter"
        idb = 1000
        book = Book.objects.get(id=idb)
        book.delete()
    return redirect('books')



def reset_all_chapters(request,idb) :

    Document.objects.all().delete()
    Section.objects.all().delete()
    book = Book.objects.get(pk=idb)
    i = 1
    for p in Parcours.objects.filter(level=book.level,subject=book.subject,teacher__user_id=2480).order_by("ranking") :
        courses    = p.course.all()
        exercises  = p.exercises.all()[:4]
        qfs        = p.quizz.filter(is_random=1)[:4]
        bibliotexs = p.bibliotexs.all()

        chapt,crea  = Chapter.objects.get_or_create(book=book,title=p.title, author_id=2480 , teacher=request.user.teacher, defaults={'is_publish':1,'ranking':i})

        # QF ###################################################################################################################
        section_qf, cre_qf = Section.objects.get_or_create(title = "Questions flash & Rituels" , chapter = chapt , defaults = {'ranking': 1, })
        for qf in qfs :
            document,created = Document.objects.get_or_create(title=qf.title, subject = book.subject, level=book.level, section  = section_qf , author_id=request.user.id , teacher=request.user.teacher, 
                                                                defaults={'is_publish':1,'is_share':1,'ranking':i,'content' : "Question flash" , 'doctype': 8 , 'doc_id' : qf.id })
        chapt.sections.add(section_qf)

        # Cours ###################################################################################################################
        section, cre = Section.objects.get_or_create(title = "Cours" , chapter = chapt , defaults = {'ranking': 2, })
        for c in courses :
            document,created = Document.objects.get_or_create(title=c.title, subject = book.subject, level=book.level, section  = section , author_id=request.user.id , teacher=request.user.teacher, defaults={'is_publish':1,'is_share':1,'ranking':i,'content' : c.annoncement})
        chapt.sections.add(section)

        # Exercices ###################################################################################################################
        section_tex, cre_tex = Section.objects.get_or_create(title = "Exercices" , chapter = chapt , defaults = {'ranking': 3, })
        for bib in bibliotexs :
            for exo in bib.relationtexs.all():
                document,created = Document.objects.get_or_create(title=exo.title, subject = book.subject, level=book.level, section  = section_tex , 
                                                                    author_id=request.user.id , teacher=request.user.teacher, defaults={'is_publish':1,'is_share':1,'ranking':i,'content' : exo.content_html , 'doctype': 6 , 'doc_id' : exo.id })
        chapt.sections.add(section_tex)

        # Exercices auto-correctifs ###################################################################################################################
        section_exe, cre_exo = Section.objects.get_or_create(title = "Exercices auto-correctifs" , chapter = chapt , defaults = {'ranking': 4, })
        for exercise in exercises :
            document,created = Document.objects.get_or_create(title=exercise.supportfile.title, subject = book.subject, level=book.level, section  = section_exe , author_id=request.user.id , 
                                                                teacher=request.user.teacher, 
                                                                defaults={'is_publish':1,'is_share':1,'ranking':i,'content' : exercise.knowledge , 'doctype': 3 , 'doc_id' : exercise.id})
        chapt.sections.add(section_exe)

        i+=1 # ranking du chapitre

    return redirect('conception_book', idb , 0 )
 

def show_conception_book(request,idb,idch,is_conception,is_chrono):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    teacher = request.user.teacher

    book = Book.objects.get(id=idb)

    chapters = book.chapters.filter(teacher=teacher).order_by("ranking")
    form = NewChapterForm(request.POST or None )

    formdoc   = DocumentForm(request.POST or None  )
    formsec   = SectionForm(request.POST or None)
    form_type = request.POST.get("form_type", None )
    form_qf   = QFlashBookForm(request.POST or None , book = book)

    if is_conception : 
        template =  'book/conception_book.html'
        sections = Section.objects.filter(chapter=idch).order_by("ranking")
    else : 
        template =  'book/show_book.html'
        sections = Section.objects.filter(is_publish=1,chapter=idch).order_by("ranking")
        context = {}


    if idch == 0 :
        chapter = chapters.first()
    else :
        chapter = Chapter.objects.get(id=idch)
        
    mentaltitles = Mentaltitle.objects.filter(subjects = book.subject, is_display=1).order_by("ranking")

    all_mentals = list()
    level_dict = dict()
 
    level_dict["level"] = book.level 
    list_mentals = list()
    for mentaltitle in mentaltitles :
        dict_mentals = dict()
        mentals = Mental.objects.filter(mentaltitle  = mentaltitle, levels = book.level, is_display=1 ).order_by("ranking")
        is_mentals = False 
        if mentals :
            dict_mentals["mentaltitle"] = mentaltitle 
            dict_mentals["mentals"] = mentals
            list_mentals.append(dict_mentals)
            is_mentals = True
            level_dict["sub"] = list_mentals

    all_mentals.append(level_dict)

    parcours = Parcours.objects.filter(level=book.level,subject=book.subject,teacher__user=request.user).order_by("ranking") 

    context = { 'book': book ,'chapters': chapters , 'form':form , 'formdoc':formdoc , 'formsec': formsec  ,'idch' : idch, 'chapter': chapter , 
                'sections': sections , 'form_qf' : form_qf ,'all_mentals':all_mentals ,'teacher' : teacher , 'parcours' : parcours }


    if is_chrono and chapter :
        sections = chapter.sections.all()
        documents = Document.objects.filter(section__in=sections).order_by("ranking")

        context.update({  'documents': documents  })
        template =  'book/chapter_chrono_concept_document.html'

    else :
        reset_all_chapters(request,idb)        

    if request.method == "POST" :
        if form_type == "book" :
            if request.POST.get("is_update") == "1" :
                pk_update = request.POST.get("pk_update" , None )
                chapter   = Chapter.objects.get(pk = pk_update)
                form      = NewChapterForm(request.POST or None , instance = chapter )
        
            if form.is_valid():
                nf = form.save(commit=False)
                nf.book = book
                nf.author = request.user.teacher
                nf.teacher = request.user.teacher                
                nf.save()
                if request.POST.get("is_update") == "1" :
                    messages.success(request, 'Le chapitre a été modifié avec succès !')
                else :
                    messages.success(request, 'Le chapitre a été créé avec succès !')
 
            else:
                messages.error(request, formdoc.errors)
            return redirect('conception_book', idb , nf.pk )
 

        elif form_type == "udpate_section_button" :
            section_id = request.POST.get('section_id')
            section = Section.objects.get(pk=section_id)
            formsec = SectionForm(request.POST or None , instance = section)
            if formsec.is_valid():
                formsec.save()

        elif form_type == "emplacement" :

            if formsec.is_valid():
                nf = formsec.save(commit=False)
                nf.chapter = chapter
                nf.ranking = 100
                nf.save()
                messages.success(request, 'La section a été créée avec succès !')
            else :
                messages.error(request, formsec.errors)
            return redirect('conception_book', idb , idch )

        elif form_type == "new_document" :
            ##################################     doctypes     ################################################    
            ##  doctypes  ["content","file","url","GGB","Quizz","Course","BiblioTex","Exotex","flashpack","QF"]
            ##  doc_id    [    0    ,   1  ,  2  ,  3  ,   4   ,   5    ,     6     ,   7    ,      8    ,  9 ]
            ##################################     doctypes     ################################################ 
            if request.POST.get("document_is_update") == "1" :
                try : 
                    document_pk_update = request.POST.get("document_pk_update" , None )
                    document   = Document.objects.get(pk = document_pk_update)
                    formdoc    = DocumentForm(request.POST or None , instance = document )
                except : pass
            if formdoc.is_valid():
                nf = formdoc.save(commit=False)
                nf.author  = request.user.teacher
                nf.level   = book.level
                nf.subject = book.subject
                nf.teacher = request.user.teacher
                nf.doctype = request.POST.get("doctype",2)
                book_section_id = request.POST.get("book_section_id",None)
                if book_section_id : 
                    nf.section = Section.objects.get(pk=book_section_id)
                else :
                    nf.section = sections.first()
                nf.save()
                messages.success(request, 'Le document a été créé avec succès !')
            else :
                messages.error(request, formdoc.errors)
 
            return redirect('conception_book', idb , idch )



        elif form_type == "get_doc" :

            select_documents = request.POST.getlist("select_this_document_for_chapter")
            section_id       = request.POST.get("book_section_id",None)
            if not section_id :
                section    = sections.first()
                section_id = section.id

            for doc in select_documents :
                ##################################     doctypes     ################################################    
                ##  doctypes  ["content","file","url","GGB","Quizz","Course","BiblioTex","Exotex","flashpack","QF"]
                ##  doc_id    [    0    ,   1  ,  2  ,  3  ,   4   ,   5    ,     6     ,   7    ,      8    ,  9 ]
                ##################################     doctypes     ################################################ 
                doc_id , this_type = doc.split("-")  

                if this_type == "BiblioTex"   :
                    b = Bibliotex.objects.get(pk=doc_id) 
                    doctype = 6 
                elif this_type == "Course"    : 
                    b = Course.objects.get(pk=doc_id) 
                    doctype = 5 
                elif this_type == "Exotex"    : 
                    b = Exotex.objects.get(pk=doc_id)
                    doctype = 7         
                elif this_type == "GGB"       : 
                    b = Exercise.objects.get(pk=doc_id)
                    doctype = 3  
                elif this_type == "Flashpack" :
                    b = Flashpack.objects.get(pk=doc_id)
                    doctype = 8         
                elif this_type == "QF" :
                    b = Quizz.objects.get(pk=doc_id)
                    doctype = 9 
                else : 
                    b = Quizz.objects.get(pk=doc_id)
                    doctype = 4 

                try : 
                    document = Document.objects.create(title = b.title, doc_id=doc_id , doctype = doctype, author = b.author, teacher = teacher, section_id = section_id , level = book.level , subject = book.subject,is_publish=1,is_share=1)
                except :
                    document = Document.objects.create(title = b.title, doc_id=doc_id , doctype = doctype, author = teacher, teacher = teacher, section_id = section_id , level = book.level , subject = book.subject,is_publish=1,is_share=1)
        
            return redirect('conception_book', idb , idch )

        elif form_type == "new_qf_document" :
            if form.is_valid():
                nf = form_qf.save(commit = False)
                nf.teacher = teacher
                nf.is_questions = 1
                nf.is_random = 1
                nf.is_archive = 0
                nf.interslide = 2
                nf.save()
                form.save_m2m()

                section_id       = request.POST.get("book_section_id",None)
                mental_ids = request.POST.getlist("mental_ids",None)

                if len(mental_ids) :
                    mentaltitles = create_questions_flash_random_variable(mental_ids, nf, nf.nb_slide)
                    nf.mentaltitles.set( mentaltitles )  

                document = Document.objects.create(title = nf.title, doc_id=nf.id , doctype = 9, author = b.author, teacher = teacher, section_id = section_id , level = book.level , subject = book.subject,is_publish=1,is_share=1)

                messages.success(request, 'Les questions flash ont été créées avec succès !')
            else :
                messages.error(request, formdoc.errors)
 
            return redirect('conception_book', idb , idch )

        elif form_type == "link_form_parcours":
            my_parcours = request.POST.get("my_parcours",None)
            parcours = Parcours.objects.get(pk=my_parcours)
            chapter.parcours = parcours
            chapter.save()
            messages.success(request, 'Le parcours a été lié avec succès !')
            return redirect('conception_book', idb , idch )

    return render(request,template,context) 


def show_book(request,idb,idch):

    request.session["show"]  = True
    request.session["chrono"] = False

    return show_conception_book(request,idb,idch,False,False)




def get_mybook(request,idb, idg):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    if idg > 0 :  request.session["book_group_id"] = idg
    else :   request.session["book_group_id"] = None

    return show_mybook(request,idb, 0)


@csrf_exempt
def goto_direct_page(request):
    n_page  = request.POST.get("acces_to_page" , None )
    idb = 9
    return show_mybook(request,idb , n_page)


def show_mybook(request,idb, n):
    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    group_id = request.session.get("book_group_id",None)
    try: group = Group.objects.get(pk=group_id)
    except : group = None
    book = Book.objects.get(pk=idb)

    prev_page, this_page , next_page , first_pages = get_the_page(int(idb),int(n))
    this_chapter = this_page.chapter

    isMenuDisplay = True
    if this_page in [9,21,33,47,61,75,87,103,119,135,147,161,175,203,213] : isMenuDisplay = False

    # Appel de la page n
    use_this_css = "css/bookstyle_6_shower.css"  #"css/bookstyle_"+str(book.level.id)+".css"   
    context = {'book': book, "n" : n ,  'this_chapter' : this_chapter , 'group':group, 'page' : this_page , 'next_page' : next_page  ,
               'prev_page' : prev_page , 'first_pages' : first_pages , 'isMenuDisplay' : isMenuDisplay , 'use_this_css' : use_this_css }
    return render(request, 'book/show_mybook.html', context)



def show_mybook_two_pages(request,idb, n):
    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    group_id = request.session.get("book_group_id",None)
    if group_id : group = Group.objects.get(pk=group_id)
    else : group = None
    book = Book.objects.get(pk=idb)
 

    prev_page, this_page , next_page , first_pages = get_the_pages(int(idb),int(n))
    prev_page_number = this_page.number - 2
    next_page_number = this_page.number + 2
    this_chapter = this_page.chapter
    # Appel de la page n
    use_this_css = "css/bookstyle_6_shower.css"  #"css/bookstyle_"+str(book.level.id)+".css"   
    context = {'book': book, "n" : n ,  'this_chapter' : this_chapter , 'group':group, 'page' : this_page , 'next_page' : next_page  ,
               'next_page_number' : next_page_number , 'prev_page_number' : prev_page_number ,
               'prev_page' : prev_page , 'first_pages' : first_pages , 'use_this_css' : use_this_css }
    return render(request, 'book/show_mybook_two_pages.html', context)







def show_mybook_student(request,idb, n):
    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
 
    book = Book.objects.get(pk=idb)
    student = request.user.student

    prev_page, this_page , next_page , first_pages = get_the_page(int(idb),int(n))
    this_chapter = this_page.chapter
    # Appel de la page n
    use_this_css = "css/bookstyle_6_shower.css"  #"css/bookstyle_"+str(book.level.id)+".css"   
    context = {'book': book, "n" : n ,  'this_chapter' : this_chapter , 'page' : this_page , 'next_page' : next_page  ,
               'prev_page' : prev_page , 'first_pages' : first_pages , 'use_this_css' : use_this_css , 'student' : student }
    return render(request, 'book/show_mybook_student.html', context)




def conception_book(request,idb,idch):

    request.session["show"]   = False
    request.session["chrono"] = False


    return show_conception_book(request,idb,idch,True,False)


def chapter_chrono_concept_document(request,idb,idch):

    request.session["show"]   = False
    request.session["chrono"] = True  

    return show_conception_book(request,idb,idch,True,True)
 


def chapter_chrono_show_document(request,idb,idch):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    request.session["show"]   = True
    request.session["chrono"] = True
  

    teacher = request.user.teacher

    book = Book.objects.get(id=idb)
    chapters = book.chapters.filter(teacher=teacher).order_by("ranking")

    if idch == 0 :
        chapter = chapters.first()
    else :
        chapter = Chapter.objects.get(id=idch)
    sections = chapter.sections.all()
    documents = Document.objects.filter(section__in=sections)

    context = { 'book': book ,'chapters': chapters , 'idch' : idch, 'chapter': chapter , 'documents': documents  }

    return render(request, 'book/chapter_chrono_show_document.html' , context )




@csrf_exempt
def publish_book_document(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    document_id  = request.POST.get("document_id" , None )
    document = Document.objects.get(pk=document_id)
    if document.is_publish : document.is_publish = False
    else : document.is_publish = True
    document.save()
    data = {}
    return JsonResponse(data) 

 

@csrf_exempt
def book_document_is_done(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    data = {}
    document_id  = request.POST.get("document_id" , None )
    document = Document.objects.get(pk=document_id)
    if document.is_done : 
        document.is_done = False
        data['html'] = ""
    else : 
        document.is_done = True
        data['html'] = "<i class='fa fa-check this_document_is_done'></i>" 
    document.save()

    return JsonResponse(data) 
#################################################################
# section
#################################################################
@csrf_exempt
def create_book_section(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    chapter_id = request.POST.get("chapter_id" , None )
    chapter = Chapter.objects.get(pk=chapter_id)
    title = request.POST.get("title" , None )
    color = request.POST.get("color" , None )

    section = Section.objects.create(title = title , color = color , chapter_id = chapter_id , ranking = 100 , is_publish =1 )
    data = {}
    context = { 'section' : section ,   'chapter' : chapter }
    data['html'] = render_to_string('book/ajax_get_section.html', context )

    return JsonResponse(data) 



@csrf_exempt
def update_book_section(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    section_id  = request.POST.get("section_id" , None )
    title = request.POST.get("title" , None )
    color = request.POST.get("color" , None )

    section = Section.objects.get(pk=section_id) 
    section.title = title
    section.color = color
    section.save()
    data = {}
    data['title'] = title
    data['color'] = color
    return JsonResponse(data) 


@csrf_exempt
def delete_book_section(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    section_id  = request.POST.get("section_id" , None )
    Section.objects.filter(pk=section_id).delete()

    data = {}
    return JsonResponse(data) 

 
@csrf_exempt
def sorter_book_section(request):

    valeurs = request.POST.getlist("valeurs")

    for i in range(len(valeurs)):
        Section.objects.filter(pk = valeurs[i]).update(ranking = i)

    data = {}
    return JsonResponse(data)

@csrf_exempt
def publish_book_section(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    section_id  = request.POST.get("section_id" , None )
    section = Section.objects.get(pk=section_id)
    if section.is_publish : section.is_publish = False
    else : section.is_publish = True
    section.save()
    data = {}
    return JsonResponse(data) 
#################################################################
# chapter
#################################################################

def create_chapter(request,idb,idch):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    book = Book.objects.get(id=idb)
    form = ChapterForm(request.POST or None  )

    if form.is_valid():
        nf = form.save(commit=False)
        nf.book = book
        nf.author = request.user.teacher
        nf.teacher = request.user.teacher
        nf.save()
        messages.success(request, 'Le chapitre a été crée avec succès !')
        return redirect('student_book_builder' , book.id , 0)
    else:
        print(form.errors)

    context = {'form': form,   'book': book  }
    return render(request, 'book/form_chapter.html', context)



def update_chapter(request,idb,idch):


    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    
    book = Book.objects.get(id=idb)
    chapter = Chapter.objects.get(id=idch)
    form = ChapterForm(request.POST or None, instance=chapter )

    if form.is_valid():
        nf = form.save()
        messages.success(request, 'Le chapitre a été modifié avec succès !')
        return redirect('books')
    else:
        print(form.errors)

    context = {'form': form, 'chapter': chapter, 'book': book  }
    return render(request, 'book/form_chapter.html', context)



def update_student_book_chapter(request,idb,idch):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    
    book = Book.objects.get(id=idb)
    chapter = Chapter.objects.get(id=idch)
    form = ChapterForm(request.POST or None, instance=chapter )

    if form.is_valid():
        form.save()
        messages.success(request, 'Le chapitre '+chapter.title+' a été modifié avec succès !')
        return redirect('student_book_builder' , idb, 0)
    else:
        print(form.errors)

    context = {'form': form, 'chapter': chapter, 'book': book  }
    return render(request, 'book/form_chapter.html', context)

 



def delete_chapter(request,idb,idch):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    chapter = Chapter.objects.get(id=idch)
    chapter.delete()
    messages.success(request, 'Le chapitre '+chapter.title+' a été supprimé avec succès !')
    return redirect('conception_book' , idb, 0)




def delete_student_book_chapter(request,idb,idch):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    Chapter.objects.filter(id=idch).delete()

    messages.success(request, 'Le chapitre  a été supprimé avec succès !')
    
    book     = Book.objects.get(id=idb)
    chapters = book.chapters.order_by("ranking")

    context = {'book': book,  'chapters': chapters,  }

    return render(request, 'book/conception_student_page.html', context)






@csrf_exempt
def sorter_chapter(request):

    valeurs = request.POST.getlist("valeurs")
    for i in range(len(valeurs)):
        Chapter.objects.filter(pk = valeurs[i]).update(ranking = i)

    data = {}
    return JsonResponse(data) 
  



#################################################################
# document
#################################################################
@csrf_exempt
def delete_book_document(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    document_id  = request.POST.get("document_id" , None )
    Document.objects.filter(pk=document_id).delete()
    data = {}
    return JsonResponse(data) 
 
 
def update_book_document(request,idb,idch,idd):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    book     = Book.objects.get(pk=idb)
    chapter     = Chapter.objects.get(pk=idch)
    document    = Document.objects.get(pk=idd)
 
 
    context = {   'book' : book , 'chapter' : chapter }
    return render(request, 'book/form_update_document.html', context)





def book_chapter_show_document(request,idb,idch,idd):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    document    = Document.objects.get(pk=idd)

    doctype_templates = ["content","file","url","GGB","Quizz","Course","BiblioTex","Exotex","flashpack","QF"]
 
    template = doctype_templates[document.doctype]

    context = { 'document' : document }

    return redirect( "" )

 

@csrf_exempt
def show_book_document(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    document_id  = request.POST.get("document_id" , None )
    this_type  = request.POST.get("this_type" , None )

    data = {}

    if this_type == "BiblioTex" :
        doc = Bibliotex.objects.get(pk=document_id)
        title = doc.title
        content = str(doc.relationtexs.count()) + " exercices"
    elif this_type == "Course" :
        doc = Course.objects.get(pk=document_id)
        title = doc.title
        content = doc.annoncement
    elif this_type == "Exotex" :        
        doc = Exotex.objects.get(pk=document_id)
        title = doc.title
        content = doc.content_html
    elif this_type == "Flashpack" :        
        doc = Flashpack.objects.get(pk=document_id)
        title = doc.title
        content = str(doc.flashcards.count()) + " flashcards"
    elif this_type == "Quizz" or  this_type == "QF" :
        doc = Quizz.objects.get(pk=document_id)
        title = doc.title
        content = str(doc.questions.count()) + " questions"
    elif this_type == "DocPerso" :
        doc = Docperso.objects.get(pk=document_id)
        title = doc.title
        if doc.link !="" : content =  "<a href='"+doc.link+"'><i class='bi bi-link'></i> "+doc.title+"</a>"
        else : content = "<a href='"+doc.file.url+"'><i class='bi bi-file'></i> "+doc.title+" </a>"
    elif this_type == "Bloc" :
        doc = Bloc.objects.get(pk=document_id)
        content = doc.content_html
        title = doc.title
    else :
        content = ""
        title   = ""

    data["body"] = content

    data["title"] = title 

    return JsonResponse(data) 
 

 
def duplicate_book_document(request,idb,idch,idd):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    document = Document.objects.get(pk=idd)
    document.pk=None
    document.save()
    return redirect('conception_book' , idb , idch ) 

 
@csrf_exempt
def sorter_book_document(request):

    valeurs = request.POST.getlist("valeurs")
    document_section_id = request.POST.get("over_section_id")
    section_id = request.POST.get("section_id")
    document_id = request.POST.get("document_id")

    data = {}
    data['section_id'] =  document_section_id

    if document_section_id != section_id :
        Document.objects.filter(pk = document_id).update(section_id = document_section_id)
        
    for i in range(len(valeurs)):
        Document.objects.filter(pk = valeurs[i]).update(ranking = i)

    return JsonResponse(data) 


@csrf_exempt
def sorter_book_chrono_document(request):

    valeurs = request.POST.getlist("valeurs")
    data = {}  
    for i in range(len(valeurs)):
        try :
            Document.objects.filter(pk = valeurs[i]).update(ranking = i)
        except : pass
    return JsonResponse(data) 



@csrf_exempt
def get_type_book_document(request):

    this_type  = request.POST.get("type")
    level_id   = request.POST.get("level_id")
    subject_id = request.POST.get("subject_id")
    chapter_id = request.POST.get("chapter_id")
    n          = int(request.POST.get("n"))


    teacher    = request.user.teacher
    data = {}
    level   = Level.objects.get(pk=level_id)
    chapter = Chapter.objects.get(pk=chapter_id)
    subject = Subject.objects.get(pk=subject_id)

    if this_type == "BiblioTex" :
        documents = Bibliotex.objects.filter(Q(teacher=teacher)|Q( is_share=1),subjects = subject , levels = level )[(n-1)*100:n*100]
    elif this_type == "Course" :
        documents = Course.objects.filter(Q(teacher=teacher)|Q( is_share=1),subject = subject , level = level )[(n-1)*100:n*100]
    elif this_type == "Exotex" :        
        documents = Exotex.objects.filter(is_share=1,subject = subject , level = level )[(n-1)*100:n*100]
    elif this_type == "GGB" : 
        documents = Exercise.objects.filter(knowledge__theme__subject = subject , level  = level, supportfile__is_title=0 )[(n-1)*100:n*100]
    elif this_type == "Flashpack" :        
        documents = Flashpack.objects.filter(Q(teacher=teacher)|Q( is_share=1),subject = subject , levels  = level )[(n-1)*100:n*100]
    elif this_type == "Quizz" :
        documents = Quizz.objects.filter(Q(teacher=teacher)|Q( is_share=1),subject  = subject , levels  = level , is_random = 0 )[(n-1)*100:n*100]
    elif this_type == "QF" :
        documents = Quizz.objects.filter(Q(teacher=teacher)|Q( is_share=1),subject  = subject , levels  = level , is_random = 1 )[(n-1)*100:n*100]
    elif this_type == "DocPerso" :
        documents = Docperso.objects.filter(Q(teacher=teacher)|Q( is_share=1),subject  = subject, levels  = level )[(n-1)*100:n*100]
    elif this_type == "Bloc" :
        documents = Bloc.objects.filter( paragraph__page__chapter__book__subject  = subject, paragraph__page__chapter__book__level  = level )

    else :
        documents = []

 
    request.session['organiser'] =  chapter.id


    context = { 'documents' : documents ,  'this_type' : this_type ,  'chapter' : chapter }
    data['html'] = render_to_string('book/ajax_get_documents.html', context )

    return JsonResponse(data)
        




@csrf_exempt
def insert_document_into_section(request):

    valeurs    = request.POST.getlist("valeurs")
    this_type  = request.POST.get("type_doc")
    section_id = request.POST.get("section_id")
    level_id   = request.POST.get("level_id")
    subject_id = request.POST.get("subject_id")

    teacher  = request.user.teacher
    documents = list()
    for doc_id in valeurs :

        if this_type == "BiblioTex"   :
            b = Bibliotex.objects.get(pk=doc_id) 
            doctype = 6 
            title , author = b.title ,  b.author
        elif this_type == "Course"    : 
            b = Course.objects.get(pk=doc_id) 
            doctype = 5 
            title , author  = b.title ,  b.author
        elif this_type == "Exotex"    : 
            b = Exotex.objects.get(pk=doc_id)
            doctype = 7      
            title , author  = b.title ,  b.author
        elif this_type == "GGB"       : 
            b = Exercise.objects.get(pk=doc_id)
            title  , author = b.supportfile.title ,  b.supportfile.author
            doctype = 3  
        elif this_type == "Flashpack" :
            b = Flashpack.objects.get(pk=doc_id)
            doctype = 8    
            title  , author = b.title    ,  b.teacher
        elif this_type == "QF" :
            b = Quizz.objects.get(pk=doc_id)
            doctype = 9 
            title  , author = b.title ,  b.teacher
        elif this_type == "DocPerso" :
            b = Docperso.objects.get(pk=doc_id)
            doctype = 10 
            title  , author = b.title ,  b.teacher
        elif this_type == "Bloc" :
            b = Bloc.objects.get(pk=doc_id)
            doctype = 11 
            title  , author = b.title , request.user.teacher
        else : 
            b = Quizz.objects.get(pk=doc_id)
            doctype = 4 
            title , author  = b.title ,  b.teacher

        document = Document.objects.create(title = title, doc_id=doc_id , doctype = doctype, author = author, teacher = teacher, section_id = section_id , level_id = level_id, subject_id = subject_id,is_publish=1,is_share=0)
        documents.append(document)

    section = Section.objects.get(pk=section_id)

    request.session['organiser'] = section.chapter.id

    data = {}
    context = { 'documents':documents , 'section' : section , }
    data["html"] = render_to_string('qcm/ajax_documents_after_choose.html', context )
 

    return JsonResponse(data)


###################################################################################################################################################################################################
###################################################################################################################################################################################################
###################################################################################################################################################################################################
#########################################################  Student book     #########################################################
###################################################################################################################################################################################################
###################################################################################################################################################################################################
###################################################################################################################################################################################################
def get_the_page(idb,n):

    book = Book.objects.get(pk=idb)
    all_pages   = dict()
    first_pages = list()
    for chapter in book.chapters.order_by('ranking'):
        pages = chapter.pages.order_by('number')
        first_pages.append(pages.first())
        for page in pages :
            all_pages[page.number] = page

    prev_page , next_page = None, None
    page = all_pages[n]    
    if n > 0 : prev_page = all_pages[n-1]
    if n < len(all_pages)-1 : next_page = all_pages[n+1]
    return  prev_page , page , next_page , first_pages




def get_the_pages(idb,n):

    book = Book.objects.get(pk=idb)
    all_pages   = dict()
    first_pages = list()
    for chapter in book.chapters.order_by('ranking'):
        pages = chapter.pages.order_by('number')
        first_pages.append(pages.first())
        for page in pages :
            all_pages[page.number] = page

    prev_page , next_page = None, None
    page = all_pages[n]    
    if n > 1 : prev_page = all_pages[n-2]
    if n < len(all_pages)-2 : next_page = all_pages[n+1]
    return  prev_page , page , next_page , first_pages





def show_student_book(request,idb, n):
    book = Book.objects.get(pk=idb)
    prev_page, this_page , next_page , first_pages = get_the_page(idb,n)
    this_chapter = this_page.chapter
    # Appel de la page n
    use_this_css = "css/bookstyle_6_shower.css"  #"css/bookstyle_"+str(book.level.id)+".css"   
    context = {'book': book, "n" : n ,  'this_chapter' : this_chapter ,  'page' : this_page , 'next_page' : next_page  ,'prev_page' : prev_page , 'first_pages' : first_pages , 'use_this_css' : use_this_css }
    return render(request, 'book/show_student_page.html', context)


def show_student_book_one_page(request,idb, n):
    book = Book.objects.get(pk=idb)
    prev_page, this_page , next_page , first_pages = get_the_page(idb,n)
    this_chapter = this_page.chapter
    # Appel de la page n
    use_this_css = "css/bookstyle_6_shower_one_page.css"  #"css/bookstyle_"+str(book.level.id)+".css"   
    context = {'book': book, "n" : n ,  'this_chapter' : this_chapter ,  'page' : this_page , 'next_page' : next_page  ,'prev_page' : prev_page , 'first_pages' : first_pages , 'use_this_css' : use_this_css }
    return render(request, 'book/show_student_page_one_page.html', context)




def student_book_builder(request,idb, n):

    if request.user.is_superuser or request.user.is_extra :
        book = Book.objects.get(pk=idb)
        i = 0
        # Création et organisation des pages à la volée
        for chapter in book.chapters.order_by("ranking") :
            for page in chapter.pages.order_by('number') :
                page.number = i
                page.chapter = chapter
                page.save()
                i += 1

        this_page_id_created = request.session.get('this_page_id_created')
        chapters = book.chapters.order_by("ranking")
        context = {'book': book,  'chapters': chapters, 'this_page_id_created' : this_page_id_created }

        return render(request, 'book/conception_student_page.html', context)
    else :
        return redirect("index")

 
@csrf_exempt
@user_is_extra 
def sorter_book_pages(request):
    valeurs = request.POST.getlist("valeurs")
    data = {}
 
    for i in range(len(valeurs)):
        Page.objects.filter(pk = valeurs[i]).update(number = i)

    return JsonResponse(data) 




def print_latex_to_pdf(request,idch,idp):

    preamb = settings.TEX_PREAMBULE_PDF_FILE

    entetes=open(preamb,"r")
    elements=entetes.read()
    entetes.close()
    elements +=r"\begin{document}"+"\n"  


    if idch :
 
        chapter = Chapter.objects.get(pk=idch)
        for page in chapter.pages.filter(is_publish=1).order_by("number"):
            if page.paragraphs.count()>0 :
                elements +=  r'{\huge '+ page.title+r'} \hfill '+str(chapter.book.level.shortname)+". "+  chapter.title
                elements +=  r" \hrule "
            for paragraph in page.paragraphs.order_by("ranking"):
                if 'Cours' in page.title and paragraph.number > 0 : elements += r'\section{'+paragraph.title+r'}'
                elif paragraph.number > 0 : elements += r'\section*{'+paragraph.title+r'}' 
                for bloc in paragraph.blocs.order_by("ranking"):
                    if bloc.size != 12 :
                        elements += r"\begin{minipage}{"+str(round(bloc.size/12 - 0.005,3)).replace(",",".") +r"\linewidth}"
                        elements +=  bloc.typebloc_latex()
                        elements += r"\end{minipage}\hfill"

                    else :
                        elements +=  bloc.typebloc_latex()

            elements += r"\newpage"

    elif idp :
        page = Page.objects.get(pk=idp)
        elements +=  r'{\huge '+ page.title+r'}'
        elements +=  r" \hrule "
        for paragraph in page.paragraphs.order_by("ranking"):
            if 'Cours' in page.title and paragraph.number > 0 : elements += r'\section{'+paragraph.title+r'}'
            elif paragraph.number > 0 : elements += r'\section*{'+paragraph.title+r'}' 
            for bloc in paragraph.blocs.order_by("ranking"):
                if bloc.size != 12 :
                    elements += r"\begin{minipage}{"+str(round(bloc.size/12 - 0.005,3)).replace(",",".") +r"\linewidth}"
                    elements +=  bloc.typebloc_latex()
                    elements += r"\end{minipage}\hfill"
                else :
                    elements +=  bloc.typebloc_latex()


    elements +=  r"\end{document}"
    ################################################################# 
    ###########################################
    ###################### Attention ERREUR si non modif
    # pour windows
    # file_path = settings.DIR_TMP_TEX+r"\\doc" 
    # pour le serveur Linux
 
    file_path = settings.DIR_TMP_TEX+ str(request.user.id)+"_"+str(idp)
    ################################################################# 
    ################################################################# 
    with open(file_path+".tex" , 'w') as file:
        file.write(elements)
        file.close()

    result = subprocess.run(["pdflatex", "-interaction","nonstopmode",  "-output-directory", settings.DIR_TMP_TEX  ,  file_path ])

    if os.path.isfile(file_path+".out"):os.remove(file_path+".out")
    if os.path.isfile(file_path+".aux"):os.remove(file_path+".aux")    
 

    try :
        return FileResponse(open(file_path+".pdf", 'rb'))
    except :
        return FileResponse(open(file_path+".log", 'rb'))




def print_latex_to_book(request,idch,idp):

    preamb = settings.TEX_PREAMBULE_PDF_FILE_BOOK

    entetes=open(preamb,"r")
    elements=entetes.read()
    entetes.close()
    elements +=r"\begin{document}" 

    if idch :
        
        chapter = Chapter.objects.get(pk=idch)
        for page in chapter.pages.filter(is_publish=1).order_by("number"):
            if 'course_page_top' == page.css  :
                elements += r"\begin{pageCours}"
            elif 'ad_page_top' == page.css  :
                elements += r"\begin{pageAd}"
            elif 'parcoursu_page_top' == page.css  :
                elements += r"\begin{pageparcoursu}"
            elif 'parcoursd_page_top' == page.css  :
                elements += r"\begin{pageParcoursd}"
            elif 'parcourst_page_top' == page.css  :
                elements += r"\begin{pageParcourst}"
            elif 'parcoursd_page_top' == page.css  :
                elements += r"\begin{pageParcoursd}"
            elif 'auto_page_top' == page.css  :
                elements += r"\begin{pageAuto}"
            elif 'algo_page_top' == page.css  :
                elements += r"\begin{pageAlgo}"
            else :
                elements += r"\begin{pageIntro}"

            for paragraph in page.paragraphs.order_by("ranking"):

                if paragraph.number > 0 : 
                    elements += r'\section{'+paragraph.title+r'}' 

                for bloc in paragraph.blocs.filter(insidebloc=None).order_by("ranking"):
                    latexbloc , latextype = bloc.typebloc.latexbloc, bloc.typebloc.latextype
                    if bloc.size != 12 :
                        elements += r"\begin{minipage}{"+str(round(bloc.size/12 - 0.005,3)).replace(",",".") +r"\linewidth}"
                        if latexbloc == 'Ex' : latexbloc = 'ExP'
                        elements += r'\begin{'+latexbloc+r'}' 
                        close_latextype = False 
                        if latextype : 
                            elements += r'\begin{'+latextype+r'}' 
                        elements += r'\begin{Bloc}'+bloc.content+r'\end{Bloc}'                              
                        if latextype and not close_latextype :
                            elements += r'\end{'+latextype+'}' 

                        for b in paragraph.blocs.filter(insidebloc=bloc.id).order_by("ranking"):
                            lbloc = b.typebloc.latexbloc
                            elements += r"\begin{minipage}{"+str(round(b.size/12 - 0.005,3)).replace(",",".")
                            if 'Ex' ==  lbloc : 
                                elements += r'\colorbox{white}{\begin{'+lbloc+r'}' + b.content + r'\end{'+lbloc+r'}}' 
                            else :
                                if 'Mt' ==  lbloc or 'ExR' ==  lbloc and latextype : 
                                    elements += r'\end{'+latextype+'}' 
                                    close_latextype = True
                                elements += r'\begin{'+lbloc+r'}' + b.content + r'\end{'+lbloc+r'}'
                            elements += r"\end{minipage}" 
                        if latexbloc == 'Ex' : latexbloc = 'ExP'  
                        elements += r'\end{'+latexbloc+r'} \end{minipage} \hfill'

                    else :
                        elements += r'\begin{'+latexbloc+r'}' 
                        if latextype : 
                            elements += r'\begin{'+latextype+r'}' 
                        elements += r'\begin{Bloc}'+bloc.content+r'\end{Bloc}\vspace{2mm}' 
                        close_latextype = False 
                        for b in paragraph.blocs.filter(insidebloc=bloc.id).order_by("ranking"):
                            lbloc = b.typebloc.latexbloc
                            if 'Ex' ==  lbloc : 
                                elements += r'\colorbox{white}{\begin{'+lbloc+r'}' + b.content + r'\end{'+lbloc+r'}}' 
                            else :
                                if 'Mt' ==  lbloc or 'ExR' ==  lbloc and latextype : 
                                    elements += r'\end{'+latextype+'}' 
                                    close_latextype = True
                                elements += r'\begin{'+lbloc+r'}' + b.content + r'\end{'+lbloc+r'}'                                     
                        if latextype and not close_latextype :
                            elements += r'\end{'+latextype+'}'  
                        elements += r'\end{'+latexbloc+r'}'

            if 'course_page_top' == page.css  :
                elements += r"\end{pageCours}"
            elif 'ad_page_top' == page.css  :
                elements += r"\end{pageAd}"
            elif 'parcoursu_page_top' == page.css  :
                elements += r"\end{pageparcoursu}"
            elif 'parcoursd_page_top' == page.css  :
                elements += r"\end{pageParcoursd}"
            elif 'parcourst_page_top' == page.css  :
                elements += r"\end{pageParcourst}"
            elif 'parcoursd_page_top' == page.css  :
                elements += r"\end{pageParcoursd}"
            elif 'auto_page_top' == page.css  :
                elements += r"\end{pageAuto}"
            elif 'algo_page_top' == page.css  :
                elements += r"\end{pageAlgo}"
            else :
                elements += r"\end{pageIntro}"

    elif idp :
        page = Page.objects.get(pk=idp)
        if 'course_page_top' == page.css  :
            elements += r"\begin{pageCours}"
        elif 'ad_page_top' == page.css  :
            elements += r"\begin{pageAd}"
        elif 'parcoursu_page_top' == page.css  :
            elements += r"\begin{pageparcoursu}"
        elif 'parcoursd_page_top' == page.css  :
            elements += r"\begin{pageParcoursd}"
        elif 'parcourst_page_top' == page.css  :
            elements += r"\begin{pageParcourst}"
        elif 'parcoursd_page_top' == page.css  :
            elements += r"\begin{pageParcoursd}"
        elif 'auto_page_top' == page.css  :
            elements += r"\begin{pageAuto}"
        elif 'algo_page_top' == page.css  :
            elements += r"\begin{pageAlgo}"
        else :
            elements += r"\begin{pageIntro}"


        for paragraph in page.paragraphs.order_by("ranking"):

            if paragraph.number > 0 : 
                elements += r'\section{'+paragraph.title+r'}' 
            for bloc in paragraph.blocs.filter(insidebloc=None).order_by("ranking"):
                latexbloc , latextype = bloc.typebloc.latexbloc, bloc.typebloc.latextype
                if bloc.size != 12 :
                    elements += r"\begin{minipage}{"+str(round(bloc.size/12 - 0.005,3)).replace(",",".") +r"\linewidth}"
                    if latexbloc == 'Ex' : latexbloc = 'ExP'
                    elements += r'\begin{'+latexbloc+r'}' 
                    close_latextype = False 
                    if latextype : 
                        elements += r'\begin{'+latextype+r'}' 
                    elements += r'\begin{Bloc}'+bloc.content+r'\end{Bloc}'                              
                    if latextype and not close_latextype :
                        elements += r'\end{'+latextype+'}' 

                    for b in paragraph.blocs.filter(insidebloc=bloc.id).order_by("ranking"):
                        lbloc = b.typebloc.latexbloc
                        elements += r"\begin{minipage}{"+str(round(b.size/12 - 0.005,3)).replace(",",".")
                        if 'Ex' ==  lbloc : 
                            elements += r'\colorbox{white}{\begin{'+lbloc+r'}' + b.content + r'\end{'+lbloc+r'}}' 
                        else :
                            if 'Mt' ==  lbloc or 'ExR' ==  lbloc and latextype : 
                                elements += r'\end{'+latextype+'}' 
                                close_latextype = True
                            elements += r'\begin{'+lbloc+r'}' + b.content + r'\end{'+lbloc+r'}'
                        elements += r"\end{minipage}" 
                    if latexbloc == 'Ex' : latexbloc = 'ExP'  
                    elements += r'\end{'+latexbloc+r'} \end{minipage} \hfill'

                else :
                    elements += r'\begin{'+latexbloc+r'}' 
                    if latextype : 
                        elements += r'\begin{'+latextype+r'}' 
                    elements += r'\begin{Bloc}'+bloc.content+r'\end{Bloc}\vspace{2mm}' 
                    close_latextype = False  
                    for b in paragraph.blocs.filter(insidebloc=bloc.id).order_by("ranking"):
                        lbloc = b.typebloc.latexbloc
                        if 'Ex' ==  lbloc : 
                            elements += r'\colorbox{white}{\begin{'+lbloc+r'}' + b.content + r'\end{'+lbloc+r'}}' 
                        else :
                            if 'Mt' ==  lbloc or 'ExR' ==  lbloc and latextype : 
                                elements += r'\end{'+latextype+'}' 
                                close_latextype = True
                            elements += r'\begin{'+lbloc+r'}' + b.content + r'\end{'+lbloc+r'}'                                     
                    if latextype and not close_latextype :
                        elements += r'\end{'+latextype+'}' 
                    elements += r'\end{'+latexbloc+r'}' 

        if 'course_page_top' == page.css  :
            elements += r"\end{pageCours}"
        elif 'ad_page_top' == page.css  :
            elements += r"\end{pageAd}"
        elif 'parcoursu_page_top' == page.css  :
            elements += r"\end{pageparcoursu}"
        elif 'parcoursd_page_top' == page.css  :
            elements += r"\end{pageParcoursd}"
        elif 'parcourst_page_top' == page.css  :
            elements += r"\end{pageParcourst}"
        elif 'parcoursd_page_top' == page.css  :
            elements += r"\end{pageParcoursd}"
        elif 'auto_page_top' == page.css  :
            elements += r"\end{pageAuto}"
        elif 'algo_page_top' == page.css  :
            elements += r"\end{pageAlgo}"
        else :
            elements += r"\end{pageIntro}"
    

    elements +=r"\end{document}"
    ################################################################# 
    ###########################################
    ###################### Attention ERREUR si non modif
    # pour windows
    # file_path = settings.DIR_TMP_TEX+r"\\doc" 
    # pour le serveur Linux
 
    file_path = settings.DIR_TMP_TEX+ str(request.user.id)+"_book_"+str(idp)
    ################################################################# 
    ################################################################# 
    with open(file_path+".tex" , 'w') as file:
        file.write(elements)
        file.close()

    result = subprocess.run(["pdflatex", "-interaction","nonstopmode",  "-output-directory", settings.DIR_TMP_TEX  ,  file_path ])

    if os.path.isfile(file_path+".out"):os.remove(file_path+".out")
    if os.path.isfile(file_path+".aux"):os.remove(file_path+".aux")    
 

    try :
        return FileResponse(open(file_path+".pdf", 'rb'))
    except :
        return FileResponse(open(file_path+".log", 'rb'))




def print_latex_to_tex_avec_cor(request,idch,idp):


    elements =""  

    if idch :
 
        chapter = Chapter.objects.get(pk=idch)
        for page in chapter.pages.filter(is_publish=1).order_by("number"):
            if page.paragraphs.count()>0 :
                elements +=  r'{\LARGE '+ page.title+r'} \hfill '+str(chapter.book.level.shortname)+". "+  chapter.title
                elements +=  r" \hrule"
            for paragraph in page.paragraphs.order_by("ranking"):
                if 'Cours' in page.title : elements += r'\section{'+paragraph.title+r'}'
                elif paragraph.number > 0 : elements += r'\section*{'+paragraph.title+r'}' 
 
                for bloc in paragraph.blocs.order_by("ranking"):

                    if bloc.size != 12 :
                        elements += r"\begin{minipage}{"+str(round(bloc.size/12 - 0.005,3)).replace(",",".") +r"\linewidth}"
                        elements +=  bloc.typebloc_latex(inclureCor=True)
                        elements += r"\end{minipage}\hfill"

                    else : 
                        elements +=  bloc.typebloc_latex(inclureCor=True)

 

            elements += r"\newpage"

    elif idp :
        page = Page.objects.get(pk=idp)
        elements +=  r'{\LARGE '+ page.title+r'}'
        elements +=  r" \hrule"
        for paragraph in page.paragraphs.order_by("ranking"):
            if 'Cours' in page.title : elements += r'\section{'+paragraph.title+r'}'
            elif paragraph.number > 0 : elements += r'\section*{'+paragraph.title+r'}' 

            for bloc in paragraph.blocs.order_by("ranking"):
                if bloc.size != 12 :
                    elements += r"\begin{minipage}{"+str(round(bloc.size/12 - 0.005,3)).replace(",",".") +r"\linewidth}"
                    elements +=  bloc.typebloc_latex(inclureCor=True)
                    elements += r"\end{minipage}\hfill"

                else : 
                    elements +=  bloc.typebloc_latex(inclureCor=True)

    ################################################################# 
    ###########################################
    ###################### Attention ERREUR si non modif
    # pour windows
    # file_path = settings.DIR_TMP_TEX+r"\\doc" 
    # pour le serveur Linux
 
    file_path = settings.DIR_TMP_TEX+ str(request.user.id)+"_"+str(idp)
    ################################################################# 
    ################################################################# 
    with open(file_path+".tex" , 'w', encoding='UTF-8') as file:
        file.write(elements)
        file.close()

    return FileResponse( open(file_path+".tex",'rb') , as_attachment=True, filename="Source_Tex.tex")






def print_latex_to_tex(request,idch,idp):


    elements =""  

    if idch :
 
        chapter = Chapter.objects.get(pk=idch)
        for page in chapter.pages.filter(is_publish=1).order_by("number"):
            if page.paragraphs.count()>0 :
                elements +=  r'{\LARGE '+ page.title+r'} \hfill '+str(chapter.book.level.shortname)+". "+  chapter.title
                elements +=  r" \hrule"
            for paragraph in page.paragraphs.order_by("ranking"):
                if 'Cours' in page.title : elements += r'\section{'+paragraph.title+r'}'
                elif paragraph.number > 0 : elements += r'\section*{'+paragraph.title+r'}' 
 
                for bloc in paragraph.blocs.order_by("ranking"):

                    if bloc.size != 12 :
                        elements += r"\begin{minipage}{"+str(round(bloc.size/12 - 0.005,3)).replace(",",".") +r"\linewidth}"
                        elements +=  bloc.typebloc_latex()
                        elements += r"\end{minipage}\hfill"

                    else : 
                        elements +=  bloc.typebloc_latex()

 

            elements += r"\newpage"

    elif idp :
        page = Page.objects.get(pk=idp)
        elements +=  r'{\LARGE '+ page.title+r'}'
        elements +=  r" \hrule"
        for paragraph in page.paragraphs.order_by("ranking"):
            if 'Cours' in page.title : elements += r'\section{'+paragraph.title+r'}'
            elif paragraph.number > 0 : elements += r'\section*{'+paragraph.title+r'}' 

            for bloc in paragraph.blocs.order_by("ranking"):
                if bloc.size != 12 :
                    elements += r"\begin{minipage}{"+str(round(bloc.size/12 - 0.005,3)).replace(",",".") +r"\linewidth}"
                    elements +=  bloc.typebloc_latex()
                    elements += r"\end{minipage}\hfill"

                else : 
                    elements +=  bloc.typebloc_latex()

    ################################################################# 
    ###########################################
    ###################### Attention ERREUR si non modif
    # pour windows
    # file_path = settings.DIR_TMP_TEX+r"\\doc" 
    # pour le serveur Linux
 
    file_path = settings.DIR_TMP_TEX+ str(request.user.id)+"_"+str(idp)
    ################################################################# 
    ################################################################# 
    with open(file_path+".tex" , 'w', encoding='UTF-8') as file:
        file.write(elements)
        file.close()

    return FileResponse( open(file_path+".tex",'rb') , as_attachment=True, filename="Source_Tex.tex")


#################################################################
# paragraphs
#################################################################

@user_is_extra 
def pages(request,idb, idp):

    book = Book.objects.get(pk=idb)
    page = Page.objects.get(id=idp)

    context = {'book': book, 'page': page   }

    return render(request, 'book/form_page.html', context)


@user_is_extra 
def create_page(request,idb, idch):

    book = Book.objects.get(pk=idb)
    chapter = Chapter.objects.get(pk=idch)

    if request.method == "POST" :
        total_number = request.POST.get("total_number",None)
        if total_number :
            tn = int(total_number)
            for i in range(tn) :
                if i == tn-1 : title , css = "Algorithmique" , "algo_page_top"
                elif i == tn-2 : title , css = "Auto-évaluation DTL" , "auto_page_top"
                elif i == tn-3 : title , css = "Parcours 3" , "parcourst_page_top"
                elif i == tn-4 : title , css = "Parcours 2" , "parcoursd_page_top"
                elif i == tn-5 : title , css = "Parcours 1" , "parcoursu_page_top"
                elif i%2 == 1 : title , css = "Cours" , "course_page_top"
                elif i%2 == 0 and i > 0 : title , css = "Applications directes" , "ad_page_top"
                else : title , css = "Introduction" , "intro_page_top"
                Page.objects.create(title=title ,  number=i , chapter = chapter , css=css)
        return redirect('student_book_builder' , idb, 0)
    context = { 'idb' : idb , 'idch' : idch }

    return render(request, 'book/form_page.html', context)



@user_is_extra 
def add_page(request,idb, idch):

    add_page = request.POST.get("add_page",None)
    chapter = Chapter.objects.get(pk=idch)
    nbp = chapter.pages.count()
    if add_page :
        tn = int(add_page)
        for i in range(nbp, nbp+tn) :
            Page.objects.create(title="Nouvelle page "+str(i) ,  number=i , chapter_id = idch , css="course_page_top")
    return redirect('student_book_builder' , idb, 0)








@user_is_extra 
def update_page(request,idb, idp):

    book = Book.objects.get(pk=idb)
    page = Page.objects.get(id=idp)
    chapter = page.chapter 

    form_page = PageForm(request.POST or None,book=book, instance=page)
    form_p  = ParagraphForm(request.POST or None,book=book)
    form_b  = BlocForm(request.POST or None,book=book,page=page)
    form_tb = TypeblocForm(request.POST or None)

    if request.method == "POST" :
        form_action = request.POST.get("form_action")
        if form_action == "new_paragraph" :
            if form_p.is_valid():
                nf = form_p.save(commit=False)
                nf.page  = page
                nf.save() 
            else:
                print(form_p.errors)


        elif form_action == "new_bloc" :

            get_from_database    = request.POST.get("get_from_database",None)
            get_this_exercise_id = request.POST.get("get_this_exercise_id",None)

            if form_b.is_valid():
                nf = form_b.save()
                if nf.typebloc.id == 6 and get_from_database and get_from_database == "1" :
                    exo = Exotex.objects.get(pk = get_this_exercise_id)
                    nf.content = exo.content
                    nf.content_html = exo.content_html
                    nf.correction = exo.correction
                    nf.correction_html = exo.correction_html
                    nf.knowledge  = exo.knowledge
                    nf.theme      = exo.theme
                    nf.is_calculator = exo.calculator
                    nf.is_python    = exo.is_python 
                    nf.is_scratch   = exo.is_scratch
                    nf.is_tableur   = exo.is_tableur
                    nf.is_corrected = 1
                    nf.is_annals    = exo.is_annals
                    nf.save()

                    nf.skills.set( exo.skills.all())
                    nf.knowledges.set(exo.knowledges.all())
                    nf.exercises.set( exo.exercises.all())

                elif nf.typebloc.id == 6 :
                    try : 
                        title = nf.title.split(".")[1]
                    except :
                        title = nf.title
                    exo,created=Exotex.objects.update_or_create( 
                                                bloc_id=nf.id,
                                                defaults =  {
                                                'title' : title , 
                                                'author' : request.user.teacher , 
                                                'subject' : page.chapter.book.subject,  
                                                'knowledge' : nf.knowledge,   
                                                'level': page.chapter.book.level, 
                                                'theme': nf.theme,
                                                'content' : nf.content, 
                                                'content_html' :nf.content_html,
                                                'correction' : nf.correction,
                                                'correction_html' :nf.correction_html,
                                                'calculator' :nf.is_calculator,
                                                'is_share'     :1,
                                                'is_python'    :nf.is_python,
                                                'is_scratch':  nf.is_scratch,
                                                'is_tableur':  nf.is_tableur,
                                                'is_corrected' :1,
                                                'is_annals': nf.is_annals,
                                                'point' : 0 
                                                }
                                                )
                    if created :
                        exo.skills.set( nf.skills.all())
                        exo.knowledges.set(nf.knowledges.all())
                        exo.exercises.set( nf.exercises.all())

            else:
                print(form_b.errors)

                try :
                    f = open('/var/www/sacado/logs/debug.log','a')
                    writer_text = "{}".format(form_b.errors)
                    print(writer_text, file=f)
                    f.close()
                except :
                    pass 

        elif form_action == "new_typebloc" :
            if form_tb.is_valid():
                nf = form_tb.save()
            else:
                print(form_tb.errors)


        elif form_action == "update_page" :
            if form_page.is_valid():
                nf = form_page.save()
            else:
                print(form_page.errors)

        return redirect('update_page',idb,idp)

    
    use_this_css = "css/bookstyle_6.css"  #"css/bookstyle_"+str(book.level.id)+".css"   
    request.session["this_page_id_created"] = idp
    context = {'form_p': form_p,  'form_b': form_b,  'form_page': form_page, 'form_tb': form_tb, 'book': book, 'page': page,  'use_this_css' : use_this_css , 'chapter' : chapter }

    return render(request, 'book/form_update_page.html', context )


@user_is_extra 
def delete_page(request, idb,idp):

    page = Page.objects.get(id=idp)
    page.delete()
    return redirect('student_book_builder',idb,0)




@csrf_exempt
@user_is_extra 
def type_de_page(request):

    book_id = request.POST.get("book_id",None)
    page_id = request.POST.get("page_id",None)
    type_page = request.POST.get("type_page","course_page_top")
    if type_page == "course_page_top" : title = "Cours" 
    elif type_page == "ad_page_top" : title = "Applications directes" 
    elif type_page == "parcoursu_page_top" : title = "Parcours 1" 
    elif type_page == "parcoursd_page_top" : title = "Parcours 2" 
    elif type_page == "parcourst_page_top" : title = "Parcours 3" 
    elif type_page == "auto_page_top" : title = "Autoévaluation DTL" 

    Page.objects.filter(pk=page_id).update(css=type_page)
    Page.objects.filter(pk=page_id).update(title=title)

    data = {}
    data['css'] = type_page
    data['title'] = title

    return JsonResponse(data)



@user_is_extra 
def goto_update_page(request, idb,n):

    page = Page.objects.get(chapter__book=idb, number=n)
    idp  = page.id
 
    return redirect('update_page',idb,idp)
 


@csrf_exempt
def ajax_create_exercise_from_scratch(request):

    id_book  = request.POST.get("id_book")
    book     = Book.objects.get(pk=id_book)
    waitings = book.level.waitings.filter(theme__subject = book.subject).order_by("theme") 
    data = dict()
    context = { 'waitings':waitings}



    data["html"] = render_to_string('book/ajax_list_exotexs_for_creation.html', context )
 

    return JsonResponse(data)




#################################################################
# paragraphs
#################################################################
@user_is_extra 
def create_paragraph(request, idb):

    book = Book.objects.get(pk=idb)
    form = ParagraphForm(request.POST or None,book=book )

    if form.is_valid():
        form.save()
        messages.success(request, 'Le paragraphe a été créé avec succès !')
        return redirect('paragraphs')
    else:
        print(form.errors)

    context = {'form': form,  'paragraph': None  }

    return render(request, 'book/form_paragraph.html', context)



@user_is_extra 
def update_paragraph(request,idb, idp, idpa):

    book = Book.objects.get(pk=idb)
    page = Page.objects.get(pk=idp)
    paragraph = Paragraph.objects.get(id=idpa)
    form = ParagraphForm(request.POST or None,  instance=paragraph,book=book )
    if request.method == "POST" :
        if form.is_valid():
            form.save()
            messages.success(request, 'Le paragraphe a été modifié avec succès !')
            return redirect('update_page',idb,idp)
        else:
            print(form.errors)

    context = {'form': form, 'book' : book , 'page' : page ,  'paragraph': paragraph,   }

    return render(request, 'book/form_paragraph.html', context )


@user_is_extra 
def delete_paragraph(request, idb, idp, idpa):

    book = Book.objects.get(pk=idb)
    paragraph = Paragraph.objects.get(id=idpa)
    paragraph.delete()
    messages.success(request, 'Le paragraphe a été supprimé avec succès !')
    return redirect('update_page', idb, idp)


#################################################################
# typebloc
#################################################################


@user_is_extra
def typeblocs(request):
 
    typeblocs = Typebloc.objects.all()

    return render(request, 'book/typeblocs.html', {'typeblocs': typeblocs, })



@user_is_extra 
def create_typebloc(request):

    form = TypeblocForm(request.POST or None  )

    if form.is_valid():
        form.save()
        messages.success(request, 'Le typebloc a été créé avec succès !')
        return redirect('typeblocs')
    else:
        print(form.errors)

    context = {'form': form,  'typebloc': None  }

    return render(request, 'book/form_typebloc.html', context)



@user_is_extra 
def update_typebloc(request, idt):

    typebloc = Typebloc.objects.get(id=idt)
    form = TypeblocForm(request.POST or None, instance=typebloc )
    if request.method == "POST" :
        if form.is_valid():
            form.save()
            messages.success(request, 'Le typebloc a été modifié avec succès !')
            return redirect('typeblocs')
        else:
            print(form.errors)

    context = {'form': form, 'communications' : [] , 'typebloc': typebloc,   }

    return render(request, 'book/form_typebloc.html', context )


@user_is_extra 
def delete_typebloc(request, idt):
    typebloc = Typebloc.objects.get(id=idt)
    typebloc.delete()
    messages.success(request, 'Le typebloc a été supprimé avec succès !')
    return redirect('typeblocs')




@user_is_extra 
def create_bloc(request, idb, idp):

    book = Book.objects.get(id=idb)
    page = Page.objects.get(id=idp)
 
    form = BlocForm(request.POST or None  , book = book, page=page)
    if request.method == "POST" :
        if form.is_valid():
            form.save()
            messages.success(request, 'Le bloc a été modifié avec succès !')
            return redirect('update_page', idb, idp)
        else:
            print(form.errors)

    context = {'form': form, 'communications' : [] ,   'book' : book   }

    return render(request, 'book/form_typebloc.html', context )



@user_is_extra 
def update_bloc(request, idb, idp, idbl):

    book = Book.objects.get(id=idb)
    page = Page.objects.get(id=idp)
    bloc = Bloc.objects.get(id=idbl)

    form = BlocForm(request.POST or None, book = book , page=page  , instance=bloc )
    if request.method == "POST" :
        if form.is_valid():
            nf = form.save()
            Exotex.objects.filter(bloc_id=nf.id).update(content = nf.content, 
                                                            content_html =nf.content_html,
                                                            calculator = nf.is_calculator,
                                                            knowledge = nf.knowledge,   
                                                            theme = nf.theme,
                                                             is_share     = 1,
                                                             is_python    = nf.is_python,
                                                             is_scratch   =  nf.is_scratch,
                                                             is_tableur   =  nf.is_tableur,
                                                             is_corrected = 1,
                                                             is_annals   = nf.is_annals,
                                                             correction = nf.correction,
                                                             correction_html =nf.correction_html)


            messages.success(request, 'Le bloc a été modifié avec succès !')
            return redirect('update_page', idb, idp)
        else:
            print(form.errors)

    context = {'form_b': form,  'bloc': bloc, 'idb' : idb , 'idp' : idp , 'book' : book  }

    return render(request, 'book/form_bloc.html', context )


@user_is_extra 
def delete_bloc(request,idb, idp, idbl):
    bloc = Bloc.objects.get(id=idbl)
    bloc.delete()
    messages.success(request, 'Le bloc a été supprimé avec succès !')
    return redirect('update_page',idb, idp)


@csrf_exempt
def sorter_book_page_bloc(request):
    valeurs           = request.POST.getlist("valeurs")
    paragraph_id      = request.POST.get("paragraph_id")
    this_paragraph_id = request.POST.get("this_paragraph_id")
    this_bloc_id      = request.POST.get("this_bloc_id")
 
    data = {}
 
    if this_paragraph_id != paragraph_id :
        Bloc.objects.filter(pk = this_bloc_id).update(paragraph_id = paragraph_id)

    for i in range(len(valeurs)):
        Bloc.objects.filter(pk = valeurs[i]).update(ranking = i)

    return JsonResponse(data) 

 

def display_details_bloc_by_qr(request,idbl):

    bloc = Bloc.objects.get(pk=idbl)
    exercises = bloc.exercises.filter(supportfile__is_title=0, supportfile__is_ggbfile=1)
    exotexs    = bloc.exotexs.all()
    appliquettes = bloc.appliquettes.all()
    use_this_css = "css/bookstyle_6.css"  #"css/bookstyle_"+str(book.level.id)+".css"   
    context = { 'bloc': bloc, 'exercises': exercises,'exotexs': exotexs,'appliquettes': appliquettes, 'use_this_css' : use_this_css     }

    return render(request, 'book/details_bloc_by_qr.html', context )




def display_details_bloc_correction(request,idbl):

    bloc = Bloc.objects.get(pk=idbl)
    use_this_css = "css/bookstyle_6.css"  #"css/bookstyle_"+str(book.level.id)+".css"   
    context = { 'bloc': bloc, }

    return render(request, 'book/details_bloc_correction.html', context )








@user_is_extra 
def create_csv_appliquettes(request) :


    this_file = request.FILES.get("this_file")
    file_data = this_file.readlines()

    for line in file_data :
 
        if ";" in line:
            fields = line.split(";")
        elif "," in line:
            fields = line.split(",")

        iframe = '<iframe scrolling="no" title="ill1_tab_entiers_6" src="https://www.geogebra.org/material/iframe/id/jswfw5bn/width/750/height/280/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false" width="750px" height="280px" style="border:0px;"></iframe>'

 
        if fields[1] != "" : forme = fields[1]
        else :  forme = "sans forme"

        if fields[2] != "" : title  = fields[2]
        if fields[3] != "" : url    = fields[3]
        if fields[4] != "" : iframe = fields[4]
        
        Appliquette.objects.get_or_create(forme=forme, title=title, url=url, iframe=iframe )
        idb = 1
        idp = 1

    return redirect('update_page',idb, idp)




@user_is_extra 
def list_appliquettes(request,idl):

    if idl == 0 :
        appliquettes = Appliquette.objects.order_by("level")
    else :
        appliquettes = Appliquette.objects.filter(level_id=idl).order_by("level")

    context = {'appliquettes': appliquettes, 'idl' : idl }

    return render(request, 'book/list_appliquettes.html', context )




def new_code(idl):

    str_code = "123456789abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ"
    exist = True
    while exist :
        new_str = str(idl)
        for i in range(3) :
            new_str += str_code[ random.randint(0,60) ] 
        if Appliquette.objects.filter(code=new_str).count() == 0: exist = False 
    return new_str





@user_is_extra 
def create_appliquette(request,idl):

    form = AppliquetteForm(request.POST or None)
    if request.method == "POST" :
        if form.is_valid():
            nf = form.save(commit=False)
            nf.level.id = idl
            nf.code = new_code(idl)
            nf.save()
            return redirect('list_appliquettes',idl)
        else:
            print(form.errors)

    context = {'form': form,  'idl' : idl }

    return render(request, 'book/form_appliquette.html', context )



@user_is_extra 
def update_appliquette(request, ida):

    app = Appliquette.objects.get(id=ida)
    form = AppliquetteForm(request.POST or None,instance=app)
    if request.method == "POST" :
        if form.is_valid():
            form.save()
            return redirect('list_appliquettes', app.level.idl)
        else:
            print(form.errors)

    context = {'form': form,  'app' : app }

    return render(request, 'book/form_appliquette.html', context )


@user_is_extra 
def delete_appliquette(request,ida):

    app = Appliquette.objects.get(id=ida)
    level_id = app.level.idl
    app.delete()
    messages.success(request, "L'appliquette a été supprimée avec succès !")
    return redirect('list_appliquettes', level_id)



def show_appliquette(request,ida):

    app = Appliquette.objects.get(id=ida)

    context = { 'app' : app }

    return render(request, 'book/show_appliquette.html', context )



@csrf_exempt
def ajax_display_correction_bloc(request):


    type_id   = request.POST.get('type_id',None)
    source_id = request.POST.get('source_id',None)
    status    = request.POST.get('status',False)
    group_id  = request.session.get('book_group_id')
    is_correction    = request.POST.get('is_correction',False)

    if status == "off" : 
        status , css , nocss = True ,  "text-success",  "text-secondary"
    else : 
        status , css,nocss =  False , "text-secondary",  "text-success"

    if type_id == "0" :            
        chapter = Chapter.objects.get(pk=source_id)
        if is_correction :
            for p in chapter.pages.all():
                for paragraph in p.paragraphs.all():
                    for bloc in  paragraph.blocs.all():
                        Mybloc.objects.filter(group_id=group_id, bloc=bloc).update(is_display_cor=status) 
        else :
            for p in chapter.pages.all():
                for paragraph in p.paragraphs.all():
                    for bloc in  paragraph.blocs.all():
                        Mybloc.objects.filter(group_id=group_id, bloc=bloc).update(is_display_comp=status) 

    elif type_id == "1" :  
        if is_correction :
            page = Page.objects.get(pk=source_id) 
            for paragraph in page.paragraphs.all():
                for bloc in  paragraph.blocs.all():
                    Mybloc.objects.filter(group_id=group_id, bloc=bloc).update(is_display_cor=status) 
        else :
            page = Page.objects.get(pk=source_id) 
            for paragraph in page.paragraphs.all():
                for bloc in  paragraph.blocs.all():
                    Mybloc.objects.filter(group_id=group_id, bloc=bloc).update(is_display_comp=status) 

    elif type_id == "2" : 
        if is_correction :
            paragraph = Paragraph.objects.get(pk=source_id) 
            for bloc in  paragraph.blocs.all():
                Mybloc.objects.filter(group_id=group_id, bloc=bloc).update(is_display_cor=status) 
        else :
            paragraph = Paragraph.objects.get(pk=source_id) 
            for bloc in  paragraph.blocs.all():
                Mybloc.objects.filter(group_id=group_id, bloc=bloc).update(is_display_comp=status) 

    elif  type_id == "3" : 
        if is_correction :
            Mybloc.objects.filter(group_id=group_id, bloc=source_id).update(is_display_cor=status)  
        else :
            Mybloc.objects.filter(group_id=group_id, bloc=source_id).update(is_display_comp=status) 

    data = {}
    data['css'] = css
    data['nocss'] = nocss
    return JsonResponse(data) 


@csrf_exempt
def group_can_get_the_book(request):    
    group_id    = request.POST.get('group_id',False)
    data = dict()
    print(group_id)

    if Mybook.objects.filter(group_id = group_id, book_id = 9 ).count() :    
        Mybook.objects.filter(group_id = group_id).delete()
        Mybloc.objects.filter(group_id = group_id).delete()

    else :
        Mybook.objects.update_or_create(group_id = group_id, book_id = 9 , defaults ={ 'is_display' : 1 })
        book = Book.objects.get(pk=9)
        for chapter in book.chapters.all():
            for p in chapter.pages.all():
                for paragraph in p.paragraphs.all():  
                    for bloc in  paragraph.blocs.all():
                        Mybloc.objects.update_or_create(group_id=group_id, bloc=bloc, defaults ={ 'is_display_cor':0, 'is_display_comp' : 1 } ) 
    return JsonResponse(data)


def ajax_insidebloc(request):

    id_paragraph   = request.POST.get('id_paragraph',None)
    paragraph = Paragraph.objects.get(pk=id_paragraph) 
    blocs =  list(paragraph.blocs.values_list('id','title'))

    data = {'blocs' : blocs}
    return JsonResponse(data)



def ajax_knowledge_inbloc(request):

    id_theme  = request.POST.get('id_theme',None)
    id_level  = request.POST.get('id_level',None)

    theme = Theme.objects.get(pk=id_theme) 
    waitings = theme.waitings.filter(level_id=id_level)
    knowledges = list()
    for w in waitings :
        knowledges+=list(w.knowledges.values_list('id','name'))

    data = {'knowledges' : list(knowledges)}


    return JsonResponse(data)