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
from module_access import views
urlpatterns = [
     path('',views.get_module_access,name='get_module_access'),
     path('get_module_access_details/<int:pk>',views.get_module_access_details,name='get_module_access_details'),
     path('set_module_role/',views.set_module_role,name='set_module_role'),
     # path('add_module_manager',views.add_module_manager,name='add_module_manager'),
     # path('edit_module_manager/<int:pk>',views.edit_module_manager,name='edit_module_manager'),
     # path('delete_module',views.delete_module,name='delete_module'),
     
     
    
] 