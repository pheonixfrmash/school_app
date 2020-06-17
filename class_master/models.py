from django.db import models
from users.models import UserProfile
from school.models import School
from django.utils.translation import ugettext_lazy as _
from teacher.models import Teacher

# Create your models here.
class class_master(models.Model):
    class_name = models.CharField(max_length=150)
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    desc = models.CharField(max_length=255)
    updated_by = models.ForeignKey(UserProfile,on_delete=models.PROTECT)
    def __int__(self):
        return self.pk

class school_class_mapping(models.Model):
    class_id=models.ForeignKey(class_master, on_delete=models.CASCADE)
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    school_id = models.ForeignKey(School,on_delete=models.CASCADE)
    def __int__(self):
        return self.pk


