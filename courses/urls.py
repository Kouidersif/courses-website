from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    ListCourses, retrieveCourse, add_lessons
)
urlpatterns = [
    path("", ListCourses.as_view(), name="home"),
    path("add/", add_lessons),
    path("course/<int:pk>/", retrieveCourse.as_view(), name="one_course"),
]
