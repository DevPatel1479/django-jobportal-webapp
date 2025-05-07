"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from jobs.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # path('job/', include('jobs.urls')),
    # path('job/<int:pk>/delete/', job_delete, name='job_delete'),
    # path('job/<int:pk>/details', job_detail, name='job_detail'),  # View Job Details
    # path('job/<int:pk>/edit/', job_edit, name='job_edit'),  # Edit Job
    path("jobs/", include("jobs.urls", namespace="jobs")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
