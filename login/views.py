from django.shortcuts import render
# dappx/views.py
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import Permission
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
import os
from operator import itemgetter
from datetime import timedelta
import io,csv
from pyfcm import FCMNotification
from django.db.models import Sum
from django.db import transaction
from dashboard import views,templates
import math, random
# Create your views here.
from users import models as user_models
from django.db.models import Q
from login.models import school_group



@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data={}
        username = request.POST.get('mobile_number')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        data={'username':username,'password':password,"status":True}
        if User.objects.filter(username=username):
            user = User.objects.get(username=username)
            if user.is_active:
                login(request,user)
                userprofileDetails = user_models.UserProfile.objects.filter(Q(user__username=username) & Q(otp=password)).values_list('user__first_name','user__last_name')
                if userprofileDetails:
                    response=JsonResponse({'status':'success'}) 
                    return response
                else:
                    response=JsonResponse({'status':'error','msg':'Invalid Otp'})
                    return response
            else:
                response=JsonResponse({'status':'error','msg':'Your account is inactive'})
                return response     
        else:
            response=JsonResponse({'status':'error','msg':'Username Does not Exits'})
            return response
    else:   
        print(request.method) 
        username=''
        password=''
        if 'username' in request.COOKIES and 'password' in request.COOKIES:
            print("cookies")
            username = request.COOKIES['username']
            password = request.COOKIES['password']
            return render(request, 'login.html', {"username" : username,"password" : password})
        else:
          print("here")
          return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def generateOTP(request) :
   import requests

   digits = "0123456789"
   text=''
   OTP = random.randint(1000,9999)
   Phone_number=request.POST.get('mobile_number')
   print(OTP,"Phone_number",Phone_number)
   userprofile=user_models.UserProfile.objects.get(user__username=str(Phone_number))
   userprofile.otp = OTP
   userprofile.save()
   #   Enter Your SMS gateway integrationhere to send the generated otp to user
  
   response=JsonResponse({'status':'success','msg':'OTP has been sent successfully.','data':OTP})
   return response

@login_required
def roleselection(request) :
  if request.method == "GET":
    group_list=[]
    resource_list = {}
    count = 1
    request_user_profile=User.objects.filter(username=str(request.user))
    request_user=user_models.UserProfile.objects.filter(user=request_user_profile[0].id)
    user_group = request.user.groups.values_list('name','pk')
    school_id=user_models.UserProfile.objects.filter(user=request_user_profile[0].id).values_list('school_id')
    for i in user_group:
       j=i[0].split('-',2)
       role_details={'id': i[1], 'name': j[0]}
       group_list.append(role_details)
    return render(request,'role_selection.html',{'data':group_list})
  else:
      role=request.POST.get('roles')
      school_name=school_group.objects.filter(group=role,app_user=request.user.pk).values_list('school_id',flat=True)
      request.session['role']=role
      response=JsonResponse({'status':'success','msg':'Login successfully.'})
      return response
