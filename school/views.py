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
# from pyfcm import FCMNotification
from django.db.models import Sum
from django.db import transaction
from users import views,templates
import requests
from module_manager import models as models
from state import models as state_models
from country import models as country_models
from city import models as city_models
from board import models as board_models
from medium import models as medium_models
from school import models as school_models
from bank import models as bank_models
from users import models as user_models
from module_access import models as models_access
from roles import models as role_models
import re


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
def get_module_manager():
    module_manager_data = []
    module_manager_list = models.Master.objects.all().values_list('module_name', 'id').order_by('-id')

    for i in module_manager_list:
        case2 = {'id': i[1], 'name': i[0]}
        module_manager_data.append(case2)
    return module_manager_data


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
    medium_list=medium_models.Medium.objects.all().values_list('id', 'medium_name')
    for i in medium_list:
        case2 = {'id': i[0], 'name': i[1]}
        medium_data.append(case2)
    return medium_data

@csrf_exempt
def get_module_list():
    models_data=[]
    module_list=models.Master.objects.all().values_list('id','module_name')
    for i in module_list:
        case2={'id':i[0],'name':i[1]}
        models_data.append(case2)
    models_data=sorted(models_data, key=itemgetter('name'))
    return models_data

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
@csrf_exempt
def check(email):
    # pass the regualar expression
    # and the string in search() method
    if (re.search(regex, email)):
        return True
    else:
        return False


