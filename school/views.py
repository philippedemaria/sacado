from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.contrib.auth.decorators import permission_required,user_passes_test
from django.contrib import messages
from .models import School, Country  , Stage
from school.forms import SchoolForm, CountryForm, GroupForm, StageForm
from group.views import include_students
from group.models import Group, Sharing_group
from account.decorators import is_manager_of_this_school
from socle.decorators import user_is_superuser
from socle.models import Subject
from account.models import User, Teacher, Student
from account.forms import UserForm , StudentForm ,NewUserSForm
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
############### bibliothèques pour les impressions pdf  #########################
import os
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
from cgi import escape
cm = 2.54
#################################################################################


def authorizing_access_school(teacher, school) :
	if (school == teacher.user.school and teacher.user.is_manager) or teacher.user.is_superuser :
		return True
	else :
		return False


def get_username(ln, fn):
    """
    retourne un username
    """
    ok = True
    i = 0
    un = str(ln) + "." + str(fn)[0]
    while ok:
        if User.objects.filter(username=un).count() == 0:
            ok = False
        else:
            i += 1
            un = un + str(i)
    return un

@user_is_superuser
def list_schools(request):
	schools = School.objects.all()
	return render(request, 'school/lists.html', { 'communications' : [], 'schools': schools})



@user_is_superuser
def create_school(request):
	form = SchoolForm(request.POST or None)
	
	if form.is_valid():
		school = form.save()

		Stage.objects.create(school = school ,low = 30,  medium = 65, up = 85)
		return redirect('schools')

	return render(request,'school/_form.html', { 'communications' : [], 'form':form})

@user_is_superuser
def update_school(request,id):
	school = School.objects.get(id=id)
	form = SchoolForm(request.POST or None, instance=school)

	if form.is_valid():
		form.save()
		return redirect('schools')

	return render(request,'school/_form.html', {'form':form,  'communications' : [],'school':school})

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
		for p in student.students_to_parcours.all():
			p.students.remove(student)
		for g in student.students_to_group.all():
			g.students.remove(student)
		for r in student.students_relationship.all():
			r.students.remove(student)
		for c in student.students_course.all() :
			c.students.remove(student)
		for a in student.answers.all() :
			a.students.remove(student)	
	except :
		pass




#@is_manager_of_this_school
def school_teachers(request):


	if request.session.get("school_id"):
		school_id = request.session.get("school_id")
		school = School.objects.get(pk=school_id)
	else:
		school = request.user.school


	teacher = Teacher.objects.get(user=request.user)

	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
		return redirect('index')



	teachers = User.objects.filter(school_id = school_id, user_type=2).order_by("last_name")  
 

	return render(request,'school/list_teachers.html', { 'communications' : [],'teachers':teachers})



#@is_manager_of_this_school
def school_groups(request):
	if request.session.get("school_id"):
		school_id = request.session.get("school_id")
		school = School.objects.get(pk=school_id)
	else:
		school = request.user.school

	teacher = Teacher.objects.get(user=request.user)

	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
		return redirect('index')



	users = school.users.all()
	groups = Group.objects.filter(teacher__user__in=users).order_by("level")

	return render(request, 'school/list_groups.html', { 'communications' : [],'groups': groups})



#@is_manager_of_this_school
def school_level_groups(request):
	if request.session.get("school_id") :
		school_id = request.session.get("school_id")
		school = School.objects.get(pk = school_id)
	else :
		school = request.user.school

	teacher = Teacher.objects.get(user=request.user)

	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
		return redirect('index')

	users = school.users.all()

	groups = Group.objects.filter(teacher__user__in = users).order_by("level") 

	return render(request,'school/list_level_groups.html', { 'communications' : [],'groups':groups})





#@is_manager_of_this_school
def school_students(request):

	if request.session.get("school_id") :
		school_id = request.session.get("school_id")
		school = School.objects.get(pk = school_id)
	else :
		school = request.user.school
	teacher = Teacher.objects.get(user=request.user)
	
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
		return redirect('index')


	users = User.objects.filter(school = school, user_type=0).order_by("last_name")  

	return render(request,'school/list_students.html', { 'communications' : [], 'users':users , 'school' : school , })



 
def new_student(request,slug):
    group = Group.objects.get(code=slug)

    user_form = NewUserSForm()
    form = StudentForm()
    return render(request,'school/student_form.html', { 'communications' : [],'group':group, 'user_form' : user_form, 'form' : form })





 
def get_school_students(request):

	school = request.user.school
	teacher = Teacher.objects.get(user = request.user)
 
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
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
    group = Group.objects.get(code=slug)
    students = group.students.all().order_by("user__last_name")
    p_students = Student.objects.filter(user__school = request.user.school).order_by("user__last_name")
    pending_students = []
    for student in p_students :
    	pending_students.append(student)
    return render(request,'school/new_student_list.html', { 'communications' : [],'group':group, 'students' : students, 'pending_students' : pending_students })

 


