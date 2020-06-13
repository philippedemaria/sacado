from django.shortcuts import render, redirect
from .models import School, Country  
from .forms import SchoolForm, CountryForm, GroupForm
from group.models import Group
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from account.decorators import is_manager_of_this_school 
from account.models import User
from account.forms import UserForm , StudentForm ,NewUserSForm
from django.forms import formset_factory


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
	teachers = User.objects.filter(school_id = school_id, user_type=2)
 

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

	groups = Group.objects.filter(teacher__user__in = users) 

	return render(request,'school/list_groups.html', {'groups':groups})

@login_required
@is_manager_of_this_school
def school_students(request):
	if request.session.get("school_id") :
		school_id = request.session.get("school_id")
	else :
		school_id = request.user.school.id
	students = User.objects.filter(school_id = school_id, user_type=0) 

	return render(request,'school/list_students.html', {'students':students})


@login_required
@is_manager_of_this_school
def new_student(request,slug):
    group = Group.objects.get(code=slug)
    user_form = NewUserSForm()
    form = StudentForm()
    return render(request,'school/student_form.html', {'group':group, 'user_form' : user_form, 'form' : form })



@login_required
@is_manager_of_this_school
def new_group(request):
	school = request.user.school
	form = GroupForm(request.POST or None, school = school)

	if request.method == "POST" :
		if form.is_valid():
			form.save()
			return redirect('school_groups')

	return render(request,'school/group_form.html', { 'school' : school ,  'form' : form })


@login_required
@is_manager_of_this_school
def new_group_many(request):

	school = request.user.school
	GroupFormSet = formset_factory(GroupForm , extra=2) 
	formset  = GroupFormSet(request.POST or None,form_kwargs={'school': school})
	if request.method == "POST" :
		
		for form in formset:
			if form.is_valid():
				form.save()
		return redirect('school_groups')

	return render(request,'school/many_group_form.html', {'formset' : formset , 'school': school})

 



