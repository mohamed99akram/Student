from django.db import models

# Create your models here.


class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

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


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField()
    student_class = models.IntegerField()
    email = models.EmailField()

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
