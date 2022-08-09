from django.db import models
from users.models import Course
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
# Create your models here.
class Assignment(models.Model):
    name=models.CharField(max_length=200)
    assignment = models.FileField(upload_to='assignments')
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    deadline = models.DateTimeField()

class Note(models.Model):
    name=models.CharField(max_length=200)
    note = models.FileField(upload_to='notes')
    course = models.ForeignKey(Course, on_delete = models.CASCADE)

admin.site.register(Assignment)
admin.site.register(Note)