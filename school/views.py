from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse
from .models import School, Country  , Stage , Town
from account.decorators import is_manager_of_this_school
from account.models import User, Teacher, Student , Parent ,Response
from qcm.models import Relationship  
from socle.models import Skill, Theme, Waiting, Knowledge
from account.forms import UserForm , StudentForm ,NewUserSForm
from association.models import Accounting, Rate, Detail, Customer
from school.forms import SchoolForm, CountryForm, GroupForm, StageForm, SchoolUpdateForm
from school.gar import *
from group.views import include_students
from group.models import Group, Sharing_group
from socle.decorators import user_is_superuser
from socle.models import Subject
from general_fonctions import *
from payment_fonctions import *
from django.conf import settings # récupération de variables globales du settings.py
from django.db.models import Avg, Count, Min, Sum
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
############### bibliothèques pour les impressions pdf  #########################
import os
from pdf2image import convert_from_path # convertit un pdf en autant d'images que de pages du pdf
from django.utils import formats
from io import BytesIO, StringIO
from django.http import  HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape , letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image , PageBreak,Frame , PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import yellow, red, black, white, blue
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from html import escape
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT 
cm = 2.54 
############## FIN bibliothèques pour les impressions pdf  #########################
import csv
#################################################################################


 
#def csv_new_school(request):

# with open ("/var/www/sacado/ressources/etablissements.csv", newline ="") as file :
# 		rows = csv.reader (file, delimiter=",")
#  	for row in rows :
#  		School.objects.create(name = row[0], country_id = 31 , town = row[1] , code_acad = "999efe" , address = "" , zip_code = "999999" , nbstudents = 500 , tiers = 411 )
#  		Town.objects.get_or_create(name =row[1] , zip_code = "999999", country_id = 31  )

# # with open ("d://uwamp/www/sacadogit/ressources/etablissementfr.csv", newline ="") as file :
# # 	rows = csv.reader (file, delimiter=";")
# # 	for row in rows :
# # 		if len(row[4]) == 4 : zip_c = "0"+str(row[4])
# # 		else : zip_c = row[4]
# # 		School.objects.create(name = row[0], country_id = 5 , town = row[1] , code_acad = row[2] , address = row[3] , zip_code = zip_c , nbstudents = 500 , tiers = 411) 



# return redirect('index')


def authorizing_access_school(teacher, school) :
	if (school == teacher.user.school and teacher.user.is_manager) or (school in teacher.user.schools.all() and teacher.user.is_manager) or teacher.user.is_superuser :
		return True
	else :
		return False



def this_school_in_session(request):

	school_id = request.session.get("school_id",None)

	if school_id :
		school = School.objects.get(pk = int(school_id))
	else :
		school = request.user.school
	return school 


def group_has_overall_parcourses(group):
    parcourses_tab = []
    for s in group.students.all() :
        pses = s.students_to_parcours.all()
        for p in pses :
            if p not in  parcourses_tab :
                parcourses_tab.append(p)

    return parcourses_tab


def sharing_teachers(request,group, teachers):

	# effacement de toute coanimation
	shares = Sharing_group.objects.filter(group  = group)
	for share in shares : 	
		share.delete()

	for folder in group.group_folders.all():
		folder.coteachers.clear()

	for parcours in group.group_parcours.all() :
		parcours.coteachers.clear()

	for bibliotex in group.bibliotexs.all():
		bibliotex.coteachers.clear()

	for flashpack in group.flashpacks.all():
		flashpack.coteachers.clear()


	choices = request.POST.getlist("choices") 
	for c in choices :
		c_tab = c.split("-")
		teacher = Teacher.objects.get(user_id = c_tab[1])
		role =  int(c_tab[0])
		sh , cre = Sharing_group.objects.get_or_create(group = group ,teacher = teacher , defaults = { 'role' : role }   )
		if not cre :
			sh.role = role
			sh.save()


		for folder in group.group_folders.all():
			folder.coteachers.add(teacher)
		for parcours in group.group_parcours.all() :
			parcours.coteachers.add(teacher)
		for bibliotex in group.bibliotexs.all():
			bibliotex.coteachers.add(teacher)
		for flashpack in group.flashpacks.all():
			flashpack.coteachers.add(teacher)




@user_is_superuser
def export_schools(request):

	schools = School.objects.filter(id__lt=10000)

	str_school = "["
	for school in schools :
		try :
			timezone=school.users.filter(user_type=2).first().timezone
		except :
			timezone="Europe/Paris"

		town = Town.objects.filter(country=school.country,zip_code=school.zip_code).first()

		try :
			str_school += "{ id :"+str(school.id)+", name :'"+school.name+"', address :'"+school.address+"', rne :'"+school.code_acad+"', timezone :'"+timezone+"', townId :"+str(town.id)+", logo :'"+str(school.logo)+"', isPrimary :'"+str(school.is_primaire)+"', isManaging :'"+str(school.is_managing)+"',nbStudent:'"+str(school.nbstudents)+"'},"
		except: 
			pass
	str_school += "]" 

 
	return render(request,'school/export_all_schools.html', {  'str_school': str_school    })

 








@user_is_superuser
def list_schools(request):

	countries = Country.objects.order_by("name")

	return render(request, 'school/lists.html', {  'countries': countries    })


@user_is_superuser
def create_school(request):
	form = SchoolForm(request.POST or None, request.FILES  or None)
	
	if form.is_valid():
		school = form.save()
		school.is_active = 1
		school.save()
		Stage.objects.create(school = school ,low = 30,  medium = 65, up = 85)
		t,r = Town.objects.get_or_create(  name=school.town ,  country=school.country ,  zip_code = school.zip_code )
		try :
			subject = "Création d'établissement"
			if school.gar : gar = "OUI"
			else : gar = "NON"
			school_datas = "\n"+school.name +"\n"+school.code_acad +  " - " + str(school.nbstudents) +  " élèves \n" + school.address +  "\n"+school.town+", "+school.country.name+"\n\nGAR : "+gar

			messages.success(request,"Création d'établissement réussie.")
			send_mail(subject,
		          "Bonjour,  :\n\n Vous avez créé un établissement \n\n" + request.user.email + " \n\n" +  school_datas +" \n\n Ceci est un mail automatique. Ne pas répondre.",
		          settings.DEFAULT_FROM_EMAIL ,
		          ["sacado.asso@gmail.com"])
		except :
			pass

		return redirect('schools')

	return render(request,'school/_form.html', { 'communications' : [], 'form':form})



 
