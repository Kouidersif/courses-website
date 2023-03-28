from django.shortcuts import render, redirect
from django.views import generic
from users_auth.forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from courses.models import Course, Lessons
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CreateCourseForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from users_auth.mixins import InstructorAccessRequired, UserAccessDenied

User = get_user_model()





class TutorSignUp(UserAccessDenied, generic.FormView):
    form_class = SignUpForm
    template_name = "auth_instructor/register.html"
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_tutor = True
        user.save()
        new_user= authenticate(
                email= form.cleaned_data['email'],
                password= form.cleaned_data['password1']
            )
        login(self.request, new_user)
        if self.request.user.full_name:
            welcome_message = f"Succesfully registred {self.request.user.full_name} 🎉"
        else:
            welcome_message = f"Succesfully registred 🎉"
        messages.success(self.request, welcome_message)
        return redirect("home")









class CreateCourse(InstructorAccessRequired, generic.FormView):
    form_class = CreateCourseForm
    template_name = "crud_inst/create.html"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instructor'] = self.request.user.instructorprofile
        return kwargs
    
    def form_valid(self, form):
        lessons = self.request.POST.getlist("lessons")
        add_instructor = form.save(commit=False)
        add_instructor.instructor = self.request.user.instructorprofile
        add_instructor.save()
        for lesson in lessons:
            get_instance = get_object_or_404(Lessons, id=lesson)
            add_instructor.lessons.add(get_instance)
        messages.success(self.request, "Course has been created!!")
        return redirect("home")
    def form_invalid(self, form):
        messages.warning(self.request, form.errors)



class UpdateCourse(InstructorAccessRequired, generic.UpdateView):
    model = Course
    form_class= CreateCourseForm
    template_name = "crud_inst/updateCourse.html"
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instructor'] = self.request.user.instructorprofile
        return kwargs
    def get_success_url(self):
        messages.success(self.request, "Course has been UPDATED!!")
        return reverse_lazy("home")






class DeleteCourse(InstructorAccessRequired, generic.DeleteView):
    model = Course
    template_name = "crud_inst/deleteCourse.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_to_delete"] = self.get_object()
        return context
    def get_success_url(self):
        messages.success(self.request, "Course has been deleted")
        return reverse_lazy("home")
    





    



