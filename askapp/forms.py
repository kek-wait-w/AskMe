from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
import re


class LoginForm(forms.Form):
    useremail = forms.CharField()
    userpassword = forms.CharField()

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrong':
            raise ValidationError('')