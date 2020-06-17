from django.db import models
from city.models import City
from state.models import State
from country.models import Country
from board.models import Board
from medium.models import Medium
commision_choices=(('fixed','Fixed'),
	('percentage','Percentage'))
# Create your models here.
def get_image_filename(instance,filename):
    print(instance)
    input()
    user_id=instance.user.id
    print(user_id)
    print('media/'+str(user_id)+'/'+str(filename))
    input()
    return 'media/'+str(user_id)+'/'+str(filename)
class School(models.Model):
    school_name = models.CharField(max_length=100)
    school_address = models.CharField(max_length=255)
    class_label = models.CharField(max_length=100,null=True,blank=True)
    division_label = models.CharField(max_length=255,null=True,blank=True)
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    school_city = models.ForeignKey(City,on_delete=models.PROTECT)
    school_board = models.ForeignKey(Board,on_delete=models.PROTECT)
    school_medium = models.ForeignKey(Medium,on_delete=models.PROTECT)
    school_label = models.CharField(max_length=100)
    school_country = models.ForeignKey(Country,on_delete=models.PROTECT)
    pincode = models.CharField(max_length=12)
    dias_number = models.CharField(max_length=50)
    school_logo = models.FileField(upload_to='media/school/',blank=True)
    about_school = models.TextField(max_length=1000)
    iml_school_code = models.CharField(max_length=100)
    school_state = models.ForeignKey(State,on_delete=models.PROTECT)
    commission_type = models.CharField(max_length=50,choices=commision_choices)
    commission_value = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=50)
    def __str__(self):
        return self.id