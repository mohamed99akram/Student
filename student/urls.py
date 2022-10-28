
from django.urls import path, include
from .views import StudentView, StudentDetailView,\
    ParentView, ParentDetailView, SubjectView, SubjectDetailView,\
        ParentSignIn

urlpatterns = [
    path("students/", include([
        path("register", StudentView.as_view()),
        path("<int:pk>", StudentDetailView.as_view()),
    ])),
    path("parents/", include([
        path("register", ParentView.as_view()),
        path("signin", ParentSignIn.as_view()),
        path("<int:id>", ParentDetailView.as_view()),
    ])),
    path("subjects/", include([
        path("", SubjectView.as_view()),
        path("<int:pk>", SubjectDetailView.as_view()),
    ]))
]
