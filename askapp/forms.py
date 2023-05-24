from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
import re
from django.db import IntegrityError
from .models import Profile


class LoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_repeat = forms.CharField(widget=forms.PasswordInput, required=True)
    avatar = forms.FileField(widget=forms.FileInput, required=False)

    class Meta:
        model = Profile
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_repeat', 'avatar']

    def clean(self):
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if password != password_repeat:
            self.add_error('password', error='')
            self.add_error('password_repeat', error='')
            raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data.copy()
        cleaned_data.pop('password_repeat')
        cleaned_data.pop('avatar')
        try:
            return User.objects.create_user(**cleaned_data)
        except IntegrityError:
            return None