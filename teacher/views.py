from django.shortcuts import render,redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from division.forms import DocumentForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from teacher.models import Teacher as teacher
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from rest_framework.response import Response
import json
import os
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from state import models as state_models
from country import models as country_models
from city import models as city_models
from board import models as board_models
from medium.models import Medium as medium_models
from school.models import School as school_models
from class_master.models import class_master as class_models
from advertisement.models import Ad_position
from bank import models as bank_models
from users import models as user_models
from operator import itemgetter
import xlwt
import datetime
from django.http import HttpResponse
import re
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404
# Create your views here.

@csrf_exempt
def get_country():
        conutry_data=[]
        state_list=country_models.Country.objects.all().values_list('id', 'country_name')
        for i in state_list:
            case2 = {'id': i[0], 'name': i[1].capitalize()}
            conutry_data.append(case2)
        conutry_data=sorted(conutry_data, key=itemgetter('name'))
        return conutry_data

@csrf_exempt
def get_state():
        state_data=[]
        state_list=state_models.State.objects.all().values_list('id', 'state_name')
     
        for i in state_list:
            case2 = {'id': i[0], 'name': i[1].capitalize()}
            state_data.append(case2)
        state_data=sorted(state_data, key=itemgetter('name'))
        return state_data


@csrf_exempt
def get_city():
        city_data=[]
        city_list=city_models.City.objects.all().values_list('id', 'city_name')

        for i in city_list:
            case2 = {'id': i[0], 'name': i[1]}
            city_data.append(case2)
        return city_data

@csrf_exempt
def get_board():
        board_data=[]
        board_list=board_models.Board.objects.all().values_list('id', 'board_name')
        for i in board_list:
            case2 = {'id': i[0], 'name': i[1]}
            board_data.append(case2)
        return board_data

@csrf_exempt
def get_medium():
        medium_data=[]
        medium_list=medium_models.objects.all().values_list('id', 'medium_name')
        for i in medium_list:
            case2 = {'id': i[0], 'name': i[1]}
            medium_data.append(case2)
        return medium_data

@csrf_exempt
def get_schools():
        school_data=[]
        school_list=school_models.objects.all().values_list('id', 'school_name')
    
        for i in school_list:
            case2 = {'id': i[0], 'name': i[1]}
            school_data.append(case2)
        return school_data

@csrf_exempt
def get_class():
        class_data=[]
        class_list=class_models.objects.all().values_list('id', 'class_name')

        for i in class_list:
            case2 = {'id': i[0], 'name': i[1]}
            class_data.append(case2)
        return class_data


@login_required
def list_teachers_data(request):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('teacher.view_teacher'):
        data=[]
        school_data=get_schools
        class_data= get_class
        state_data= get_state
        city_data= get_city
        country_data= get_country 
        board_data= get_board
        medium_data= get_medium
        user_id = user_models.User.objects.get(username=str(request.user))
        school_id = user_models.UserProfile.objects.get(user=user_id.id)
        count=1
        if request.method == 'GET':
            teacher_list = teacher.objects.filter(school_id=school_id.school_id)
            for div in teacher_list:
              teacher_desc=''
              ad_id=div.id
              teacher_name = div.name
              user_details=user_models.UserProfile.objects.filter(school_id=school_id.school_id,user__first_name=teacher_name,date_of_birth=div.dob).values_list('user')
              teacher_desc=user_models.User.objects.filter(pk=user_details[0][0]).values_list('username')
              teacher_dob = div.dob
              timestampStr = teacher_dob.strftime("%d-%b-%Y")
              teacher_address=div.address
              teacher_status = 'Active' if str(div.status)=='True' else 'Inactive'
              teacher_email=user_models.User.objects.filter(username=str(teacher_desc[0][0])).values_list('email')
              posted_date = div.created_at
              resource_posted_date = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', str(posted_date.date()))
              Edit='<div class="btn-group"><form class="span4 text-left" action="/teacher/edit/'+str(ad_id)+'" method="POST"><button style="margin:5px" class="btn btn-primary"><i class="fas fa-edit"></i> Edit</button></form>'
              View='<form class="span4 text-center" action="/teacher/details/'+str(ad_id)+'" method="POST"><button style="margin:5px" class="btn btn-primary"><i class="fas fa-eye"></i>View</button></form>'
              Delete='<form action="/module_manager/edit_module_manager/21" method="get"><button style="margin:5px" type="button" class="btn btn-primary"><i class="far fa-trash-alt"></i>Delete</button></form></div>'
              actions = Edit          
              serialised_data = [count,teacher_name,teacher_desc[0][0],teacher_email[0][0],timestampStr,teacher_address,teacher_status,actions]
              data.append(serialised_data)
              count+=1
            context = {'data': data,"country_data":country_data ,"state_data":state_data,"city_data":city_data,'board_data':board_data,'medium_data':medium_data,'school_data':school_data,'class_data':class_data }
            template = 'teacher_list.html'
            return render(request,template,context)
        else:
            response=JsonResponse({'status':'error','msg':'Bad Request'})
            return response
     else:
        return render(request,'forbidden_page.html')
    
