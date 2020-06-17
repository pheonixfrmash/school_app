from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from resources.forms import adminForm, resourceForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from resources.models import admin, resource
from rest_framework.views import APIView
from django.utils import timezone
from resources.serializer import adminSerializer
import json
import re
from django.core.exceptions import ObjectDoesNotExist
from resources.models import admin, resource, content_type
from state import models as state_models
from country import models as country_models
from city import models as city_models
from board.models import Board as board_models
from medium.models import Medium as medium_models
from school import models as school_models
from class_master import models as class_models
from division.models import Division as division_models
from teacher.models import Teacher as teacher
from users.models import UserProfile,User
from subject.models import Subject
from bank import models as bank_models
from users import models as user_models
from rest_framework import status
from operator import itemgetter
from django.template.defaulttags import register
from division import models as division
from student import models as student
from attendance.models import Attendance as attendance
from django.db.models.functions import Trunc
from datetime import datetime 

# Create your views here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@csrf_exempt
def get_division_old(school_id):
    division_data = []
    division_list = division_models.objects.filter(school_id=school_id).values_list('id', 'division_name')
    for i in division_list:
        case2 = {'id': i[0], 'name': i[1].capitalize()}
        division_data.append(case2)
    division_data = sorted(division_data, key=itemgetter('name'))
    return division_data

@csrf_exempt
def get_division(school_id,division_id):
    division_data = []
    print(division_id)
    division_list = division.school_division_mapping.objects.filter(division_id=division_id).values_list('division_id__id','division_id__division_name','class_id__id')
    for i in division_list:
        case2 = {'id': i[0], 'name': i[1].capitalize(),'class_id':i[2]}
        division_data.append(case2)
    division_data = sorted(division_data, key=itemgetter('name'))
    return division_data

@csrf_exempt
def get_class(school_id,class_id):
    class_data = []
    class_list = class_models.class_master.objects.filter(pk=class_id).values_list('id', 'class_name')
    print(class_list)
    for i in class_list:
        case2 = {'id': i[0], 'name': i[1]}
        class_data.append(case2)
    return class_data

@login_required
@permission_required('attendance.add_attendance', raise_exception=True)
def mark_attn(request):
  if request.method == 'GET': 
    student_list=[]
    request_user_profile=User.objects.filter(username=str(request.user))
    request_user=UserProfile.objects.filter(user=request_user_profile[0].id)
    pr = teacher.objects.filter(user = (request_user[0].id))
    class_division=division.teacher_class_mapping.objects.filter(class_teacher=(pr[0].id))
    print(class_division)
    print(class_division[0].school_division.id)
    list_of_studentid = division.student_class_mapping.objects.filter(school_division=class_division[0].school_division.id)
    print(list_of_studentid[0].id)
    list_of_students= student.Student.objects.filter(pk__in=list_of_studentid).values_list('id','first_name','last_name')
    print(list_of_students)
    for i in list_of_students:
        case2 = {'id': i[0], 'name': str(i[1]+" "+i[2])}
        student_list.append(case2)
    return render(request, 'markattd.html', {'list':student_list})
  else:
     response=JsonResponse({'status': 'error', 'msg': 'Bad Request'})
     return response

@login_required
def save_attendance(request):
  if request.method=='POST':
     all_students=[]
     student_list=request.POST.getlist('students')
     date = request.POST.get('attd_date') 
     request_user_profile=User.objects.filter(username=str(request.user))
     request_user=UserProfile.objects.filter(user=request_user_profile[0].id)
     pr = teacher.objects.filter(user = (request_user[0].id))
     class_division=division.teacher_class_mapping.objects.filter(class_teacher=(pr[0].id))
     list_of_studentid = division.student_class_mapping.objects.filter(school_division=class_division[0].school_division.id)

     list_of_students= student.Student.objects.filter(pk__in=list_of_studentid).values_list('id')
     print(list_of_students)
     for i in list_of_students:
         all_students.append(i[0])
     school_division=division.school_division_mapping.objects.filter(pk=class_division[0].school_division.id)
     for i in all_students:
       student_id=student.Student.objects.filter(pk=i)
       if (str(i) in student_list):
        new_attd=attendance.objects.create(date=date,student_id=student_id[0],school_division=school_division[0],teacher_id=pr[0],is_present=1)
       else:
        new_attd=attendance.objects.create(date=date,student_id=student_id[0],school_division=school_division[0],teacher_id=pr[0],is_present=0)
     response=JsonResponse({'status': 'success', 'msg': 'Attendance added sucessfully'})
     return response

