
from django.urls import path
from .views import Student1, Student2
urlpatterns = [
    path("", Student1.as_view()),
    path("<int:id>", Student2.as_view()),
]
