from django.contrib import admin
from django.urls import path,include
from resources.views import Resources
urlpatterns = [
    path('add',Resources.add_resource,name='resource_add'),
    path('details/<id>',Resources.view_resources,name='resource_details'),
    path('edit/<id>',Resources.edit_resources,name='resource_edit'),
    path('',Resources.list_resources,name='resource'),
    path('save_resources/<id>',Resources.save_resources,name='save_resource')
]