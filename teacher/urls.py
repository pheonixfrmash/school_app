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
from teacher.views import *
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    # path('add', add,name='div_add'),
    # path('web/add', add_ads,name='web_add'),
    url(r'^teacher_sample_download/$', send_file, name='teacher_sample_download'),
    path('excel/',download_excel_data,name='teacher_view'),
    path('',list_teachers_data,name='teacher'),
    path('add', teacher_upload,name='teacher_upload'),
    path('edit/<id>', edit_teacher,name='teacher_edit'),
    path('details/<id>', view_teacher,name='teacher_view'),
    path('save_teacher/<id>', save_teacher,name='save_teacher')
]
