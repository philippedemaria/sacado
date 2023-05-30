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

 


##################################     doctypes     ########################################     
##########  ["content","file","url","GGB","Quizz","Course","BiblioTex","Exotex","flashpack"]
##########  [    0    ,   1  ,  2  ,  3  ,   4   ,   5    ,     6     ,   7    ,      8]
##################################     doctypes     ########################################

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
        nf.teacher = user.teacher        
        nf.save()
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



def reset_all_chapters(request,idb) :

    Document.objects.all().delete()
    Section.objects.all().delete()
    book = Book.objects.get(pk=idb)
    i = 1
    for p in Parcours.objects.filter(level=book.level,subject=book.subject,teacher__user_id=2480).order_by("ranking") :
        chapt,crea  = Chapter.objects.get_or_create(book=book,title=p.title, author_id=2480 , teacher=request.user.teacher, defaults={'is_publish':1,'ranking':i})
        section, cre = Section.objects.get_or_create(title = "Cours" , chapter = chapt , defaults = {'ranking': 1, })
        courses = p.course.all()
        i+=1
        documents = list()
        for c in courses :
            document,created = Document.objects.get_or_create(title=c.title, subject = book.subject, level=book.level, section  = section , author_id=request.user.id , teacher=request.user.teacher, defaults={'is_publish':1,'is_share':1,'ranking':i,'content' : c.annoncement})
        chapt.sections.add(section)
    return redirect('conception_book', idb , 0 )
 

def show_conception_book(request,idb,idch,is_conception,is_chrono):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    teacher = request.user.teacher

    book = Book.objects.get(id=idb)
    chapters = book.chapters.filter(teacher=teacher).order_by("ranking")
    form = NewChapterForm(request.POST or None )

    formdoc = DocumentForm(request.POST or None  )
    formsec = SectionForm(request.POST or None)
    form_type = request.POST.get("form_type", None )

    if is_conception : 
        template =  'book/conception_book.html'
    else : 
        template =  'book/show_book.html'
        context = {}


    if idch == 0 :
        chapter = chapters.first()
    else :
        chapter = Chapter.objects.get(id=idch)
    sections = Section.objects.filter(chapter=idch).order_by("ranking")
    context = { 'book': book ,'chapters': chapters , 'form':form , 'formdoc':formdoc , 'formsec': formsec  ,'idch' : idch, 'chapter': chapter , 'sections': sections  }


    if is_chrono :
        sections = chapter.sections.all()
        documents = Document.objects.filter(section__in=sections).order_by("ranking")

        context.update({  'documents': documents  })
        template =  'book/chapter_chrono_concept_document.html'

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
            document_id      = request.POST.get("document_id")
            section_id       = request.POST.get("book_section_id_get",None)
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

                document = Document.objects.create(title = b.title, doc_id=doc_id , doctype = doctype, author = b.author, teacher = teacher, section_id = section_id , level = book.level , subject = book.subject,is_publish=1,is_share=1)
 
            return redirect('conception_book', idb , idch )

 
    return render(request, template , context )


def show_book(request,idb,idch):

    return show_conception_book(request,idb,idch,False,False)

 
def conception_book(request,idb,idch):

    return show_conception_book(request,idb,idch,True,False)


def chapter_chrono_concept_document(request,idb,idch):

    return show_conception_book(request,idb,idch,True,True)
 


def chapter_chrono_show_document(request,idb,idch):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

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
def update_book_section(request):

    request.session["tdb"] = "Books" # permet l'activation du surlignage de l'icone dans le menu gauche
    request.session["subtdb"] = "Chapter"

    section_id  = request.POST.get("section_id" , None )
    title  = request.POST.get("title" , None )

    Section.objects.filter(pk=section_id).update(title=escape(title))
    data = {}
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
    form_update = UpdateDocumentForm(instance=document )
 
    context = { 'form_update' : form_update , 'book' : book , 'chapter' : chapter }
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
    document = Document.objects.get(pk=document_id)
    data = {}
    data["body"] = document.content
    data["title"] = document.title 
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
    teacher    = request.user.teacher

    data = {}
    level   = Level.objects.get(pk=level_id)
    chapter = Chapter.objects.get(pk=chapter_id)
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
    else :
        documents = []

    context = { 'documents' : documents ,  'this_type' : this_type ,  'chapter' : chapter }
    data['html'] = render_to_string('book/ajax_get_documents.html', context )

    return JsonResponse(data)
        


###################################################################################################################################################################################################
###################################################################################################################################################################################################
###################################################################################################################################################################################################
#########################################################  Student book     #########################################################
###################################################################################################################################################################################################
###################################################################################################################################################################################################
###################################################################################################################################################################################################

def show_student_book(request,idb, n):
    book = Book.objects.get(pk=idb)
    i = 1
    for p in Parcours.objects.filter(level=book.level,subject=book.subject,teacher__user_id=2480).order_by("ranking") :
        chapt,crea  = Chapter.objects.get_or_create(book=book,title=p.title, author_id=2480 , teacher=request.user.teacher, defaults={'is_publish':1,'ranking':i})
        i+=1
 
    try :
        chapters = book.chapters.order_by("ranking")
        context = {'book': book,  'chapters': chapters,  }
    except :
        context = {'book': book, }

    return render(request, 'book/show_student_page.html', context)


