# Generated by Django 4.1.2 on 2022-10-22 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0004_alter_student_parent"),
    ]

    operations = [
        migrations.RemoveField(model_name="student", name="subject",),
        migrations.AddField(
            model_name="student",
            name="subjects",
            field=models.ManyToManyField(related_name="students", to="student.subject"),
        ),
    ]
