from django.contrib import admin

# Register your models here.
from .models import Advertisement,Ad_position,Ads_report
# Register your models here.
admin.site.register(Advertisement)
admin.site.register(Ad_position)
admin.site.register(Ads_report)