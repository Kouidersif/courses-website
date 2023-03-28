from django.urls import path
from .views import (
    StudentSignup, EnrollToCourse
)
urlpatterns = [
    path('', StudentSignup.as_view(), name="student_signup"),
    path('enroll/<int:pk>/', EnrollToCourse.as_view(), name="enroll"),
]
