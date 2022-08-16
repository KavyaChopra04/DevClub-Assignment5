from django.contrib import admin
from users.models import *
from .models import *
from django import forms
from datetimepicker.widgets import DateTimePicker
# Register your models here.
class AddGradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('course', 'student', 'grade', )
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super(AddGradeForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(profs=request.user)
        