def update_school(request,id):

	school = School.objects.get(id=id)
	form = SchoolUpdateForm(request.POST or None, request.FILES  or None, instance=school)
	if school.gar : gar =" GAR demandé" 
	else : gar =" GAR non demandé" 
	old_school_datas = "\n"+school.name +"\n"+school.code_acad +  " - " + str(school.nbstudents) +  " élèves \n" + school.address +  "\n"+school.town+", "+school.country.name+"\n\nGAR : "+ gar
	
	nb_total = school.users.filter(user_type=0).count()
	nb = 150
	if nb > nb_total:
		nb = nb_total

	ok = False
	if request.user.is_superuser or request.user.is_manager or request.user.school == school :
		form = SchoolForm(request.POST or None, request.FILES  or None, instance=school)
		ok = True
	else :
		form = SchoolUpdateForm(request.POST or None, request.FILES  or None, instance=school)


	if request.user.is_superuser or ok :
		if form.is_valid():
			school = form.save()
			school.is_active = 1
			school.save()

			if request.user.is_superuser :
				return redirect('schools')
			else :
				try :
					subject = "Modification d'établissement"
					if school.gar : gar = "OUI"
					else : gar = "NON"

					school_datas = "\n"+school.name +"\n"+school.code_acad +  " - " + str(school.nbstudents) +  " élèves \n" + school.address +  "\n"+school.town+", "+school.country.name+"\n\nGAR : "+ gar

					messages.success(request,"Modification de votre établissement réussie.")
					send_mail(subject,
				          "Bonjour,  :\n\n Vous avez modifié votre établissement \n\n" + request.user.email + " \n\nAnciennes données : \n\n" + old_school_datas + " \n\n----------------\n\nNouvelles données : \n\n" + school_datas +" \n\n Ceci est un mail automatique. Ne pas répondre.",
				          settings.DEFAULT_FROM_EMAIL ,
				          [request.user.email, "sacado.asso@gmail.com"])
				except :
					pass
				return redirect('admin_tdb')



	return render(request,'school/_form.html', {'form':form,  'communications' : [],'school':school ,'nb':nb ,'nb_total':nb_total  })


@user_is_superuser
def delete_school(request,id):
	school = School.objects.get(id=id)
	school.delete()
	return redirect('schools')


@user_is_superuser
def list_countries(request):
	countries = Country.objects.all()
	return render(request,'school/lists_country.html', { 'communications' : [], 'countries':countries})

@user_is_superuser
def create_country(request):
	form = CountryForm(request.POST or None,request.FILES or None )
	
	if form.is_valid():
		form.save()
		return redirect('countries')

	return render(request,'school/country_form.html', { 'communications' : [], 'form':form})

@user_is_superuser
def update_country(request,id):
	country = Country.objects.get(id=id)
	form = CountryForm(request.POST or None,request.FILES or None, instance=country)

	if form.is_valid():
		form.save()
		return redirect('countries')

	return render(request,'school/country_form.html', { 'communications' : [], 'form':form, 'country':country})

@user_is_superuser
def delete_country(request,id):
	country = Country.objects.get(id=id)
	country.delete()
	return redirect('countries')


###############################################################################################
###############################################################################################
######  School 
###############################################################################################
###############################################################################################


def clear_detail_student(student):
	try : 
		for p in student.folders.all():
			p.students.remove(student)
	except :
		pass
	try : 
		for p in student.students_to_parcours.all():
			p.students.remove(student)
	except :
		pass
	try : 
		for g in student.students_to_group.all():
			g.students.remove(student)
	except :
		pass
	try : 
		for r in student.students_relationship.all():
			r.students.remove(student)
	except :
		pass
	try : 
		for c in student.students_course.all() :
			c.students.remove(student)
	except :
		pass
	try : 	
		for a in student.relationtexs.all() :
			a.students.remove(student)
	except :
		pass
	try : 
		for f in student.flashpacks.all() :
			f.students.remove(student)
	except :
		pass
	try : 	
		for a in student.answercards.all() :
			a.students.remove(student)
	except :
		pass


#@is_manager_of_this_school
def school_teachers(request):


	school = this_school_in_session(request)


	teacher = Teacher.objects.get(user=request.user)

	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')


	teachers = User.objects.filter(Q(school=school)|Q(schools=school), user_type=2).order_by("last_name")  
 

	return render(request,'school/list_teachers.html', { 'communications' : [],'teachers':teachers, "school" : school })


#@is_manager_of_this_school
def school_groups(request):

	school = this_school_in_session(request)

	teacher = Teacher.objects.get(user=request.user)

	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')
		
	users = school.users.filter(user_type=2)
	groups = Group.objects.filter(teacher__user__in=users).order_by("level__ranking")

	for g in groups :
		g.school = school
		g.save()

	return render(request, 'school/list_groups.html', { 'communications' : [],'groups': groups, "school" : school })




#@is_manager_of_this_school
def school_level_groups(request):

	school = this_school_in_session(request)

	teacher = Teacher.objects.get(user=request.user)

	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')

	users = school.users.all()

	groups = Group.objects.filter(teacher__user__in = users).order_by("level") 

	return render(request,'school/list_level_groups.html', { 'communications' : [],'groups':groups, "school" : school })

#@is_manager_of_this_school
def school_students(request):

	
	school = this_school_in_session(request)
	teacher = Teacher.objects.get(user=request.user)

	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')


	users = User.objects.prefetch_related("student").filter(school = school, user_type=0).exclude(username__contains="_e-test_").order_by("last_name")    

	return render(request,'school/list_students.html', { 'communications' : [], 'users':users , 'school' : school , })


def school_students_gar(request):

	
	school = this_school_in_session(request)
	teacher = Teacher.objects.get(user=request.user)

	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')

	users = User.objects.prefetch_related("student").filter(school = school, user_type=0).exclude(username__contains="_e-test_").exclude(email__contains="@sacado.xyz").order_by("last_name")    

	return render(request,'school/list_students.html', { 'communications' : [], 'users':users , 'school' : school , })



def school_accounting(request):

	
	school = this_school_in_session(request)
	teacher = Teacher.objects.get(user=request.user)

	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')

	accountings = Accounting.objects.filter(school = school).order_by("-date")


	return render(request,'school/list_accountings.html', { 'accountings' : accountings , 'school' : school })



def new_student(request,slug):

    school = this_school_in_session(request)
    group = Group.objects.get(code=slug)
 
    user_form = NewUserSForm()
    form = StudentForm()
    return render(request,'school/student_form.html', { 'groups':None, 'group':group,  'user_form' : user_form, 'form' : form, "school" : school  })


