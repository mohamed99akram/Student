# Django School

It is an application built with Django to create, read, update, and delete students from the database in the backend server.

# How to run it

* Clone this repository
* install django & poetry
* run `poetry shell`
* run `poetry install`
* run `python manage.py runserver 8000`

# Endpoints:
Using mixins:
* `http://127.0.0.1:8000/api/students` 
  * GET, POST
* `http://127.0.0.1:8000/api/students/2` 
  * GET, PUT, DELETE

Using APIView:
* `http://127.0.0.1:8000/api/parents` 
  * GET, POST
* `http://127.0.0.1:8000/api/parents/2` 
  * GET, PUT, DELETE

Using generics:
* `http://127.0.0.1:8000/api/subjects` 
  * GET, PUT
* `http://127.0.0.1:8000/api/subjects/2` 
  * GET, PUT, DELETE

API Documentation:
`http://127.0.0.1:8000/swagger/`