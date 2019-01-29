from django import forms
from .models import *


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        exclude = ['adminid']
        widgets = {
            'adminpass': forms.PasswordInput(),
        }