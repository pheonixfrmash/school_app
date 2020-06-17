from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,Group
import json

from django.db.models import Q
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
from users import views,templates
import requests
from users import models as user_models
from roles import models as role_models




@login_required
@csrf_exempt
@transaction.atomic
def add_user(request):
    gr_no=[]
    group_data=[]
    first_name=''
    company_name=''
    last_name=''
    city_name=''
    user_photo=''
    role_name=''
    aadhar_card=''
    pan_card=''
    vote_id=''
    soil_card=''
    fertilizer_photo=''
    gst_photo=''
    pincode=0

    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])
    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
    if request.method == 'POST':
        data={}
        username = request.POST.get('mobile_number')

        password = request.POST.get('mobile_number')
        email = request.POST.get('email')
        full_name = request.POST.get('name')
        #user_photo = request.POST.get('user_photo')
        gender = request.POST.get('gender')
        designation = request.POST.get('designation')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if (' ' in full_name) == True:
            full_name_split=full_name.split(' ')
            if len(full_name_split)==2:
                first_name=full_name_split[0]
                last_name=full_name_split[1]
            if len(full_name_split)==3:
                first_name=full_name_split[0]
                last_name=full_name_split[2]
        else:
            first_name=full_name
       

        new_user = User.objects.create(username = username,first_name=first_name,last_name=last_name,is_active=1,email=email,is_staff=1)
        new_user.set_password(password)
        # new_user.save()
        new_Uid = new_user.id

        try:
            group_obj = Group.objects.get(id=user_type)
        except:
            group_obj = None

        user_id = request.user.id
        school_id = user_models.UserProfile.objects.get(user=user_id).school_id
        if group_obj is not None:

            user_roll_mappping_obj = user_models.UserRoleMapping.objects.create(user_id=new_Uid, group_id=user_type,
                                                                                school=school_id)
            user_roll_mappping_obj.save()


        if request.FILES.get('user_photo'):
            user_photo = request.FILES['user_photo']
            

        userprofile = user_models.UserProfile.objects.create(user_id=new_Uid,user_photo=user_photo,gender=gender,designation=designation,created_at=datetime.now(),school_id=school_id)
        userprofile.save()

        
        response=JsonResponse({'status':'success'})
        return response

    else:
        # group_data1=[]
        #school_id = user_models.UserProfile.objects.get(user=request.user.id).school_id
        print(request.user.id)
        my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
        for i in my_user_type:
            role_name=i[0]
            role_id=i[1]
        if role_name=="Ignite Admin":
                my_user_type1=Group.objects.all().values_list('id','name')

        else:
                my_user_type1=role_models.SchoolRoleMapping.objects.filter(posted_by=request.user.id).values_list('group', 'group__name').order_by('-id')

        for i in my_user_type1:
            name=i[1]
            
            name = name.split("-", 1)[0]
            case = {'id': i[0], 'name': name}

            group_data.append(case)
        print(group_data)
        group_data1=sorted(group_data, key=itemgetter('name'))
        print(group_data1)
        return render(request, 'add_user.html', {'group_data':group_data1})


