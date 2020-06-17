from django.shortcuts import render,redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from division.serializer import DivisionSerializer
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from division.forms import DocumentForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from division.models import Division as division
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
from division.models import school_division_mapping,school_class_mapping
import xlwt
from django.http import HttpResponse
import re
from rest_framework import status
# Create your views here.

class Division(View):
    
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
    def list_divisions_data(request):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('division.view_division'):
        data=[]
        school_data=Division.get_schools
        class_data=Division.get_class
        state_data=Division.get_state
        city_data=Division.get_city
        country_data=Division.get_country 
        board_data=Division.get_board
        medium_data=Division.get_medium
        ob = Division()
        print(request.user)
        user_id = user_models.User.objects.get(username=str(request.user))
        school_id = user_models.UserProfile.objects.get(user=user_id.id)
        count=1
        if request.method == 'GET':
            division_list = division.objects.filter(school_id=school_id.school_id)
            for div in division_list:
              ad_id=div.id
              division_name = div.division_name
              division_desc = div.division_desc
              division_status = 'Active' if str(div.status)=='True' else 'Inactive'
              posted_by = div.created_by
              posted_person=user_models.User.objects.filter(username=str(posted_by)).values_list('first_name')
              posted_date = div.created_at
              resource_posted_date = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', str(posted_date.date()))
              posted_user = posted_person[0][0]
              Edit='<div class="btn-group"><form class="span4 text-left" action="/division/edit/'+str(ad_id)+'" method="POST"><button style="margin:5px" class="btn btn-primary"><i class="fas fa-edit"></i> Edit</button></form>'
              View='<form class="span4 text-center" action="/division/details/'+str(ad_id)+'" method="POST"><button style="margin:5px" class="btn btn-primary"><i class="fas fa-eye"></i>View</button></form>'
              Delete='<form action="/module_manager/edit_module_manager/21" method="get"><button style="margin:5px" type="button" class="btn btn-primary"><i class="far fa-trash-alt"></i>Delete</button></form></div>'
              actions = Edit       
              serialised_data = [count,division_name,division_desc,division_status,posted_user,str(resource_posted_date),actions]
              data.append(serialised_data)
              count+=1
            context = {'data': data,"country_data":country_data ,"state_data":state_data,"city_data":city_data,'board_data':board_data,'medium_data':medium_data,'school_data':school_data,'class_data':class_data }
            template = 'division_list.html'
            return render(request,template,context)
        else:
            response=JsonResponse({'status':'error','msg':'Bad Request'})
            return response
     else:
        return render(request,'forbidden_page.html')

    @login_required
    def download_excel_data(request):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('division.view_division'):
        # content-type of response
        response = HttpResponse(content_type='application/ms-excel')

        #decide file name
        response['Content-Disposition'] = 'attachment; filename="division_master.xls"'

        #creating workbook
        wb = xlwt.Workbook(encoding='utf-8')

        #adding sheet
        ws = wb.add_sheet("division")

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        # headers are bold
        font_style.font.bold = True

        #column header names, you can use your own headers here
        columns = ['Sr.No','Division Name', 'Division Description', 'Created by', 'Created Date' ]

        #write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        #get your data, from database or from a text file...
        data = Division.list_divisions_data(request) #dummy method to fetch data.
        for my_row in data:
            row_num = row_num + 1
            ws.write(row_num, 0, str(row_num), font_style)
            ws.write(row_num, 1, my_row['division_name'], font_style)
            ws.write(row_num, 2, my_row['division_desc'], font_style)
            ws.write(row_num, 3, user_models.User.objects.get(pk=user_models.UserProfile.objects.get(pk=my_row['created_by']).user_id).first_name, font_style)
            ws.write(row_num, 4, my_row['created_at'], font_style)
        wb.save(response)
        return response
     else:
        return render(request,'forbidden_page.html') 

    @login_required
    def send_file(request):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('division.add_division'):
        file_path="/home/oem/Downloads/sample_division.xlsx"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
     else:
        return render(request,'forbidden_page.html') 

    @login_required
    @transaction.atomic
    def division_upload(request):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('division.add_division'):
        user_id = user_models.User.objects.get(username=str(request.user))
        userprofile_id = user_models.UserProfile.objects.filter(user=user_id.id)
        school = user_models.UserProfile.objects.filter(user=user_id.id).values_list('school_id')
        school_details = school_models.objects.get(pk=school[0][0])
        template = "add_division_excel.html"
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
        
        df = pd.read_excel(xlsx_file)
        if ('division_name' in df.columns) and ('division_description' in df.columns):

            for i in df.index:
                division_name        = df['division_name'][i]
                division_description = df['division_description'][i]
                userData.append([division_name,division_description])

        else:
            response=JsonResponse({'status':'error','msg':"Please check excel columns"})
            return response
        duplicated_names       = df[df.duplicated(['division_name'])]
        duplicated_description = df[df.duplicated(['division_description'])]
        if(duplicated_names.empty==False):
            response = JsonResponse(
                    {'status': 'error', 'msg': "Please Correct the below records:" + duplicated_names['division_name'].to_string() + ""})
            return response
        if(duplicated_description.empty==False):
            response = JsonResponse(
                    {'status': 'error', 'msg': "Please Correct the below records:" + duplicated_names['division_description'].to_string() + ""})
            return response
        for i in userData:
            count1+=1
            division_name        = i[0]
            division_description = i[1]
            if len(str(division_name))==0:
                response=JsonResponse({'status':'error','msg':"Please Enter Division Name At Row: "+str(count1)+""})
                return response
            if len(str(division_description))==0:
                response=JsonResponse({'status':'error','msg':"Please Enter Division Description At Row: "+str(count1)+""})
                return response
            if (division.objects.filter(division_name=division_name,division_desc=division_description,school_id=school_details).exists()):
                response=JsonResponse({'status':'error','msg':"Divsion At Row: "+str(count1)+" already exists"})
                return response
        for i in userData:
            count1+=1
            division_name        = i[0]
            division_description = i[1]                
            new_division  = division.objects.create(division_name=division_name,division_desc=division_description,created_by=userprofile_id[0],school_id=school_details)
            new_division.save()        
        response=JsonResponse({'status':'success','msg':" "+str(count1)+" "+"Division Added Successfully"})
        return response
     else:
        return render(request,'forbidden_page.html') 

    @login_required
    def edit_division(request,id):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('division.change_division'):
        try:
         ads = division.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            # ad = resources.objects.get(pk= id)
            ad_id=ads.id
            division_name=ads.division_name
            division_desc = ads.division_desc
            serialised_data = {'ad_id':ad_id,'division_name':division_name,'division_desc':division_desc}
            
            return render(request,'edit_division.html',{'data':serialised_data})
     else:
        return render(request,'forbidden_page.html') 

    @login_required
    def view_division(request,id):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('division.view_division'):
        try:
         ads = division.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            # ad = resources.objects.get(pk= id)
            ad_id=ads.id
            division_name=ads.division_name
            division_desc = ads.division_desc
            serialised_data = {'ad_id':ad_id,'division_name':division_name,'division_desc':division_desc}
            
            return render(request,'view_division.html',{'data':serialised_data})
     else:
        return render(request,'forbidden_page.html') 

    @login_required    
    def save_division(request,id):
     user=user_models.User.objects.get(username=request.user.username)
     if user.has_perm('division.change_division'):
        try:
         ads = division.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method =='POST':
            division_name = request.POST.get('division_name')
            division_description = request.POST.get('division_description')
            division.objects.filter(pk=ads.id).update(division_name= division_name ,division_desc=division_description)
            response=JsonResponse({'status':'success'})
            return response
        else:
           response=JsonResponse({'status':'fail','error':'Invalid Request'})
           return response
     else:
        return render(request,'forbidden_page.html') 