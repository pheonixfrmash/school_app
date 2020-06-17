from django.db import models
from school.models import School
from users.models import UserProfile
from bank.models import Bank
from class_master.models import class_master
from division.models import Division
from student.models import Student
# Create your models here.
class Fees(models.Model):
    title = models.CharField(max_length=200,default='')
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    school_id = models.ForeignKey(School,on_delete=models.PROTECT)
    posted_by = models.ForeignKey(UserProfile,on_delete=models.PROTECT)
    description = models.CharField(max_length=200)
    bank_id =models.ForeignKey(Bank,on_delete=models.PROTECT)
    def __str__(self):
        return self.title

class Fees_allocation(models.Model):
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fees_id = models.ForeignKey(Fees,on_delete=models.PROTECT)
    class_id = models.ForeignKey(class_master,on_delete=models.PROTECT)
    amount = models.FloatField(max_length=50)
    due_date = models.DateField()
    division_id = models.ForeignKey(Division,on_delete=models.PROTECT)
    def __int__(self):
        return self.pk

class Fees_transaction(models.Model):
    fees_id = models.ForeignKey(Fees, on_delete=models.PROTECT)
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    school_id = models.ForeignKey(School,on_delete=models.PROTECT)
    class_id = models.ForeignKey(class_master,on_delete=models.PROTECT)
    student_id = models.ForeignKey(Student,on_delete=models.PROTECT) 
    paid_date = models.DateField()
    transaction_request = models.CharField(max_length=255)
    transaction_response = models.CharField(max_length=255)
    transaction_amount = models.FloatField(max_length=50)
    def __str__(self):
        return self.transaction_response
