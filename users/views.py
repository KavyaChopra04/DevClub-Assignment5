from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from .admin import *
from django.contrib import auth
from django.conf import settings
from django.views import generic
from django.shortcuts import get_object_or_404
import logging
# Define function to download pdf file using template
def home(request):
    return redirect('profile')

def register(request):
    if request.method=='POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been successfully created!')   
            return redirect('login')
    else: 
        form=UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    courses=None
    if request.user.is_authenticated:
        curr_user = UserInfo.objects.get(email=request.user.email)
        if curr_user.userType == 'Student':
            courses = Course.objects.filter(students=curr_user)
        if curr_user.userType == 'Instructor':
            courses = Course.objects.filter(profs=curr_user)
        if curr_user.userType=='Admin':
            courses = Course.objects.all()
    return render(request, 'users/dashboard.html', {'courses': courses})
# Create your views here.
def course_detail_view(request, code):
    try:
        course= Course.objects.get(code = code)
    except Course.DoesNotExist:
        raise Http404('Course does not exist')
    return render(request, 'users/course.html', {'course': course})
def course_participants(request, code):
    try:
        course= Course.objects.get(code = code)
    except Course.DoesNotExist:
        raise Http404('Course does not exist')
    return render(request, 'users/course-participants.html', {'course': course})
def add_course(request):
    if(request.user.userType!="Admin"):
        messages.success(request, f'request.user.userType') 
        return redirect('profile')
    if request.method=='POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Course successfully created!')   
            return redirect('profile')
    else: 
        form=AddCourseForm()
    return render(request, 'users/course-add.html', {'form': form})
class CourseDetailView(generic.DetailView):
    model = Course
