
from django.urls import path, include
from .views import StudentView, StudentDetailView,\
    ParentView, ParentDetailView, SubjectView, SubjectDetailView

urlpatterns = [
    path("students/", include([
        path("", StudentView.as_view()),
        path("<int:pk>", StudentDetailView.as_view()),
    ])),
    path("parents/", include([
        path("", ParentView.as_view()),
        path("<int:id>", ParentDetailView.as_view()),
    ])),
    path("subjects/", include([
        path("", SubjectView.as_view()),
        path("<int:pk>", SubjectDetailView.as_view()),
    ])),
]
