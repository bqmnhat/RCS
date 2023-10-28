from django import forms
from rcapp.models import Patient, Doctor, Specialist
from django.contrib.auth.models import User
from functools import partial
import datetime

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class UserForm(forms.ModelForm):
	password = forms.CharField(label="Password", widget=forms.PasswordInput)
	confirm_password=forms.CharField(label="Password (again)", widget=forms.PasswordInput)

	def clean_confirm_password(self):
		password1 = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("confirm_password")
		if password1 != password2:
			raise forms.ValidationError("Your passwords do not match")
		return password2

	class Meta():
		model = User
		fields = ('username','password','confirm_password','first_name','last_name','email')
		help_texts = {
		'username': None,
		}

class PatientForm(forms.ModelForm):
	bod = forms.DateField(label="Birth of Date",widget=DateInput())
	created_at = forms.DateField(label="Created at", input_formats=['%d-%m-%y'], initial=datetime.date.today,disabled=True)
	class Meta():
		model = Patient
		fields = ('bod', 'address', 'city', 'phone', 'created_at', 'pic')

class DoctorForm(forms.ModelForm):
	bod = forms.DateField(label="Birth of Date",widget=DateInput())
	created_at = forms.DateField(label="Created at", input_formats=['%d-%m-%y'], initial=datetime.date.today,disabled=True)
	class Meta():
		model = Doctor
		fields = ('bod', 'address', 'city', 'phone', 'created_at', 'pic')

class SpecialistForm(forms.ModelForm):
	class Meta():
		model = Specialist
		fields = ('description',)

class SpecialistChoiceField(forms.Form):
	specialist = forms.ModelChoiceField(queryset=Specialist.objects.all(), empty_label=None)