def create_new_student(request):

    school = this_school_in_session(request)
    groups = school.school_group.all()
 
    user_form = NewUserSForm()
    form = StudentForm()
    return render(request,'school/student_form.html', {  'groups':groups, 'group':None, 'user_form' : user_form, 'form' : form, "school" : school  })




 
def get_school_students(request):

	
	school = this_school_in_session(request)
	teacher = Teacher.objects.get(user = request.user)
 
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')

	time_zone = request.user.time_zone
	teachers = Teacher.objects.filter(user__school = school)
	groups = Group.objects.filter(teacher__in = teachers)
	group_tab = []
	for group in groups :
		for student in group.students.filter(user__school=None, user__user_type=0): # ce sont les élèves de l'établissement pas encore assigné
			usr = student.user
			usr.school = school
			usr.time_zone = time_zone
			usr.save()
 
	messages.success(request, "Scan terminé avec succès. Les élèves trouvés sont importés.")

	return redirect('school_students')


 


#@is_manager_of_this_school
def new_student_list(request,slug):
	
    school = this_school_in_session(request)
    group = Group.objects.get(code=slug)
    students = group.students.all().order_by("user__last_name")

    p_students = Student.objects.filter(user__school = school).exclude(pk__in = group.students.values_list("user_id",flat=True)).order_by("user__last_name")
    pending_students = []
    for student in p_students :
    	pending_students.append(student)
    return render(request,'school/new_student_list.html', { 'communications' : [],'group':group, 'students' : students, 'pending_students' : pending_students, "school" : school  })

 


#@is_manager_of_this_school
def push_student_group(request):
	
	school = this_school_in_session(request)	
	group_id = request.POST.get("group_id")
	group = Group.objects.get(pk=group_id)

	student_ids = request.POST.getlist("student_ids")  

	for student_id in student_ids :
		student = Student.objects.get(pk=student_id)	
		group.students.add(student)
	return redirect('school_groups')
 

def get_username_teacher(request ,ln):
    """
    retourne un username
    """
    ok = True
    i = 0
    code = str(uuid.uuid4())[:3] 
    if request.user.school :
        suffixe = request.user.school.country.name[2]
    else :
        suffixe = ""
    name = str(ln).replace(" ","_")    
    un = name + "_" + suffixe + code 

    while ok:
        if User.objects.filter(username=un).count() == 0:
            ok = False
        else:
            i += 1
            un = un + str(i)
    return un 

def create_student_profile_inside_this_group(request,group) : 

    first_name = str(group.teacher.user.first_name).replace(" ", "")
    last_name  = str(group.teacher.user.last_name).replace(" ","") 
    name       = last_name + "_e-test"
    username   = get_username_teacher(request,name)
    password   = make_password("sacado2020")  
    email      = group.teacher.user.email

    if group.students.filter( user__username__contains=name).count() == 0 :
        user,created = User.objects.get_or_create(username=username , defaults= { 'last_name' : last_name, 'first_name' : first_name,  'password' : password , 'email' : "", 'user_type' : 0})

        if created :
            code = str(uuid.uuid4())[:8]                 
            student,created = Student.objects.get_or_create(user=user, level=group.level, code=code)
            group.students.add(student)
        else :
            student = Student.objects.get(user=user)
    else :
        student = False
    return student




#@is_manager_of_this_school
def new_group(request):
	
	school = this_school_in_session(request)
	teachers = Teacher.objects.filter(user__school=school)

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')

	form = GroupForm(request.POST or None, school = school)

	if request.method == "POST" :
		if form.is_valid():
			group = form.save()
			group.studentprofile = 1
			group.is_gar = school.gar
			group.save()
			stdts = request.POST.get("students")
			sharing_teachers(request,group,teachers)

			try :
				if stdts :
					include_students(request , stdts,group)        
			except :
				pass

			create_student_profile_inside_this_group(request,group)

			return redirect('school_groups')
		else :
			print(form.errors)

	return render(request,'school/group_form.html', {  'communications' : [], 'school' : school ,  'group' : None ,  'form' : form , 'teachers' : teachers ,  })





#@is_manager_of_this_school
def update_group_school(request,id):
	
	school = this_school_in_session(request)
	group = Group.objects.get(id=id)
	teachers = Teacher.objects.filter(user__school=school).exclude(user =  group.teacher.user)
	form = GroupForm(request.POST or None, school = school, instance = group)

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')

	if request.method == "POST" :
		if form.is_valid():
			form.save()
			################################################### Si l'élève n'est pas rattaché à un établissement on le joint ici
			teacher_school = group.teacher.user.school
			if teacher_school :
				for student in group.students.all():
					if not student.user.school :
						student.user.school = group.teacher.user.school
						student.user.save()
			###################################################

			sharing_teachers(request,group,teachers)
			stdts = request.POST.get("students")
			try :
				if len(stdts) > 0 :
					include_students(request,stdts,group)

			except :
				pass

			return redirect('school_groups')
		else :
			print(form.errors)

	return render(request,'school/group_form.html', { 'school' : school , 'group' : group ,  'form' : form , 'communications' : []  , 'teachers' : teachers , })




#@is_manager_of_this_school
def delete_student_group(request,id,ids):
	
	school = this_school_in_session(request)

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')

	group = Group.objects.get(id=id)
	student = Student.objects.get(user_id=ids)
	form = GroupForm(request.POST or None, school = school, instance = group)
	clear_detail_student(student)
	return redirect('update_group_school', group.id)




#@is_manager_of_this_school
def delete_all_students_group(request,id):
	
	school = this_school_in_session(request)

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')

	group = Group.objects.get(id=id)
	form = GroupForm(request.POST or None, school = school, instance = group)
	#for student in group.students.all() :
	#	clear_detail_student(student)
	group.students.all().delete()
	return redirect('update_group_school', group.id)

 

@csrf_exempt
def ajax_subject_teacher(request):
 	
    school = this_school_in_session(request)	
    subject_id =  int(request.POST.get("subject_id"))
    subject =  Subject.objects.get(pk = subject_id)
    data = {}
 
    teachers = Teacher.objects.filter(subjects = subject, user__school=school).order_by("user__last_name")
    tchs = []
    for t in teachers : 
    	tchs.append([t.user.id, t.user.last_name+" "+t.user.first_name])
		
    data['teachers'] = list(tchs)
 
    return JsonResponse(data)



#@is_manager_of_this_school
def delete_school_students(request):
	
	school = this_school_in_session(request)

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')

	User.objects.filter(school = school, user_type = 0).exclude(username__contains="_e-test_").delete()

	return redirect('admin_tdb')
 


