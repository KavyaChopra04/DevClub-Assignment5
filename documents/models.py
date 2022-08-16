from django.db import models
from users.models import *
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
# Create your models here.
class Assignment(models.Model):
    name=models.CharField(max_length=200, unique=True, help_text="Enter display name")
    assignment = models.FileField(upload_to='assignments')
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    deadline = models.DateTimeField()
    resubmissions_allowed = models.BooleanField() 
    REQUIRED_FIELDS=['name', 'assignment', 'course', 'deadline', 'resubmissions_allowed']
    def __str__ (self):
        return self.name

class Note(models.Model):
    name=models.CharField(max_length=200, help_text="Enter display name")
    note = models.FileField(upload_to='notes')
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    REQUIRED_FIELDS=['name', 'note', 'course']
    def __str__ (self):
        return self.name

class Submission(models.Model):
    name=models.CharField(max_length=200, help_text="Enter display name")
    student= models.ForeignKey(UserInfo, on_delete = models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE)
    submission=models.FileField(upload_to='submissions')
    submission_time = models.DateTimeField(auto_now_add=True)
    REQUIRED_FIELDS=['student', 'assignment']
    def __str__ (self):
        return self.student
admin.site.register(Submission)
admin.site.register(Assignment)
admin.site.register(Note)