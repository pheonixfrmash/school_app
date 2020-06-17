from django.db import models
from django.contrib.auth.models import User,Group
import datetime
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User as Usertest



class Role_Mapping(models.Model):
    role_id = models.CharField(max_length = 255)
    action_id = models.CharField(max_length = 255,null=True, blank=True)
    module_id = models.CharField(max_length = 255,null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.module_id


