from django.contrib import admin
from .models import JobApplication

# Register your models here.

class JobApplicationAdmin(admin.ModelAdmin):
    search_fields = ['job__title', 'job_seeker__name']

admin.site.register(JobApplication, JobApplicationAdmin)