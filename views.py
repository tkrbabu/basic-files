from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout

#from django.contrib import messages


from .models import *
from .forms import * 
from .decorators import unauthenticated_user, allowed_users
# Create your views here.



def home(request):
	return render(request,'onlinet/index.html')




def subjectRegister(request):

	form=SubjectForm()
	if request.method == 'POST':
		form=SubjectForm(request.POST)
		if form.is_valid():
			form.save()
	context={'form':form}
	return render(request,'onlinet/subject_register.html',context)

def studentRegister(request):

	form = CreateStudentForm()

	if request.method == 'POST':
		form=CreateStudentForm(request.POST)
		if form.is_valid():
			user=form.save()
			username=form.cleaned_data.get('username')
			group=Group.objects.get(name='student')
			user.groups.add(group)
			Student.objects.create(user=user,name=user.username,email=user.email,val=user.username)
			print("Profile created") 
			return redirect('slogin')
			
	context={'form':form}
	return render(request,'onlinet/student_register.html',context)
	

def studentLogin(request):
	role="None"
	if request.method =='POST':
		username=request.POST.get('uname')
		password=request.POST.get('password')
		user=authenticate(request,username=username,password=password)
		if user is not None:
			role=user.groups.all()[0].name
			print(role)
		if role=="student" and user is not None:
			login(request,user)
			return redirect('sprofile')
		else:
			messages.info(request,'username or password incorrect')

	context={}
	return render(request,'onlinet/student_login.html',context)

def studentPage(request):
	return render(request,'onlinet/student_page.html')

@allowed_users(allowed_roles=['student'])
def studentProfile(request):
	form=request.user.student
	context={'form':form}
	return render(request,'onlinet/student_profile.html',context)

def tpr(request):
	form=Txtp()
	if request.method=='POST':
		form=Txtp(request.POST)
		if form.is_valid():
			return HttpResponse('qelocme')
	
	context={'form':form}
	
	return render(request,'onlinet/tp.html',context)



@allowed_users(allowed_roles=['student'])
def studentProfileEdit(request):
	student1=request.user.student
	name=student1.name

	form=StudentForm(instance=student1)
	print("****")
	if request.method =='POST':
		print("****")
		form = StudentForm(request.POST,request.FILES, instance=student1)
		if form.is_valid():
			form.save()

	context={'form':form,'name':name}
	print(context)

	return render(request,'onlinet/sprofile_edit.html',context)


def tutorRegister(request):

	form = CreateTutorForm()
	if request.method == 'POST':
		form=CreateTutorForm(request.POST)
		if form.is_valid():
			user=form.save()
			username=form.cleaned_data.get('username')
			group=Group.objects.get(name='tutor')
			user.groups.add(group)
			Tutor.objects.create(tuser=user,tutor_name=user.username,)
			print("Profile created") 
			return redirect('tlogin')
			
	context={'form':form}
	return render(request,'onlinet/tutor_register.html',context)

def tutorLogin(request):
	role="None"
	if request.method =='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(request,username=username,password=password)
		if user is not None:
			role=user.groups.all()[0].name
		if role=="tutor" and user is not None:
			login(request,user)
			return redirect('tprofile')
		else:
			messages.info(request,'username or password incorrect')

	context={}
	return render(request,'onlinet/tutor_login.html',context)

@allowed_users(allowed_roles=['tutor'])
def tutorProfile(request):
	tutor1=request.user.tutor

	context={'tutor1':tutor1}
	print(context)

	return render(request,'onlinet/tutor_profile1.html',context)

def tutorPage(request):
	return render(request,'onlinet/tutor_page.html')


@allowed_users(allowed_roles=['tutor'])
def tutorProfileEdit(request):
	tutor1=request.user.tutor
	name=tutor1.tutor_name
	form=TutorForm(instance=tutor1)
	if request.method =='POST':
		form = TutorForm(request.POST,request.FILES, instance=tutor1)
		if form.is_valid():
			print("****")
			form.save()
			

	context={'form':form,'name':name}
	print(context)

	return render(request,'onlinet/tprofile_edit.html',context)



def logoutUser(request):
	logout(request)
	return redirect('home')


