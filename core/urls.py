from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # URL pattern for the homepage
    path('about/', views.about_us, name='about_us'),
    path('register/', views.registration, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', include('jobseekers.urls')),
    path('employer/', include('employers.urls')),
    path('applications/', include('applications.urls')),
    path('logout/', views.CustomLogoutView.as_view(next_page='home'), name='logout'),
    path('all-jobs/', views.job_list, name='job_list'),
    path('send-otp/', views.send_otp, name="send_email_otp"),
    path('verify-otp/', views.verify_otp, name="verify_email_otp"),

    # Add more URL patterns here as needed
]
