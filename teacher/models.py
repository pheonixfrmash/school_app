from django.db import models
from school.models import School
from django.utils.translation import ugettext_lazy as _
from users.models import UserProfile

# Create your models here.
class Teacher(models.Model):
    status     = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name       = models.CharField(max_length=100)
    dob        = models.DateField()
    address    = models.CharField(max_length=1000,default=None) 
    school_id = models.ForeignKey(School,on_delete=models.PROTECT)
    is_classteacher = models.BooleanField(default = False)
    user       = models.ForeignKey(UserProfile,on_delete=models.PROTECT,default=None)
