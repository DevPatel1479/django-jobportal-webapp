from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views



urlpatterns = [
    path('employers_view/', views.employer_dashboard, name='employer_dashboard'),
    path('profile', views.employer_profile_view, name="employer_profile"),
    path('profile/edit/', views.edit_employer_profile, name='edit_employer_profile'),
    # path('job/', include('jobs.urls'))
    
]