@allowed_users(allowed_roles=['student'])
def searchSubject(request):
	cnt=tutor1=None
	student1=request.user.student
	t=student1.payment_status

	a=request.GET.get("search",None)
	area=request.GET.get("asearch",None)
	if a or area:
		tutor1=Tutor.objects.filter(tags__subject_name__icontains=a,tutor_area__icontains=area)
		tutor1=tutor1.distinct()
		print(tutor1.count())	
		cnt=tutor1.count()

	context={'tutor1':tutor1,'t':t,'cnt':cnt}
	return render(request,'onlinet/searchpage.html',context)

def generalSearchSubject(request):
	tutor1=t=cnt=None
	tag="Enter atleast 3 letters to search"
	#tutor1=Tutor.objects.all()
	a=request.GET.get("search",None)
	area=request.GET.get("asearch",None)

	if a or area:
		tutor1=Tutor.objects.filter(tags__subject_name__icontains=a,tutor_area__icontains=area)
		tutor1=tutor1.distinct()
		print(tutor1.count())	
		cnt=tutor1.count()
		if cnt>0:
			tag="To see details of the tutor you must be a registered student"
	else:
		t='no'

	context={'tutor1':tutor1,'cnt':cnt,'t':t,'tag':tag}
	return render(request,'onlinet/search.html',context)

@allowed_users(allowed_roles=['student'])
def searchTutorProfile(request,pk):
	tutor1=Tutor.objects.get(id=pk)

	context={'tutor1':tutor1}
	print(context)

	return render(request,'onlinet/search_tutor_profile.html',context)


def adminLogin(request):
	role="None"
	if request.method =='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(request,username=username,password=password)
		if user is not None:
			role=user.groups.all()[0].name
		if role=="admin" and user is not None:
			login(request,user)
			return redirect('adash')
		else:
			messages.info(request,'username or password incorrect')

	context={}
	return render(request,'onlinet/admin_login.html',context)


@allowed_users(allowed_roles=['admin'])
def adminDashboard(request):
	return render(request,'onlinet/dashboard.html')


@allowed_users(allowed_roles=['admin'])
def adminSubjectAdd(request):
	form=SubjectForm()
	if request.method == 'POST':
		form=SubjectForm(request.POST)
		if form.is_valid():
			form.save()
	context={'form':form}
	return render(request,'onlinet/subject_register.html',context)

@allowed_users(allowed_roles=['admin'])
def adminTutorAdd(request):

	form = CreateTutorForm()
	if request.method == 'POST':
		form=CreateTutorForm(request.POST)
		if form.is_valid():
			user=form.save()
			username=form.cleaned_data.get('username')
			group=Group.objects.get(name='tutor')
			user.groups.add(group)
			Tutor.objects.create(tuser=user,tutor_name=user.username,)
			print("Profile created") 
			
	context={'form':form}
	return render(request,'onlinet/admin_tutor_reg.html',context)

@allowed_users(allowed_roles=['admin'])

def adminStudentAdd(request):

	form = CreateStudentForm()

	if request.method == 'POST':
		form=CreateStudentForm(request.POST)
		if form.is_valid():
			user=form.save()
			username=form.cleaned_data.get('username')
			group=Group.objects.get(name='student')
			user.groups.add(group)
			Student.objects.create(user=user,name=user.username,email=user.email)
			print("Profile created") 

			
	context={'form':form}
	return render(request,'onlinet/admin_student_reg.html',context)
	
@allowed_users(allowed_roles=['admin'])
def adminTutorModify(request,pk_tutor):
	tutor1=Tutor.objects.get(id=pk_tutor)

	context={'tutor1':tutor1}
	print(context)

	return render(request,'onlinet/search_tutor_profile.html',context)


@allowed_users(allowed_roles=['admin'])
def adminCreate(request):
	pass



@allowed_users(allowed_roles=['admin'])

def adminSubjectDisplay(request):
	subject=Subject.objects.all()
	a=request.GET.get("search",None)
	area=request.GET.get("asearch",None)
	if a or area:
		subject=Subject.objects.filter(subject_name__icontains=a,class_name__icontains=area)
	cnt=subject.count()

	context={'subject':subject,'cnt':cnt}

	return render(request,'onlinet/subject_search.html',context)

@allowed_users(allowed_roles=['admin'])

def asubjectEdit(request,pk_sub):
	subject=Subject.objects.get(id=pk_sub)
	print(subject.subject_name)
	form=SubjectForm(instance=subject)
	if request.method =='POST':
		form = SubjectForm(request.POST,request.FILES, instance=subject)
		if form.is_valid():
			form.save()
	context={'subject':subject,'form':form}
	print(context)

	return render(request,'onlinet/subject_edit.html',context)