#@is_manager_of_this_school
def delete_school_group_and_students(request):
	
	school = this_school_in_session(request)

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')

	students = Student.objects.filter(user__school = school, user__user_type = 0)
	for s in students :
		relations = Relationship.objects.filter(students = s)
		for r in relations :
			r.students.remove(s)
		s.user.delete()

	for g in school.school_group.all():
		for sg in g.group_sharingteacher.all():
			sg.delete()		
		g.delete()

	return redirect('admin_tdb')







#@is_manager_of_this_school
def delete_selected_students(request):
	
	school = this_school_in_session(request)
	teacher = Teacher.objects.get(user=request.user)

	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')


	user_ids = request.POST.getlist("user_ids")
	ebep = request.POST.get("ebep", None)

	if ebep : 
		for user_id in user_ids :
			student = Student.objects.get(user_id=user_id)
			if student.ebep :
				Student.objects.filter(user_id=user_id).update(ebep = False)
			else :
				Student.objects.filter(user_id=user_id).update(ebep = True)
	else :
		for user_id in user_ids :
			try :
				student = Student.objects.get(user_id=user_id)
				clear_detail_student(student)
				student.delete()
			except :
				pass
			user = User.objects.get(pk=user_id)
			user.delete()
	return redirect('school_students')





#@is_manager_of_this_school
def delete_selected_students_gar(request):
	
	school = this_school_in_session(request)
	teacher = Teacher.objects.get(user=request.user)

	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')


	user_ids = request.POST.getlist("user_ids")
	ebep = request.POST.get("ebep", None)

	if ebep : 
		for user_id in user_ids :
			student = Student.objects.get(user_id=user_id)
			if student.ebep :
				Student.objects.filter(user_id=user_id).update(ebep = False)
			else :
				Student.objects.filter(user_id=user_id).update(ebep = True)
	else :
		for user_id in user_ids :
			try :
				student = Student.objects.get(user_id=user_id)
				clear_detail_student(student)
				student.delete()
			except :
				pass
			user = User.objects.get(pk=user_id)
			user.delete()
	return redirect('school_students_gar')






#@is_manager_of_this_school
def new_group_many(request):
	
	school = this_school_in_session(request)

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')


	GroupFormSet = formset_factory(GroupForm , extra=2) 
	group_formset  = GroupFormSet(request.POST or None, form_kwargs={'school': school, })

	if request.method == "POST" :	
		if group_formset.is_valid():
			for f in group_formset :
				f.save()
			messages.success(request, "Groupes créés avec succès.")
			return redirect('school_groups')
		else :
			print(group_formset.errors)
 
	return render(request,'school/many_group_form.html', {'formset' : group_formset , 'school': school , 'communications' : [] , 'group' : None  })

 
def chargeschools(request) :

    data = {}
    country_id =  request.POST.get("country_id")  
    schools = School.objects.values_list('id', 'name').filter(country_id=country_id) 
    data['schools'] = list(schools)
    return JsonResponse(data)


def manager_teachers(request):
	school = this_school_in_session(request)
	for u in school.users.filter(user_type=2) :
		User.objects.filter(pk=u.id).update(is_manager=1)
	return redirect("school_teachers")

###############################################################################################
######  Renouvellement de l'adhésion
###############################################################################################
def get_first_adhesion(request):
	""" renouvellement de la cotisation annuelle"""

	user = request.user

	form = SchoolForm(request.POST or None)
	token = request.POST.get("token", None)
	today = datetime.now()


	if request.method == "POST" :
		if form.is_valid():
			name = request.POST.get("name")
			town = request.POST.get("town")
			code_acad = request.POST.get("code_acad")
			if School.objects.filter(name= name , town = town, code_acad = code_acad).count() == 0 :
				school = form.save()


				today = datetime.now()
				if today < datetime(today.year,7,1) :
				    somme = Rate.objects.filter(quantity__gte=school.nbstudents).first().discount
				else :
				    somme = Rate.objects.filter(quantity__gte=school.nbstudents).first().amount


				#accounting_id =  accounting_adhesion(school, today , None , user, False , "Premier abonnement" )
				# accounting = Accounting.objects.get(pk = accounting_id) 
				# date_start, date_stop = date_abonnement(today)
				# abonnement, abo_created = Abonnement.objects.get_or_create(school = school, date_start = date_start, date_stop = date_stop,  accounting_id = accounting_id , is_gar = school.gar , defaults={ 'user' : user, 'is_active' : 0}  )


				subject = "Adhésion SACADO - demande d'IBAN"
				school_datas = "\n"+school.name +"\n"+school.code_acad +  " - " + str(school.nbstudents) +  " élèves \n" + school.address +  "\n"+school.town+", "+school.country.name


				send_mail(subject,
				          "Bonjour,  :\n\n Vous avez formulé une demande d'abonnement \n\n" + user.email + " \n\n" +  school_datas +" \n\n Ceci est un mail automatique. Ne pas répondre.",
				          settings.DEFAULT_FROM_EMAIL ,
				          [user.email, "sacado.asso@gmail.com"])
 

 
				messages.success(request,"Demandé envoyée. Nous allons vous répondre rapidement. Merci.")
				return redirect( 'index')

			else :
				messages.error(request,"Etablissement déjà enregistré")



	context =  {  'user' : user , 'form' : form ,  }

	return render(request, 'school/get_first_adhesion.html', context)




def renew_school_adhesion(request):
	""" renouvellement de la cotisation annuelle"""
	school = request.user.school
	today = datetime.now()
	user = request.user
	school.customer.status = 0
	school.customer.save()

	subject = "Abonnement SACADO - demande d'IBAN"
	school_datas = "\n"+school.name +"\n"+school.code_acad +  " - " + str(school.nbstudents) +  " élèves \n" + school.address +  "\n"+school.town+", "+school.country.name

	send_mail(subject,
	          "Bonjour,  :\n\n Vous avez formulé une demande de renouvellement d'abonnement. Nous traitons votre demande. \n\n" + user.email + " \n\n" +  school_datas +" \n\n Ceci est un mail automatique. Ne pas répondre.",
	          settings.DEFAULT_FROM_EMAIL ,
	          [user.email, "sacado.asso@gmail.com"])

	messages.success(request,"Vous venez d'envoyer une demande d'adhésion à l'associaton SACADO. Ce bouton disparaitra lorsque notre trésorier traitera votre opération. Merci pour votre confiance. L'équipe SACADO.")

	context =  {  'school' : school  , 'user' : user   }
	return render(request, 'school/renew_school_adhesion.html', context)


 


