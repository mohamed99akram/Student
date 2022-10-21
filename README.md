# Django School

It is an application built with Django to create, read, update, and delete students from the database in the backend server.

# How to run it

* Clone this repository
* install django & poetry
* run `poetry shell`
* run `poetry add django`
* run `python manage.py runserver 8000`

# Endpoints:

* `http://127.0.0.1:8000/api/` 
  * GET: retrieve all the database
  * POST: create a new student with the given json body
* `http://127.0.0.1:8000/api/4` 
  * GET: retrive student with id = 4
  * PUT: change data of studetnt with id = 4
  * DELETE: delete student with id = 4

You can use Postman to send requests
