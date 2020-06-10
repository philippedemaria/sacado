from django.shortcuts import render, redirect
from .models import School, Country  
from .forms import SchoolForm, CountryForm
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from account.decorators import is_manager_of_this_school 
from account.models import User

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
	school_id = request.user.school_id
	teachers = User.objects.filter(school_id = school_id, user_type=2) 

	return render(request,'school/list_teachers.html', {'teachers':teachers})

@login_required
@is_manager_of_this_school
def school_groups(request,id):
	school_id = request.user.school_id
	groups = Group.objects.filter(teacher__school_id = school_id) 

	return render(request,'school/list_groups.html', {'groups':groups})

@login_required
@is_manager_of_this_school
def school_students(request,id):
	school_id = request.user.school_id
	students = User.objects.filter(school_id = school_id, user_type=0) 

	return render(request,'school/list_students.html', {'students':students})




def csv_teachers():
	pass

def csv_students():
	pass

def csv_groups():

	pass