def delete_renewal_school_adhesion(request):

	school = request.user.school
	today  = date.today()
	if school.customer.date_stop > today :
		school.customer.status = 3
		school.customer.save()


	school_datas = "\n"+school.name +"\n"+school.code_acad +  " - " + str(school.nbstudents) +  " élèves \n" + school.address +  "\n"+school.town+", "+school.country.name

	send_mail("Résiliation d'abonnement",
	      "Bonjour,  :\n\n Vous avez formulé une demande de résiliation d'abonnement   \n\n" + request.user.email + " \n\n" +  school_datas +" \n\n Ceci est un mail automatique. Ne pas répondre.",
	      settings.DEFAULT_FROM_EMAIL ,
	      [request.user.email, "sacado.asso@gmail.com"])


	messages.success(request,"Demande de résiliation d'abonnement réussie")
	return redirect('admin_tdb')



 
def print_bill_school(request,a_id):

    school =  request.user.school 
    now = datetime.now().date()
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="Facture'+str(school.id)+"-"+str(datetime.now().strftime('%Y%m%d'))+".pdf"
    doc = SimpleDocTemplate(response,   pagesize=A4, 
                                        topMargin=0.3*inch,
                                        leftMargin=0.3*inch,
                                        rightMargin=0.3*inch,
                                        bottomMargin=0.3*inch     )

    sample_style_sheet = getSampleStyleSheet()

    sacado = ParagraphStyle('sacado', 
                            fontSize=20, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )

    elements = []                 
    title_black = ParagraphStyle('title', fontSize=20, )
    subtitle = ParagraphStyle('title', fontSize=16,  textColor=colors.HexColor("#00819f"),)
    normal = ParagraphStyle(name='Normal',fontSize=10,)
    normalr = ParagraphStyle(name='Normal',fontSize=12,alignment= TA_RIGHT)
 
    logo = Image('https://sacado.xyz/static/img/sacadoA1.png')  
    logo_tab = [[logo, "ASSOCIATION SACADO.XYZ \n2B avenue de la pinède \n83400 La Capte Hyères \nFrance" ]]
    logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5*inch])

    elements.append(logo_tab_tab)
    elements.append(Spacer(0, 0.2*inch))

    try :
        accounting = Accounting.objects.get(id=a_id, school = school,is_active =1)
    except :
        messages.error(request,"Violation de droit. Accès interdit.")
        return redirect("index")

    paragraph0 = Paragraph( accounting.objet  , sacado )
    elements.append(paragraph0)
    elements.append(Spacer(0, 0.5*inch))

    school_datas =  "REF : "+accounting.chrono +"\n\n"+school.name +"\n"+school.code_acad +  "\n" + str(school.nbstudents) +  " élèves \n" + school.address +  "\n"+school.town+", "+school.country.name
    demandeur =  school_datas+   "\n\nMontant de la cotisation : "+str(school.amount )+"€" 


    demandeur_tab = [[demandeur, "ASSOCIATION SACADO.XYZ \n2B avenue de la pinède \n83400 La Capte \nHyères \nFrance \n\n\n\n" ]]
    demandeur_tab_tab = Table(demandeur_tab, hAlign='LEFT', colWidths=[5*inch,2*inch])

    elements.append(demandeur_tab_tab)
    elements.append(Spacer(0, 0.2*inch))



    my_texte_ = "Sous réserve du bon fonctionnement de son hébergeur LWS, l'association SACADO met l'ensemble des fonctionnalités du site https://sacado.xyz à disposition des enseignants de l'établissement sus-mentionné et dénommé par "+school.name+"."
    paragraph = Paragraph( my_texte_  , normal )
    elements.append(paragraph)
    elements.append(Spacer(0, 0.2*inch))

 
    my_texte = "La cotisation est acquittée le "+str(accounting.date.strftime('%d-%m-%Y'))+"."

    paragraph = Paragraph( my_texte  , normal )
    elements.append(paragraph)
    elements.append(Spacer(0, 1*inch))

 
    my__texte =  "Le trésorier Bruno Serres "

    paragraf = Paragraph( my__texte  , normal )
    elements.append(paragraf)
 



    doc.build(elements)

    return response















###############################################################################################
###############################################################################################
######  Niveau d'acquisition par établissement 
###############################################################################################
###############################################################################################

def choose_managing_school(request):
	''' Choix du mode d'Admin'''
	school = this_school_in_session(request)
	authorize_managing = request.POST.get('authorize_managing',None)
	# 0 si tout enseignant
	# 1 si seulement l'Admin
	# 2 si seulement l'ajout d'élèves déjà inscrit
	School.objects.filter(pk=school.id).update(is_managing=authorize_managing)
	return redirect('admin_tdb')


#@is_manager_of_this_school
def manage_stage(request):

	
	school = this_school_in_session(request)
	try :
		stage = Stage.objects.get(school = school)
		stage_form = StageForm(request.POST or None, instance = stage)
		eca , ac , dep = stage.medium - stage.low ,  stage.up - stage.medium ,  100 - stage.up
	except :
		stage = None
		stage_form = StageForm(request.POST or None )
		eca , ac , dep = 25 ,  20 ,  15

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès. ")
		return redirect('index')


	if request.method == "POST" :
		if stage_form.is_valid():
			nf = stage_form.save(commit = False) 
			nf.school = school
			nf.save()
			return redirect('admin_tdb')




	context =  {'stage_form': stage_form , 'stage': stage , 'eca': eca , 'ac': ac , 'dep': dep , 'communications' : [] , "school" : school  }  



	return render(request, 'school/stage.html', context )


 
###############################################################################################
###############################################################################################
######  Compte
###############################################################################################
###############################################################################################



#@is_manager_of_this_school
def send_account(request, id):

	if id == 0:
		school = this_school_in_session(request)
		for user in school.users.filter(user_type=2):
			if user.email : 
				msg = f'Bonjour, votre compte Sacado est disponible.\r\n\r\nVotre identifiant est {user.username} \r\n\r\nPour une première connexion, le mot de passe est : sacado2020 . Il faut le modifier lors de la première connexion.\r\n\r\n Dans le cas contraire, utilisez votre mot de passe habituel.\r\n\r\nPour vous connecter, redirigez-vous vers https://sacado.xyz.\r\n\r\nCeci est un mail automatique. Ne pas répondre.'
				send_mail('Compte Sacado', msg ,'info@sacado.xyz', [user.email])

	else:
		user = User.objects.get(id=id)
		if user.email : 
			msg = f'Bonjour, votre compte Sacado est disponible.\r\n\r\nVotre identifiant est {user.username} \r\n\r\nPour une première connexion, le mot de passe est : sacado2020 . Il faut le modifier lors de la première connexion.\r\n\r\n Dans le cas contraire, utilisez votre mot de passe habituel.\r\n\r\nPour vous connecter, redirigez-vous vers https://sacado.xyz.\r\n\r\nCeci est un mail automatique. Ne pas répondre.'
			send_mail('Compte Sacado', msg ,'info@sacado.xyz', [user.email])

	

	return redirect('school_teachers') 





