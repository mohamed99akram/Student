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

class CheckParentRegister(CheckUserRegister):
    def __init__(self):
        super().__init__()
        self.model = Parent