@login_required
@csrf_exempt
@transaction.atomic
def add_school(request):
    action_name=''
    role_name=''
    action_url=''
    country_data=get_country()
    state_data=get_state()
    city_data=get_city()
    board_data=get_board()
    medium_data=get_medium()
    module_data=get_module_list()
    module_manager_data = get_module_manager()
    action_id_list=[]
    bank_deatils=[]
    jsonlist=[]
    datajsonlist={}


    if request.method == 'POST':
        school_name = request.POST.get('school_name')
        school_label = request.POST.get('school_label')
        iml_school_code = request.POST.get('iml_school_code')
        school_address = request.POST.get('school_address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        medium = request.POST.get('medium')
        board = request.POST.get('board')
        dise_no = request.POST.get('dise_no')
        school_photo = request.POST.get('school_photo')
        #print("school_photoschool_photo",school_photo)
        about_school = request.POST.get('about_school')
        class_label = request.POST.get('class_label')
        division_label=request.POST.get('division_label')
        exampleRadios = request.POST.get('exampleRadios')
        commision_value = request.POST.get('commision_value')
        school_admin_name = request.POST.get('school_admin_name')
        email_id = request.POST.get('email_id')
        school_admin_number = request.POST.get('school_admin_number')
        #disivion_label = request.POST.get('disivion_label')
        bank_name=request.POST.getlist('bank_name[]')
        account_no=request.POST.getlist('account_no[]')
        ifsc_code=request.POST.getlist('ifsc_code[]')
        branch_name=request.POST.getlist('branch_name[]')
        school_name = request.POST.get('school_name')
        school_label = request.POST.get('school_label')
        module_manager=request.POST.getlist('module_manager')
        print("bank_deatils",module_manager)



        country=country_models.Country.objects.get(id=country)
        state=state_models.State.objects.get(id=state)
        city=city_models.City.objects.get(id=city)
        medium=medium_models.Medium.objects.get(id=medium)
        board=board_models.Board.objects.get(id=board)

        new_module = school_models.School.objects.create(school_name = school_name,school_label = school_label,iml_school_code=iml_school_code,school_address=school_address,school_country=country,school_state=state,school_city=city,pincode=pincode,school_medium=medium,dias_number=dise_no,school_logo=school_photo,about_school=about_school,school_board=board,class_label=class_label,division_label=division_label)

        new_module.save()
        newSid=new_module.id
        school_id=school_models.School.objects.get(id=newSid)
        #print(school_id)

        new_user = User.objects.create(username = school_admin_number,password = school_admin_number,first_name=school_admin_name,is_active=1,email=email_id)
        new_user.set_password(school_admin_number)
        new_user.save()
        new_Uid = new_user.id

        userprofile = user_models.UserProfile.objects.create(user_id=new_Uid,school_id=school_id,created_at=datetime.now())
        userprofile.save()

        # userprofile1 = user_models.UserRoleMapping.objects.create(user_id=new_Uid,group_id=2,school=school_id)
        # userprofile1.save()

        if Group.objects.filter(name='school_admin_'+school_name).exists():
            response=JsonResponse({'status':'error','msg':'Group Already exists'})
            return response
        group_obj = Group.objects.create(name='school_admin_'+school_label+'_' + school_name)
        group_id =group_obj.id

        user_roll_mappping_obj = user_models.UserRoleMapping.objects.create(user_id=new_Uid,group_id=group_id,school=school_id)

        for module_id in module_manager:

            try:
                action_obj = models.Action.objects.get(module=module_id, action_name='View').id
            except:
                action_obj = None
            if action_obj is not None:
                print(action_obj,'-----action_obj------')


                roll_mappping = models_access.Role_Mapping.objects.create(role_id=group_id,module_id=module_id,action_id=action_obj)
                roll_mappping.save()
        user_roll_mappping_obj.save()
        # userprofile1.save()
        group_obj.save()
        new_Uid=User.objects.get(id=new_Uid)
        user_roll_mappping_obj1 = role_models.SchoolRoleMapping.objects.create(posted_by=new_Uid, group_id=group_id,
                                                                                    school=school_id)
        user_roll_mappping_obj1.save()

        for i in range(0,len(bank_name)):
            print(i)
            print(bank_name[i],type(bank_name))
            try:
                bank_obj=bank_models.Bank.objects.get(bank_name=bank_name[i],account_number=account_no[i],ifsc_code=ifsc_code[i],school_id=school_id)
            except:
                bank_obj = None
            if bank_obj is None:
                bank_obj = bank_models.Bank.objects.create(bank_name=bank_name[i],branch_name=branch_name[i], account_number=account_no[i],ifsc_code=ifsc_code[i],school_id=school_id)
                bank_obj.save()




        #print("jsonlist",jsonlist)

        response=JsonResponse({'status':'success'})
        return response

    else:
        return render(request, 'add_school.html', {"country_data":country_data ,"state_data":state_data,"city_data":city_data,'board_data':board_data,'medium_data':medium_data,'module_data':module_data ,'module_manager_data':module_manager_data,'class_label':'standard','division_label':'section','commision_value':'0'})


@login_required
@csrf_exempt
def get_manage_school(request):
    data = []
    user_type = ""
    district = ""
    role_name=''
    state = ""
    count = 0
    row = []
    user_id=request.user.id
    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
    for i in my_user_type:
        role_name=i[0]
    if role_name=="Ignite Admin":
        pass
    else:
        userRolemap=user_models.UserProfile.objects.filter(user_id=user_id).values_list('school_id')

        for i in userRolemap:
            school_id=i[0]
    if role_name=="Ignite Admin":
        user_info = school_models.School.objects.all().values_list('id', 'school_label', 'school_name', 'status').order_by(
        '-id')
    else:
        user_info = school_models.School.objects.filter(id=school_id).values_list('id', 'school_label', 'school_name', 'status').order_by(
        '-id')

    
    for i in user_info:
        school_id = i[0]
        school_label = i[1]
        school_name = i[2]
        school_status = i[3]
        print(school_name)

        user_info = user_models.UserRoleMapping.objects.filter(school=school_id).values_list('id', 'user__first_name',
                                                                                             'user__email',
                                                                                             'user__username')
        for i in user_info:
            super_admin_name = i[1]
            super_admin_email = i[2]
            super_admin_no = i[3]

            count += 1
            edit_btn = "<div class='editBut'><button class='btn btn-block btn-danger btn-sm delete' data-module_id=" + str(
                school_id) + ">Delete</button></div>"
            view_btn = "<div class='viewBut'><button class='btn btn-block btn-danger btn-sm delete' data-module_id=" + str(
                school_id) + ">Delete</button></div>"
            status_btn = "<div class='statusBut'><button class='btn btn-block btn-danger btn-sm delete' data-module_id=" + str(
                school_id) + ">Delete</button></div>"

            if school_status == True:
                school_status = 'Inactive'
                icon = 'fas fa-times'
            else:
                school_status = 'Active'
                icon = 'fas fa-check'

            data.append([count, str(school_label), str(school_name), str(super_admin_name), str(super_admin_email),
                         str(super_admin_no),
                         "<a href='/school/edit_school/" + str(
                             school_id) +"/"+str(super_admin_no)+ "' class='btn'><i class='fas fa-edit'></i> Edit</a>",
                         "<a href='/school/view_school/" + str(
                             school_id) +"/"+str(super_admin_no)+ "' class='btn'><i class='fas fa-eye'></i> View</a>",
                         "<a href='/school/edit_school/" + str(
                             school_id) + "' class='btn'><i class='" + icon + "'></i>" + str(school_status) + "</a>"])
    #print("data",data)
    return render(request, 'get_school.html', {'data': (data)})


# @login_required
# @csrf_exempt
# def get_manage_school(request):
#     data=[]
#     user_type=""
#     district=""
#     state=""
#     count=0
#     row=[]
#     user_info=school_models.School.objects.all().values_list('id','school_label','school_name').order_by('-id')
#     for i in user_info:
#         school_id=i[0]
#         school_label=i[1]
#         school_name=i[2]

#         user_info=user_models.UserRoleMapping.objects.filter(school=school_id).values_list('id','user__first_name','user__email','user__username')
#         for i in user_info:
#             super_admin_name=i[1]
#             super_admin_email=i[2]
#             super_admin_no=i[3]

#             count+=1
#             btn="<div class='editBut'><button class='btn btn-block btn-danger btn-sm delete' data-module_id="+str(school_id)+">Delete</button></div>"



#             data.append([count,str(school_label),str(school_name),str(super_admin_name),str(super_admin_email),str(super_admin_no),"<a href='/module_manager/edit_module_manager/"+str(school_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a>"])

#         return render(request, 'get_school.html', {'data':(data)})


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



@csrf_exempt
@transaction.atomic
def school_upload(request):
    template = "add_school_excel.html"
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
    count=0
    count1=0
    count2=0
    count3=0
    count4=0
    count5=0
    usernameData=[]
    districtData=[]
    stateData=[]
    userData=[]
    import pandas as pd
    from pandas import ExcelWriter
    from pandas import ExcelFile
    import math
    df = pd.read_excel(xlsx_file)
    print(df,'_____________')
    if ('school_name' in df.columns) and ('school_label' in df.columns) and ('iml_code' in df.columns) and ('school_address' in df.columns) and ('country' in df.columns) and ('state' in df.columns) and ('city' in df.columns) and ('pincode' in df.columns) and ('board' in df.columns) and ('medium' in df.columns)  and ('dise_no' in df.columns)  and ('about_school' in df.columns) and ('class_label' in df.columns) and ('disivion_label' in df.columns) and ('commision_label' in df.columns) and ('commision_value' in df.columns) and ('school_admin_name' in df.columns) and ('school_admin_number' in df.columns) and ('school_admin_email' in df.columns):

        for i in df.index:
            school_name = df['school_name'][i]
            school_label=df['school_label'][i]
            iml_code=df['iml_code'][i]
            school_address = df['school_address'][i]
            country = df['country'][i]
            state=df['state'][i]
            city=df['city'][i]
            pincode=df['pincode'][i]
            board=df['board'][i]
            medium=df['medium'][i]
            dise_no=df['dise_no'][i]
            about_school=df['about_school'][i]
            class_label=df['class_label'][i]
            disivion_label=df['disivion_label'][i]
            commision_label = df['commision_label'][i]
            commision_value = df['commision_value'][i]
            school_admin_name = df['school_admin_name'][i]
            school_admin_number=df['school_admin_number'][i]
            school_admin_email=df['school_admin_email'][i]

            userData.append([school_name,school_label,iml_code,school_address,country,state,city,pincode,board,medium,dise_no,about_school,class_label,disivion_label,commision_label,commision_value,school_admin_name,school_admin_number,school_admin_email])

    else:
        response=JsonResponse({'status':'error','msg':"Please check excel columns"})
        return response

    for i in userData:
        print(i[17])
        count1+=1
        school_name = i[0]
        school_label = i[1]
        iml_code = i[2]
        school_address = i[3]
        print(i[4])
        country = i[4]
        state = i[5]
        city = i[6]
        pincode = i[7]
        board = i[8]
        medium = i[9]
        dise_no = i[10]
        about_school = i[11]
        class_label = i[12]
        disivion_label = i[13]
        commision_label = i[14]
        commision_value = i[15]
        school_admin_name = i[16]
        school_admin_number = i[17]
        school_admin_email = i[18]


        if user_models.User.objects.filter(username=school_admin_number).exists():
            response=JsonResponse({'status':'error','msg':"Mobile Number is Already Exits At Row:"+str(count1)+""})
            return response
        if school_models.School.objects.filter(school_label=school_label).exists():
            response=JsonResponse({'status':'error','msg':"School Label Already Exits At Row:"+str(count1)+""})
            return response
        if Group.objects.filter(name='school_admin_' + school_name).exists():
            response = JsonResponse({'status': 'error', 'msg': "Group Already Exits At Row:" + str(count1) + ""})
            return response

        if state_models.State.objects.filter(state_name=state.strip().capitalize()).exists():
            state_models.State.objects.get(state_name=state.strip().capitalize())
        else:
            response = JsonResponse({'status': 'error', 'msg': "Please Enter Correct State At Row:" + str(count1) + ""})
            return response

        if city_models.City.objects.filter(city_name=city.strip().capitalize()).exists():
            city_models.City.objects.get(city_name=city.strip().capitalize())
        else:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter Correct City At Row:" + str(count1) + ""})
            return response

        if country_models.Country.objects.filter(country_name=country.strip().capitalize()).exists():
            country_models.Country.objects.get(country_name=country.strip().capitalize())
        else:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter Correct Country At Row:" + str(count1) + ""})
            return response

        if board_models.Board.objects.filter(board_name=board).exists():
            board_models.Board.objects.get(board_name=board)
        else:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter Correct Board At Row:" + str(count1) + ""})
            return response

        if medium_models.Medium.objects.filter(medium_name=medium).exists():
            medium_models.Medium.objects.get(medium_name=medium)
        else:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter Correct Medium At Row:" + str(count1) + ""})
            return response

        if len(str(school_label))==0:
            response=JsonResponse({'status':'error','msg':"Please Enter School Label At Row:"+str(count1)+""})
            return response
        if len(str(school_name))==0:
            response=JsonResponse({'status':'error','msg':"Please Enter School Name At Row:"+str(count1)+""})
            return response
        if len(str(iml_code))==0:
            response=JsonResponse({'status':'error','msg':"Please Enter School IML Code At Row:"+str(count1)+""})
            return response
        if len(str(school_admin_name))==0:
            response=JsonResponse({'status':'error','msg':"Please Enter School Admin Name At Row:"+str(count1)+""})
            return response
        if len(str(dise_no))==0:
            response=JsonResponse({'status':'error','msg':"Please Enter DISE Number At Row:"+str(count1)+""})
            return response

        if len(str(school_admin_number))!=10:
            response=JsonResponse({'status':'error','msg':"Please Enter 10 digit Mobile No At Row:"+str(count1)+""})
            return response
        if math.isnan(pincode):
            pincode=0
        else:
            if len(str(pincode))!=6:
                response=JsonResponse({'status':'error','msg':"Please Enter 6 digit Pincode At Row:"+str(count1)+""})
                return response
        try:
            int(school_admin_number)
            school_admin_number=True
        except:
            response=JsonResponse({'status':'error','msg':"Please Enter digits only in Mobile No At Row:"+str(count1)+""})
            return response
        print(check(school_admin_email),'_____email__________')
        if check(school_admin_email) == True:
            school_admin_email=True
        else:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter valid email id At Row:" + str(count1) + ""})
            return response


    countdata=0
    for i in userData:
        countdata+=1
        school_name = i[0]
        school_label = i[1]
        iml_code = i[2]
        school_address = i[3]
        print(type(i[3]),'ssssssssssssssss')
        country = i[4]
        state = i[5]
        city = i[6]
        pincode = i[7]
        board = i[8]
        medium = i[9]
        dise_no = i[10]
        about_school = i[11]
        class_label = i[12]
        disivion_label = i[13]
        commision_label = i[14]
        commision_value = i[15]
        school_admin_name = i[16]
        school_admin_number = i[17]
        school_admin_email = i[18]
        state = state_models.State.objects.get(state_name=state.strip().capitalize())
        city = city_models.City.objects.get(city_name=city.strip().capitalize())
        country = country_models.Country.objects.get(country_name=country.strip().capitalize())
        board = board_models.Board.objects.get(board_name=board)
        medium = medium_models.Medium.objects.get(medium_name=medium)


        new_school = school_models.School.objects.create(school_name=school_name, school_label=school_label,
                                                         iml_school_code=iml_code, school_address=school_address,
                                                         school_country=country, school_state=state, school_city=city,
                                                         pincode=pincode, school_medium=medium, dias_number=dise_no,
                                                        about_school=about_school,
                                                         school_board=board, class_label=class_label,
                                                         division_label=disivion_label)
        new_user = User.objects.create(username=school_admin_number, password=school_admin_number,
                                       first_name=school_admin_name, is_active=1, email=school_admin_email)

        userprofile = user_models.UserProfile.objects.create(user=new_user, created_at=datetime.now())
        print('----gggg------------')
        group_obj = Group.objects.create(name='school_admin_'+school_label+'_' + school_name)
        print('----gggg-------kkkkk-----')

        group_id = group_obj.id
        user_roll_mappping_obj = user_models.UserRoleMapping.objects.create(user_id=new_user.id, group_id=group_id,
                                                                            school=new_school)

        new_school.save()
        new_user.save()
        userprofile.save()
        group_obj.save()
        # user_roll_mappping_id = user_roll_mappping_obj.id
        #
        # for module_id in module_manager:
        #     try:
        #         action_obj = models.Action.objects.get(module=module_id, action_name='View').id
        #     except:
        #         action_obj = None
        #     if action_obj is not None:
        #         roll_mappping = models_access.Role_Mapping.objects.create(role_id=group_id, module_id=module_id,
        #                                                                   action_id=action_obj)
        #         roll_mappping.save()
        # user_roll_mappping_obj.save()
        # userprofile1.save()


    response=JsonResponse({'status':'success','msg':" "+str(countdata)+" "+"User Added Successfully"})
    return response

@csrf_exempt
def edit_school(request, user_id_pk,school_id_pk):


    data = {}
    action_url_list = []
    action_name_list = []
    action_id_list = []
    action_name = ''
    action_url = ''
    school_photo = "/media/default/placeholder.png"
    country_data = get_country()
    state_data = get_state()
    city_data = get_city()
    board_data = get_board()
    medium_data = get_medium()
    module_manager_data = get_module_manager()
    action_id_list = []
    bank_deatils = []
    jsonlist = []
    datajsonlist = {}

    try:
        school_obj = school_models.School.objects.get(id=school_id_pk)
    except:
        school_obj = None


    bank_data = bank_models.Bank.objects.filter(school_id=school_id_pk).values('id','bank_name','ifsc_code','account_number','branch_name')
    bank_details = []
    for i in bank_data:
        bank_details.append(i)

    if school_obj is not None:
        school_details = [str(school_obj.school_name), str(school_obj.school_label), str(school_obj.iml_school_code),
                          str(school_obj.school_address), str(school_obj.school_country.id), str(school_obj.school_state.id),
                          str(school_obj.school_city.id), str(school_obj.pincode), str(school_obj.school_medium.id),
                          str(school_obj.dias_number), str(school_obj.school_logo), str(school_obj.about_school),
                          str(school_obj.school_board.id),str(school_obj.class_label),str(school_obj.division_label),
                          str(school_obj.academic_year),str(school_obj.commission_type),str(school_obj.commission_value)]
    else:
        school_details= []

    role_id_list=[]
    role_module_list=[]
    wholesaler_data1=[]
    user_roll_mappping_obj = user_models.UserRoleMapping.objects.filter(school=school_id_pk).values_list('group_id')
    for i in user_roll_mappping_obj:
        role_id_list.append(i[0])

    roll_mappping = models_access.Role_Mapping.objects.filter(role_id__in=role_id_list).values_list('module_id')

    for j in roll_mappping:
        role_module_list.append(j[0])

    print("role_module_list",role_id_list)

    user_link_data= models.Master.objects.filter(id__in=role_module_list).values_list('id','module_name')
    wholesaler_data1=[]
    for w in user_link_data:
        full_name1=str(w[1])
        wholesaler_data={"name":full_name1,'id':w[0]}
        wholesaler_data1.append(wholesaler_data)
    print("wholesaler_data1",wholesaler_data1)

    try:
        user_obj = user_models.User.objects.get(username=user_id_pk)
    except:
        user_obj = None

    if user_obj is not None:

        school_admin_number = user_obj.username
        school_admin_name = user_obj.first_name
        email = user_obj.email
        school_admin_details_list = [school_admin_number, school_admin_name, email]
    else:
        school_admin_details_list = []

    print("school_admin_details_list",school_admin_details_list)
    if request.method == 'POST':
        data = {}
        school_photo=''
        school_name = request.POST.get('school_name')
        school_label = request.POST.get('school_label')
        iml_school_code = request.POST.get('iml_school_code')
        school_address = request.POST.get('school_address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        medium = request.POST.get('medium')
        board = request.POST.get('board')
        dise_no = request.POST.get('dise_no')
        # school_photo = request.FILES['school_photo']
        about_school = request.POST.get('about_school')
        class_label = request.POST.get('class_label')
        exampleRadios = request.POST.get('exampleRadios')
        commision_value = request.POST.get('commision_value')
        school_admin_name = request.POST.get('school_admin_name')
        email_id = request.POST.get('email_id')
        school_admin_number = request.POST.get('school_admin_number')
        disivion_label = request.POST.get('disivion_label')

        bank_name = request.POST.getlist('bank_name[]')
        account_no = request.POST.getlist('account_no[]')
        ifsc_code = request.POST.getlist('ifsc_code[]')
        branch_name = request.POST.getlist('branch_name[]')
        print(bank_name)
        if request.FILES.get('school_photo'):
            school_photo = request.FILES['school_photo']
            print(school_photo)
        else:
            school_photo = "/media/default/placeholder.png"
        try:
            school_admin_details = User.objects.get(username=user_id_pk)
        except:
            school_admin_details = None
        if school_admin_details is not None:

            # school_admin_details.username = school_admin_number
            school_admin_details.first_name = school_admin_name
            school_admin_details.email = email_id
        school_obj.school_name=school_name
        if school_obj.school_label != school_label:
          if school_models.School.objects.filter(school_label=school_label):
            response=JsonResponse({'status':'error','msg':"School label already exists"})
            return response
            # school_obj.update(school_label=school_label)
          else:
              school_obj.school_label=school_label
             
        if  school_obj.school_logo:
            # school_obj.update(school_logo=school_photo)
            school_obj.school_logo=school_photo

        school_obj.iml_school_code=iml_school_code
        school_obj.school_address=school_address
        school_obj.school_country=country_models.Country.objects.get(id=country)
        school_obj.school_state.id=state_models.State.objects.get(id=state)
        school_obj.school_city.id=city_models.City.objects.get(id=city)
        school_obj.pincode=pincode
        school_obj.school_medium.id=medium_models.Medium.objects.get(id=medium)
        school_obj.dias_number=dise_no
        school_obj.school_logo=school_photo
        school_obj.about_school=about_school
        school_obj.school_board=board_models.Board.objects.get(id=board)
        school_obj.class_label=class_label
        school_obj.division_label=disivion_label
        school_obj.commission_type = exampleRadios
        school_obj.commission_value = commision_value
        # school_obj.academic_year=a
        
        # bank_models.Bank.objects.filter(school_id=school_obj.id).delete()
        for i in range(0,len(bank_name)):

            bank_obj = bank_models.Bank.objects.create(bank_name=bank_name[i],branch_name=branch_name[i], account_number=account_no[i],ifsc_code=ifsc_code[i],school_id=school_obj)
            bank_obj.save()
        # school_obj.update()
        school_obj.save()
        school_admin_details.save()
        response=JsonResponse({'status':'success','msg':"School Updated Successfully"})
        return response

    return render(request, 'edit_school.html',
                      {'data': data, "country_data": country_data, "state_data": state_data, "city_data": city_data,
                       'board_data': board_data, 'medium_data': medium_data, 'module_manager_data': wholesaler_data1,
                       'school_details': school_details,'bank_details':bank_details,'school_admin_details_list': school_admin_details_list,'school_id':school_id_pk,'user_id':user_id_pk,'school_photo':school_photo})

# @csrf_exempt
# def edit_school(request, pk):
#     user_id = pk
#     data = {}
#     action_url_list = []
#     action_name_list = []
#     action_id_list = []
#     action_name = ''
#     action_url = ''
#     country_data = get_country()
#     state_data = get_state()
#     city_data = get_city()
#     board_data = get_board()
#     medium_data = get_medium()
#     module_manager_data = get_module_manager()
#     action_id_list = []
#     bank_deatils = []
#     jsonlist = []
#     datajsonlist = {}
#     try:
#         school_obj = school_models.School.objects.get(id=pk)
#     except:
#         school_obj = None
#     # school_name = school_obj.school_name
#     # school_label = school_obj.school_label
#     # iml_school_code = school_obj.iml_school_code
#     # school_address = school_obj.school_address
#     # school_country = school_obj.school_country
#     # school_state = school_obj.school_state
#     # school_city = school_obj.school_city
#     # pincode = school_obj.pincode
#     # school_medium = school_obj.school_medium
#     # dias_number = school_obj.dise_number
#     # school_logo = school_obj.school_logo
#     # about_school = school_obj.about_school
#     # school_board = school_obj.board
#     try:
#         bank_obj = bank_models.Bank.objects.get(school_id=pk)
#     except:
#         bank_obj = None



#     if bank_obj is not None:
#         bank_name = ((bank_obj.bank_name).replace('[', '').replace(']', '').replace("'", '')).split(',')
#         ifsc_code = ((bank_obj.ifsc_code).replace('[', '').replace(']', '').replace("'", '')).split(',')
#         account_number = ((bank_obj.account_number).replace('[', '').replace(']', '').replace("'", '')).split(',')
#         branch_name = ((bank_obj.branch_name).replace('[', '').replace(']', '').replace("'", '')).split(',')
#         bank_details = [bank_name,ifsc_code,account_number,branch_name]
#     else:
#         bank_details=[]

#     if school_obj is not None:
#         school_details = [school_obj.school_name, school_obj.school_label, school_obj.iml_school_code,
#                       school_obj.school_address, school_obj.school_country.id, school_obj.school_state.id,
#                       school_obj.school_city.id, school_obj.pincode, school_obj.school_medium.id,
#                       school_obj.dias_number, school_obj.school_logo, school_obj.about_school,
#                       school_obj.school_board.id,str(school_obj.class_label),str(school_obj.division_label),
#                       school_obj.academic_year]
#     else:
#         school_details= []
#     role_id_list=[]
#     role_module_list=[]
#     wholesaler_data1=[]
#     user_roll_mappping_obj = user_models.UserRoleMapping.objects.filter(school=pk).values_list('group_id')
#     for i in user_roll_mappping_obj:
#         role_id_list.append(i[0])

#     roll_mappping = models_access.Role_Mapping.objects.filter(role_id__in=role_id_list).values_list('module_id')

#     for j in roll_mappping:
#         role_module_list.append(j[0])

#     print("role_module_list",role_id_list)

#     user_link_data= models.Master.objects.filter(id__in=role_module_list).values_list('id','module_name')
#     wholesaler_data1=[]
#     for w in user_link_data:
#         full_name1=str(w[1])
#         wholesaler_data={"name":full_name1,'id':w[0]}
#         wholesaler_data1.append(wholesaler_data)
#     print("wholesaler_data1",wholesaler_data1)

#     if request.method == 'POST':
#         data = {}
#         school_name = request.POST.get('school_name')
#         school_label = request.POST.get('school_label')
#         iml_school_code = request.POST.get('iml_school_code')
#         school_address = request.POST.get('school_address')
#         country = request.POST.get('country')
#         state = request.POST.get('state')
#         city = request.POST.get('city')
#         pincode = request.POST.get('pincode')
#         medium = request.POST.get('medium')
#         board = request.POST.get('board')
#         dise_no = request.POST.get('dise_no')
#         school_photo = request.FILES['school_photo']
#         about_school = request.POST.get('about_school')
#         class_label = request.POST.get('class_label')
#         exampleRadios = request.POST.get('exampleRadios')
#         commision_value = request.POST.get('commision_value')
#         school_admin_name = request.POST.get('school_admin_name')
#         email_id = request.POST.get('email_id')
#         school_admin_number = request.POST.get('school_admin_number')
#         disivion_label = request.POST.get('disivion_label')
#         bank_name = request.POST.getlist('bank_name[]')
#         account_no = request.POST.getlist('account_no[]')
#         ifsc_code = request.POST.getlist('ifsc_code[]')
#         branch_name = request.POST.getlist('branch_name[]')
#         print(type(bank_name),'============')

#         school_obj.school_name=school_name
#         school_obj.school_label=school_label
#         school_obj.iml_school_code=iml_school_code
#         school_obj.school_address=school_address
#         school_obj.school_country=country_models.Country.objects.get(id=country)
#         school_obj.school_state.id=state_models.State.objects.get(id=state)
#         school_obj.school_city.id=city_models.City.objects.get(id=city)
#         school_obj.pincode=pincode
#         school_obj.school_medium.id=medium_models.Medium.objects.get(id=medium)
#         school_obj.dias_number=dise_no
#         school_obj.school_logo=school_photo
#         school_obj.about_school=about_school
#         school_obj.school_board=board_models.Board.objects.get(id=board)
#         school_obj.class_label=class_label
#         school_obj.division_label=disivion_label
#         # school_obj.academic_year=a

#         bank_obj.bank_name=bank_name
#         bank_obj.ifsc_code=ifsc_code
#         bank_obj.account_number=account_no
#         bank_obj.branch_name=branch_name
#         school_obj.save()
#         bank_obj.save()





#         # data = {"module_name": module_name, "module_description": module_description, 'user_id': module_id,
#         #             "module_path": module_path, "module_icon": module_icon, 'action_name_list': action_name_list,
#         #             'action_url_list': action_url_list}
#     return render(request, 'edit_school.html',
#                       {'data': data, "country_data": country_data, "state_data": state_data, "city_data": city_data,
#                        'board_data': board_data, 'medium_data': medium_data, 'module_manager_data': wholesaler_data1,
#                        'school_details': school_details,'bank_details':bank_details})

# @csrf_exempt
# def view_school(request, pk):

#     country_data = get_country()
#     state_data = get_state()
#     city_data = get_city()
#     board_data = get_board()
#     medium_data = get_medium()
#     module_manager_data = get_module_manager()

#     try:
#         school_obj = school_models.School.objects.get(id=pk)
#     except:
#         school_obj = None

#     try:
#         bank_obj = bank_models.Bank.objects.get(school_id=pk)
#     except:
#         bank_obj = None
#     if bank_obj is not None:
#         bank_name = ((bank_obj.bank_name).replace('[', '').replace(']', '').replace("'", '')).split(',')
#         ifsc_code = ((bank_obj.ifsc_code).replace('[', '').replace(']', '').replace("'", '')).split(',')
#         account_number = ((bank_obj.account_number).replace('[', '').replace(']', '').replace("'", '')).split(',')
#         branch_name = ((bank_obj.branch_name).replace('[', '').replace(']', '').replace("'", '')).split(',')
#         bank_details = [bank_name,ifsc_code,account_number,branch_name]
#     else:
#         bank_details=[]

#     if school_obj is not None:
#         school_details = [school_obj.school_name, school_obj.school_label, school_obj.iml_school_code,
#                       school_obj.school_address, school_obj.school_country.id, school_obj.school_state.id,
#                       school_obj.school_city.id, school_obj.pincode, school_obj.school_medium.id,
#                       school_obj.dias_number, school_obj.school_logo, school_obj.about_school,
#                       school_obj.school_board.id,str(school_obj.class_label),str(school_obj.division_label),
#                       school_obj.academic_year]
#     else:
#         school_details= []

#     return render(request, 'view_school.html',
#                       {"country_data": country_data, "state_data": state_data, "city_data": city_data,
#                        'board_data': board_data, 'medium_data': medium_data, 'module_manager_data': module_manager_data,
#                        'school_details': school_details,'bank_details':bank_details})


@csrf_exempt
def view_school(request,user_id_pk,school_id_pk):

    country_data = get_country()
    state_data = get_state()
    city_data = get_city()
    board_data = get_board()
    medium_data = get_medium()
    module_manager_data = get_module_manager()
    school_photo = "/media/default/placeholder.png"
    try:
        school_obj = school_models.School.objects.get(id=school_id_pk)
    except:
        school_obj = None

    bank_obj = bank_models.Bank.objects.filter(school_id=school_id_pk).values('id', 'bank_name', 'ifsc_code',
                                                                              'account_number', 'branch_name')
    bank_details = []
    for i in bank_obj:
        bank_details.append(i)
    print(bank_details)
    if school_obj is not None:
        school_details = [str(school_obj.school_name), str(school_obj.school_label), str(school_obj.iml_school_code),
                          str(school_obj.school_address), str(school_obj.school_country.id), str(school_obj.school_state.id),
                          str(school_obj.school_city.id), str(school_obj.pincode), str(school_obj.school_medium.id),
                          str(school_obj.dias_number), str(school_obj.school_logo), str(school_obj.about_school),
                          str(school_obj.school_board.id),str(school_obj.class_label),str(school_obj.division_label),
                          str(school_obj.academic_year),str(school_obj.commission_type),str(school_obj.commission_value)]
    else:
        school_details= []
    try:
        user_obj = user_models.User.objects.get(username=user_id_pk)
    except:
        user_obj = None

    if user_obj is not None:

        school_admin_number = user_obj.username
        school_admin_name = user_obj.first_name
        email = user_obj.email
        school_admin_details_list = [school_admin_number, school_admin_name, email]
    else:
        school_admin_details_list = []

    return render(request, 'view_school.html',
                      {"country_data": country_data, "state_data": state_data, "city_data": city_data,
                       'board_data': board_data, 'medium_data': medium_data, 'module_manager_data': module_manager_data,
                       'school_details': school_details,'bank_details':bank_details,'school_admin_details_list':school_admin_details_list,'school_photo':school_photo})


def send_file(request):
   file_path="C:/Users/Downloads/sample_test.xlsx" #Enter your file path here where you store the master files
   if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response





@csrf_exempt
def check_bank_dtls(request):
    account_no = request.POST.get('account_no')
    ifsc_code = request.POST.get('ifsc_code')
    school_label = request.POST.get('school_label')
    print(account_no, ifsc_code, school_label)
    try:
        school_obj = school_models.School.objects.get(school_label=school_label)
        school_id = school_obj.id
    except:
        school_obj = None
        school_id = ''
    if school_obj is not None:
        try:
            bank_obj = bank_models.Bank.objects.get(school_id=school_obj, account_no=account_no, ifsc_code=ifsc_code)
        except:
            bank_obj = None

        if bank_obj is not None:
            bank_name = ((bank_obj.bank_name).replace('[', '').replace(']', '').replace("'", '')).split(',')
            ifsc_code = ((bank_obj.ifsc_code).replace('[', '').replace(']', '').replace("'", '')).split(',')
            account_number = ((bank_obj.account_number).replace('[', '').replace(']', '').replace("'", '')).split(',')
            branch_name = ((bank_obj.branch_name).replace('[', '').replace(']', '').replace("'", '')).split(',')
            bank_details = [bank_name, ifsc_code, account_number, branch_name]
            count = 0
            print(bank_details)
            for i in range(0, int(len((bank_details[0])) + 1)):
                if account_number == account_number[i] and ifsc_code == ifsc_code[i]:
                    count = count + 1
            if count > 0:
                res = "false"
            else:
                res = "true"
            return HttpResponse(res)

        else:
            res = "true"
            return HttpResponse(res)
    else:
        res = "true"
        return HttpResponse(res)

@csrf_exempt
def check_school_lable(request):
    school_label = request.POST.get('school_label')

    try:
        school_obj = school_models.School.objects.get(school_label=school_label)
    except:
        school_obj = None

    if school_obj is not None:
        if school_obj.school_label != school_label:
            res="false"
        else:
            res="true"

        return HttpResponse(res)
    res = "true"
    return HttpResponse(res)

@csrf_exempt
def check_edit_school_lable(request):
    school_label = request.POST.get('school_label')
    school_id_pk = request.POST.get('school_id_pk')

    try:
        school_obj = school_models.School.objects.get(school_label=school_label)
    except:
        school_obj = None
    if school_obj is not None:
        if school_models.School.objects.get(id=school_id_pk).school_label != school_label:
            res="false"
        else:
            res = "true"
        return HttpResponse(res)
    res = "true"
    return HttpResponse(res)





