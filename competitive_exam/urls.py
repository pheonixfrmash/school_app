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
from competitive_exam import views
urlpatterns = [
     path('',views.get_competitive_exam,name='get_competitive_exam'),
     path('add_competitive_exam',views.add_competitive_exam,name='add_competitive_exam'),
     #path('add_competitive_exam1/2)',views.add_competitive_exam1,name='add_competitive_exam1'),

     path('get_school_list',views.get_school_list,name='get_school_list'),
     path('post_competitive_exam/<int:pk>',views.post_competitive_exam,name='post_competitive_exam'),
path('cancel_competitive_exam/<int:pk>',views.cancel_competitive_exam,name='cancel_competitive_exam'),

    #  url(r'^add_school_excel/$',views.school_upload,name='add_school_excel'),
    # url(r'^school_sample_download/$',views.send_file, name='school_sample_download'), 

     path('edit_competitive_exam/<int:competitive_exam_id_pk>',views.edit_competitive_exam,name='edit_competitive_exam'),
path('view_competitive_exam/<int:competitive_exam_id_pk>',views.view_competitive_exam,name='view_competitive_exam'),
     # path('delete_module',views.delete_module,name='delete_module'),
     
     
    
] 