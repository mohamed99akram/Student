from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response
from student.permissions.common_permissions import CheckUserSignIn
from student.permissions.parent_permissions import ParentPermissions, CheckParentRegister
from student.permissions.student_permissions import StudentPermissions, CheckStudentRegister

from student.serializers import StudentSerializer, SubjectSerializer, ParentSerializer
from .models import Student, Subject, Parent, Token, User

from rest_framework import mixins, generics, status, exceptions
import json
from .common import generateToken


class StudentSignIn(APIView):
    @CheckUserSignIn(cl=Student)
    def post(self, request, *args, **kwargs):
        user_token = kwargs['user_token']
        return Response({'msg': 'User Signed in Sucessfully', 'token': user_token.token})

# Student Register
class StudentView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [CheckStudentRegister]
    # CheckSutdentRegister.authenticate -> perform_create -> create

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token_id = response.data['token']
        try:
            token = Token.objects.get(id=token_id)
        except:
            raise exceptions.AuthenticationFailed(
                {'message': 'Token was not created'})

        return Response({'message': 'Student created successfully', 'token': token.token}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user_data = self.request.data
        encoded_jwt = generateToken(
            user_data['username'], user_data['password'])
        p = None
        if 'parent_id' in user_data:
            try:
                parent_id = user_data['parent']
                p = Parent.objects.get(id=parent_id)
            except Parent.DoesNotExist:
                raise exceptions.AuthenticationFailed(
                    {'message': 'No parent with this id'})
        if 'parent_username' in user_data:
            try:
                parent_username = user_data['parent_username']
                p = Parent.objects.get(username=parent_username)
            except Parent.DoesNotExist:
                raise exceptions.AuthenticationFailed(
                    {'message': 'No parent with this username'})

        user_token = Token.objects.create(token=encoded_jwt)
        serializer.validated_data.update(token=user_token)
        if p is not None:
            serializer.validated_data.update(parent=p)
        return super().perform_create(serializer)


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [StudentPermissions]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        token_id = response.data['token']
        try:
            token = Token.objects.get(id=token_id)
        except:
            raise exceptions.AuthenticationFailed(
                {'message': 'Token was not updated'})

        return Response({'message': 'Student updated successfully', 'token': token.token}, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        print(serializer.instance.__dict__)
        if 'username' not in self.request.data and 'password' not in self.request.data:
            return super().perform_update(serializer)
        token_id = serializer.instance.token_id
        user_data = self.request.data
        new_token = generateToken(user_data['username'], user_data['password'])
        try:
            token_obj = Token.objects.get(id=token_id)
            token_obj.token = new_token
            token_obj.save()
        except Exception as e:
            print(e)
            raise exceptions.AuthenticationFailed(
                {'message': 'Token was not updated'})
        serializer.validated_data.update(token=token_obj)
        return super().perform_update(serializer)

class ParentSignIn(APIView):
    # authentication_classes = [CheckParentSignin2]
    @CheckUserSignIn(cl=Parent)
    def post(self, request, *args, **kwargs):
        # user_name = request.data['username']
        # encoded_jwt = generateToken(user_name, request.data['password'])
        # token_id = Parent.objects.get(username=user_name).token_id
        # token = Token.objects.get(id=token_id)
        # token.token = encoded_jwt
        # token.save()
        # return Response({'msg': 'User Signed in Sucessfully', 'token':encoded_jwt})
        user_token = kwargs['user_token']
        return Response({'msg': 'User Signed in Sucessfully', 'token': user_token.token})


class ParentView(APIView):
    # def get(self, request):
    #     data = ParentSerializer(Parent.objects.all(), many=True)
    #     return Response(data.data)

    authentication_classes = [CheckParentRegister]

    def post(self, request, *args, **kwargs):
        # Create a new token
        encoded_jwt = generateToken(
            request.data['username'], request.data['password'])
        user_token = Token.objects.create(token=encoded_jwt)
        # user_token = kwargs['user_token']
        serializer = ParentSerializer(
            data={**request.data, 'token': user_token.id})
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            return Response({'msg': 'User Created Sucessfully', 'token': user_token.token})
        else:
            return Response(serializer.errors)


class ParentDetailView(APIView):
    permission_classes = [ParentPermissions]

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
