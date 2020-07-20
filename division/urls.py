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
from division.views import Division
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    # path('add',Division.add,name='div_add'),
    # path('web/add',Division.add_ads,name='web_add'),
    url(r'^division_sample_download/$',Division.send_file, name='division_sample_download'),
    path('excel/',Division.download_excel_data,name='div_view'),
    path('',Division.list_divisions_data,name='division'),
    path('add',Division.division_upload,name='division_upload'),
    path('edit/<id>',Division.edit_division,name='division_edit'),
    path('details/<id>',Division.view_division,name='division_view'),
    path('save_division/<id>',Division.save_division,name='save_division')
]
