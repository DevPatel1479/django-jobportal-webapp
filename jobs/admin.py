from django.contrib import admin
from .models import Job
# Register your models here.


class JobAdmin(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(Job, JobAdmin)