@login_required
def download_excel_data(request):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('teacher.view_teacher'):
        # content-type of response
        response = HttpResponse(content_type='application/ms-excel')

        #decide file name
        response['Content-Disposition'] = 'attachment; filename="teacher_master.xls"'

        #creating workbook
        wb = xlwt.Workbook(encoding='utf-8')

        #adding sheet
        ws = wb.add_sheet("teacher")

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        # headers are bold
        font_style.font.bold = True

        #column header names, you can use your own headers here
        columns = ['Sr.No','Name', 'Mobile Number', 'Email Id', 'Date of Birth', 'Address' ]

        #write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        #get your data, from database or from a text file...
        data = teacher.list_teachers_data(request) #dummy method to fetch data.
        for my_row in data:
            row_num = row_num + 1
            ws.write(row_num, 0, str(row_num), font_style)
            ws.write(row_num, 1, my_row['teacher_name'], font_style)
            ws.write(row_num, 2, my_row['teacher_desc'], font_style)
            ws.write(row_num, 3, user_models.User.objects.get(pk=user_models.UserProfile.objects.get(pk=my_row['created_by']).user_id).first_name, font_style)
            ws.write(row_num, 4, my_row['created_at'], font_style)
        wb.save(response)
        return response
     else:
        return render(request,'forbidden_page.html')
    
@login_required
def send_file(request):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('teacher.add_teacher'):
        file_path="/home/oem/Downloads/sample_teacher.xlsx"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
     else:
        return render(request,'forbidden_page.html')

@login_required
@transaction.atomic
def teacher_upload(request):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('teacher.add_teacher'):
        user_id = user_models.User.objects.get(username=str(request.user))
        userprofile_id = user_models.UserProfile.objects.filter(user=user_id.id)
        school = user_models.UserProfile.objects.filter(user=user_id.id).values_list('school_id')
        school_details = school_models.objects.get(pk=school[0][0])
        template = "add_teacher_excel.html"
        response=''
        if request.method =='GET':
            return render(request, template)

        xlsx_file = request.FILES['file']
        if not xlsx_file.name.endswith('.xlsx'):
            response=JsonResponse({'status':'error','msg':"Please upload a xlsx file"})
            return response

        # data_set = csv_file.read().decode('UTF-8')
        # io_string =io.StringIO(data_set)
        # next(io_string)
        count1=0
        userData=[]
        corrected_data=[]
        user_count=[]
        teacher_count=[]
        user_profile_count=[]
        import pandas as pd
        from pandas import ExcelWriter
        from pandas import ExcelFile
        import math
        
        df = pd.read_excel(xlsx_file)
        if ('Name' in df.columns) and ('Mobile Number' in df.columns) and ('Email Id' in df.columns) and ('Date of Birth' in df.columns) and ('Address' in df.columns):

            for i in df.index:
                teacher_name        = df['Name'][i]
                teacher_mobile      = df['Mobile Number'][i]
                teacher_email       = df['Email Id'][i]
                teacher_dob         = df['Date of Birth'][i]
                teacher_address     = df['Address'][i]
                userData.append([teacher_name,teacher_mobile,teacher_email,teacher_dob,teacher_address])

        else:
            response=JsonResponse({'status':'error','msg':"Please check excel columns"})
            return response
        duplicated_names       = df[df.duplicated(['Mobile Number'])]
        if(duplicated_names.empty==False):
            response = JsonResponse(
                    {'status': 'error', 'msg': "Teacher with mobile number at the following records already exists:" + duplicated_names['Mobile Number'].to_string() + ""})
            return response
        for i in userData:
            count1+=1
            teacher_name        = i[0]
            teacher_mobile      = i[1]
            teacher_email       = i[2]
            teacher_dob         = i[3]
            teacher_address     = i[4]
            if len(str(teacher_name))==0:
                response=JsonResponse({'status':'error','msg':"Please Enter Name At Row: "+str(count1)+""})
                return response
            if len(str(teacher_mobile)) < 10:
                response=JsonResponse({'status':'error','msg':"Please Enter Valid number At Row: "+str(count1)+""})
                return response
            teacher_user=user_models.User.objects.filter(username=teacher_mobile)
            user_profile=user_models.UserProfile.objects.filter(user=teacher_user[0].id,school_id=school_details)
            teacher_school=teacher.objects.filter(user=user_profile[0].id,school_id=school_details)
            if teacher_school.exists():
              if count1==1: 
                response=JsonResponse({'status':'error','msg':"Teacher at Row: "+str(count1)+" already exists"})
                return response
              else:
                teacher.objects.filter(pk__in=teacher_count).delete()
                user_models.UserProfile.objects.filter(pk__in=user_profile_count).delete()
                user_models.User.objects.filter(pk__in=user_count).delete()
                response=JsonResponse({'status':'error','msg':"Teacher at Row: "+str(count1)+" already exists"})
                return response
            else:        
                new_user = user_models.User.objects.create(username=teacher_mobile,first_name=teacher_name, is_active=1, email=teacher_email)
                new_user.save()
                user_count.append(new_user.id)
                userprofile = user_models.UserProfile.objects.create(user=new_user,school_id=school_details,date_of_birth=teacher_dob)
                userprofile.save()
                user_profile_count.append(userprofile.id)
                new_teacher  = teacher.objects.create(name=teacher_name,school_id=school_details,dob=teacher_dob,address=teacher_address,user_id=userprofile.id)
                new_teacher.save()
                teacher_count.append(new_teacher.id)        
        response=JsonResponse({'status':'success','msg':" "+str(count1)+" "+"Teachers Added Successfully"})
        return response
     else:
        return render(request,'forbidden_page.html')
