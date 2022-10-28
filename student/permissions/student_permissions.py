from rest_framework.response import Response
from server.settings import SECRET_KEY
from ..models import Token, Parent, Student
import jwt
from datetime import datetime, timezone
from rest_framework import permissions, exceptions, status, authentication
from ..common import generateToken
from .common_permissions import CheckUser

class CheckStudentRegister(CheckUser):
    def __init__(self):
        super().__init__()
        self.model = Student
    