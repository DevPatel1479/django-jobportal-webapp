from django.contrib import admin
from .models import JobSeekerProfile
# Register your models here.



class JobSeekerAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(JobSeekerProfile, JobSeekerAdmin)

