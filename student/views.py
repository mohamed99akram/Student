from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response

from student.serializers import StudentSerializer, SubjectSerializer, ParentSerializer
from .models import Student, Subject, Parent

from rest_framework import mixins, generics, status


class StudentView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ParentView(APIView):
    def get(self, request):
        data = ParentSerializer(Parent.objects.all(), many=True)
        return Response(data.data)

    def post(self, request):
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ParentDetailView(APIView):
    def put(self, request, id): 
        serializer = ParentSerializer(
            data=request.data, instance=Parent.objects.get(id=id))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def get(self, request, id): 
        try:  # use it to avoid get errors
            serializer = ParentSerializer(Parent.objects.get(id=id))
            return Response(serializer.data)
        except Parent.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):  # no need for REST framework, endpoint GUT will have a DELETE button
        try:  # use it to avoid get errors
            Parent.objects.get(id=id).delete()
            return Response(status=status.HTTP_200_OK)
        except Parent.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)


class SubjectView(generics.GenericAPIView,  # should be there
                  mixins.CreateModelMixin,  # needs id
                  mixins.ListModelMixin):  # all data

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SubjectDetailView(generics.GenericAPIView,  # should be there
                        mixins.CreateModelMixin,  # needs id
                        mixins.UpdateModelMixin,  # needs id
                        mixins.DestroyModelMixin,  # needs id
                        mixins.RetrieveModelMixin):  # single -> needs id

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, *args, **kwargs):  # uses id -> should be pk in urls.py
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
