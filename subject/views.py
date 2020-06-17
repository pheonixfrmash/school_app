from django.shortcuts import render,redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth.models import Permission
from django.views.decorators.csrf import csrf_exempt
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
from division.models import Division,school_division_mapping
from subject.models import Subject as subject,Subject_teacher_mapping,Class_Cordinator_teacher
from teacher.models import Teacher as teacher
import xlwt
from django.http import HttpResponse
import re
from rest_framework import status
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
def list_subjects_data(request):
    user_id=user_models.User.objects.get(username=request.user.username)
    if user_id.has_perm('subject.view_subject'):
        data=[]
        school_data=get_schools
        class_data=get_class
        state_data=get_state
        city_data=get_city
        country_data=get_country 
        board_data=get_board
        medium_data=get_medium
        ob = subject()

        school_id = user_models.UserProfile.objects.get(user=user_id.id)

        count=1
        if request.method == 'GET':
            subject_list = subject.objects.filter(school_id=school_id.school_id)
            for sub in subject_list:
              ad_id=sub.id
              subject_name = sub.name
              subject_status = 'Active' if str(sub.status)=='True' else 'Inactive'
              posted = subject.objects.filter(pk=sub.id).values_list('created_by')[0][0]
              posted_by=user_models.UserProfile.objects.filter(pk=posted).values_list('user__username')[0][0]
              posted_person=user_models.User.objects.filter(username=str(posted_by)).values_list('first_name')
              posted_date = sub.created_at
              resource_posted_date = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', str(posted_date.date()))
              posted_user = posted_person[0][0]
              subject_elective = 'Elective' if str(sub.is_elective)=='True' else 'Mandatory'
              Edit='<div class="btn-group"><form class="span4 text-left" action="/subject/edit/'+str(ad_id)+'" method="POST"><button style="margin:5px" class="btn btn-primary"><i class="fas fa-edit"></i> Edit</button></form>'
              View='<form class="span4 text-center" action="/subject/details/'+str(ad_id)+'" method="POST"><button style="margin:5px" class="btn btn-primary"><i class="fas fa-eye"></i>View</button></form>'
              Delete='<form action="/module_manager/edit_module_manager/21" method="get"><button style="margin:5px" type="button" class="btn btn-primary"><i class="far fa-trash-alt"></i>Delete</button></form></div>'
              actions = Edit       
              serialised_data = [count,subject_name,subject_status,subject_elective,posted_user,str(resource_posted_date),actions]
              data.append(serialised_data)
              count+=1
            context = {'data': data,"country_data":country_data ,"state_data":state_data,"city_data":city_data,'board_data':board_data,'medium_data':medium_data,'school_data':school_data,'class_data':class_data }
            template = 'subject_list.html'
            return render(request,template,context)
        else:
            response=JsonResponse({'status':'error','msg':'Bad Request'})
            return response
    else:
        return HttpResponse("You can't view this page.")

@login_required
def download_excel_data(request):
        # content-type of response
        response = HttpResponse(content_type='application/ms-excel')

        #decide file name
        response['Content-Disposition'] = 'attachment; filename="division_master.xls"'

        #creating workbook
        wb = xlwt.Workbook(encoding='utf-8')

        #adding sheet
        ws = wb.add_sheet("subject")

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        # headers are bold
        font_style.font.bold = True

        #column header names, you can use your own headers here
        columns = ['Sr.No','Subject Name', 'Subject Status','Subject Elective','Created by', 'Created Date' ]

        #write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        #get your data, from database or from a text file...
        data = Subject.list_subjects_data(request) #dummy method to fetch data.
        print(data)
        for my_row in data:
            row_num = row_num + 1
            ws.write(row_num, 0, str(row_num), font_style)
            ws.write(row_num, 1, my_row['subject_name'], font_style)
            ws.write(row_num, 2, my_row['status'], font_style)
            ws.write(row_num, 3, my_row['is_elective'], font_style)
            ws.write(row_num, 4, user_models.User.objects.get(pk=user_models.UserProfile.objects.get(pk=my_row['created_by']).user_id).first_name, font_style)
            ws.write(row_num, 5, my_row['created_at'], font_style)
        wb.save(response)
        return response
    
