from django import forms
from .models import Student
from django.forms import ValidationError
import re


def check_first_name(value: str):
    if value[0].upper() != value[0]:
        raise ValidationError('first_name should start with a Capital letter')


def check_last_name(value: str):
    if value[0].upper() != value[0]:
        raise ValidationError('last_name should start with a Capital letter')


def check_email(value):
    if re.match(r'[^@]+@[^@]+\.[^@]+', value) is None:
        raise ValidationError('Email is not valid')


class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, validators=[check_first_name])
    last_name = forms.CharField(max_length=100, validators=[check_last_name])
    email = forms.CharField(max_length=100, validators=[check_email])
    
    class Meta:
        model = Student
        fields = "__all__"
        exclude = ['parent', 'subjects']