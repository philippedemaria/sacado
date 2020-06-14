from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from django.contrib import messages
from .models import School, Country  , Stage
from .forms import SchoolForm, CountryForm, GroupForm, StageForm
from group.views import include_students
from group.models import Group
from account.decorators import is_manager_of_this_school 
from account.models import User, Teacher, Student
from account.forms import UserForm , StudentForm ,NewUserSForm


@login_required
def list_schools(request):
	schools = School.objects.all()
	return render(request,'school/lists.html', {'schools':schools})


@login_required
def create_school(request):
	form = SchoolForm(request.POST or None)
	
	if form.is_valid():
		form.save()
		return redirect('schools')

	return render(request,'school/_form.html', {'form':form})

@login_required
def update_school(request,id):
	school = School.objects.get(id=id)
	form = SchoolForm(request.POST or None, instance=school)

	if form.is_valid():
		form.save()
		return redirect('schools')

	return render(request,'school/_form.html', {'form':form, 'school':school})

@login_required
def delete_school(request,id):
	school = School.objects.get(id=id)
	school.delete()
	return redirect('schools')





@login_required
def list_countries(request):
	countries = Country.objects.all()
	return render(request,'school/lists_country.html', {'countries':countries})

@login_required
def create_country(request):
	form = CountryForm(request.POST or None,request.FILES or None )
	
	if form.is_valid():
		form.save()
		return redirect('countries')

	return render(request,'school/country_form.html', {'form':form})

@login_required
def update_country(request,id):
	country = Country.objects.get(id=id)
	form = CountryForm(request.POST or None,request.FILES or None, instance=country)

	if form.is_valid():
		form.save()
		return redirect('countries')

	return render(request,'school/country_form.html', {'form':form, 'country':country})

@login_required
def delete_country(request,id):
	country = Country.objects.get(id=id)
	country.delete()
	return redirect('countries')


###############################################################################################
###############################################################################################
######  School 
###############################################################################################
###############################################################################################


@login_required
@is_manager_of_this_school
def school_teachers(request):
	if request.session.get("school_id") :
		school_id = request.session.get("school_id")
	else :
		school_id = request.user.school.id
	teachers = User.objects.filter(school_id = school_id, user_type=2).order_by("last_name")  
 

	return render(request,'school/list_teachers.html', {'teachers':teachers})

@login_required
@is_manager_of_this_school
def school_groups(request):
	if request.session.get("school_id") :
		school_id = request.session.get("school_id")
		school = School.objects.get(pk = school_id)
	else :
		school = request.user.school

	users = school.user.all()

	groups = Group.objects.filter(teacher__user__in = users).order_by("level")  

	return render(request,'school/list_groups.html', {'groups':groups})


@login_required
@is_manager_of_this_school
def school_level_groups(request):
	if request.session.get("school_id") :
		school_id = request.session.get("school_id")
		school = School.objects.get(pk = school_id)
	else :
		school = request.user.school

	users = school.user.all()

	groups = Group.objects.filter(teacher__user__in = users).order_by("level") 

	return render(request,'school/list_level_groups.html', {'groups':groups})




@login_required
@is_manager_of_this_school
def school_students(request):
	if request.session.get("school_id") :
		school_id = request.session.get("school_id")
		school = School.objects.get(pk = school_id)
	else :
		school = request.user.school
	users = User.objects.filter(school = school, user_type=0).order_by("last_name")  

	return render(request,'school/list_students.html', {'users':users})


@login_required
@is_manager_of_this_school
def new_student(request,slug):
    group = Group.objects.get(code=slug)
    user_form = NewUserSForm()
    form = StudentForm()
    return render(request,'school/student_form.html', {'group':group, 'user_form' : user_form, 'form' : form })




@login_required
@is_manager_of_this_school
def get_school_students(request):

	school = request.user.school
	teachers = Teacher.objects.filter(user__school = school)
	groups = Group.objects.filter(teacher__in = teachers)
	group_tab = []
	for group in groups :
		for student in group.students.filter(user__school=None, user__user_type=0): # ce sont les élèves de l'établissement pas encore assigné
			usr = student.user
			usr.school = school
			usr.save()
 
	messages.success(request, "Scan terminé avec succès. Les élèves trouvés sont importés.")

	return redirect('school_students')


 




@login_required
@is_manager_of_this_school
def new_group(request):
	school = request.user.school
	form = GroupForm(request.POST or None, school = school)

	if request.method == "POST" :
		if form.is_valid():
			form.save()
			stdts = request.POST.get("students")

			if len(stdts) > 0 :
				tested = include_students(stdts,form)
				if not tested :
					messages.error(request, "Erreur lors de l'enregistrement. Un étudiant porte déjà cet identifiant. Modifier le prénom ou le nom.")

			return redirect('school_groups')
		else :
			print(form.errors)

	return render(request,'school/group_form.html', { 'school' : school ,  'form' : form })


@login_required
@is_manager_of_this_school
def new_group_many(request):

	school = request.user.school
	GroupFormSet = formset_factory(GroupForm , extra=2) 
	formset  = GroupFormSet(request.POST or None,form_kwargs={'school': school})
	if request.method == "POST" :
		
		if formset.is_valid():
			formset.save()
			messages.success(request, "Groupes créés avec succès.")
			return redirect('school_groups')

	return render(request,'school/many_group_form.html', {'formset' : formset , 'school': school})

 

###############################################################################################
###############################################################################################
######  Niveau d'acquisition par établissement 
###############################################################################################
###############################################################################################



@login_required
@is_manager_of_this_school
def manage_stage(request):

	school = request.user.school

	try : 
		stage = Stage.objects.get(school = school)
		stage_form = StageForm(request.POST or None, instance = stage)

		if request.method == "POST" :
			if stage_form.is_valid():
				nf = stage_form.save(commit = False) 
				nf.school = school
				nf.save()

			eca, ac , dep = stage.medium - stage.low ,  stage.up - stage.medium ,  100 - stage.up

		context =  {'stage_form': stage_form , 'stage': stage , 'eca': eca , 'ac': ac , 'dep': dep}  

	except : 
		stage  = None
		stage_form = StageForm(request.POST or None)
		if request.method == "POST" :
			if stage_form.is_valid():
				nf = stage_form.save(commit = False) 
				nf.school = school
				nf.save() 

		context =  {'stage_form': stage_form , 'stage': stage}


	return render(request, 'school/stage.html', context )