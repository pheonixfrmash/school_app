from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from attendance import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('',views.list_attendance,name='attendance'),
    path('add',views.mark_attn,name='attendance_add'),
    path('save_attendance/',views.save_attendance,name='save_attendance')
]