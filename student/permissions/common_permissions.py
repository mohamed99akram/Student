from server.settings import SECRET_KEY
import jwt
from rest_framework.response import Response
from ..models import Token, Parent
from rest_framework import exceptions, status, authentication, permissions
from ..common import generateToken


class CheckUserRegister(authentication.BaseAuthentication):
    def __init__(self):
        self.model = None

    def authenticate(self, request):

        user_data = request.data

        # Check username and password exist in the request
        if 'username' not in user_data or 'password' not in user_data:
            raise exceptions.AuthenticationFailed(
                {'message': 'Username or password is missing'})

        # Check if the user already exists
        username = user_data['username']
        db_user = self.model.objects.filter(username=username)
        if len(db_user) != 0:
            raise exceptions.AuthenticationFailed(
                {'message': 'User already exists'})

        # encoded_jwt = generateToken(username, user_data['password'])
        # Create token, save it and attach it to the user
        # user_token = Token.objects.create(token=encoded_jwt)

        # response = post_data(self, request, user_token=user_token)
        response = (request, None)
        return response


def CheckUserSignIn(**kwargs2):
    def innerCheckUserSignIn(post_func):
        def middleware(self, request, *args, **kwargs):
            if kwargs2['cl'] is None:
                kwargs2['cl'] = Parent

            user_data = request.data

            # Check username and password exist in the request
            if 'username' not in user_data or 'password' not in user_data:
                return Response({'message': 'Username or password is missing'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user exists
            try:
                db_user = kwargs2['cl'].objects.get(
                    username=user_data['username'])
            except kwargs2['cl'].DoesNotExist:
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
    return innerCheckUserSignIn


class UserPermissions(permissions.BasePermission):

    def __init__(self) -> None:
        # super().__init__()
        self.message = 'aaa'
        self.model = None

    def has_permission(self, request, view):
        print('entered has permission')
        token = request.headers.get('token')
        self.message = 'You do not have access 1'
        try:
            decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            # if self.model == Parent:
            view.check_object_permissions(
                request, decoded_jwt)  # is this correct?
            return True
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed('Token decode is invalid')
        except Exception as e:
            print(e)
            raise exceptions.AuthenticationFailed(e)


    # For PUT, PATCH , DELETE
    def has_object_permission(self, request, view, obj):
        print('entered has object permission')
        try:
            user = self.model.objects.get(id=view.kwargs[self.id])
            if type(user) is not dict:
                user = user.__dict__
            if type(obj) is not dict:
                obj = obj.__dict__

            if user['username'] == obj['username'] and user['id'] == view.kwargs[self.id]:
                return True
            raise exceptions.AuthenticationFailed(
                'this user cannot perform this action')
        except self.model.DoesNotExist as e:
            raise exceptions.AuthenticationFailed('No user with this id')

