from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from .models import Lessons






class ListCourses(generic.ListView):
    queryset = Course.objects.all()
    template_name = "list_courses.html"



class retrieveCourse(LoginRequiredMixin, generic.DetailView):
    queryset = Course.objects.all()
    context_object_name = "course"
    template_name = "crud/course_detail.html"




#get some dummy data from this endpoint
def add_lessons(request):
    r = requests.get("https://jsonplaceholder.typicode.com/posts")
    response = r.json()
    for resp in response:
        Lessons.objects.create(
            instructor = request.user.instructorprofile,
            lesson_title = resp["title"],
            description = resp["body"]
        )
    return HttpResponse("done")