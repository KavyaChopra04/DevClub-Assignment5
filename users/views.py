from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from .admin import *
from documents.models import *
from documents.admin import *
from communication.models import *
from communication.admin import *
from grades.models import *
from grades.admin import *
from django.contrib import auth
from django.conf import settings
from django.views import generic
from django.shortcuts import get_object_or_404
import logging
import mimetypes
import os
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
        notes = Note.objects.filter(course = course)
        assignments = Assignment.objects.filter(course=course)
    except Course.DoesNotExist:
        raise Http404('Course does not exist')
    return render(request, 'users/course.html', {'course': course, 'addassgn' : False, 'addnote' : False, 'notes': notes, 'assignments': assignments})
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



def course_assignment(request, code):
    course= Course.objects.get(code = code)
    notes = Note.objects.filter(course = course)
    assignments = Assignment.objects.filter(course=course)
    if(request.user.userType!="Instructor"):
        messages.success(request, f'request.user.userType') 
        return redirect('profile')
    if request.method=='POST':
        form = AddAssignmentForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()
            return course_detail_view(request,code)
    else: 
        form=AddAssignmentForm()
    return render(request, 'users/course.html', {'course': course, 'form': form, 'addassgn' : True, 'addnote' : False, 'notes': notes, 'assignments': assignments}) 
def course_note(request, code):
    course= Course.objects.get(code = code)
    notes = Note.objects.filter(course = course)
    assignments = Assignment.objects.filter(course=course)
    if(request.user.userType!="Instructor"):
        messages.success(request, f'request.user.userType') 
        return redirect('profile')
    if request.method=='POST':
        form = AddNoteForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()
            return course_detail_view(request,code)
    else: 
        form=AddNoteForm()
    return render(request, 'users/course.html', {'course': course, 'form': form, 'addassgn' : False, 'addnote' : True, 'notes': notes, 'assignments': assignments}) 
def download_file(request,  code, filename, name):
    name=name+".pdf"
    if filename != '':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR + filename
        path = open(filepath, 'rb')
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % name
        # Return the response value
        return response
    else:
        # Load the template
        return course_detail_view(request,code)
def submit_assignment(request, code, name):
    course= Course.objects.get(code = code)
    assignment=Assignment.objects.filter(course=course, name=name).first()
    resubmit=False
    if(assignment is not None):
        resubmit=assignment.resubmissions_allowed
    submission=Submission.objects.filter(assignment=assignment, student=request.user).first()
    course= Course.objects.get(code = code)
    submitted=False
    if(request.user.userType=="Instructor"):
        return render(request, 'users/assignment.html', {'course': course, 'assignment': assignment}) 
    if(request.user.userType=="Admin"):
        redirect('profile')
    if request.method=='POST':
        form = AddSubmissionForm(request.POST,request.FILES, instance=submission)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.student = request.user
            obj.course= course
            obj.assignment=assignment
            obj.save()
            submitted=True
    else: 
        form=AddSubmissionForm()
    return render(request, 'users/assignment.html', {'course': course, 'submitted': submitted, 'assignment': assignment, 'resubmit': resubmit, 'form':form}) 
def view_submissions(request, code, name):
    course= Course.objects.get(code = code)
    assignment=Assignment.objects.filter(course=course, name=name).first()
    submissions=Submission.objects.filter(assignment=assignment)
    return render(request, 'users/assignment.html', {'assignment': assignment, 'course': course, 'submissions': submissions, 'viewsub': True}) 
def edit_assignment(request, code, name):
    course= Course.objects.get(code = code)
    assignment=Assignment.objects.get(course=course, name=name)
    if(request.user.userType!="Instructor"):
        return redirect('profile')
    if request.method=='POST':
        form = AddAssignmentForm(request.POST,request.FILES, instance=assignment)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()
            return submit_assignment(request, code, obj.name)
    else: 
        form=AddAssignmentForm(instance=assignment)
    return render(request, 'users/edit-assignment.html', {'form':form}) 


def course_announcements(request,code):
    course= Course.objects.get(code = code)
    announcements=Announcement.objects.filter(course=course)
    if request.method=='POST':
        form = AddAnnouncementForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.author=request.user
            obj.save()
    else: 
        form=AddAnnouncementForm()
    return render(request, 'users/course-announcements.html', {'form':form, 'course': course, 'announcements' : announcements})

def course_announcement_page(request, code, name):
    course= Course.objects.get(code = code)
    announcement=Announcement.objects.get(course=course, title=name)
    
    if request.method=='POST':
        form = AddReplyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.announcement = announcement
            obj.author= request.user
            obj.save()
    else: 
        form=AddReplyForm()
    replies=Reply.objects.filter(announcement=announcement)
    return render(request, 'users/announcement-page.html', {'form':form,'course': course, 'announcement' : announcement, 'replies' : replies})
def all_assignments(request):
    courses= Course.objects.filter(students=request.user)
    assignments=Assignment.objects.none()
    for course in courses:
        assignments=assignments.union(Assignment.objects.filter(course=course))
    return render(request, 'users/all-assignments.html', {'assignments' : assignments})
def all_announcements(request):
    courses= Course.objects.filter(students=request.user)
    announcements=Announcement.objects.none()
    for course in courses:
        announcements=announcements.union(Announcement.objects.filter(course=course))
    return render(request, 'users/all-announcements.html', {'announcements' : announcements})
def show_gradesheet(request):
    grades=Grade.objects.filter(student=request.user)
    creds=0
    totsum=0
    for grade in grades:
        totsum+=(grade.grade)*(grade.course.course_credits)
        creds+=grade.course.course_credits
    if(creds!=0):
        cgpa=totsum/creds
    else:
        cgpa=0
    return render(request, 'users/gradesheet.html', {'grades' : grades, 'cgpa': cgpa})
def upload_grades(request):
    if(request.user.userType!="Instructor"):
        return redirect('profile')
    if request.method=='POST':
        form = AddGradeForm(request.POST, request=request)
        if form.is_valid():
            form.save()
    else: 
        form=AddGradeForm(request=request)
    return render(request, 'users/upload-grades.html', {'form': form})
class CourseDetailView(generic.DetailView):
    model = Course
