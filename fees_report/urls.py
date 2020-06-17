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
from fees_report import views
urlpatterns = [
     path('',views.get_manage_fees_report,name='get_manage_fees_report'),
     path('add_fees_structure',views.add_fees_structure,name='add_fees_structure'),
     path('get_account_no', views.get_account_no, name='get_account_no'),
     # url(r'^add_school_excel/$',views.school_upload,name='add_school_excel'),
     # url(r'^school_sample_download/$',views.send_file, name='school_sample_download'),
     path('edit_fees/<int:fees_id_pk>',views.edit_fees,name='edit_fees'),
     path('view_fees_structure/<int:fees_id_pk>',views.view_fees_structure,name='view_fees_structure'),    
] 