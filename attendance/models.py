from django.db import models
from division.models import school_division_mapping
from student.models import Student
from teacher.models import Teacher
# Create your models here.
class Attendance(models.Model):
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField()
    school_division = models.ForeignKey(school_division_mapping,on_delete=models.CASCADE,db_constraint=False)
    student_id = models.ForeignKey(Student,on_delete=models.PROTECT,db_constraint=False)
    teacher_id = models.ForeignKey(Teacher,on_delete=models.PROTECT,db_constraint=False)
    is_present = models.BooleanField(default=True)