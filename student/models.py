from django.db import models
from class_master.models import class_master
from school.models import School
from users.models import UserProfile,User
from city.models import City
from state.models import State
from country.models import Country
from django.utils.translation import ugettext_lazy as _

gender_choices = (
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
        )
# Create your models here.
class Student(models.Model):
   class_name = models.ForeignKey(class_master,on_delete=models.PROTECT,null=True,blank=True)
   division = models.CharField(max_length=10, null=False, blank=False)
   school = models.ForeignKey(School,on_delete=models.PROTECT,null=True,blank=True)
   first_name = models.CharField(max_length=255)
   status  = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   last_name = models.CharField(max_length=255)
   middle_name = models.CharField(max_length=255)
   parent= models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)
   profile_picture = models.FileField(verbose_name=_("profile_pic"), upload_to='media/profile/', max_length=100,blank=True,null=True)
   gender =  models.CharField(max_length=10,choices=gender_choices)
   date_of_birth = models.DateField(blank=True, null=True)
   roll_number = models.IntegerField()
   gr_number = models.IntegerField()
   student_address = models.CharField(max_length=255)
   pincode = models.CharField(max_length=10)
   student_city = models.ForeignKey(City, on_delete=models.PROTECT)
   student_country = models.ForeignKey(Country, on_delete=models.PROTECT)
   student_state = models.ForeignKey(State, on_delete=models.PROTECT)