@login_required
# @permission_required('attendance.view_attendance', raise_exception=True)
def list_attendance(request):
  user=user_models.User.objects.get(username=request.user.username)
  request_user_profile=User.objects.filter(username=str(request.user))

  if user.has_perm('attendance.view_attendance'):
    data = []
    group_list=[]
    ob = admin()
    resource_list = {}
    count = 1
    request_user_profile=User.objects.filter(username=str(request.user))
    request_user=UserProfile.objects.filter(user=request_user_profile[0].id)
    user_group = request.user.groups.values_list('name', flat=True)
    if 'role' in request.session:
     roles_used = request.session['role']
    print(user_group)
    for i in user_group:
        print(i)
        j=i.split('-',2)
        print(j[0])
        group_list.append(j[0])
    print(request_user_profile[0].username)
    if (roles_used=="Parent"):
      pr=request_user_profile
      class_id=student.Student.objects.filter(parent=pr[0].id).values_list('class_name','division','id')
      class_details=class_id[0][0]
      division_details=class_id[0][1]
      student_id=class_id[0][2]
    else:
      pr = teacher.objects.filter(user = (request_user[0].id))
      class_division=division.teacher_class_mapping.objects.filter(class_teacher=(pr[0].id))
      print(class_division)
      print(class_division[0].school_division.id)
      division_id=division.school_division_mapping.objects.filter(pk=class_division[0].school_division.id)
      division_details=division_id[0].division_id.id
      class_details=division_id[0].class_id.id
    school_id=UserProfile.objects.filter(user=request_user_profile[0].id).values_list('school_id')
    print(school_id)
    class_list = get_class(school_id[0][0],class_details)
    division_list = get_division(school_id[0][0],division_details) 
    if request.method == 'GET':
        print("call122222")
        context = {'data':data,'class_list':class_list,'division_list':division_list}
        template = 'attendance_list.html'
        return render(request, template, context)

    else:
        date_list=[]
        student_names=[]
        class_lists=request.POST.get('class_list')
        division_lists=request.POST.get('division_list')
        start_date = request.POST.get('start_date')
        end_date   = request.POST.get('end_date')
        # roles_used = request.POST.get('roles')

        print(roles_used)
        print(class_lists)
        print(division_lists)
        print(start_date)
        print(end_date)
        class_id=class_models.class_master.objects.filter(pk=class_lists)
        print(class_id)
        division_id=division.Division.objects.filter(pk=division_lists)
        print(division_id)
        print(class_id[0])
        print(division_id[0])
        print(school_id[0])
        # print(school_id[0][0])
        school_division=division.school_division_mapping.objects.filter(class_id=class_id[0],division_id=division_id[0],school_id=school_id[0][0])
        
        if ((roles_used=="Parent") and (school_division)):
          
            student_group= attendance.objects.filter(date__range=(start_date, end_date),school_division=school_division[0],student_id=student_id).values_list('student_id').distinct()
        elif school_division:
            student_group= attendance.objects.filter(date__range=(start_date, end_date),school_division=school_division[0]).values_list('student_id').distinct()
        else:
           response=JsonResponse({'status': 'error', 'msg': 'Class division combination doesnt exist'})
           return response
        dates_list=["Sr No","Roll Number","Student Name"]
        if student_group:
         for students in student_group:
             students_list=attendance.objects.filter(date__range=(start_date, end_date),school_division=school_division[0]).filter(student_id=students[0]).order_by('date')

             serialised_data=[]
             student_details=student.Student.objects.filter(pk=students[0])
             student_name=student_details[0].first_name+" "+student_details[0].last_name
             serialised_data.append(count)
             serialised_data.append(student_details[0].roll_number)
             student_names=student_name
             serialised_data.append(student_names)
             attendance_status=[]
             for i in students_list:
                present_status=('Present' if i.is_present  else 'Absent')
                date_list.append(str(i.date))
                attendance_status.append(present_status)
             count = count + 1
             serialised_data.extend(attendance_status)
             data.append(serialised_data)
         dates_list.extend(date_list[-(len(attendance_status)):])
        else:
           response=JsonResponse({'status': 'error', 'msg': 'Attendance for the selected period doesnot exist'})
           return response
    context = {'data': data,'student_list':student_names,'date_list':dates_list,'class_list':class_list,'division_list':division_list,'attdate':start_date,'enddate':end_date,'class_lists':class_lists,'division':division_id[0].division_name}
    template = 'attendance_list.html'
    return render(request, template, context)

  else:
        return render(request,'forbidden_page.html')



