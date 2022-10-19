
from django.urls import path
from .views import index, create, update, remove
urlpatterns = [
    path("", index),
    path("add/", create),
    path("change/", update),
    path("remove/", remove)
]
