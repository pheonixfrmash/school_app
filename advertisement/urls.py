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
from advertisement.views import Advertisement
urlpatterns = [
    path('add',Advertisement.add,name='add'),
    path('web_add',Advertisement.add_ads,name='web_add'),
    path('',Advertisement.list_ads,name='get_ads'),
    path('details/<id>',Advertisement.view_ads,name='details'),
    path('edit/<id>',Advertisement.edit_ads,name='edit'),
    path('save_ads/<id>',Advertisement.save_ads,name='save_ads'),

]
