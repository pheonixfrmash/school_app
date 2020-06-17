from django.db import models
from state.models import State
from city.models import City
from class_master.models import class_master
from school.models import School
from medium.models import Medium
from country.models import Country
from board.models import Board
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class Ad_position(models.Model):
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    position = models.CharField(max_length=150)
    def __int__(self):
        return self.position

class Advertisement(models.Model):
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True,editable=False)
    message = models.CharField(max_length=250)
    ad_name = models.CharField(max_length=150)
    ad_from = models.DateField(verbose_name=_("start_date"), default=None)
    ad_to = models.DateField(verbose_name=_("end_date"), default=None)
    ad_position = models.ForeignKey(Ad_position,on_delete=models.PROTECT,default=None)
    country = models.ForeignKey(Country,on_delete=models.PROTECT,default=None)
    board = models.ForeignKey(Board,on_delete=models.PROTECT,default=None,blank=True,null=True)
    state = models.ForeignKey(State,on_delete=models.PROTECT,default=None,blank=True,null=True)
    city = models.ForeignKey(City,on_delete=models.PROTECT,default=None,blank=True,null=True)
    class_id = models.ForeignKey(class_master,on_delete=models.PROTECT,default=None,blank=True,null=True)
    school_id = models.ForeignKey(School,on_delete=models.PROTECT,default=None,blank=True,null=True)
    school_medium = models.ForeignKey(Medium, on_delete=models.PROTECT,default=None,null=True,blank=True)
    ad_image = models.FileField(verbose_name=_("ad_media"), upload_to='media/advertisements/', max_length=100)
    contact_number = models.CharField(max_length=15)
    contact_name = models.CharField(max_length=100)
    ad_url = models.CharField(max_length=150,blank=True)
    def __int__(self):
        return self.pk

class Ads_report(models.Model):
    ad_id = models.ForeignKey(Advertisement, verbose_name=_("advertisement"), on_delete=models.CASCADE)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    def __int__(self):
       return self.pk