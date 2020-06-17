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
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from student import views

urlpatterns = [

    path('', views.get_manage_student, name='student'),
    path('student_upload', views.student_upload, name='student_upload'),
    path('send_file_student', views.send_file_student, name='send_file_student'),
    path('edit_student/<int:student_id_pk>', views.edit_student, name='edit_student'),
    path('view_student/<int:student_id_pk>', views.view_student, name='view_student'),
    # path('check_roll_no/<int:roll_no>/<int:class_name>/<int:division>/<int:student_id_pk>', views.check_roll_no,
    #      name='check_roll_no'),
    # path('check_gr_no/<int:gr_no>/<int:student_id_pk>', views.check_gr_no, name='check_gr_no'),

    # path('edit_module_manager/<int:pk>',views.edit_module_manager,name='edit_module_manager'),
    # path('delete_module',views.delete_module,name='delete_module'),

]
