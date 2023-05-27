from django.conf import settings # récupération de variables globales du settings.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import  permission_required,user_passes_test, login_required
from django.db.models import Q , Sum , Avg
from django.core.mail import send_mail
from django.http import JsonResponse 
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import Book, Chapter
from .forms import *
from account.models import User
from qcm.models import Parcours

from socle.decorators import user_is_superuser
from django.utils.html import escape
 

################################################################################################
########################    FONCTIONS ANNEXE    ################################################
################################################################################################

@user_is_superuser 
def books(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    teacher = request.user.teacher
    mybooks = Book.objects.filter(level__in=teacher.levels.all(), subject__in=teacher.subjects.all(),is_publish=1).order_by('subject','level')
    
    levels   = teacher.levels.order_by("ranking")
    subjects = teacher.subjects.all()

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


@user_is_superuser 
def create_book(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    
    form = BookForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        nf = form.save(commit=False)
        user = User.objects.get(id=2480)
        nf.author = user.teacher
        nf.save()
        nf.teachers.add(request.user.teacher)
        messages.success(request, 'Le livre a été créé avec succès !')
        return redirect('books')
    else:
        print(form.errors)

    context = {'form': form,  }
    return render(request, 'book/form_book.html', context)


@user_is_superuser 
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


@user_is_superuser 
def delete_book(request):


    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    book = Book.objects.get(id=idb)
    book.delete()
    return redirect('books')



def implement_book_courses(request,book) :

    i = 1
    for p in Parcours.objects.filter(level=book.level,subject=book.subject,teacher__user_id=2480).order_by("ranking") :
        chapt,crea  = Chapter.objects.get_or_create(book=book,title=p.title,author_id=2480,defaults={'is_publish':1,'ranking':i})
        courses = p.course.all()
        i+=1
        documents = list()
        for c in courses :
            document,created = Document.objects.get_or_create(title=c.title, subject = book.subject, level=book.level, section_id=2, author_id=2480, defaults={'is_publish':1,'is_share':1,'ranking':i,'content' : c.annoncement})
            if created : documents.append(document)
        chapt.documents.set(documents)
        chapt.teachers.add(request.user.teacher)


def show_conception_book(request,idb,idch,is_conception):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    teacher = request.user.teacher

    book = Book.objects.get(id=idb)
    chapters = book.chapters.filter(teachers=teacher).order_by("ranking")
    form = NewChapterForm(request.POST or None )

    formdoc = DocumentForm(request.POST or None,teacher=teacher )
    formsec = SectionForm(request.POST or None)
    form_type = request.POST.get("form_type", None )

    sections = teacher.sections.order_by("ranking")
    if is_conception : 
        template =  'book/conception_book.html'
        if idch == 0 :
            chapter = chapters.first()
        else :
            chapter = Chapter.objects.get(id=idch)
        if chapter :
            documents = chapter.documents.order_by("section__ranking","ranking")
            context = { 'chapter': chapter , 'documents': documents  }
        else :
            context = { }
    else : 
        template =  'book/show_book.html'
        context = {}

    context.update({ 'book': book ,'chapters': chapters , 'form':form , 'formdoc':formdoc , 'formsec': formsec  , 'sections' : sections  })

    if request.method == "POST" :
        if form_type == "book" :
            if request.POST.get("is_update") == "1" :
                try : 
                    pk_update = request.POST.get("pk_update" , None )
                    chapter   = Chapter.objects.get(pk = pk_update)
                    form      = NewChapterForm(request.POST or None , instance = chapter )
                except : pass

            if form.is_valid():
                nf = form.save(commit=False)
                nf.book = book
                nf.author = request.user.teacher
                nf.save()
                nf.teachers.add(request.user.teacher)
                messages.success(request, 'Le chapitre a été modifié avec succès !')

            else:
                messages.error(request, formdoc.errors)

        elif form_type == "emplacement" :

            if formsec.is_valid():
                nf = formsec.save(commit=False)
                nf.teacher = request.user.teacher
                nf.save()
                messages.success(request, 'La section a été crée avec succès !')
            else :
                messages.error(request, formsec.errors)

        elif form_type == "document" :
            #doctypes = ["content","file","url","exercise","quizz","question","bibliotex","exotex","flashcard","flashpack"]
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
                nf.doctype = request.POST.get("doctype",2)
                nf.save()
                nf.teachers.add(teacher)
                chapter.documents.add(nf)
                messages.success(request, 'Le document a été créé avec succès !')
            else :
                messages.error(request, formdoc.errors)

        return redirect('conception_book',idb,idch)

    implement_book_courses(request,book)

    return render(request, template , context )




def show_book(request,idb):

    return show_conception_book(request,idb,0,False)

 
def conception_book(request,idb,idch):

    return show_conception_book(request,idb,idch,True)


@csrf_exempt
def sorter_chapter(request):

    valeurs = request.POST.getlist("valeurs")
    for i in range(len(valeurs)):
        Chapter.objects.filter(pk = valeurs[i]).update(ranking = i)

    data = {}
    return JsonResponse(data) 
  


#def duplicate_book(request,level,subject):
    
    # level_id   = request.POST.get("level_id")
    # subject_id = request.POST.get("subject_id")
    # school_id  = request.POST.get("school_id")
    # school     = School.objects.get(pk=school_id)

    # book = Book.objects.get( level_id=level_id , subject_id =subject_id )
    # for user in school.users.all() :
    #     teacher = user.teacher
    #     book.teachers.add(teacher)
    #     titles = ["Activités","Cours","Exercices","Fichiers téléchargeables","Quizz","Questions Flash","Vidéos"]
    #     for i in  range(len(titles)) :
    #         Document.objects.get_or_create( title=titles[i] , teacher=teacher ,defaults={'ranking':i} )



#################################################################
# section
#################################################################
@csrf_exempt
def update_section(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    section_id  = request.POST.get("section_id" , None )
    title  = request.POST.get("title" , None )

    Section.objects.filter(pk=section_id).update(title=escape(title))
    data = {}
    return JsonResponse(data) 

@csrf_exempt
def delete_section(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    section_id  = request.POST.get("section_id" , None )
    Section.objects.filter(pk=section_id).delete()
    data = {}
    return JsonResponse(data) 

 
@csrf_exempt
def sorter_section(request):

    valeurs = request.POST.getlist("valeurs")

    print(valeurs)
    for i in range(len(valeurs)):
        Section.objects.filter(pk = valeurs[i]).update(ranking = i)

    data = {}
    return JsonResponse(data) 
#################################################################
# chapter
#################################################################
def update_chapter(request,idb,idch):


    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"
    

    chapter = Chapter.objects.get(id=idch)
    form = BookForm(request.POST or None, instance=chapter )

    if form.is_valid():
        nf = form.save()
        messages.success(request, 'Le chapitre a été modifié avec succès !')
        return redirect('books')
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


def show_chapter(request,idb,idch):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    book    = Book.objects.get(id=idb)
    chapter = Chapter.objects.get(id=idch)
    return render(request, 'book/show_chapter.html', {'chapter': chapter , 'book': book  })




#################################################################
# document
#################################################################
@csrf_exempt
def delete_document(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    document_id  = request.POST.get("document_id" , None )
    Document.objects.filter(pk=document_id).delete()
    data = {}
    return JsonResponse(data) 

@csrf_exempt
def show_document(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    document_id  = request.POST.get("document_id" , None )
    document = Document.objects.get(pk=document_id)
    data = {}
    if document.section.id == 2 : 
        data["body"] = document.content
    data["title"] = document.title 
    return JsonResponse(data) 


 
@csrf_exempt
def sorter_document(request):

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
def get_type_document(request):

    this_type  = request.POST.get("type")
    level_id   = request.POST.get("level_id")
    subject_id = request.POST.get("subject_id")
    teacher    = request.user.teacher

    data = {}
    level   = Level.objects.get(pk=level_id)
    subject = Subject.objects.get(pk=subject_id)

    if this_type == "BiblioTex" :
        documents = Bibliotex.objects.filter(Q(teacher=teacher)|Q( is_share=1),subjects = subject , levels = level )[:100]
    elif this_type == "Course" :
        documents = Course.objects.filter(Q(teacher=teacher)|Q( is_share=1),subject = subject , level = level )[:100]
    elif this_type == "Exotex" :        
        documents = Exotex.objects.filter(is_share=1,subject = subject , level = level )[:100]
    elif this_type == "GGB" : 
        documents = Exercise.objects.filter(knowledge__theme__subject = subject , level  = level )[:100]
    elif this_type == "Flashpack" :        
        documents = Flashpack.objects.filter(Q(teacher=teacher)|Q( is_share=1),subject = subject , levels  = level )[:100]
    elif this_type == "Quizz" :
        documents = Quizz.objects.filter(Q(teacher=teacher)|Q( is_share=1),subject  = subject , levels  = level , is_random = 0 )[:100]
    elif this_type == "QF" :
        documents = Quizz.objects.filter(Q(teacher=teacher)|Q( is_share=1),subject  = subject , levels  = level , is_random = 1 )[:100]

    context = { 'documents' : documents ,  'this_type' : this_type }
    data['html'] = render_to_string('book/ajax_get_documents.html', context )

    return JsonResponse(data)
        


