from django import forms
from .models import TimePackage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TimePackageForm(forms.ModelForm):
    class Meta:
        model = TimePackage
        fields = ['description', 'duration_minutes', 'use_type']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("This email is already in use. Please enter a different one.")
        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError("This username already is taken. Please enter a different one.")
        return username
    class Meta: 
        model = User
        fields = ("username", "email", "password1", "password2")