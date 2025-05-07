from django.db import models
from users.models import User
# Create your models here.


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="N/A")
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text="Upload a profile photo (JPEG, PNG)"
    )
    resume = models.FileField(upload_to='resumes/')
    skills = models.ManyToManyField(Skill, blank=True)
    about_me = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name
