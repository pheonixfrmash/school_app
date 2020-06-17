from django.db import models

# Create your models here.
class Medium(models.Model):
    medium_name = models.CharField(max_length=150)
    medium_code = models.CharField(max_length=100)
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)