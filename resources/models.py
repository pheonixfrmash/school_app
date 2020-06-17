from django.db import models
from django.utils.translation import ugettext_lazy as _
from class_master.models import class_master
from country.models import Country as country
from school.models import School as school
from city.models import City as city
from board.models import Board as board
from medium.models import Medium as medium
from state.models import State as state
from division.models import Division as division
from subject.models import Subject as subject
from users.models import User,UserProfile
import os
#from jsonfield import JSONField
# Create your models here.


class content_type(models.Model):
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_type = models.CharField(max_length=100)
    def __int__(self):
      return self.content_type  

class resource(models.Model):
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(verbose_name=_("resource_title"),max_length=150)
    description = models.CharField(verbose_name=_("resource_description"),max_length=1000)
    file_media = models.FileField(verbose_name=_("resource_file"), upload_to='media/resources/', max_length=100)
    content_type = models.ForeignKey(content_type,on_delete=models.PROTECT)
    def __int__(self):
       return self.pk

class admin(models.Model):
    resource = models.ForeignKey(resource,  on_delete=models.PROTECT,null=True)
    class_master = models.ForeignKey(class_master,on_delete=models.PROTECT, default=None,blank=True,null=True,related_name='class_master')
    school = models.ForeignKey(school,on_delete=models.PROTECT,default=None,blank=True,null=True,related_name='school')
    division_master = models.ManyToManyField(division,default=None,blank=True,null=True,related_name='division')
    subject_master = models.ManyToManyField(subject,verbose_name=_("subject_id"),blank=True,null=True,default=None,related_name='subject')
    resource_data  = models.CharField(max_length=20000,null=True)
    uploaded_by = models.ForeignKey(User,  on_delete=models.PROTECT)
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __int__(self):
        return self.pk