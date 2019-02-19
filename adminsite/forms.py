from django import forms
from .models import *


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        exclude = ['adminid']
        widgets = {
            'adminpass': forms.PasswordInput(),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['']
