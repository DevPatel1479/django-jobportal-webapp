from django.urls import path, include
from . import views


app_name = 'jobs'

urlpatterns = [
    path('<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('<int:pk>/details/', views.job_detail, name='job_detail'),  # View Job Details
    path('<int:pk>/edit/', views.job_edit, name='job_edit'),  # Edit Job
    path('bulk-delete/', views.bulk_delete_jobs, name='bulk_delete'),
    path('employer/', include('employers.urls')),
]