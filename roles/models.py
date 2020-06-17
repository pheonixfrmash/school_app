from django.db import models
from django.contrib.auth.models import User,Group
import datetime
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User as Usertest
from school.models import School


class SchoolRoleMapping(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE,default=None,blank=True,null=True)
    status  = models.BooleanField(default=True)
    posted_by=models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
