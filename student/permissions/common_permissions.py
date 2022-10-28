
from ..models import Token, Parent
from rest_framework import permissions, exceptions, status, authentication

class CheckUser(authentication.BaseAuthentication):
    def __init__(self):
        self.model = None
    
    def authenticate(self, request):

        user_data = request.data

        # Check username and password exist in the request
        if 'username' not in user_data or 'password' not in user_data:
            raise exceptions.AuthenticationFailed({'message': 'Username or password is missing'})

        # Check if the user already exists
        username = user_data['username']
        db_user = self.model.objects.filter(username=username)
        if len(db_user) != 0:
            raise exceptions.AuthenticationFailed({'message': 'User already exists'})

        # encoded_jwt = generateToken(username, user_data['password'])
        # Create token, save it and attach it to the user
        # user_token = Token.objects.create(token=encoded_jwt)

        # response = post_data(self, request, user_token=user_token)
        response = ( request, None)
        return response