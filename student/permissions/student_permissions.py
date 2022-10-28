from ..models import Student
from .common_permissions import CheckUserRegister, UserPermissions

class CheckStudentRegister(CheckUserRegister):
    def __init__(self):
        super().__init__()
        self.model = Student
        
class StudentPermissions(UserPermissions):
    def __init__(self) -> None:
        # super().__init__()
        self.model = Student
        self.id = 'pk'