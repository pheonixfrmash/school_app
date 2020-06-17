
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
from fees import models as fees_models



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

@login_required
@csrf_exempt
# @transaction.atomic
def add_fees(request):
    action_name=''
    action_url=''

    user_id = request.user.id
    school_id = user_models.UserProfile.objects.get(user =  user_id).school_id
    bank_list = bank_models.Bank.objects.filter(school_id=school_id).values('id','bank_name','account_number')

    action_id_list=[]
    bank_deatils=[]
    jsonlist=[]
    datajsonlist={}
    if request.method == 'POST':
        bank_name = request.POST.get('fees_bank_name')
        fees_desc = request.POST.get('fees_desc')
        fees_title = request.POST.get('fees_title')

        try:
            bank_id = bank_models.Bank.objects.get(id=bank_name)
        except:
            bank_id = None
        try:
           userprofile_id = user_models.UserProfile.objects.get(user_id=user_id)
        except:
           userprofile_id = None

        new_fees = fees_models.Fees.objects.create(title=fees_title,description=fees_desc,bank_id=bank_id,school_id=school_id,posted_by=userprofile_id)
        new_fees.save()

        response=JsonResponse({'status':'success'})
        return response

    else:
        return render(request, 'add_fees.html', {'bank_list':bank_list})


@login_required
@csrf_exempt
def get_manage_fees(request):
    data = []
    user_type = ""
    district = ""
    state = ""
    count = 0
    row = []
    request_user_profile=User.objects.filter(username=str(request.user))
    school_id=user_models.UserProfile.objects.filter(user=request_user_profile[0].id).values_list('school_id')
    fees_info = fees_models.Fees.objects.filter(school_id=school_id[0][0]).values_list('id','title', 'description', 'bank_id__bank_name','bank_id__account_number', 'status').order_by(
        '-id')
    for i in fees_info:
        fees_id = i[0]
        fees_title = i[1]
        fees_desc = i[2]
        bank_name = i[3]
        account_no = i[4]
        status = i[5]
        count += 1

        # if status == True:
        #     status = 'Inactive'
        #     icon = 'fas fa-times'
        # else:
        #     status = 'Active'
        #     icon = 'fas fa-check'
        if status == True:
            status = 'Active'
        else:
            status = 'Inactive'

        data.append([count,str(fees_title), str(fees_desc), str(bank_name), str(account_no), str(status), "<a href='/fees/edit_fees/" + str(
                         fees_id)+ "' class='btn'><i class='fas fa-edit'></i> Edit</a>",
                     "<a href='/fees/view_fees/" + str(
                         fees_id) + "' class='btn'><i class='fas fa-eye'></i> View</a>",
                     "<a href='/fees/block_fees/" + str(
                         fees_id) + "' class='btn'><i class='fas fa-times'></i>Block</a>"])
#print("data",data)
    return render(request, 'get_fees.html', {'data': (data)})


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
        group_obj = Group.objects.create(name='school_admin_' + school_name)
        print('----gggg-------kkkkk-----')
        new_school.save()
        new_user.save()
        userprofile.save()
        group_obj.save()
        # group_id = group_obj.id
        # user_roll_mappping_obj = user_models.UserRoleMapping.objects.create(user_id=new_Uid, group_id=group_id,
        #                                                                     school=school_id)
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
def edit_fees(request, fees_id_pk):
    user_id = request.user.id
    school_id = user_models.UserProfile.objects.get(user=user_id).school_id
    bank_list = bank_models.Bank.objects.filter(school_id=school_id).values('id', 'bank_name', 'account_number')

    try:
        fees_obj = fees_models.Fees.objects.get(id=fees_id_pk)
    except:
        fees_obj = None
    if fees_obj is  not None:
        data=[str(fees_obj.description),str(fees_obj.bank_id.id),str(fees_obj.bank_id.account_number),str(fees_obj.title)]
    else:
        data=[]


    if request.method == 'POST':

        bank_name = request.POST.get('fees_bank_name')
        fees_desc = request.POST.get('fees_desc')
        fees_title = request.POST.get('fees_title')

        try:
            bank_id = bank_models.Bank.objects.get(id=bank_name)
        except:
            bank_id = None

        try:
           userprofile_id = user_models.UserProfile.objects.get(user_id=user_id)
        except:
           userprofile_id = None

        fees_obj = fees_models.Fees.objects.get(id=fees_id_pk)
        fees_obj.description = fees_desc
        fees_obj.bank_id=bank_id
        fees_obj.posted_by=userprofile_id
        fees_obj.title=fees_title
        fees_obj.save()

        response=JsonResponse({'status':'success','msg':"Fees Updated Successfully"})
        return response

    return render(request, 'edit_fees.html',
                      {'data': data,'fees_id_pk':fees_id_pk,'bank_list':bank_list })

@csrf_exempt
def view_fees(request, fees_id_pk):
    user_id = request.user.id
    school_id = user_models.UserProfile.objects.get(user=user_id).school_id
    bank_list = bank_models.Bank.objects.filter(school_id=school_id).values('id', 'bank_name', 'account_number')

    try:
        fees_obj = fees_models.Fees.objects.get(id=fees_id_pk)
    except:
        fees_obj = None
    if fees_obj is not None:
        data = [str(fees_obj.description), str(fees_obj.bank_id.bank_name), str(fees_obj.bank_id.account_number),str(fees_obj.title)]
    else:
        data = []

    return render(request, 'view_fees.html',
                  {'data': data, 'fees_id_pk': fees_id_pk, 'bank_list': bank_list})
def send_file(request):

    file_path="C:/Users/ANAND/Downloads/sample_test.xlsx"
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
def get_account_no(request):
    if request.method == 'POST':
        bank_id=request.POST.get('bank_id')
        try:
            account_no = bank_models.Bank.objects.get(id=bank_id).account_number
        except:
            account_no = None
        if account_no is not None:
            response=JsonResponse({'status':'success','account_no':account_no})
        else:
            response = JsonResponse({'status': 'success', 'account_no': 'Not found'})
        return response


