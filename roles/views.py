from django.shortcuts import render
# dappx/views.py
# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,Group
import json


from django.utils.timezone import get_current_timezone
from datetime import datetime
import dateutil.parser
#from django.utils.encoding import smart_str, smart_unicode
import os
from operator import itemgetter
from datetime import timedelta
import io,csv
from pyfcm import FCMNotification
from django.db.models import Sum
from django.db import transaction
from dashboard import views,templates
import requests
from users import models as user_models
from roles import models as role_models
# Create your views here.

@login_required
@csrf_exempt
@transaction.atomic
def view_role(request):
    group_data=[]
    data=[]
    if request.method == 'POST':
        new_user = User.objects.create(username = username,password = password,first_name=first_name,last_name=last_name,is_active=1,email=email)
        new_user.set_password(password)
        new_user.save()
        new_Uid = new_user.id
        response=JsonResponse({'status':'success'})
        return response

    else:
        count=0
        role_name=''
        user_id=request.user.id
        my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
        for i in my_user_type:
            role_name=i[0]

        if role_name=="Ignite Admin":
            user_type=Group.objects.all().values_list('id', 'name').order_by('-id')
        else:
            user_type=role_models.SchoolRoleMapping.objects.filter(posted_by=request.user.id).values_list('group', 'group__name').order_by('-id')
        
        for i in user_type:
            count+=1
            name=i[1]
            name = name.split("-", 1)[0]
            data.append([count,str(i[0]),name,"<a href='/roles/edit_role/"+str(i[0])+"' class='btn'><i class='fas fa-edit'></i> Edit</a>"])

        return render(request, 'role.html', {'data':data})
     

@login_required
@csrf_exempt
def add_role(request):
    gr_no=[]
    group_data=[]
    first_name=''
    company_name=''
    last_name=''
    city_name=''
    user_photo=''
    aadhar_card=''
    pan_card=''
    vote_id=''
    soil_card=''
    fertilizer_photo=''
    gst_photo=''
    role_name=''
    pincode=0
    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])
    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
    if my_user_type:
        print(my_user_type[0][0])

    school_label=user_models.UserProfile.objects.filter(user=request.user.id).values_list('school_id__school_label')
    for ij in school_label:
        school_label1=ij[0]
    print("school_label",school_label1)
    if request.method == 'POST':
        name = request.POST.get('name')
        name=name.strip()+'-'+school_label1
        print(name)
        if Group.objects.filter(name=name).exists():
            response=JsonResponse({'status':'error','msg':'Group Already exists'})
            return response
        Group.objects.get_or_create(name=name)
        my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
        for i in my_user_type:
            role_name=i[0]
            role_id=i[1]
        if role_name=="Ignite Admin":
            
            group_id=Group.objects.filter(name=name).values_list('id')
            for i in group_id:
                group_obj=i[0]

            try:
                user_id = User.objects.get(id=request.user.id)
            except:
                user_id = None

            
            school_id=None
            if group_obj is not None:
                user_roll_mappping_obj = role_models.SchoolRoleMapping.objects.create(posted_by=user_id, group_id=group_obj,
                                                                                    school=school_id)
                user_roll_mappping_obj.save()
        else:
            group_id=Group.objects.filter(name=name).values_list('id')
            for i in group_id:
                group_obj=i[0]
                
            try:
                user_id = User.objects.get(id=request.user.id)
            except:
                user_id = None

            school_id = user_models.UserProfile.objects.get(user=request.user.id).school_id
            if group_obj is not None:
                user_roll_mappping_obj = role_models.SchoolRoleMapping.objects.create(posted_by=user_id, group_id=group_obj,
                                                                                    school=school_id)
                user_roll_mappping_obj.save()

        

        response=JsonResponse({'status':'success'})
        return response

    else:
        
        return render(request, 'add_role.html', {})


@login_required
@csrf_exempt
def edit_role(request, pk):
    gr_no=[]
    group_data1=[]
    data={}
   
    user_id=pk
    school_label=user_models.UserProfile.objects.filter(user=request.user.id).values_list('school_id__school_label')
    for ij in school_label:
        school_label1=ij[0]
    print("school_label",school_label1)
    if request.method == 'POST':
        data={}
        grp_id = request.POST.get('grp_id')
        name = request.POST.get('name')
        name=name.strip()+'-'+school_label1
        Group.objects.filter(id=grp_id).update(name=name)
        response=JsonResponse({'status':'success'})
        return response
    else:
        user_info=Group.objects.filter(id=pk).values_list('id','name')
        for i in user_info:
            grp_id=i[0]
            name=i[1]
            name = name.split("-", 1)[0]
            data={"id":grp_id,"name":name}

        return render(request, 'edit_role.html',{'data':data})


@login_required
def save_role(request, pk):
    gr_no=[]
    group_data1=[]
    data={}
    user_id=pk
    school_label=user_models.UserProfile.objects.filter(user=request.user.id).values_list('school_id__school_label')
    for ij in school_label:
        school_label1=ij[0]
    print("school_label",school_label1)
    if request.method == 'POST':
        data={}
        grp_id = request.POST.get('grp_id')
        name = request.POST.get('name')
        name=name.strip()+'-'+school_label1
        Group.objects.filter(id=grp_id).update(name=name)
        response=JsonResponse({'status':'success'})
        return response