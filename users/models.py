from django.db import models
from django.contrib.auth.models import User,Group
import datetime
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User as Usertest
from school.models import School


def get_image_filename(instance,filename):
    user_id=instance.user.id
    return 'media/'+str(user_id)+'/'+str(filename)

gender_choices = (
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
        )   
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    secondary_first_name = models.CharField(max_length=255,blank=True,null=True)
    secondary_middle_name = models.CharField(max_length=255,blank=True,null=True)
    secondary_last_name = models.CharField(max_length=255,blank=True,null=True)
    secondary_mobile_no = models.CharField(max_length=15,blank=True,null=True)
    secondary_email_id = models.CharField(max_length=50, blank=True, null=True)
    user_photo = models.ImageField(upload_to=get_image_filename,blank=True)
    gender = models.CharField(max_length=10,choices=gender_choices,blank=True,null=True)
    designation = models.CharField(max_length=100,blank=True,null=True)
    status  = models.BooleanField(default=True,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fcm_id = models.CharField(max_length=255,blank=True,null=True)
    otp = models.CharField(max_length=100,blank=True,null=True)
    school_id = models.ForeignKey(School,on_delete=models.PROTECT,blank=True,null=True) 
    date_of_birth = models.DateField(blank=True,null=True)
    def __str__(self):
        return str(self.user)



class UserRoleMapping(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