@login_required
def edit_teacher(request,id):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('teacher.change_teacher'):
        try:
         div = teacher.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            ad_id=div.id
            teacher_name=div.name
            user_id = user_models.User.objects.get(username=str(request.user))
            school_id = user_models.UserProfile.objects.get(user=user_id.id)
            user_details=user_models.UserProfile.objects.filter(pk=div.user.id).values_list('user')
            teacher_desc=user_models.User.objects.filter(pk=user_details[0][0]).values_list('username','email')
            division_desc = teacher_desc[0][0]
            teacher_email = teacher_desc[0][1]
            teacher_status = 'Active' if str(div.status)=='True' else 'Inactive'
            serialised_data = {'ad_id':ad_id,'division_name':div.name,'division_desc':division_desc,'teacher_email':teacher_email,'teacher_dob':str(div.dob),'teacher_status':teacher_status,'teacher_address':div.address}
            return render(request,'edit_teacher.html',{'data':serialised_data})
        else:
            response=JsonResponse({'status':'error','msg':"Bad Request"})
            return response
     else:
        return render(request,'forbidden_page.html')
@login_required
def view_teacher(request,id):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('teacher.view_teacher'):
        try:
         div = teacher.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            ad_id=div.id
            teacher_name=div.name
            user_id = user_models.User.objects.get(username=str(request.user))
            school_id = user_models.UserProfile.objects.get(user=user_id.id)
            user_details=user_models.UserProfile.objects.filter(pk=div.user.id).values_list('user')
            teacher_desc=user_models.User.objects.filter(pk=user_details[0][0]).values_list('username','email')
            division_desc = teacher_desc[0][0]
            teacher_email = teacher_desc[0][1]
            teacher_status = 'Active' if str(div.status)=='True' else 'Inactive'
            serialised_data = {'ad_id':ad_id,'division_name':div.name,'division_desc':division_desc,'teacher_email':teacher_email,'teacher_dob':str(div.dob),'teacher_status':teacher_status,'teacher_address':div.address}
            
            return render(request,'view_teacher.html',{'data':serialised_data})
     else:
        return render(request,'forbidden_page.html')

@login_required    
def save_teacher(request,id):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('teacher.change_teacher'):
        try:
         teachr = teacher.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method =='POST':
            teacher_name=teachr.name
            name    = request.POST.get('teacher_name')
            mobile  = request.POST.get('teacher_mobile')
            email   = request.POST.get('teacher_email')
            dob     = request.POST.get('teacher_dob')
            status  = request.POST.get('teacher_status')
            address = request.POST.get('teacher_address')
            userprofile_id=user_models.UserProfile.objects.filter(school_id=teachr.school_id,user__first_name=teacher_name,date_of_birth=teachr.dob).values_list('user')
            teacher_desc=user_models.User.objects.filter(pk=userprofile_id[0][0]).values_list('username','email')
            teacher_mobile = teacher_desc[0][0]
            teacher_email = teacher_desc[0][1]
            if teacher_email!=email:
             user_details=user_models.User.objects.filter(pk=userprofile_id[0][0]).update(email=email)
            if teacher_mobile!=mobile:
             try:
                user_models.User.objects.get(username=mobile)
                response=JsonResponse({'status':'error','msg':'User already exists'})
                return response
             except ObjectDoesNotExist:
              user_details=user_models.User.objects.filter(pk=userprofile_id[0][0]).update(username=mobile)
            if teachr.dob!=dob:
                user_models.UserProfile.objects.filter(user=userprofile_id[0][0]).update(date_of_birth=dob)
            if (status=='Active'):
                status=True
            else:
                status=False               
            teacher_update=teacher.objects.filter(pk=teachr.id).update(name= name ,dob=dob,address=address,status=status)
            response=JsonResponse({'status':'success'})
            return response
        else:
           response=JsonResponse({'status':'fail','error':'Invalid Request'})
           return response
     else:
        return render(request,'forbidden_page.html')
