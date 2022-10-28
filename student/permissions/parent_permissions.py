from rest_framework.response import Response
from server.settings import SECRET_KEY
from ..models import Token, Parent
import jwt
from datetime import datetime, timezone
from rest_framework import permissions, exceptions, status, authentication
from ..common import generateToken
from .common_permissions import CheckUserRegister, UserPermissions


class ParentPermissions(UserPermissions):

    def __init__(self) -> None:
        # super().__init__()
        self.model = Parent
        self.id = 'id'
    # def has_permission(self, request, view):
    #     token = request.headers.get('token')
    #     self.message = 'You do not have access 1'

    #     try:
    #         decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms="HS256")
    #         view.check_object_permissions(
    #             request, decoded_jwt)  # is this correct?
    #         return True
    #     except jwt.exceptions.DecodeError:
    #         # print('Token decode is invalid')
    #         raise exceptions.AuthenticationFailed('Token decode is invalid')
    #         return False
    #     except Exception as e:
    #         # print(e)
    #         raise exceptions.AuthenticationFailed(e)
    #         return False

    # # For PUT, PATCH , DELETE
    # def has_object_permission(self, request, view, obj):
    #     try:
    #         user = Parent.objects.get(id=view.kwargs['id'])
    #         if user.username == obj['username'] and user.id == view.kwargs['id']:
    #             return True
    #         # print('this user cannot perform this action')
    #         raise exceptions.AuthenticationFailed(
    #             'this user cannot perform this action')
    #     except Parent.DoesNotExist as e:
    #         raise exceptions.AuthenticationFailed('No user with this id')
    #         return False


class CheckParentRegister(CheckUserRegister):
    def __init__(self):
        super().__init__()
        self.model = Parent
