from django.db import models
from class_master.models import class_master
from division.models import school_division_mapping
from school.models import School
from teacher.models import Teacher
from django.utils.translation import ugettext_lazy as _
from users.models import UserProfile,User

# Create your models here.

class Subject(models.Model):
    status      = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    name        = models.CharField(max_length=100)
    is_elective = models.BooleanField(default=False)
    school_id   = models.ForeignKey(School,on_delete=models.PROTECT)
    created_by  = models.ForeignKey(UserProfile,on_delete=models.PROTECT)

class Subject_teacher_mapping(models.Model):
    status                  = models.BooleanField(default=True)
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)
    subject                 = models.ForeignKey(Subject, verbose_name=_("subject_id"), on_delete=models.CASCADE,null=True,blank=True)
    teacher                 = models.ForeignKey(Teacher, verbose_name=_("teacher_id"), on_delete=models.CASCADE,null=True,blank=True)
    school_division_mapping = models.ForeignKey(school_division_mapping,verbose_name=_("school_division_mapping"),on_delete=models.CASCADE,blank=True,null=True)


class Class_Cordinator_teacher(models.Model):
    status        = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    class_teacher = models.ForeignKey(Teacher,on_delete=models.PROTECT)
    co_ordinator  = models.ForeignKey(UserProfile,on_delete=models.PROTECT)
    school_division_mapping = models.ForeignKey(school_division_mapping,verbose_name=_("school_division_mapping"),on_delete=models.CASCADE,blank=True,null=True)