@user_is_superuser 
def student_book_builder(request,idb, n):

    book = Book.objects.get(pk=idb)
    chapters = book.chapters.order_by("ranking")
    context = {'book': book,  'chapters': chapters,  }

    return render(request, 'book/conception_student_page.html', context)

 
#################################################################
# paragraphs
#################################################################

@user_is_superuser 
def pages(request,idb, idp):

    book = Book.objects.get(pk=idb)
    page = Page.objects.get(id=idp)

    context = {'book': book, 'page': page   }

    return render(request, 'book/form_page.html', context)


@user_is_superuser 
def create_page(request,idb, idch):

    book = Book.objects.get(pk=idb)
    chapter = Chapter.objects.get(pk=idch)

    if request.method == "POST" :
        total_number = request.POST.get("total_number",None)
        if total_number :
            tn = int(total_number)
            for i in range(book.pages.count(),tn) :
                Page.objects.create(number=i , chapter = chapter , css="cours")
        return redirect('student_book_builder' , idb, 0)
    context = { }

    return render(request, 'book/form_page.html', context)



@user_is_superuser 
def update_page(request,idb, idp):

    book = Book.objects.get(pk=idb)
    page = Page.objects.get(id=idp)

    form_page  = PageForm(request.POST or None,instance=page)
    form_p  = ParagraphForm(request.POST or None)
    form_b  = BlocForm(request.POST or None,book=book)
    form_tb = TypeblocForm(request.POST or None)

    if request.method == "POST" :
        form_action = request.POST.get("form_action")
        if form_action == "new_paragraph" :
            if form_p.is_valid():
                nf = form_p.save(commit=False)
                nf.page  = page
                nf.save() 
                messages.success(request, 'Le paragraphe a été créé avec succès !')
            else:
                print(form_p.errors)


        elif form_action == "new_bloc" :
            if form_b.is_valid():
                nf = form_b.save()
                messages.success(request, 'Le bloc a été créé avec succès !')
            else:
                print(form_b.errors)


        elif form_action == "new_typebloc" :
            if form_tb.is_valid():
                nf = form_tb.save()
                messages.success(request, 'Le typebloc a été créé avec succès !')
            else:
                print(form_tb.errors)


        elif form_action == "update_page" :
            if form_page.is_valid():
                nf = form_page.save()
                messages.success(request, 'La page a été modifiée avec succès !')
            else:
                print(form.errors)

        return redirect('update_page',idb,idp)

    
    use_this_css = "css/bookstyle_"+str(book.level.id)+".css"   

    context = {'form_p': form_p,  'form_b': form_b,  'form_page': form_page, 'form_tb': form_tb, 'book': book, 'page': page,  'use_this_css' : use_this_css , }

    return render(request, 'book/form_update_page.html', context )


@user_is_superuser 
def delete_page(request, idb,idp):

    book = Book.objects.get(pk=idb)
    page = Page.objects.get(id=idp)
    page.delete()
    if idp>0:
        idp -= 1
    messages.success(request, 'La page a été supprimée avec succès !')
    return redirect('pages',idb,idp)




#################################################################
# paragraphs
#################################################################



@user_is_superuser 
def create_paragraph(request,idb):

    book = Book.objects.get(pk=idb)
    form = ParagraphForm(request.POST or None , book=book )

    if form.is_valid():
        form.save()
        messages.success(request, 'Le paragraphe a été créé avec succès !')
        return redirect('paragraphs')
    else:
        print(form.errors)

    context = {'form': form,  'paragraph': None  }

    return render(request, 'book/form_paragraph.html', context)



@user_is_superuser 
def update_paragraph(request,idb, idp):

    book = Book.objects.get(pk=idb)
    paragraph = Paragraph.objects.get(id=idt)
    form = ParagraphForm(request.POST or None, book=book , instance=paragraph )
    if request.method == "POST" :
        if form.is_valid():
            form.save()
            messages.success(request, 'Le paragraphe a été modifié avec succès !')
            return redirect('paragraphs')
        else:
            print(form.errors)

    context = {'form': form, 'communications' : [] , 'paragraph': paragraph,   }

    return render(request, 'book/form_paragraph.html', context )


@user_is_superuser 
def delete_paragraph(request, idb,idp):

    book = Book.objects.get(pk=idb)
    paragraph = Paragraph.objects.get(id=idt)
    paragraph.delete()
    messages.success(request, 'Le paragraphe a été supprimé avec succès !')
    return redirect('paragraphs')


#################################################################
# typebloc
#################################################################


@user_is_superuser
def typeblocs(request):
 
    typeblocs = Typebloc.objects.all()

    return render(request, 'book/typeblocs.html', {'typeblocs': typeblocs, })



@user_is_superuser 
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



@user_is_superuser 
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


@user_is_superuser 
def delete_typebloc(request, idt):
    typebloc = Typebloc.objects.get(id=idt)
    typebloc.delete()
    messages.success(request, 'Le typebloc a été supprimé avec succès !')
    return redirect('typeblocs')


