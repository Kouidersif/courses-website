from django.urls import path

from .views import (
    TutorSignUp, CreateCourse, DeleteCourse, UpdateCourse
)
urlpatterns = [
    path('', TutorSignUp.as_view(), name="tutor_Signup"),
    path('create/', CreateCourse.as_view(), name="create_course"),
    path('delete/<int:pk>/', DeleteCourse.as_view(), name="delete_course"),
    path('edit/<int:pk>/', UpdateCourse.as_view(), name="update_course"),
]
