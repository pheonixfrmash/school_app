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
from module_manager import models as models



@login_required
@csrf_exempt
# @transaction.atomic
def add_module_manager(request):
    action_name=''
    action_url=''
    action_id_list=[]
    if request.method == 'POST':
        module_name = request.POST.get('module_name')
        description = request.POST.get('description')
        module_path = request.POST.get('module_path')
        module_icon = request.POST.get('module_icon')
        module_action=request.POST.getlist('name[]')
        #actionlist=module_action[::2]
        print("module action",module_action)
        #actionurllist=module_action[1::2]

        
        new_module = models.Master.objects.create(module_name = module_name,module_description = description,module_path=module_path,module_icon=module_icon)
       
        new_module.save()

        new_Uid = new_module.id
        new_Uid1=models.Master.objects.get(id=new_Uid)
        # for k in actionurllist:
        	
        # 	new_moduleq = models.Action.objects.create(module=new_Uid1)
        # 	new_moduleq.save()
        # 	new_Uid55 = new_moduleq.id
        action_l=''
       	for i in range(0, len(module_action)): 
            if i % 2:
                action_l=module_action[i]
                abc=models.Action.objects.all().values_list('id').order_by("-id")[0]
                for t in abc:
                	idd=t
                	action_id_list.append(idd)
                
                actionupurl=models.Action.objects.get(id=idd)
                actionupurl.action_url=action_l
                actionupurl.save()

            else :
                
                action_name=module_action[i]
                new_moduleq = models.Action.objects.create(module=new_Uid1,action_name=action_name)
                new_moduleq.save()
                new_Uid55 = new_moduleq.id
                actionupurl=models.Action.objects.get(id=new_Uid55)
                actionupurl.action_url=action_name
                actionupurl.save()
        commnasring=str(action_id_list)[1:-1]
        #print("action_id_list",commnasring)
        #group_id = ','.join(action_id_list) 
        #print("action_id_list",action_id_list)
        new_module_update = models.Master.objects.get(id = new_Uid)
        new_module_update.action_item=commnasring
        new_module_update.save()


    

        response=JsonResponse({'status':'success'})
        return response

    else:
          
        return render(request, 'add_module_manager.html')


@login_required
@csrf_exempt
def get_module_manager(request):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.Master.objects.all().values_list('module_name','id').order_by('-id')
    for i in user_info:
        module_name=i[0]
        module_id=i[1]
        count+=1
        btn="<div class='editBut'><button class='btn btn-block btn-danger btn-sm delete' data-module_id="+str(module_id)+">Delete</button></div>"
        
        data.append([count,str(module_name),"<a href='/module_manager/edit_module_manager/"+str(module_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a>",btn])
        
    return render(request, 'get_module_manager.html', {'data':(data)})


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
def edit_module_manager(request, pk):
    
    user_id=pk
    data={}
    action_url_list=[]
    action_name_list=[]
    action_id_list=[]
    if request.method == 'POST':
        data={}
        module_name = request.POST.get('module_name')
        description = request.POST.get('description')
        module_path = request.POST.get('module_path')
        module_icon = request.POST.get('module_icon')
        module_action=request.POST.getlist('name[]')
        user_id1=models.Master.objects.get(id=user_id)
        #print("module_actionmodule_action",module_action)
        action_info=models.Action.objects.filter(module=pk).values_list('id','action_name','action_url')
        for i in action_info:
            action_name=i[1]
            action_url=i[2]
            action_id_list.append(i[0])
            action_name_list.append(action_name)
            action_name_list.append(action_url)
        #print("action_name_list",action_name_list)
        result = set(module_action) - set(action_name_list) # correct elements, but not yet in sorted order
        #print("ssss",sorted(result))
        final_list=sorted(result)
        if final_list:
	        for i in range(0, len(final_list)): 
	            if i % 2:
	                action_l=final_list[i]
	                abc=models.Action.objects.filter(module=user_id1).values_list('id').order_by("-id")[0]
	                for t in abc:
	                	idd=t
	                	#action_id_list.append(idd)
	                
	                actionupurl=models.Action.objects.get(id=idd)
	                actionupurl.action_url=action_l
	                actionupurl.save()

	            else :
	                
	                action_name=final_list[i]
	                new_moduleq = models.Action.objects.create(module=user_id1,action_name=action_name)
	                new_moduleq.save()
	                new_Uid55 = new_moduleq.id
	                actionupurl=models.Action.objects.get(id=new_Uid55)
	                actionupurl.action_url=action_name
	                actionupurl.save()

        commnasring=str(action_id_list)[1:-1]
        module_info=models.Master.objects.filter(id=user_id).update(module_name=module_name,module_description=description,module_path=module_path,module_icon=module_icon,action_item=commnasring)
        response=JsonResponse({'status':'success'})
        return response
    else:
        module_info=models.Master.objects.filter(id=pk).values_list('id','module_name','module_description','module_path','module_icon')
        for i in module_info:
            module_id=i[0]
            module_name=i[1]
            module_description=i[2]
            module_path=i[3]
            module_icon=i[4]

        action_info=models.Action.objects.filter(module=pk).values_list('id','action_name','action_url')
        for i in action_info:
            action_name=i[1]
            action_url=i[2]
            action_name_list.append(action_name)
            action_url_list.append(action_url)
            #print("action_name_list",action_name_list)
       
            data={"module_name":module_name,"module_description":module_description,'user_id':module_id,"module_path":module_path,"module_icon":module_icon,'action_name_list':action_name_list,'action_url_list':action_url_list}
        return render(request, 'edit_module_manager.html',{'data':data})


@login_required
@csrf_exempt
def delete_module(request):
    pk=request.POST.get('module_id')
    models.Master.objects.filter(id=pk).delete()
    response=JsonResponse({'status':'success','msg':'Module Deleted Successfuly'})
    return response
    