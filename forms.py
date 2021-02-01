from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

# Subject registration
class SubjectForm(ModelForm):
	class Meta:
		model=Subject
		fields='__all__'

#student details for profile

class StudentForm(ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		exclude = ['user','payment_status','val']


	def clean_phone(self):
		phone1 = self.cleaned_data['phone']
		t=Student.objects.filter(phone=phone1)
		if t:
			raise forms.ValidationError("Mobile number already registered")
			return false
		elif not phone1.isdigit():
			raise forms.ValidationError("Enter valid number")
		elif len(phone1)!=10:
			raise forms.ValidationError("Number is 10 digit")
		return phone1

class CreateStudentForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username','email','password1','password2']

#tutor registartion page

class CreateTutorForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username','email','password1','password2']


# tutor dispaly profile
class TutorForm(ModelForm):
	class Meta:
		model = Tutor
		fields = '__all__'
		exclude = ['tuser','tpayment_status','val']

class AdminStudentForm(ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		exclude = ['user','val']

class AdminTutorForm(ModelForm):
	class Meta:
		model = Tutor
		fields = '__all__'
		exclude = ['tuser','val']



class Txtp(forms.Form):

	fields= forms.CharField(label='Your name', max_length=100)

	def clean_fields(self):
		name1 = self.cleaned_data['fields']
		if name1=="tt":
			raise forms.ValidationError("Mobile number already registered")
		return name1


