from django.db import models
from school.models import School
# Create your models here.
class Bank(models.Model):
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bank_name = models.CharField(max_length=255)
    school_id = models.ForeignKey(School,on_delete=models.PROTECT)
    ifsc_code = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=100) 