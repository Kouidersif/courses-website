from django.db import models
from courses.models import Course
from django.conf import settings
from django.utils import timezone


User = settings.AUTH_USER_MODEL

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="instructor/profile/", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    courses_enrolled = models.ManyToManyField(Course)
    time_created = models.DateTimeField(auto_now_add=timezone.now())
    time_updated = models.DateTimeField(auto_now=timezone.now())
    def __str__(self):
        return self.user.full_name or self.user.email




