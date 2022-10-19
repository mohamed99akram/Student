# Django School

It is an application built with Django to create, read, update, and delete students from a json file in the backend server.

# How to run it

* Clone this repository
* install django & poetry
* run `poetry shell`
* run `poetry add django`
* run `python manage.py runserver 8000`

# Endpoints:

* `http://127.0.0.1:8000/api/` to GET students in the json file
    * No body required for this request
* `http://127.0.0.1:8000/api/add` to POST a student to the json file
    * Example for the body: {"id": 1, "name": "Mohamed", "age": 32, "class": "F"}
* `http://127.0.0.1:8000/api/change` to PUT a student to the json file
    * It will update the student with the existing ID, if the ID doesn't exist it will create it.
    * Example for the body: {"id": 1, "name": "Saad", "age": 23, "class": "H"}
* `http://127.0.0.1:8000/api/remove` to DELETE a student from the json file
    * Example for the body: {"id":1}

You can use Postman to send requests