#@is_manager_of_this_school
def pdf_account(request,id):

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="compte_sacado.pdf"'
	p = canvas.Canvas(response)
	teachers = []
	
	school = this_school_in_session(request)
	if id == 0:
		for u in school.users.filter(user_type=2):
			teachers.append(u)
	else:
		user = User.objects.get(id=id)
		teachers.append(user)

	for u in teachers :
		p.setFont("Helvetica-Bold", 12)
		p.drawString(50, 800, u.school.name)
		p.setFont("Helvetica-Bold", 12)
		p.drawString(50, 785, u.school.town)
		p.setFont("Helvetica-Bold", 12)
		p.drawString(50, 770, u.school.country.name)

		p.setFont("Helvetica-Bold", 14)
		p.drawString(50, 710, str(u.civilite) + " " + str(u.first_name) + " " + str(u.last_name))

		p.setFont("Helvetica-Bold", 16)
		p.drawString(200, 650, "COMPTE SACADO")
		p.setFont("Helvetica", 12)
		p.drawString(50, 550, "Votre compte SACADO est actif. Votre identifiant est : " + u.username)
		p.setFont("Helvetica", 12)
		p.drawString(50, 535, "Pour une première connexion, le mot de passe est : sacado2020 ")
		p.setFont("Helvetica", 12)
		p.drawString(50, 520, "Il faut le modifier lors de la première connexion.")
		p.setFont("Helvetica", 12)
		p.drawString(50, 505, "Votre mot de passe est secret.")
		p.setFont("Helvetica", 12)
		p.drawString(50, 490, "Si vous avez déjà un compte, utilisez votre mot de passe habituel.")
		p.setFont("Helvetica", 12)
		p.drawString(50, 460, "Pour vous connecter, redirigez-vous vers https://sacado.xyz.")
		p.showPage()
	p.save()
 

	return response 


def get_school(request):
	""" permet à un enseignant de rejoindre un établissement"""
	if request.method == "POST":
		school = request.POST.get("school",None)
		try :
			user = User.objects.filter(pk=request.user.id).update(school = school)

			# Si le prof ne change pas d'école alors on lui rattache ses élèves
			changing_school = False
			if request.user.school :
				changing_school = True
			if not changing_school : 
				teacher = request.user.teacher
				groups  = teacher.groups.all()
				for g in groups :
					Group.objects.filter(pk=g.id).update(school = school) 
					for s in g.students.all() :
						User.objects.filter(pk=s.user.id).update(school = school)
			try :
				send_mail("Rattachement d'établissement",
						"Bonjour la Team,  :\n\n L'enseignant  \n\n" + user + " \n\na rejoint l'établissement" +  school +". \n\n Ceci est un mail automatique. Ne pas répondre.",
						settings.DEFAULT_FROM_EMAIL ,
						[request.user.email, "sacado.asso@gmail.com"])
			except:
				pass
			messages.success(request,"Rattachement à l'établissement réussi")
		except :
			messages.error(request,"Echec du rattachement à l'établissement."  )
		return redirect("index")

	countries = Country.objects.order_by("name")

 
	context = { 'countries' : countries  }
	return render(request, 'school/get_school.html', context )



 

def ask_school_adhesion(request):
	""" permet à un enseignant de rejoindre un établissement"""
	school = request.user.school
	user   = request.user
	form   = SchoolUpdateForm(request.POST or None, request.FILES  or None, instance = school)
	if request.method == "POST" : 
		if form.is_valid():   
			school = form.save()
			try : 
				Customer.objects.update_or_create(school=school , defaults = {'user' : user , 'phone' : '' ,'status' : 0 } )
			except :
				with open("logs/output.txt", "a") as f:
					print("problème de Customer" , file=f)

			if school.gar : asking_gar = " Accès au GAR demandé"
			else : asking_gar = " Pas d'accès au GAR demandé"
			
			send_mail("Demande d'abonnement à la version établissement",
			          "Bonjour l'équipe SACADO, \nl'établissement suivant demande la version établissement :\n"+ school.name +" via son enseignant "+ user.first_name +" "+ user.last_name +" : "+ user.email +".\n"+asking_gar+"\n\n Cotisation : "+str(school.fee())+" €.\n\nEnregistrement de l'établissement dans la base de données.\nEn attente de paiement. \nhttps://sacado.xyz. Ne pas répondre.",
			          settings.DEFAULT_FROM_EMAIL,
			          ['sacado.asso@gmail.com','tresorier.sacado@gmail.com'])

			send_mail("Demande d'abonnement à la version établissement",
		              "Bonjour "+user.first_name+" "+user.last_name +", \nVous avez demandé la version établissement pour :\n"+ school.name +"\n"+asking_gar+"\n\nCotisation : "+str(school.fee())+" €.\nEn attente de paiement. \nL'équipe SACADO vous remercie de votre confiance. \nCeci est un mail automatique. Ne pas répondre. ",
	               settings.DEFAULT_FROM_EMAIL,[user.email])

			messages.success(request,"Demande d'abonnement envoyée. Vous recevrez rapidement l'IBAN de l'association à transmettre à votre DAF")

		else :
			print(form.errors)

	try :
		status = school.customer.status
		if customer.status < 2 : customer = False
		else : customer = True
	except :
		customer = False
 
 
	context = {  'school' : school , 'form' : form , 'customer' : customer }
	return render(request, 'school/ask_school_adhesion.html', context )





###############################################################################################
###############################################################################################
######  Création par csv
###############################################################################################
###############################################################################################


