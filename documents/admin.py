from django.contrib import admin
from users.models import *
from .models import *
from django import forms
from datetimepicker.widgets import DateTimePicker
# Register your models here.
class DateTimeInput(forms.DateTimeInput):
    input_type='datetime-local'
class AddAssignmentForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=DateTimeInput())
    assignment = forms.FileField()
    class Meta:
        model = Assignment
        fields = ('name','deadline', 'assignment', 'resubmissions_allowed')
        
class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('name', 'note')

class AddSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('submission', 'name')