"""school_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings 
from django.conf.urls.static import static
from login import views
from module_manager import models


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('login.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('roles/',include('roles.urls')),
    path('manage_user/',include('users.urls')),
    path('module_manager/',include('module_manager.urls')),
    path('module_access/',include('module_access.urls')),
    path('advertisement/',include('advertisement.urls')),
    path('resources/',include('resources.urls')),
    path('school/',include('school.urls')),
    path('division/',include('division.urls')),
    path('state/',include('state.urls')),
    path('city/',include('city.urls')),
    path('competitive_exam/',include('competitive_exam.urls')),
    path('student/',include('student.urls')),
    path('users/',include('users.urls')),
    path('class_master/',include('class_master.urls')),
    path('fees/',include('fees.urls')),
    path('fees_report/',include('fees_report.urls')),
    path('teacher/',include('teacher.urls')),
    path('subject/',include('subject.urls')),
    path('permissions/',include('permissions.urls')),    
    path('attendance/',include('attendance.urls')),  
]

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 