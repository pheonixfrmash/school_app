from django.db import models
from users.models import UserProfile
from school.models import School
from class_master.models import *
from django.utils.translation import ugettext_lazy as _
from student.models import Student
from teacher.models import Teacher
# Create your models here.
class Division(models.Model):
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    division_name = models.CharField(max_length=255)
    division_desc = models.CharField(max_length=255)
    created_by = models.ForeignKey(UserProfile,on_delete=models.PROTECT)
    school_id = models.ForeignKey(School,on_delete=models.PROTECT)

class school_division_mapping(models.Model):
    class_id=models.ForeignKey(class_master,  on_delete=models.CASCADE)
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)
    division_id = models.ForeignKey(Division,  on_delete=models.CASCADE)


class student_class_mapping(models.Model):
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    school_division = models.ForeignKey(school_division_mapping,on_delete=models.PROTECT)
    student = models.ForeignKey(Student, verbose_name=_("student_id"), on_delete=models.CASCADE) 

class teacher_class_mapping(models.Model):
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    school_division = models.ForeignKey(school_division_mapping,on_delete=models.CASCADE)
    class_teacher = models.ForeignKey(Teacher, verbose_name=_("teacher_id"), on_delete=models.CASCADE)
    co_ordinator =  models.ForeignKey(UserProfile,on_delete=models.PROTECT)