from django.db import models
from instructors.models import InstructorProfile
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import os
import time
from django.utils import timezone
from moviepy.video.io.VideoFileClip import VideoFileClip
from django.db.models.signals import pre_delete
from django.dispatch import receiver





@deconstructible
class VideoValidator:
    def __init__(self, allowed_extensions=['mp4', "MOV"]):
        self.allowed_extensions = allowed_extensions

    def __call__(self, file):
        ext = os.path.splitext(file.name)[1][1:].lower()
        if ext not in self.allowed_extensions:
            raise ValidationError('Only %s files are allowed.' % ', '.join(self.allowed_extensions))







def get_upload_path(instance, filename):
    try:
        # generate unique filename by appending timestamp
        filename, ext = os.path.splitext(filename)
        timestamp = str(int(time.time()))
        filename = f"{filename}_{timestamp}{ext}"

        # get user's to ensure unique URL
        lesson_name = instance.lesson_title[:3]

        # construct upload path
        return f"lessons/videos/{lesson_name}/{filename}"
    except:
        return "lessons/videos/"


def get_course_name(instance, filename):
    # generate unique filename by appending timestamp
    filename, ext = os.path.splitext(filename)
    timestamp = str(int(time.time()))
    filename = f"{filename}_{timestamp}{ext}"

    #get course name
    course_name = instance.course_name
    
    # construct upload path
    return f"courses/thumbnail/{course_name}/{filename}"





class CourseCategory(models.Model):
    category = models.CharField(max_length=255)
    def __str__(self):
        return self.category



class Lessons(models.Model):
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    lesson_title = models.CharField(max_length=350)
    description = models.TextField()
    video = models.FileField(upload_to=get_upload_path, validators=[VideoValidator()])
    time_posted = models.DateTimeField(auto_now_add=timezone.now())
    time_edited = models.DateTimeField(auto_now=timezone.now())
    def __str__(self) -> str:
        return self.lesson_title
    def get_video_length(self):
        try:
            clip = VideoFileClip(self.video.path)
            length = clip.duration
            clip.close()
            return length
        except:
            print("error")

    


class Course(models.Model):
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=300)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, blank=True, null=True)
    lessons = models.ManyToManyField(Lessons, blank=True)
    description = models.TextField()
    tags = models.ManyToManyField("Tags", blank=True)
    thumbnail = models.ImageField(upload_to=get_course_name, null=True)
    time_posted = models.DateTimeField(auto_now_add=timezone.now())
    time_edited = models.DateTimeField(auto_now=timezone.now())
    def __str__(self) -> str:
        return self.course_name



class Tags(models.Model):
    tag_name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.tag_name


@receiver(pre_delete, sender=Course)
def set_lessons_to_null(sender, instance, **kwargs):
    try:
        instance.lessons.clear()
    except:
        pass

