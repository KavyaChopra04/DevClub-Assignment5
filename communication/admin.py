from django.db import models
from users.models import *
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
# Register your models here.

admin.site.register(Announcement)
admin.site.register(Reply)
class AddAnnouncementForm(forms.ModelForm):
    body=forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Announcement
        fields = ('title', 'body')
class AddReplyForm(forms.ModelForm):
    body=forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Reply
        fields = ('body',)