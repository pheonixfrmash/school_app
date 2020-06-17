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
from django.conf.urls import url
from django.conf import settings 
from django.conf.urls.static import static
from users import views

urlpatterns = [
     path('',views.get_manage_user,name='get_manage_user'),
     path('add_user',views.add_user,name='add_user'),
     path('check_user_mobile',views.check_user_mobile,name='check_user_mobile'),
     path('edit_user/<int:pk>',views.edit_user,name='edit_user'),
     
    
] 

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 