#@is_manager_of_this_school
def push_student_group(request):
	group_id = request.POST.get("group_id")
	group = Group.objects.get(pk=group_id)

	student_ids = request.POST.getlist("student_ids")  

	for student_id in student_ids :
		student = Student.objects.get(pk=student_id)	
		group.students.add(student)
	return redirect('school_groups')




def sharing_teachers(request,group, teachers):

	shares = Sharing_group.objects.filter(group  = group)
	for share in shares : 	
		share.delete()

	choices = request.POST.getlist("choices") 

	for c in choices :
		c_tab = c.split("-")
		teacher = Teacher.objects.get(user_id = c_tab[1])
		role =  int(c_tab[0])
		Sharing_group.objects.create(group = group ,teacher = teacher, role = role  )





#@is_manager_of_this_school
def new_group(request):
	school = request.user.school
	teachers = Teacher.objects.filter(user__school=school)

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
		return redirect('index')

	form = GroupForm(request.POST or None, school = school)

	if request.method == "POST" :
		print(request.POST)	
		if form.is_valid():
			group = form.save()
			stdts = request.POST.get("students")
			sharing_teachers(request,group,teachers)

			try :
				if stdts :
					tested = include_students(stdts,group)
			except :
				pass

			return redirect('school_groups')
		else :
			print(form.errors)

	return render(request,'school/group_form.html', {  'communications' : [], 'school' : school ,  'group' : None ,  'form' : form , 'teachers' : teachers ,  })





#@is_manager_of_this_school
def update_group_school(request,id):
	school = request.user.school
	group = Group.objects.get(id=id)
	teachers = Teacher.objects.filter(user__school=school).exclude(user =  group.teacher.user)
	form = GroupForm(request.POST or None, school = school, instance = group)

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
		return redirect('index')

	if request.method == "POST" :
		if form.is_valid():
			form.save()

			sharing_teachers(request,group,teachers)


			stdts = request.POST.get("students")
			try :
				if len(stdts) > 0 :
					tested = include_students(stdts,group)

			except :
				pass

			return redirect('school_groups')
		else :
			print(form.errors)

	return render(request,'school/group_form.html', { 'school' : school , 'group' : group ,  'form' : form , 'communications' : []  , 'teachers' : teachers , })




#@is_manager_of_this_school
def delete_student_group(request,id,ids):
	school = request.user.school

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
		return redirect('index')

	group = Group.objects.get(id=id)
	student = Student.objects.get(user_id=ids)
	form = GroupForm(request.POST or None, school = school, instance = group)
	clear_detail_student(student)
	return redirect('update_group_school', group.id)




#@is_manager_of_this_school
def delete_all_students_group(request,id):
	school = request.user.school

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
		return redirect('index')

	group = Group.objects.get(id=id)
	form = GroupForm(request.POST or None, school = school, instance = group)
	for student in group.students.all() :
		clear_detail_student(student)
	group.students.clear()
	return redirect('update_group_school', group.id)

 

@csrf_exempt
def ajax_subject_teacher(request):
 	
    school = request.user.school
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
	school = request.user.school

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
		return redirect('index')


	students = Student.objects.filter(user__school = school, user_type = 0)
	for s in students :
		clear_detail_student(s)
		s.delete()
	return redirect('admin_tdb')




#@is_manager_of_this_school
def delete_selected_students(request):
	user_ids = request.POST.getlist("user_ids")
	for user_id in user_ids :
		user = User.objects.get(pk=user_id)
		student = Student.objects.get(user=user)
		user.delete()
		clear_detail_student(student)
		student.delete()
	return redirect('school_students')




#@is_manager_of_this_school
def new_group_many(request):

	school = request.user.school

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
		return redirect('index')


	GroupFormSet = formset_factory(GroupForm , extra=2) 
	group_formset  = GroupFormSet(request.POST or None, form_kwargs={'school': school, })
	if request.method == "POST" :	
		if group_formset.is_valid():
			for f in group_formset :
				f.save()
			messages.success(request, "Groupes créés avec succès.")
			return redirect('school_groups')
 
	return render(request,'school/many_group_form.html', {'formset' : group_formset , 'school': school , 'communications' : [] , 'group' : None  })

 

###############################################################################################
###############################################################################################
######  Niveau d'acquisition par établissement 
###############################################################################################
###############################################################################################




#@is_manager_of_this_school
def manage_stage(request):

	school = request.user.school
	stage = Stage.objects.get(school = school)
	stage_form = StageForm(request.POST or None, instance = stage)

	teacher = Teacher.objects.get(user=request.user)
	if not authorizing_access_school(teacher, school):
		messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
		return redirect('index')


	if request.method == "POST" :
		if stage_form.is_valid():
			nf = stage_form.save(commit = False) 
			nf.school = school
			nf.save()

	eca , ac , dep = stage.medium - stage.low ,  stage.up - stage.medium ,  100 - stage.up

	context =  {'stage_form': stage_form , 'stage': stage , 'eca': eca , 'ac': ac , 'dep': dep , 'communications' : []  }  



	return render(request, 'school/stage.html', context )


 
