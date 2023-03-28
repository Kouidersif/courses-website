from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.utils import timezone



class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="instructor/profile/", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=timezone.now())
    time_updated = models.DateTimeField(auto_now=timezone.now())
    def __str__(self):
        return self.user.full_name or "instructor"
