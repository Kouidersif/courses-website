from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from .forms import CustomUserLogin, UpdateUserInfo
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .mixins import UserAccessDenied

User = get_user_model()






class LoginUser(UserAccessDenied, generic.FormView):
    form_class = CustomUserLogin
    template_name = "login.html"
    def form_valid(self, form):
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        login(self.request, user)
        if self.request.user.full_name:
            welcome_message = f"Welcome Back {self.request.user.full_name} 🎉"
        else:
            welcome_message = f"Welcome Back 🎉"
        messages.success(self.request, welcome_message)
        return redirect("home")



class UpdateUser(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UpdateUserInfo
    template_name = "user_form.html"
    def get(self, *args, **kwargs):
        if self.request.user.id != kwargs["pk"]:
            messages.warning(self.request, "Access Denied")
            return redirect("home")
        return super().get(*args, **kwargs)
    def get_success_url(self):
        messages.success(self.request, "User has been UPDATED!")
        return reverse_lazy("home")




class UserProfile(generic.DetailView):
    model = User
    fields = ("email", "full_name")
    template_name = "profile.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = self.get_object()
        return context
