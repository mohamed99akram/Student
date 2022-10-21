from django.db import models

# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField()
    student_class = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = 'Student'	