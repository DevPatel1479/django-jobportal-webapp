from django.urls import path
from . import views

urlpatterns = [
    path('job/', views.job_applications, name='job_applications'),
    path('withdraw-application/', views.withdraw_application, name='withdraw_application'),
    path('applications/<int:job_id>/view-applicants/', views.view_applicants, name='view_applicants'),
]
