
from django.urls import path
from . import views



urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),    
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('delete-resume/', views.delete_resume, name='delete_resume'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('remove-skill/', views.remove_skill, name='remove_skill'),
    path('apply/<int:job_id>/', views.apply_to_job, name='apply_to_job'),
    path('dashboard/search/', views.job_search, name='job_search'),
    

]
