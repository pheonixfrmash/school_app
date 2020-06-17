from django.db import models
from django.contrib.auth.models import User,Group
import datetime
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User as Usertest



class Master(models.Model):
    module_name = models.CharField(max_length = 255)
    module_name_constant = models.CharField(max_length = 255,null=True, blank=True)
    menu_order = models.CharField(max_length = 255,null=True, blank=True)
    module_description = models.CharField(max_length = 255,null=True, blank=True)
    module_path = models.CharField(max_length = 150,null=True, blank=True)
    module_icon = models.CharField(max_length = 150,null=True, blank=True)
    action_item = models.CharField(max_length = 150,null=True, blank=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.module_name


class Action(models.Model):
    action_name = models.CharField(max_length = 255,null=True, blank=True)
    action_description = models.CharField(max_length = 255,null=True, blank=True)
    action_url = models.CharField(max_length = 255,null=True, blank=True)
    module = models.ForeignKey(Master, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.action_name