from rest_framework import serializers
from .models import Student, Parent, Subject
from django.forms import ValidationError
import re


def check_name(value: str):
    if value[0].upper() != value[0]:
        raise ValidationError('first_name should start with a Capital letter')


def check_email(value):
    if re.match(r'[^@]+@[^@]+\.[^@]+', value) is None:
        raise ValidationError('Email is not valid')


class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name']


class ParentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100, validators=[check_name])
    last_name = serializers.CharField(max_length=100, validators=[check_name])
    students = StudentListSerializer(many=True, read_only=True)

    class Meta:
        model = Parent
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    students = StudentListSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = '__all__'

############# Student ############


class ParentSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['first_name', 'last_name']


class SubjectSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']


class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100, validators=[check_name])
    last_name = serializers.CharField(max_length=100, validators=[check_name])
    email = serializers.CharField(max_length=100, validators=[check_email])
    parent = ParentSerializer2(read_only=True)
    subjects = SubjectSerializer2(many=True, read_only=True)
    # like forms

    class Meta:
        model = Student
        fields = '__all__'