@login_required
def send_file(request):
        file_path="/home/oem/Downloads/sample_subject.xlsx"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response

@login_required
def send_file_class_teacher(request):
        file_path="/home/oem/Downloads/sample_class_teacher.xlsx"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response

@login_required
def send_file_subject_teacher(request):
        file_path="/home/oem/Downloads/sample_subject_teacher.xlsx"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response

@login_required
@transaction.atomic
def subject_upload(request):
    user=user_models.User.objects.get(username=request.user.username)
    if user.has_perm('subject.add_subject'):
        user_id = user_models.User.objects.get(username=str(request.user))
        userprofile_id = user_models.UserProfile.objects.filter(user=user_id.id)
        school = user_models.UserProfile.objects.filter(user=user_id.id).values_list('school_id')
        school_details = school_models.objects.get(pk=school[0][0])
        template = "add_subject_excel.html"
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
        import pandas as pd
        from pandas import ExcelWriter
        from pandas import ExcelFile
        import math
        subject_added=[]
        df = pd.read_excel(xlsx_file)
        print(df,'_____________')
        if ('subject_name' in df.columns) and ('status' in df.columns) and ('is_elective' in df.columns):

            for i in df.index:
                subject_name        = df['subject_name'][i]
                subject_status      = df['status'][i]
                subject_elective    = df['is_elective'][i] 
                userData.append([subject_name,subject_status,subject_elective])

        else:
            response=JsonResponse({'status':'error','msg':"Please check excel columns"})
            return response
        duplicated_names       = df[df.duplicated(['subject_name'])]
        if(duplicated_names.empty==False):
            response = JsonResponse(
                    {'status': 'error', 'msg': "Please Correct the below records:" + duplicated_names['subject_name'].to_string() + ""})
            return response
        
        for i in userData:
            count1+=1
            subject_name        = i[0]
            subject_status      = i[1]
            subject_elective    = i[2]
            if len(str(subject_name))==0:
                response=JsonResponse({'status':'error','msg':"Please Enter Subject Name At Row:"+str(count1)+""})
                return response
            if len(str(subject_status))==0:
                response=JsonResponse({'status':'error','msg':"Please Enter Subject status At Row:"+str(count1)+""})
                return response
            if len(str(subject_elective))==0:
                response=JsonResponse({'status':'error','msg':"Please Enter Subject elective At Row:"+str(count1)+""})
                return response
            if subject.objects.filter(name=subject_name,school_id=school_details).exists():
                subject.objects.filter(pk__in=subject_added).delete()
                response=JsonResponse({'status':'error','msg':"Subject "+str(i[0])+" At Row: "+str(count1) +" Already added"})
                return response
            else:
                new_subject  = subject.objects.create(name=subject_name,status=subject_status,is_elective=subject_elective,created_by=userprofile_id[0],school_id=school_details)
                new_subject.save()
                subject_added.append(new_subject.id)
        print(subject_added)      
        response=JsonResponse({'status':'success','msg':" "+str(count1)+" "+"Subjects Added Successfully"})
        return response
    else:
        return render(request,'forbidden_page.html')

@login_required
def edit_subject(request,id):
    user=user_models.User.objects.get(username=request.user.username)
    if user.has_perm('subject.change_subject'):
        print(request)
        print(id)
        try:
         sub = subject.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            ad_id=sub.id
            subject_name=sub.name
            subject_elective = 'Elective' if str(sub.is_elective)=='True' else 'Mandatory'
            subject_status = 'Active' if str(sub.status)=='True' else 'Inactive'
            serialised_data = {'ad_id':ad_id,'subject_name':subject_name,'subject_elective':subject_elective,'subject_status':subject_status}
            
            return render(request,'edit_subject.html',{'data':serialised_data})
        else:
            response=JsonResponse({'status':'error','msg':"Bad Request"})
            return response
    else:
        return render(request,'forbidden_page.html')

