from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
import re


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput(), min_length=4)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), min_length=4)

