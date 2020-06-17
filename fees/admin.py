from django.contrib import admin
from .models import Fees,Fees_transaction,Fees_allocation
# Register your models here.
admin.site.register(Fees)
admin.site.register(Fees_transaction)
admin.site.register(Fees_allocation)