#@is_manager_of_this_school
def csv_full_group(request):
    """
    Enregistrement par csv : key est le code du user_type : 0 pour student, 2 pour teacher
    """
	
    school = this_school_in_session(request)
    if request.method == "POST":
        # try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Le fichier n'est pas format CSV")
            return redirect ("csv_full_group")
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Le fichier est trop lourd (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return redirect ("csv_full_group")
        try:
            file_data = csv_file.read().decode("utf-8")
        except UnicodeDecodeError:
            messages.error(request, 'Erreur..... Votre fichier contient des caractères spéciaux qui ne peuvent pas être décodés. Merci de vérifier que votre fichier .csv est bien encodé au format UTF-8.')
            return redirect ("csv_full_group")

        lines = file_data.split("\r\n")
        # loop over the lines and save them in db. If error , store as string and then display
        group_history = []
        list_names = ""
        simple = request.POST.get("simple",None)
        i=0
        teacher = Teacher.objects.get(user = request.user)
        for line in lines:
        	try :
	            ln, fn, username , password , email , group_name , level , is_username_changed = separate_values(request, line, 0 , simple) # 0 donne la forme du CSV
	            if group_name not in group_history :
	                group, created_group = Group.objects.get_or_create(name=group_name, teacher = teacher , defaults={ 'color': '#46119c' , 'level_id': level  })
	                if created_group :
	                	group_history.append(group_name)

	            user, created = User.objects.get_or_create(last_name=ln, first_name=fn, email=email, user_type=0,
	                                                       school= school, 
	                                                       time_zone=request.user.time_zone, is_manager=0,
	                                                       defaults={'username': username, 'password': password, 'cgu' : 1 , 'is_extra': 0})

	            student, creator = Student.objects.get_or_create(user=user, level= group.level, task_post=1)

	            if creator : #Si l'élève n'est pas créé alors il existe dans des groupes. On l'efface de ses anciens groupes pour l'inscrire à nouveau !
	                group.students.add(student)
	            if is_username_changed :
	                list_names += ln+" "+fn+" : "+username+"; "
	        except :
	        	pass

 
        if len(list_names) >  0 :
            messages.error(request,"Les identifiants  suivants ont été modifiés lors de la création "+list_names)
 
        return redirect('admin_tdb')
    else:
 
        context = { 'communications' : []  , "school" : school  }
        return render(request, 'school/csv_full_group.html', context )

 

def group_to_teacher(request):

    school = this_school_in_session(request)
    teacher = Teacher.objects.get(user = request.user)
    if not authorizing_access_school(teacher, school):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    groups = Group.objects.filter(Q(teacher__user__school=school)|Q(teacher__user__schools=school)).order_by('level_id') 
    teachers = Teacher.objects.filter(Q(user__school=school)|Q(user__schools=school)).order_by("user__last_name")

    if request.method == "POST" :
        group_ids = request.POST.getlist("groups")
        teacher_id = int(request.POST.get("teacher"))
 
        for group_id in group_ids :
        	Group.objects.filter(pk = group_id).update(teacher_id = teacher_id)  

        return redirect('group_to_teacher') 
 

    context = {'groups': groups,  'teachers': teachers ,   'communications' : [] , 'school' : school  }

    return render(request, 'school/group_to_teacher.html', context )



def ajax_get_this_school_in_session(request):
	""" Place school_id en session """
	school_id = request.POST.get("school_id",None)
	request.session["school_id"] = school_id
	data = {}
	return JsonResponse(data)



###############################################################################################
###############################################################################################
######  Contrôle à distance
###############################################################################################
###############################################################################################

from django.contrib.auth.hashers import make_password
def get_the_teacher_profile(request,idt):

    school  = this_school_in_session(request)
    teacher = request.user.teacher
    if not authorizing_access_school(teacher, school):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    teacher_to_get_the_profile = Teacher.objects.get(pk=idt)
    get_the_password           = teacher_to_get_the_profile.user.password # le passwrd du demandeur est enregistré
    teacher_to_get_the_profile.user.set_password("0__sacado2020__9")
    teacher_to_get_the_profile.user.save()

    user = authenticate(username=teacher_to_get_the_profile.user.username, password="0__sacado2020__9")
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    request.session["get_the_profile"] = True
    request.session["get_the_admin_id"] = teacher.user_id
    request.session["teacher_to_get_the_profile_password"] = get_the_password
    request.session["teacher_to_get_the_profile_id"] = user.id

    messages.error(request, "Attention vous naviguez avec le profil de "+teacher_to_get_the_profile.user.first_name+" "+teacher_to_get_the_profile.user.last_name)   
    return redirect('index')




def get_reverse_the_teacher_profile(request):

	get_the_admin_id                    = request.session.get("get_the_admin_id") 
	teacher_to_get_the_profile_password = request.session.get("teacher_to_get_the_profile_password") 
	teacher_to_get_the_profile_id       = request.session.get("teacher_to_get_the_profile_id") 

	User.objects.filter(pk=teacher_to_get_the_profile_id).update(password=teacher_to_get_the_profile_password) 
	logout(request)
	messages.success(request, "Déconnexion du profil réussi. Accès à distance terminé.")  

	return redirect('index')


def register_school_new(request):

	school_name       = request.POST.get("school_name",None) 
	school_country    = request.POST.get("school_country",None) 
	school_town       = request.POST.get("school_town",None) 
	school_rne        = request.POST.get("school_rne",None) 
	school_address    = request.POST.get("school_address",None) 
	school_nbstudents = request.POST.get("school_nbstudents",None) 
	school_zip        = request.POST.get("school_zip",None) 
	email             = request.POST.get("email",None) 
	token             = request.POST.get("token",None)

	if token :
		if int(token) == 7 :
		#### Si c'est un établissement qui fait une demande 
			school_datas = ""

			try :
				school_country_name = Country.object.get(pk = school_country).name
			except:
				school_country_name = school_name

			subject = "Nouvel établissement"
			school_datas = "\n"+school_name +"\nRNE : "+school_rne+"\nNb élèves : " + str(school_nbstudents) +  " élèves \n" + school_address +  "\nVille, pays : "+school_town+", "+school_country_name +  "\nCode postal : "+school_zip
			############################################################  

			send_mail(subject,
		            "Salut la Team, ce mail est envoyé à partir de l'adresse : " + email + "\n\n" + school_datas,
		          settings.DEFAULT_FROM_EMAIL,
		          ["sacado.asso@gmail.com" ])
			messages.success(request,"Message envoyé.....Nous vous répondrons à l'adresse indiquée dans les plus brefs délais. Merci. L'équipe Sacado.")

		else :
			messages.error(request,"Erreur d'opération....")
	else :
		messages.error(request,"Oubli de token.")

	return redirect("register_teacher_accueil")

###############################################################################################
###############################################################################################
######  Exports des résultats 
###############################################################################################
###############################################################################################
 

def export_csv_all_students_school(request) :
	pass
	


def export_pdf_all_students_school(request) :

    school = request.user.school
    today = datetime.now()
    scolar_year = this_year_from_today(today)
    subjects = []
    teacher = request.user.teacher

    elements = []        

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="export_pdf_all_students_school_'+scolar_year+'.pdf"'

    doc = SimpleDocTemplate(response,   pagesize=A4, 
                                        topMargin=0.3*inch,
                                        leftMargin=0.3*inch,
                                        rightMargin=0.3*inch,
                                        bottomMargin=0.3*inch     )

    sample_style_sheet = getSampleStyleSheet()

    sacado = ParagraphStyle('sacado', 
                            fontSize=20, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )

    title = ParagraphStyle('title', 
                            fontSize=20, 
                            textColor=colors.HexColor("#00819f"),
                            )

    subtitle = ParagraphStyle('title', 
                            fontSize=16, 
                            textColor=colors.HexColor("#00819f"),
                            )
 
    normal = ParagraphStyle(name='Normal',fontSize=12,)    
    style_cell = TableStyle(
            [
                ('SPAN', (0, 1), (1, 1)),
                ('TEXTCOLOR', (0, 1), (-1, -1),  colors.Color(0,0.7,0.7))
            ]
        )

    subjects = Subject.objects.all()

 

    for user in school.users.filter(user_type=0).order_by("student__level","last_name"):
 
        logo = Image('D:/uwamp/www/sacado/static/img/sacadoA1.png')
 
        logo_tab = [[logo, "SACADO \nBilan de compétences - Année scolaire "+scolar_year ]]
        logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5*inch])
        logo_tab_tab.setStyle(TableStyle([ ('TEXTCOLOR', (0,0), (-1,0), colors.Color(0,0.5,0.62))]))
        elements.append(logo_tab_tab)
        elements.append(Spacer(0, 0.1*inch))


        paragraph = Paragraph( user.last_name+" "+user.first_name+" - "+user.student.level.name , title )
        elements.append(paragraph)
        elements.append(Spacer(0, 1*inch))
 

        for subject in subjects :
            elements.append(Spacer(0, 0.5*inch))
            groups = subject.subject_group.filter(students= user.student)
            g_name = "-"
            for g in groups :
            	g_name += g.teacher.user.last_name+ " - "

            paragraph = Paragraph(subject.name + " - " + g_name, title )
            elements.append(paragraph)


            elements.append(Spacer(0, 0.5*inch))
            ##########################################################################
            #### Gestion des compétences
            ##########################################################################
            sk_tab = []
            skills = Skill.objects.filter(subject= subject)

            for skill  in skills :

                resultlastskills  = skill.student_resultskill.filter(student = user.student)
                point = 0
                i=1
                for rs in resultlastskills :
                    point += rs.point
                    i+=1
                if point == 0 :
                    sc = "N.E"
                elif i>1  :
                    sc = str(round(point/(i-1),0))+"%"
                else :
                    sc = str(point)+"%" 
                sk_tab.append([skill.name,  sc  ])



            skill_tab = Table(sk_tab, hAlign='LEFT', colWidths=[5.2*inch,1*inch])
            skill_tab.setStyle(TableStyle([
                   ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                   ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                   ]))


            elements.append(skill_tab)

        elements.append(PageBreak())

    doc.build(elements)
    return response