@login_required
@csrf_exempt
def get_manage_user(request):
    data=[]
    user_type=""
    district=""
    state=""
    role_name=''
    count=0
    row=[]
    school_id = user_models.UserProfile.objects.get(user=request.user.id).school_id
    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
    for i in my_user_type:
        role_name=i[0]
        role_id=i[1]
    if role_name=="Ignite Admin":
        
        user_info=user_models.UserProfile.objects.filter(~Q(id='1')).values_list('user__first_name','user__last_name','user__email','user__date_joined','user__id','user__username').order_by('-id')
    else:
        user_info=user_models.UserProfile.objects.filter(school_id=school_id).values_list('user__first_name','user__last_name','user__email','user__date_joined','user__id','user__username').order_by('-id')
        print("dfdffdfdf",user_info.query)

   
    for i in user_info:
        first_name=i[0]
        last_name=i[1]
        full_name=str(first_name)+" "+str(last_name)
        email=i[2]
        date_joined=i[3]
        formatedDate1= (date_joined + timedelta(hours = 5,minutes = 30))
        formatedDate = formatedDate1.strftime("%d-%m-%Y %H:%M:%S")
        auth_id=i[4]
        mobile_number=i[5]
        my_user_type=Group.objects.filter(user=auth_id).values_list('name','id')
        for j in my_user_type:
            user_type=j[0]
        count+=1
        
        data.append([count,str(full_name),str(user_type),str(mobile_number),str(email),str(formatedDate),"<a href='/users/edit_user/"+str(auth_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a>"])
        
    return render(request, 'manage_user.html', {'data':(data)})


@csrf_exempt
def check_user_mobile(request):
    mobile_number=request.POST.get('mobile_number')
    user_id=request.POST.get('user_id')
    if mobile_number:
        if user_id:
            if User.objects.filter(~Q(id = user_id),username=mobile_number).exists():
                res="false"
            else:
                res="true"
        else:
            if User.objects.filter(username=mobile_number).exists():
                res="false"
            else:
                res="true"
    else:
        res="false"
    return HttpResponse(res)

def get_group():
    group_data=[]
    group_data1=[]

    gr_no=[]
    first_name=''
    last_name=''
    city_name=''
    state=''
    data={}
   
    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        case = {'id': i[0], 'name': i[1]}
        group_data1.append(case)
        group_data=sorted(group_data1, key=itemgetter('name'))
    return group_data


@login_required
@csrf_exempt
def edit_user(request, pk):
    gr_no=[]
    group_data1=[]
    first_name=''
    last_name=''
    city_name=''
    company_name=''
    state=''
    pincode=0
    user_photo="/media/default/placeholder.png"
    aadhar_card="/media/default/placeholder.png"
    pan_card="/media/default/placeholder.png"
    vote_id="/media/default/placeholder.png"
    soil_card="/media/default/placeholder.png"
    gst_photo="/media/default/placeholder.png"
    fertilizer_photo="/media/default/placeholder.png"
    data={}
    group_data=get_group()
    user_id=pk

    if request.method == 'POST':
        data={}
        user_photo=''
        #user_id = request.POST.get('user_id')
        password = request.POST.get('mobile_number')
        user_type = request.POST.get('user_type')
        email = request.POST.get('email')
        full_name = request.POST.get('name')
        if (' ' in full_name) == True:
            full_name_split=full_name.split(' ')
            if len(full_name_split)==2:
                first_name=full_name_split[0]
                last_name=full_name_split[1]
            if len(full_name_split)==3:
                first_name=full_name_split[0]
                last_name=full_name_split[2]
        else:
            first_name=full_name

        #user_photo = request.POST.get('user_photo')
        gender = request.POST.get('gender')
        designation = request.POST.get('designation')
        #password = request.POST.get('password')

        

        User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,email=email,username=password)

        user_type=Group.objects.get(id=user_type)
       
        user_type.user_set.add(user_id)

        if request.FILES.get('user_photo'):
            user_photo = request.FILES['user_photo']

        user_profile = models.UserProfile.objects.get(user=pk)
        user_profile.user_photo=user_photo
        user_profile.gender=gender
        user_profile.designation=designation
        user_profile.updated_at=datetime.now()
        user_profile.save()


        response=JsonResponse({'status':'success'})
        return response
    else:
        user_info=models.UserProfile.objects.filter(user=pk).values_list('user__first_name','user__last_name','user__email','user__date_joined','user__id','user__username','designation','user__password','user_photo','gender')
        for i in user_info:
            first_name=i[0]
            last_name=i[1]
            email=i[2]
            date_joined=i[3]
            auth_id=i[4]
            mobile_number=i[5]
            designation=i[6]
            password=i[7]
            
            
            if i[8]:
                user_photo=i[8]

            #print("user_photouser_photo",i[8])

            gender=i[9]
           
            
            gender1={"name":gender}
            
            full_name=str(first_name)+" "+str(last_name)
            my_user_type=Group.objects.filter(user=auth_id).values_list('name','id')
            for i in my_user_type:
                case = {'id': i[1], 'name': i[0]}
            gender_data= [{'name': 'Male'}, {'name': 'Female'}]
            data={"user_type":case,"full_name":full_name,"email":email,"mobile_number":mobile_number,'group_data':group_data,'user_id':auth_id,"designation":designation,"password":password,"user_photo":user_photo,"gender":gender1,"gender_data":gender_data}
        return render(request, 'edit_user.html',{'data':data})