@login_required
def view_subject(request,id):
    user=user_models.User.objects.get(username=request.user.username)
    if user.has_perm('subject.view_subject'):
        try:
         sub = subject.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            ad_id=sub.id
            subject_name=sub.name
            subject_elective = 'Elective' if str(sub.is_elective)=='True' else 'Mandatory'
            subject_status = 'Active' if str(sub.status)=='True' else 'Inactive'
            serialised_data = {'ad_id':ad_id,'subject_name':subject_name,'subject_elective':subject_elective,'subject_status':subject_status}
            
            return render(request,'view_subject.html',{'data':serialised_data})
        else:
           response=JsonResponse({'status':'error','error':'Invalid Request'})
           return response
    else:
        return render(request,'forbidden_page.html')

@login_required    
def save_subject(request,id):
        print(request)
        try:
         sub = subject.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method =='POST':
            subject_name = request.POST.get('subject_name')
            subject_status = request.POST.get('subject_status')
            subject_elective = request.POST.get('subject_elective')
            if (subject_status=='Active'):
                subject_status=True
            else:
                subject_status=False
            if (subject_elective=='Elective'):
                subject_elective=True
            else:
                subject_elective=False
            subject.objects.filter(pk=sub.id).update(name= subject_name ,status=subject_status,is_elective=subject_elective)
            response=JsonResponse({'status':'success'})
            return response
        else:
           response=JsonResponse({'status':'error','msg':'Invalid Request'})
           return response


@login_required
@transaction.atomic
def subject_teacher_upload(request):
    user=user_models.User.objects.get(username=request.user.username)
    if user.has_perm('subject.add_subject_teacher'):   
        user_id = user_models.User.objects.get(username=str(request.user))
        userprofile_id = user_models.UserProfile.objects.filter(user=user_id.id)
        school = user_models.UserProfile.objects.filter(user=user_id.id).values_list('school_id')
        school_details = school_models.objects.get(pk=school[0][0])
        template = "add_subject_teacher_mapping.html"
        response = ''
        if request.method =='GET':
            return render(request, template)
        else:    
            xlsx_file = request.FILES['file']
            if not xlsx_file.name.endswith('.xlsx'):
                response=JsonResponse({'status':'error','msg':"Please upload a xlsx file"})
                return response
            count1=1
            userData=[]
            import pandas as pd
            from pandas import ExcelWriter
            from pandas import ExcelFile
            import math
            
            df = pd.read_excel(xlsx_file)
            print(df,'_____________')
            if ('subject_name' in df.columns) and ('status' in df.columns) and ('subject_type' in df.columns) and ('class' in df.columns) and ('division' in df.columns) and ('subject_teacher' in df.columns) and ('mobile_number' in df.columns):

                for i in df.index:
                    subject_name        = df['subject_name'][i]
                    subject_status      = df['status'][i]
                    subject_elective    = df['subject_type'][i]
                    class_master        = df['class'][i] 
                    division_name       = df['division'][i]
                    subject_teacher     = df['subject_teacher'][i]
                    teacher_mobile      = df['mobile_number'][i]
                    userData.append([subject_name,subject_status,subject_elective,class_master,division_name,subject_teacher,teacher_mobile])

            else:
                response=JsonResponse({'status':'error','msg':"Please check excel columns"})
                return response
            duplicated_names       = df[df.duplicated(['subject_name','class','division','subject_teacher','mobile_number'])]
            if(duplicated_names.empty==False):
                response = JsonResponse(
                        {'status': 'error', 'msg': "Please Correct the below records:" + duplicated_names['subject_teacher'].to_string() + ""})
                return response
            for i in userData:
                count1+=1
                subject_name        = i[0]
                subject_status      = i[1]
                subject_elective    = i[2]
                class_name          = i[3]
                division_name       = i[4]
                subject_teacher     = i[5]
                teacher_mobile      = i[6]
                if len(str(subject_name))==0:
                    response=JsonResponse({'status':'error','msg':"Please Enter Subject Name At Row:"+str(count1)+""})
                    return response
                if len(str(subject_status))==0:
                    response=JsonResponse({'status':'error','msg':"Please Enter Subject status At Row:"+str(count1)+""})
                    return response
                if len(str(subject_elective))==0:
                    response=JsonResponse({'status':'error','msg':"Please Enter Subject elective At Row:"+str(count1)+""})
                    return response
                if len(str(class_master))==0:
                    response=JsonResponse({'status':'error','msg':"Please Enter Class At Row:"+str(count1)+""})
                    return response
                if len(str(division_name))==0:
                    response=JsonResponse({'status':'error','msg':"Please Enter Division At Row:"+str(count1)+""})
                    return response
                if len(str(subject_teacher))==0:
                    response=JsonResponse({'status':'error','msg':"Please Enter Subject teacher At Row:"+str(count1)+""})
                    return response
                if len(str(teacher_mobile))==0:
                    response=JsonResponse({'status':'error','msg':"Please Enter Mobile Number At Row:"+str(count1)+""})
                    return response                
                class_id           = class_models.objects.filter(class_name=class_name)
                subject_id         = subject.objects.filter(name=subject_name,school_id=school[0][0])
                division_id        = Division.objects.filter(division_name=division_name,school_id=school[0][0])
                teacher_details    = user_models.UserProfile.objects.filter(user__username=teacher_mobile)
                if teacher_details.exists():
                    teacher_id         = teacher.objects.filter(name=subject_teacher,school_id=school[0][0],user=teacher_details[0])
                else:
                    response=JsonResponse({'status':'error','msg':"Please Enter valid Mobile Number At Row:"+str(count1)+""})
                    return response 
                school_division    = school_division_mapping.objects.filter(class_id=class_id[0],division_id=division_id[0],school_id=school_details)
                if school_division.exists():
                    new_mapping        = school_division[0]
                else:
                    response = JsonResponse({'status':'error','msg':"Please Enter valid entry for class and division At Row:"+str(count1)+""})
                    return response 
                if Subject_teacher_mapping.objects.filter(subject=subject_id[0],teacher=teacher_id[0],school_division_mapping=new_mapping).exists():
                    response=JsonResponse({'status':'error','msg':"Teacher at Row: "+str(count1)+" already exists."})
                    return response
                else:
                    new_sub_techer     = Subject_teacher_mapping.objects.create(subject=subject_id[0],teacher=teacher_id[0],school_division_mapping=new_mapping)
                    new_sub_techer.save()       
                response=JsonResponse({'status':'success','msg':" "+str(count1)+" "+"Subject Teacher Mapping Added Successfully"})
            return response
    else:
        return render(request,'forbidden_page.html')