def reset_all_students_school(request) :

	Parent.objects.all().delete()
	Response.objects.all().delete()
	school = request.user.school
	for u in school.users.filter(user_type=0).exclude(username__contains= "_e-test")[:150] : 
		u.delete()

	form = SchoolForm(request.POST or None, instance=school)
	nb_total = school.users.filter(user_type=0).exclude(username__contains= "_e-test").count()
	nb = 150
	if nb > nb_total:
		nb = nb_total

	context = {'form':form,  'communications' : [], 'school':school ,'nb':nb ,'nb_total':nb_total }
	return render(request,'school/_form.html', context)


def reset_all_groups_school(request) :

	school = request.user.school

	form = SchoolForm(request.POST or None, instance=school)
	nb_total = school.users.filter(user_type=0).count()
	nb = 150
	if nb > nb_total:
		nb = nb_total

	users = school.users.all()

	for u in  users :
		Group.objects.filter(teacher=u.teacher).delete()
 
	context = {'form':form,  'communications' : [], 'school':school ,'nb':nb ,'nb_total':nb_total }
	return render(request,'school/_form.html', context)





@csrf_exempt
def ajax_charge_town(request):

    id_country =  request.POST.get("id_country")
    data = {}
    if id_country == 5 :
        data['towns'] = None
    else : 
        towns = Town.objects.values_list('name','name').filter(country_id=id_country).order_by("name") 
        data['towns']  = list(towns)
    data['id_country'] = id_country
    return JsonResponse(data)



@csrf_exempt
def ajax_charge_school(request):

    id_country =  request.POST.get("id_country")
    town       =  request.POST.get("id_town")

    data = {}
    schools = School.objects.filter(country_id=id_country, town = town).order_by("name")  
 
    context = {  'schools': schools,   }
    data['html'] = render_to_string('school/ajax_list_schools.html', context)
 
    return JsonResponse(data)

@csrf_exempt
def ajax_charge_school_by_rne(request):

    id_rne       =  request.POST.get("id_rne")
    data = {}
    schools = School.objects.filter(country_id=5,code_acad=id_rne)
 
    context = {  'schools': schools,   }
    data['html'] = render_to_string('school/ajax_list_schools.html', context)
 
    return JsonResponse(data)





def paypal_module(request):

	user       = request.user
	school     = user.school
	accounting = Accounting.objects.filter(school=school).last()
	amount     = str(round(float(str(accounting.amount)) * 1.03,1))

	context    = {'user':user,  'school' : school , 'accounting' : accounting , 'amount' : amount }

	return render(request,'school/paypal_module.html', context)


def approve_payment_paypal(request):

	user       = User.objects.get(pk=user_id)
	accounting = Accounting.objects.get(pk=accounting_id)
	school     = School.objects.get(pk=school_id)
 
	msg = "L'établissement {} #{} \n\n  vient de payer sa cotisation \n\n  #{} de chrono : {} pour la somme de {}€ \n\n  par {} {}".format( school.name, school.id, accounting.id, accounting.chrono, accounting.amount,  user.first_name.capitalize() , user.last_name.capitalize()  )

	send_mail("Paiement par PAYPAL", msg ,settings.DEFAULT_FROM_EMAIL,["sacado.asso@gmail.com"])  

	return redirect(  'index' )