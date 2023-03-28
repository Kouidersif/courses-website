from django import forms
from courses.models import Lessons, Course
from django.contrib.auth.forms import UserChangeForm




class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("course_name", "course_category", "lessons", "description", "tags", "thumbnail")
    def __init__(self, instructor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lessons'].queryset = Lessons.objects.filter(instructor=instructor)
        self.fields['lessons'].widget.attrs["class"] = "form-select mb-2"
        self.fields['course_name'].widget.attrs["class"] = "form-control mb-2"
        self.fields['course_category'].widget.attrs["class"] = "form-control mb-2"
        self.fields['description'].widget.attrs["class"] = "form-control mb-2"
        self.fields['tags'].widget.attrs["class"] = "form-control mb-2"
        self.fields['thumbnail'].widget.attrs["class"] = "form-control mb-2"




