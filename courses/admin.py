from django.contrib import admin
from .models import (
    Course,
Lessons, CourseCategory, Tags
)


admin.site.register(Course)
admin.site.register(Lessons)
admin.site.register(CourseCategory)
admin.site.register(Tags)