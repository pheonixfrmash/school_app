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

urlpatterns = [
    # path('add',Subject.add,name='div_add'),
    # path('web/add',Subject.add_ads,name='web_add'),
    url(r'^subject_sample_download/$',send_file, name='subject_sample_download'),
    url(r'^subject_teacher_sample_download/$',send_file_subject_teacher, name='subject_teacher_sample_download'),
    url(r'^class_teacher_sample_download/$',send_file_class_teacher, name='class_teacher_sample_download'),
    path('excel/',download_excel_data,name='sub_view'),
    path('',list_subjects_data,name='subject'),
    path('add',subject_upload,name='subject_upload'),
    path('edit/<id>',edit_subject,name='subject_edit'),
    path('details/<id>',view_subject,name='subject_view'),
    path('save_subject/<id>',save_subject,name='save_subject'),
    path('subject_teacher',subject_teacher_upload,name='subject_teacher'),
    path('class_teacher',class_teacher_upload,name='class_teacher')
]
