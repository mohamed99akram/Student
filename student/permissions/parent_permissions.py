from rest_framework.response import Response
from server.settings import SECRET_KEY
from ..models import Token, Parent
import jwt
from datetime import datetime, timezone
from rest_framework import permissions, exceptions, status, authentication
from ..common import generateToken
from .common_permissions import CheckUser


def CheckParentSignin(post_func):
    def middleware(self, request, *args, **kwargs):
        user_data = request.data

        # Check username and password exist in the request
        if 'username' not in user_data or 'password' not in user_data:
            return Response({'message': 'Username or password is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user exists
        try:
            db_user = Parent.objects.get(username=user_data['username'])
        except Parent.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the password is correct
        if db_user.password != user_data['password']:
            return Response({'message': 'Password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the token is valid
        try:

            token_id = db_user.token_id
            token = Token.objects.get(id=token_id)
            decoded_jwt = jwt.decode(
                token.token, SECRET_KEY, algorithms="HS256")

            if decoded_jwt['username'] != db_user.username or decoded_jwt['password'] != db_user.password:
                return Response({'message': 'Token is invalid'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return Response({'message': 'Token decode is invalid'}, status=status.HTTP_400_BAD_REQUEST)

        except Token.DoesNotExist:
            return Response({'message': 'Token does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # update token for this user
        token.token = generateToken(db_user.username, db_user.password)
        token.save()

        response = post_func(self, request, user_token=token)
        return response

    return middleware


class ParentPermissions(permissions.BasePermission):

    def __init__(self) -> None:
        super().__init__()
        self.message = 'aaa'

    def has_permission(self, request, view):
        token = request.headers.get('token')
        self.message = 'You do not have access 1'

        try:
            decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            view.check_object_permissions(
                request, decoded_jwt)  # is this correct?
            return True
        except jwt.exceptions.DecodeError:
            # print('Token decode is invalid')
            raise exceptions.AuthenticationFailed('Token decode is invalid')
            return False
        except Exception as e:
            # print(e)
            raise exceptions.AuthenticationFailed(e)
            return False

    # For PUT, PATCH , DELETE
    def has_object_permission(self, request, view, obj):
        try:
            user = Parent.objects.get(id=view.kwargs['id'])
            if user.username == obj['username'] and user.id == view.kwargs['id']:
                return True
            # print('this user cannot perform this action')
            raise exceptions.AuthenticationFailed(
                'this user cannot perform this action')
        except Parent.DoesNotExist as e:
            raise exceptions.AuthenticationFailed('No parent with this id')
            return False

class CheckParentRegister(CheckUser):
    def __init__(self) -> None:
        super().__init__()
        self.model = Parent