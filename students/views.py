from django.shortcuts import render, redirect
from django.views import generic
from users_auth.forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from courses.models import Course
from users_auth.mixins import UserAccessDenied, AccessOnlyToStudents
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import StudentProfile






User = get_user_model()






class StudentSignup(UserAccessDenied, generic.FormView):
    form_class = SignUpForm

    template_name = "auth_student/register.html"
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_student = True
        user.save()
        new_user= authenticate(
                email= form.cleaned_data['email'],
                password= form.cleaned_data['password1']
        )
        login(self.request, new_user)
        # If user has no full name, then show different message
        if self.request.user.full_name:
            welcome_message = f"Succesfully registred {self.request.user.full_name} 🎉"
        else:
            welcome_message = f"Succesfully registred 🎉"
        messages.success(self.request, welcome_message)
        return redirect("home")





class EnrollToCourse(AccessOnlyToStudents, generic.DetailView):
    model = Course
    template_name = "enroll.html"
    def get_object(self, queryset=None):
        # Get the Course object
        course = super().get_object(queryset=queryset)

        # Get the current user's StudentProfile
        student_profile = self.request.user.studentprofile

        student_profile.courses_enrolled.add(course)
        return course
    
