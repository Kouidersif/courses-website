from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.db.models.signals import post_save
from django.dispatch import receiver
from students.models import StudentProfile
from instructors.models import InstructorProfile


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True , is_staff=False, is_superuser=False):
        if not email:
            raise ValueError("User Must Have an Email")
        if not password:
            raise ValueError("User Must Have a Password")
        user = self.model(
            email = self.normalize_email(email)
        )
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_staff(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff= True
        )
        return user
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email, password=password, is_staff=True, is_superuser=True
        )
        return user




class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name=('date joined'), auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    

    @property
    def get_full_name(self):
        return self.full_name
    @property
    def is_user_tutor(self):
        return self.is_tutor
    @property
    def is_user_student(self):
        return self.is_student
    @property
    def is_user_staff(self):
        return self.is_staff
    @property
    def is_super_user(self):
        return self.is_superuser
    
    @property
    def is_user_active(self):
        return self.is_active
    






@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_tutor:
            InstructorProfile.objects.create(user=instance)
        elif instance.is_student:
            #student profile
            StudentProfile.objects.create(user=instance)

