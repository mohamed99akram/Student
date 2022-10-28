from django.db import models

# Create your models here.

class Token(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tokens'
class User(models.Model):
    # id = models.AutoField(primary_key=True)
    
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    token = models.ForeignKey(Token, on_delete=models.CASCADE, null=True)
    class Meta:
        abstract = True


class Parent(User):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # user_data = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = "parent"


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "subject"


class Student(User):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField()
    student_class = models.IntegerField()

    # user_data = models.OneToOneField(User, on_delete=models.CASCADE)

    # One to many relationship
    parent = models.ForeignKey(
        Parent, related_name="students", on_delete=models.SET_NULL, null=True)
    # Many to many relationship
    subjects = models.ManyToManyField(Subject, related_name='students')

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = 'Student'
        constraints = [
            models.CheckConstraint(
                name='age greater than 5', check=models.Q(age__gt=5)),
            models.CheckConstraint(
                name='class greater than 0', check=models.Q(student_class__gt=0)),
        ]
