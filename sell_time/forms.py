from django import forms
from .models import TimePackage

class TimePackageForm(forms.ModelForm):
    class Meta:
        model = TimePackage
        fields = ['description', 'duration_minutes', 'use_type']