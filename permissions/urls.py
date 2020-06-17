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
from subject.views import *
from django.conf import settings 
from django.conf.urls.static import static
from permissions.views import assign_user_permissions,get_all_permissions,get_user_permissions,get_user_groups,assign_group_permissions,assign_group_users,assign_permissions
urlpatterns = [
    path('',assign_permissions,name='permissions'),
    path('group_permission',assign_group_permissions,name='group_permission'),
    path('user_permission',assign_user_permissions,name='user_permission'),
    path('user_group',assign_group_users,name='group_users'),
]