from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()


class UpdateUserInfo(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "full_name")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs["class"] = "form-control mb-2"
        self.fields['full_name'].widget.attrs["class"] = "form-control mb-2"






class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["full_name","email", "password1", "password2"]
    def __init__(self, *args,**kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs["class"] = "form-control"
        self.fields["full_name"].widget.attrs["placeholder"] = "Full Name"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"



class CustomUserLogin(AuthenticationForm):
    class Meta:
        model = User
        fields= ["username", 'password']
    def __init__(self, *args, **kwargs):
        super(CustomUserLogin, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs['class'] = 'form-control'
        self.fields["username"].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
    def clean_username(self):
        email = self.cleaned_data['username']
        if '@' not in email:
            raise ValidationError("Invalid Email")
        else:
            return email
