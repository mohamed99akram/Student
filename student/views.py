from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from .models import Student
from .forms import StudentForm
import json

# student without id


class Student1(View):
    def get(self, request):
        data = list(Student.objects.all().values())
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            form = StudentForm(data=json.loads(request.body))
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Student created successfully',
                                    'data': list(Student.objects.all().values())}, status=201)
            return JsonResponse(form.errors, status=422) 
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Unknown Format'}, status=500)

# Student with id


class Student2(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        data = list(Student.objects.filter(id=id).values())
        return JsonResponse(data, safe=False)

    def put(self, request, *args, **kwargs):
        try:
            id = kwargs['id']
            student = Student.objects.get(id=id)
            form = StudentForm(data=json.loads(request.body),instance=student)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Student updated successfully',
                                    'data': list(Student.objects.all().values())}, status=201)
            return JsonResponse(form.errors, status=422) 
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    def delete(self, request, *args, **kwargs):
        id = kwargs['id']
        Student.objects.get(id=id).delete()
        assert(Student.objects.filter(id=id).count() == 0)
        return JsonResponse({'message': 'Student deleted successfully', }, status=201)