###############################################################################################
###############################################################################################
######  Compte
###############################################################################################
###############################################################################################



#@is_manager_of_this_school
def send_account(request, id):
	rcv = []
	if id == 0:
		school = request.user.school
		for u in school.users.all():
			rcv.append(u.email)
	else:
		user = User.objects.get(id=id)
		rcv.append(user.email)
	send_mail('Compte   Sacado',
	f'Bonjour, votre compte Sacado est disponible.\r\n\r\nVotre identifiant est {user.username} \r\n\r\n\Votre mot de passe est secret. Pour une première connexion, le mot de passe est : sacado2020 . Il faut le modifier lors de la première connexion.\r\n\r\n Dans le cas contraire, utilisez votre mot de passe habituel.\r\n\r\nPour vous connecter, redirigez-vous vers https://sacado.xyz.\r\n\r\nCeci est un mail automatique. Ne pas répondre.',
	'info@sacado.xyz',
	rcv)

	return redirect('school_teachers') 





#@is_manager_of_this_school
def pdf_account(request,id):

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="compte_sacado.pdf"'
	p = canvas.Canvas(response)
	teachers = []
	school = request.user.school
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



 
###############################################################################################
###############################################################################################
######  Création par csv
###############################################################################################
###############################################################################################

import csv

#@is_manager_of_this_school
def csv_full_group(request):
    """
    Enregistrement par csv : key est le code du user_type : 0 pour student, 2 pour teacher
    """
    if request.method == "POST":
        # try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Le fichier n'est pas format CSV")
            return HttpResponseRedirect(reverse("register_teacher_csv"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Le fichier est trop lourd (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("register_teacher_csv"))

        try:
            file_data = csv_file.read().decode("utf-8")
        except UnicodeDecodeError:
            return HttpResponse('Votre fichier contient des caractères spéciaux qui ne peuvent pas être décodés. Merci de vérifier que votre fichier .csv est bien encodé au format UTF-8.')

        lines = file_data.split("\r\n")
        # loop over the lines and save them in db. If error , store as string and then display
        group_history = []
        for line in lines:
            try : 
                # loop over the lines and save them in db. If error , store as string and then display
                fields = line.split(";")
                ln = str(fields[2]).replace(' ', '').replace('\ufeff', '').lower().capitalize()
                fn = str(fields[3]).lower().capitalize()
                level = fields[1]
                group_name = str(fields[0])
                username =  get_username(ln,fn)
                password = make_password("sacado2020")
                try:
                    if fields[4] != "":
                        email = fields[4]
                    else:
                        email = ""
                except:
                    email = ""
                teacher = Teacher.objects.get(user = request.user)

                if group_name not in group_history :
                    group, created_group = Group.objects.get_or_create(name=group_name, teacher = teacher , defaults={'color': '#46119c','level_id': level  })
                    if created_group :
                    	group_history.append(group_name)

                user, created = User.objects.get_or_create(last_name=ln, first_name=fn, email=email, user_type=0,
                                                           school=request.user.school, 
                                                           time_zone=request.user.time_zone, is_manager=0,
                                                           defaults={'username': username, 'password': password, 'cgu' : 1 ,
                                                                     'is_extra': 0})
                student, creator = Student.objects.get_or_create(user=user, level=group.level, task_post=1)
                if creator : #Si l'élève n'est pas créé alors il existe dans des groupes. On l'efface de ses anciens groupes pour l'inscrire à nouveau !
                    group.students.add(student)
            except :
                pass
 
        return redirect('admin_tdb')
    else:
 
        context = { 'communications' : []   , }
        return render(request, 'school/csv_full_group.html', context )


def group_to_teacher(request):

    school = request.user.school
    teacher = Teacher.objects.get(user = request.user)
    if not authorizing_access_school(teacher, school):
        messages.error(request, "  !!!  Redirection automatique  !!! Violation d'accès.")
        return redirect('index')

    groups = Group.objects.filter(teacher__user__school = school).order_by("level")  
    teachers = Teacher.objects.filter(user__school = school)

 

    if request.method == "POST" :
        group_ids = request.POST.getlist("groups")
        teacher_id = int(request.POST.get("teacher"))
 
        for group_id in group_ids :
        	Group.objects.filter(pk = group_id).update(teacher_id = teacher_id)  

        return redirect('admin_tdb') 
 

    context = {'groups': groups,  'teachers': teachers ,   'communications' : [] , 'school' : school  }

    return render(request, 'school/group_to_teacher.html', context )
