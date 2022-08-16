from django.db import models
from users.models import *
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
# Create your models here.
class Score(models.Model):
    student = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assessment_name = models.CharField(max_length=25)
    weightage = models.FloatField(help_text="In percentage")
    total_score = models.FloatField(help_text="maximum score")
    student_score = models.FloatField(help_text="student's score")
class Grade(models.Model):
    student = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    GRADES_CHOICES = [
        (10, 'A'),
        (9, 'A-'),
        (8, 'B'),
        (7, 'B-'),
        (6, 'C'),
        (5, 'C-'),
        (4, 'D'),
        (3, 'D-'),
        (2, 'E'),
        (1, 'F')
    ]
    grade = models.IntegerField(choices=GRADES_CHOICES)
admin.site.register(Score)
admin.site.register(Grade)