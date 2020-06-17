from django.contrib import admin
from .models import admin as admin_resources,resource,content_type
# Register your models here.
admin.site.register(admin_resources)
admin.site.register(resource)
admin.site.register(content_type)

