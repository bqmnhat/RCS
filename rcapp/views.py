from django.shortcuts import render, get_object_or_404
from rcapp.forms import UserForm, PatientForm, DoctorForm, SpecialistForm, SpecialistChoiceField
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rcapp.models import Patient, Doctor, Specialist, TimeTable
from django.contrib.auth.models import User

def index(request):
	return render(request,'rcapp/index.html')

@login_required
def patient_index(request):
	#Check if user is patient
	user = User.objects.get(username=request.user)
	if Patient.objects.filter(pk=user.id):
		return render(request,'rcapp/patient_index.html',{})
	else:
		return HttpResponse("You must be PATIENT.")

@login_required
def doctor_index(request):
	#Check if user is doctor
	user = User.objects.get(username=request.user)
	if Doctor.objects.filter(user_id=user.id):
		return render(request,'rcapp/doctor_index.html',{})
	else:
		return HttpResponse("You must be DOCTOR.")


@login_required
def special(request):
	return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def patient_register(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		patient_form = PatientForm(data=request.POST)
		if user_form.is_valid() and patient_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			patient = patient_form.save(commit=False)
			patient.user = user

			if 'pic' in request.FILES:
				print('found it')
				patient.pic = request.FILES['pic']
			
			patient.save()
			registered = True
		else:
			print(user_form.errors,patient_form.errors)
	else:
		user_form = UserForm()
		patient_form = PatientForm()
	return render(request,'rcapp/patient_registration.html',
						  {'user_form':user_form,
						   'patient_form':patient_form,
						   'registered':registered})

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				if Patient.objects.filter(user_id=user.id):
					print('Patient')
					return render(request,'rcapp/patient_index.html')
				else:
					print('Doctor')
					return render(request,'rcapp/doctor_index.html')
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details given")
	else:
		return render(request, 'rcapp/login.html', {})

def doctor_register(request):
	registered = False
	pic=""
	specialist_choice = SpecialistChoiceField()
	if request.method == 'POST':
		#binding data to form
		specialist_choice = SpecialistChoiceField(data=request.POST)
		user_form = UserForm(data=request.POST)
		doctor_form = DoctorForm(data=request.POST)
		if user_form.is_valid() and doctor_form.is_valid() and specialist_choice.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			doctor = doctor_form.save(commit=False)
			doctor.user = user
			if 'pic' in request.FILES:
				print('found it')
				doctor.pic = request.FILES['pic']
				pic = doctor.pic
			doctor.specialist_id = request.POST['specialist']
			doctor.save()
			registered = True
		else:
			print(user_form.errors,doctor_form.errors)
	else:
		user_form = UserForm()
		doctor_form = DoctorForm()
	
	if pic == "":
		return render(request,'rcapp/doctor_registration.html',
						  {'user_form':user_form,
						   'doctor_form':doctor_form,
						   'specialist_choice':specialist_choice,
						   'registered':registered})
	else:
		return render(request,'rcapp/doctor_registration.html',
						  {'user_form':user_form,
						   'doctor_form':doctor_form,
						   'pic':pic.url,
						   'Specialist_choice':specialist_choice,
						   'registered':registered})

@login_required
def booking(request):
	#Check if user is patient
	user = User.objects.get(username=request.user)
	if Patient.objects.filter(pk=user.id):
		doctor_list = Doctor.objects.select_related('specialist').all()
		return render(request,'rcapp/booking.html',{'doctor_list':doctor_list})
	else:
		return HttpResponse("You must be PATIENT.")
@login_required
def booking_detail(request,doc_id):
	#Check if user is patient
	user = User.objects.get(username=request.user)
	if Patient.objects.filter(pk=user.id):
		selected_doctor = get_object_or_404(Doctor, pk=doc_id)
		time_table = TimeTable.objects.filter(doctor_id=doc_id)
		return render(request,'rcapp/booking_detail.html',
			{'selected_doctor':selected_doctor, 'time_table':time_table})
	else:
		return HttpResponse("You must be PATIENT.")

@login_required
def appointment(request):
	#Check if user is patient
	user = User.objects.get(username=request.user)
	if Patient.objects.filter(pk=user.id):
		return render(request,'rcapp/appointment.html',{})
	else:
		return HttpResponse("You must be PATIENT.")
