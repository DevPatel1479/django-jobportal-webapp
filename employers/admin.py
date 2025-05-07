from django.contrib import admin
from .models import EmployerProfile
# Register your models here.


class EmployerAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'user__name']



admin.site.register(EmployerProfile, EmployerAdmin)
