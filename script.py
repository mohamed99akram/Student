# To run from shell: from script import *
from student.models import *

s1 = Student.objects.get(id=1)
s2 = Student.objects.get(id=2)
# s2 = Student.objects.create(first_name='Mohamed', last_name='Akram', age=20, student_class=10)
p1 = Parent.objects.get(id=1)
p2 = Parent.objects.get(id=2)
# p2 = Parent.objects.create(first_name='Akram', last_name='Abdo')
b1 = Subject.objects.get(id=1)
b2 = Subject.objects.get(id=2)
