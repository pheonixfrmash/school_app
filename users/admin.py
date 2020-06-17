from django.contrib import admin
from users.models import UserProfile,UserRoleMapping

admin.site.register(UserProfile)
admin.site.register(UserRoleMapping)