@login_required
@transaction.atomic
def class_teacher_upload(request):
    user_id = user_models.User.objects.get(username=str(request.user))
    userprofile_id = user_models.UserProfile.objects.filter(user=user_id.id)
    school = user_models.UserProfile.objects.filter(user=user_id.id).values_list('school_id')
    school_details = school_models.objects.get(pk=school[0][0])
    template = "add_class_teacher_mapping.html"
    response = ''
    if request.method =='GET':
            return render(request, template)
    else:
        xlsx_file = request.FILES['file']
        if not xlsx_file.name.endswith('.xlsx'):
            response=JsonResponse({'status':'error','msg':"Please upload a xlsx file"})
            return response

        count1=0
        userData=[]
        import pandas as pd
        from pandas import ExcelWriter
        from pandas import ExcelFile
        import math
        
        df = pd.read_excel(xlsx_file)
        if ('class' in df.columns) and ('division' in df.columns) and ('class_teacher' in df.columns) and ('class_coordinator' in df.columns) and ('teacher_mobile_number' in df.columns) and ('coordinator_mobile_number' in df.columns):

            for i in df.index:
                class_master        = df['class'][i] 
                division_name       = df['division'][i]
                class_teacher       = df['class_teacher'][i]
                class_mobile        = df['teacher_mobile_number'][i]
                class_coordinator   = df['class_coordinator'][i]
                coordinator_mobile  = df['coordinator_mobile_number'][i]
                userData.append([class_master,division_name,class_teacher,class_coordinator,class_mobile,coordinator_mobile])

        else:
            response=JsonResponse({'status':'error','msg':"Please check excel columns"})
            return response
        duplicated_names       = df[df.duplicated(['class','division','class_teacher'])]
        if(duplicated_names.empty==False):
            response = JsonResponse(
                    {'status': 'error', 'msg': "Please Correct the below records:" + duplicated_names['class_teacher'].to_string() + ""})
            return response
        for i in userData:
            count1+=1
            class_name          = i[0]
            division_name       = i[1]
            class_teacher       = i[2]
            class_coordinator   = i[3]
            class_mobile        = i[4]
            coordinator_mobile  = i[5]
            school_division_new = False
            if len(str(class_coordinator))==0:
                response=JsonResponse({'status':'error','msg':"Please Enter co-ordinator At Row:"+str(count1)+""})
                return response
            if len(str(class_master))==0:
                response=JsonResponse({'status':'error','msg':"Please Enter Class At Row:"+str(count1)+""})
                return response
            if len(str(division_name))==0:
                response=JsonResponse({'status':'error','msg':"Please Enter Division At Row:"+str(count1)+""})
                return response
            if len(str(class_teacher))==0:
                response=JsonResponse({'status':'error','msg':"Please Enter Class teacher At Row:"+str(count1)+""})
                return response
            if len(str(class_mobile))==0:
                response=JsonResponse({'status':'error','msg':"Please Enter Class teacher mobile At Row:"+str(count1)+""})
                return response
            if len(str(coordinator_mobile))==0:
                response=JsonResponse({'status':'error','msg':"Please Enter Class coordinator mobile At Row:"+str(count1)+""})
                return response
            
            teacher_details    = user_models.UserProfile.objects.filter(user__username=class_mobile)
            co_ordinator       = user_models.UserProfile.objects.filter(user__first_name=class_coordinator,school_id=school[0][0])
            class_id           = class_models.objects.filter(class_name=class_name)
            division_id        = Division.objects.filter(division_name=division_name,school_id=school[0][0])
            school_div_mapping = school_division_mapping.objects.filter(class_id=class_id[0],division_id=division_id[0],school_id=school_details).exists()
            teacher_id         = teacher.objects.filter(school_id=school[0][0],user=teacher_details[0])

            if school_div_mapping:
                school_division = school_division_mapping.objects.filter(class_id=class_id[0],division_id=division_id[0],school_id=school_details)
                coordinator_id=Class_Cordinator_teacher.objects.filter(co_ordinator=co_ordinator[0],class_teacher=teacher_id[0],school_division_mapping=school_division[0]).exists()
            if school_div_mapping == False:
                school_division    = school_division_mapping.objects.create(class_id=class_id[0],division_id=division_id[0],school_id=school_details)
                school_division.save()
                coordinator_id=Class_Cordinator_teacher.objects.filter(co_ordinator=co_ordinator[0],class_teacher=teacher_id[0],school_division_mapping=school_division).exists()
            if teacher_details.exists() == False:
                response=JsonResponse({'status':'error','msg':"Teacher Entry at Row: "+str(count1)+" does not exist."})
                return response
            if coordinator_id:
                response=JsonResponse({'status':'error','msg':"Teacher Entry at Row: "+str(count1)+" already exists."})
                return response
            if teacher_id.exists() == False:        
                response=JsonResponse({'status':'error','msg':"Teacher Entry at Row: "+str(count1)+" does not exist."})
                return response
        count1=0
        for i in userData:
            count1+=1
            class_name          = i[0]
            division_name       = i[1]
            class_teacher       = i[2]
            class_coordinator   = i[3]
            class_mobile        = i[4]
            coordinator_mobile  = i[5]
            class_id           = class_models.objects.filter(class_name=class_name)
            division_id        = Division.objects.filter(division_name=division_name,school_id=school[0][0])
            teacher_details    = user_models.UserProfile.objects.filter(user__username=class_mobile)
            co_ordinator       = user_models.UserProfile.objects.filter(user__first_name=class_coordinator,school_id=school[0][0])
            school_division    =school_division_mapping.objects.filter(class_id=class_id[0],division_id=division_id[0],school_id=school_details)
            new_sub_techer     = Class_Cordinator_teacher.objects.create(co_ordinator=co_ordinator[0],class_teacher=teacher_id[0],school_division_mapping=school_division[0])
            new_sub_techer.save()    
        response=JsonResponse({'status':'success','msg':" "+str(count1)+" "+"Class Teacher's and Co-ordinator's Added Successfully"})
        return response