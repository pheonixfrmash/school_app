from django.db import models
from city.models import City
from state.models import State
from country.models import Country
from board.models import Board
from medium.models import Medium
from school.models import School
from class_master.models import class_master


# Create your models here.
class Competitive_Exam_Master(models.Model):
    exam_name = models.CharField(max_length=100)
    exam_description = models.TextField(max_length=1000)
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField()
    last_date = models.DateTimeField()
    exam_date = models.DateTimeField()
    def __str__(self):
        return self.exam_name
    

class Competitive_Exam_Transaction(models.Model):
    competitive_exam = models.ForeignKey(Competitive_Exam_Master,on_delete=models.PROTECT)
    exam_school = models.ForeignKey(School,on_delete=models.PROTECT,null=True,blank=True)
    exam_class= models.ForeignKey(class_master,on_delete=models.PROTECT,null=True,blank=True)
    exam_amount= models.CharField(max_length=100,null=True,blank=True)
    exam_tax= models.CharField(max_length=100,null=True,blank=True)
    exam_total_amount=models.CharField(max_length=100,null=True,blank=True)
    paid_by=models.CharField(max_length=100,null=True,blank=True)
    status  = models.BooleanField(default=True)
    confirm_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    request_data=models.CharField(max_length=1000,null=True,blank=True)
    def __str__(self):
        return str(self.competitive_exam)