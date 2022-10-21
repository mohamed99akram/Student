from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from .models import Student
import json

# student without id


class Student1(View):
    def get(self, request):
        data = list(Student.objects.all().values())
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        Student.objects.create(**data)
        return JsonResponse({'message': 'Student created successfully',
                             'data': list(Student.objects.all().values())}, status=201)


# Student with id
class Student2(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        data = list(Student.objects.filter(id=id).values())
        return JsonResponse(data, safe=False)

    def put(self, request, *args, **kwargs):
        id = kwargs['id']
        data = json.loads(request.body)
        Student.objects.filter(id=id).update(**data)
        return JsonResponse({'message': 'Student updated successfully',
                             'data': list(Student.objects.filter(id=id).values())}, status=201)

    def delete(self, request, *args, **kwargs):
        id = kwargs['id']
        Student.objects.get(id=id).delete()
        assert(Student.objects.filter(id=id).count() == 0)
        return JsonResponse({'message': 'Student deleted successfully', }, status=201)
