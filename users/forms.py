from django import forms
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.password_validation import validate_password
from .models import *
class UserRegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta: 
        model=UserInfo
        fields = ['userid', 'password','email','userType', 'name']
    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")
        
        validate_password(password)

        return cleaned_data

class UserLoginForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta: 
        model=UserInfo
        fields = ['email', 'password']
