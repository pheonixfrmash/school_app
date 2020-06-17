from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
import json
from django.db.models import Count
from django.db.models import Q
from django.utils.timezone import get_current_timezone
from datetime import datetime
import dateutil.parser
# from django.utils.encoding import smart_str, smart_unicode
import os
from operator import itemgetter
from datetime import timedelta
import io, csv
from pyfcm import FCMNotification
from django.db.models import Sum
from django.db import transaction
from users import views, templates
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
from competitive_exam import models as exam_models
from class_master import models as class_models


@csrf_exempt
def get_country():
    conutry_data = []
    state_list = country_models.Country.objects.all().values_list('id', 'country_name')
    for i in state_list:
        case2 = {'id': i[0], 'name': i[1].capitalize()}
        conutry_data.append(case2)
    conutry_data = sorted(conutry_data, key=itemgetter('name'))
    return conutry_data


@csrf_exempt
def get_school():
    school_data = []
    school_list = school_models.School.objects.all().values_list('id', 'school_name')
    for i in school_list:
        case2 = {'id': i[0], 'name': i[1].capitalize()}
        school_data.append(case2)
    school_data = sorted(school_data, key=itemgetter('name'))
    return school_data


@csrf_exempt
def get_state():
    state_data = []
    state_list = state_models.State.objects.all().values_list('id', 'state_name')
    for i in state_list:
        case2 = {'id': i[0], 'name': i[1].capitalize()}
        state_data.append(case2)
    state_data = sorted(state_data, key=itemgetter('name'))
    return state_data


@csrf_exempt
def get_city():
    city_data = []
    city_list = city_models.City.objects.all().values_list('id', 'city_name')
    for i in city_list:
        case2 = {'id': i[0], 'name': i[1]}
        city_data.append(case2)
    return city_data


@csrf_exempt
def get_board():
    board_data = []
    board_list = board_models.Board.objects.all().values_list('id', 'board_name')
    for i in board_list:
        case2 = {'id': i[0], 'name': i[1]}
        board_data.append(case2)
    return board_data


@csrf_exempt
def get_medium():
    medium_data = []
    medium_list = medium_models.Medium.objects.all().values_list('id', 'medium_name')
    for i in medium_list:
        case2 = {'id': i[0], 'name': i[1]}
        medium_data.append(case2)
    return medium_data


@csrf_exempt
def get_module_list():
    models_data = []
    module_list = models.Master.objects.all().values_list('id', 'module_name')
    for i in module_list:
        case2 = {'id': i[0], 'name': i[1]}
        models_data.append(case2)
    models_data = sorted(models_data, key=itemgetter('name'))
    return models_data


@csrf_exempt
def get_class():
    class_data = []
    state_list = class_models.class_master.objects.all().values_list('id', 'class_name')
    for i in state_list:
        case2 = {'id': i[0], 'name': i[1].capitalize()}
        class_data.append(case2)
    class_data = sorted(class_data, key=itemgetter('name'))
    return class_data


@csrf_exempt
def get_school_list(request):
    if request.method == 'POST':
        school_data = []
        city = request.POST.get('city')
        print("city", city)
        city = json.loads(city)
        medium = request.POST.get('medium')
        medium = json.loads(medium)
        board = request.POST.get('board')
        board = json.loads(board)
        # state=request.POST.get('state')
        # state=json.loads(state)
        # state_id=json.loads(state_id)
        city_list = class_models.school_class_mapping.objects.filter(school_id__school_city__in=city,
                                                                     school_id__school_medium__in=medium,
                                                                     school_id__school_board__in=board,
                                                                     status=1).values_list('id',
                                                                                           'school_id__school_name',
                                                                                           'school_id__school_city__city_name',
                                                                                           'school_id')
        for i in city_list:
            case2 = {'id': str(i[3]), 'name': i[1] + ' - ' + i[2]}
            if case2 in school_data:
                print('Exists')
            else:
                school_data.append(case2)
                school_data = sorted(school_data, key=itemgetter('name'))

        response = JsonResponse({'status': 'success', 'school_data': school_data})
        return response


@login_required
@csrf_exempt
@transaction.atomic
def add_competitive_exam(request):
    action_name = ''
    action_url = ''
    country_data = get_country()
    state_data = get_state()
    city_data = get_city()
    board_data = get_board()
    medium_data = get_medium()
    module_data = get_module_list()
    school_data = []
    class_data = get_class()
    action_id_list = []
    bank_deatils = []
    jsonlist = []
    school_data12 = []
    datajsonlist = {}
    class_list1 = []
    datarequest = {}
    if request.method == 'POST':

        exam_name = request.POST.get('exam_name')
        description = request.POST.get('description')
        country = request.POST.getlist('country')
        # country=json.loads(country)
        state = request.POST.getlist('state')
        # state=json.loads(state)
        # state = request.POST.get('state')
        city = request.POST.getlist('city')
        # city=json.loads(city)
        print("state", state)
        medium = request.POST.getlist('medium')
        print("mediummedium", medium)
        # medium=json.loads(medium)
        board = request.POST.getlist('board')
        # board=json.loads(board)
        pincode = request.POST.get('pincode')
        school = request.POST.getlist('school')
        # school=json.loads(school)
        class_name = request.POST.getlist('class_master')
        print("class_name", class_name)
        # input()
        # class_name=json.loads(class_name)
        amount = request.POST.get('amount')
        per = request.POST.get('per')
        total_amount = request.POST.get('total_amount')
        start_date = request.POST.get('start_date')

        last_date = request.POST.get('last_date')

        exam_date = request.POST.get('exam_date')

        datarequest = {'country': country, 'state': state, 'city': city, 'board': board, 'medium': medium,
                       'school': school, 'class_name': class_name}

        print("datarequest", datarequest)

        # input()
        new_module = exam_models.Competitive_Exam_Master.objects.create(exam_name=exam_name,
                                                                        exam_description=description,
                                                                        start_date=start_date, last_date=last_date,
                                                                        exam_date=exam_date)

        new_module.save()
        newSid = new_module.id

        school_count = class_models.school_class_mapping.objects.all().count()
        school_count_front = class_models.school_class_mapping.objects.filter(school_id__in=school).count()

        if school_count_front == school_count:
            school_id = ''
            class_id = ''
            try:
                school = school_models.School.objects.get(id=school_id)
            except:
                school = None

            try:
                class_master = class_models.class_master.objects.get(id=class_id)
            except:
                class_master = None

            exam_id = exam_models.Competitive_Exam_Master.objects.get(id=newSid)
            new_transaction = exam_models.Competitive_Exam_Transaction.objects.create(competitive_exam=exam_id,
                                                                                      exam_school=school,
                                                                                      exam_class=class_master,
                                                                                      exam_amount=amount, exam_tax=per,
                                                                                      exam_total_amount=total_amount,
                                                                                      request_data=datarequest)

            new_transaction.save()

            response = JsonResponse({'status': 'success', 'exam_id': new_transaction.id})
            return response
        else:
            exam_id = exam_models.Competitive_Exam_Master.objects.get(id=newSid)
            new_transaction = exam_models.Competitive_Exam_Transaction.objects.create(competitive_exam=exam_id,
                                                                                      exam_amount=amount,
                                                                                      exam_tax=per,
                                                                                      exam_total_amount=total_amount,
                                                                                      request_data=datarequest)

            new_transaction.save()

            response = JsonResponse({'status': 'success', 'exam_id': new_transaction.id})
            return response

    else:
        return render(request, 'add_competitive_exam.html',
                      {"country_data": country_data, "state_data": state_data, "city_data": city_data,
                       'school_data': school_data, 'module_data': module_data,
                       'board_data': board_data, 'medium_data': medium_data, 'class_data': class_data})


@csrf_exempt
def edit_competitive_exam(request, competitive_exam_id_pk):
    print(competitive_exam_id_pk)
    print('_________________________')
    resource_id = id
    data = {}
    country_data = get_country()
    state_data = get_state()
    city_data = get_city()
    board_data = get_board()
    medium_data = get_medium()
    school_data = get_school()
    class_data = get_class()
    try:
        competitive_exam_transaction_obj = exam_models.Competitive_Exam_Transaction.objects.get(
            id=int(competitive_exam_id_pk))
    except:
        competitive_exam_transaction_obj = None

    if competitive_exam_transaction_obj is not None:
        competitive_exam_data = [str(competitive_exam_transaction_obj.competitive_exam.exam_name),
                                 str(competitive_exam_transaction_obj.competitive_exam.exam_description),
                                 str(competitive_exam_transaction_obj.exam_tax),
                                 str(competitive_exam_transaction_obj.exam_amount),
                                 str(competitive_exam_transaction_obj.exam_total_amount),
                                 str(competitive_exam_transaction_obj.competitive_exam.start_date.strftime("%Y-%m-%d")),
                                 str(competitive_exam_transaction_obj.competitive_exam.exam_date.strftime("%Y-%m-%d")),
                                 str(competitive_exam_transaction_obj.competitive_exam.last_date.strftime("%Y-%m-%d"))]
    else:
        competitive_exam_data = []

    try:
        response_data = eval(competitive_exam_transaction_obj.request_data)
    except:
        response_data = None
    if response_data is not None:
        all_country = response_data['country']
        all_city = response_data['city']
        all_state = response_data['state']
        all_school = response_data['school']
        all_medium = response_data['medium']
        all_board = response_data['board']
        all_class = response_data['class_name']
        competitive_exam_transaction_data = [all_country, all_state, all_city, all_school, all_class, all_board,
                                             all_medium,
                                             ]
        print(competitive_exam_transaction_data)
    else:
        competitive_exam_transaction_data = []
        response = JsonResponse({'status': 'error', 'message': 'Data no fount'})
        return response
    if request.method == 'POST':
        exam_name = request.POST.get('exam_name')
        description = request.POST.get('description')
        country = request.POST.getlist('country')
        state = request.POST.getlist('state')
        city = request.POST.getlist('city')
        medium = request.POST.getlist('medium')
        board = request.POST.getlist('board')
        school = request.POST.getlist('school')
        class_name = request.POST.getlist('class_master')
        amount = request.POST.get('amount')
        per = request.POST.get('per')
        total_amount = request.POST.get('total_amount')
        start_date = request.POST.get('start_date')
        last_date = request.POST.get('last_date')
        exam_date = request.POST.get('exam_date')

        datarequest = {'country': country, 'state': state, 'city': city, 'board': board, 'medium': medium,
                       'school': school, 'class_name': class_name}

        print("datarequest", datarequest)

        # input()

        competitive_exam_master_id = competitive_exam_transaction_obj.competitive_exam_id
        competitive_exam_master_obj = exam_models.Competitive_Exam_Master.objects.get(id=competitive_exam_master_id)
        competitive_exam_master_obj.exam_name = exam_name
        competitive_exam_master_obj.exam_description = description
        competitive_exam_master_obj.start_date = start_date
        competitive_exam_master_obj.last_date = last_date
        competitive_exam_master_obj.exam_date = exam_date

        school_count = class_models.school_class_mapping.objects.all().count()
        school_count_front = class_models.school_class_mapping.objects.filter(school_id__in=school).count()

        if school_count_front == school_count:
            school_id = ''
            class_id = ''
            try:
                school = school_models.School.objects.get(id=school_id)
            except:
                school = None

            try:
                class_master = class_models.class_master.objects.get(id=class_id)
            except:
                class_master = None
            competitive_exam_transaction_obj.exam_school = school
            competitive_exam_transaction_obj.exam_class = class_master
            competitive_exam_transaction_obj.exam_amount = amount
            competitive_exam_transaction_obj.exam_tax = per
            competitive_exam_transaction_obj.exam_total_amount = total_amount
            competitive_exam_transaction_obj.request_data = datarequest
            competitive_exam_transaction_obj.save()

            response = JsonResponse({'status': 'success', 'exam_id': competitive_exam_transaction_obj.id})
            return response
        else:

            competitive_exam_transaction_obj.exam_tax = per
            competitive_exam_transaction_obj.exam_total_amount = total_amount
            competitive_exam_transaction_obj.request_data = datarequest
            competitive_exam_transaction_obj.save()

            response = JsonResponse({'status': 'success', 'exam_id': competitive_exam_transaction_obj.id})
            return response

    return render(request, 'edit_competitive_exam.html',
                  {"country_data": country_data, "school_data": school_data, "state_data": state_data,
                   "city_data": city_data,
                   'board_data': board_data, 'medium_data': medium_data, 'competitive_exam_id': competitive_exam_id_pk,
                   "class_data": class_data, 'competitive_exam_data': competitive_exam_data,
                   'competitive_exam_transaction_data': competitive_exam_transaction_data,
                   'resource_id': resource_id})


@csrf_exempt
def view_competitive_exam(request, competitive_exam_id_pk):
    print(competitive_exam_id_pk)
    print('_________________________')
    resource_id = id
    data = {}
    country_data = get_country()
    state_data = get_state()
    city_data = get_city()
    board_data = get_board()
    medium_data = get_medium()
    school_data = get_school()
    class_data = get_class()
    try:
        competitive_exam_transaction_obj = exam_models.Competitive_Exam_Transaction.objects.get(
            id=int(competitive_exam_id_pk))
    except:
        competitive_exam_transaction_obj = None

    if competitive_exam_transaction_obj is not None:
        competitive_exam_data = [str(competitive_exam_transaction_obj.competitive_exam.exam_name),
                                 str(competitive_exam_transaction_obj.competitive_exam.exam_description),
                                 str(competitive_exam_transaction_obj.exam_tax),
                                 str(competitive_exam_transaction_obj.exam_amount),
                                 str(competitive_exam_transaction_obj.exam_total_amount),
                                 str(competitive_exam_transaction_obj.competitive_exam.start_date.strftime("%Y-%m-%d")),
                                 str(competitive_exam_transaction_obj.competitive_exam.exam_date.strftime("%Y-%m-%d")),
                                 str(competitive_exam_transaction_obj.competitive_exam.last_date.strftime("%Y-%m-%d"))]
    else:
        competitive_exam_data = []

    try:
        response_data = eval(competitive_exam_transaction_obj.request_data)
    except:
        response_data = None
    if response_data is not None:
        all_country = response_data['country']
        all_city = response_data['city']
        all_state = response_data['state']
        all_school = response_data['school']
        all_medium = response_data['medium']
        all_board = response_data['board']
        all_class = response_data['class_name']
        competitive_exam_transaction_data = [all_country, all_state, all_city, all_school, all_class, all_board,
                                             all_medium,
                                             ]

    else:
        competitive_exam_transaction_data = []

    return render(request, 'view_competitive_exam.html',
                  {"country_data": country_data, "school_data": school_data, "state_data": state_data,
                   "city_data": city_data,
                   'board_data': board_data, 'medium_data': medium_data, 'competitive_exam_id': competitive_exam_id_pk,
                   "class_data": class_data, 'competitive_exam_data': competitive_exam_data,
                   'competitive_exam_transaction_data': competitive_exam_transaction_data,
                   'resource_id': resource_id})


@login_required
@csrf_exempt
# @transaction.atomic
def cancel_competitive_exam(request, pk):
    if request.method == 'POST':

        try:
            exam_transaction = exam_models.Competitive_Exam_Transaction.objects.get(id=pk)
        except:
            exam_transaction = None
        if exam_transaction is not None:
            exam_models.Competitive_Exam_Transaction.objects.filter(id=pk).delete()
            try:
                exam_master_obj = exam_models.Competitive_Exam_Master.objects.get(
                    id=exam_transaction.competitive_exam_id)
            except:
                exam_master_obj = None
            if exam_master_obj is not None:
                exam_master_obj.delete()
                response = JsonResponse({'status': 'success', 'msg': 'Exam canceled successfully'})
                return response
            else:
                response = JsonResponse({'status': 'error', 'msg': 'Exam details not found'})
                return response
        else:
            response = JsonResponse({'status': 'error', 'msg': 'Exam details not found'})
            return response
    return HttpResponseRedirect('/competitive_exam/')


def post_competitive_exam(request, pk):
    action_name = ''
    action_url = ''
    country_data = get_country()
    state_data = get_state()
    city_data = get_city()
    board_data = get_board()
    medium_data = get_medium()
    module_data = get_module_list()
    school_data = get_school()
    action_id_list = []
    bank_deatils = []
    jsonlist = []
    datajsonlist = {}
    print(pk)
    exam_obj = exam_models.Competitive_Exam_Transaction.objects.filter(id=pk).values('id',
                                                                                     'competitive_exam__exam_name',
                                                                                     'competitive_exam__exam_description',
                                                                                     'request_data',
                                                                                     'competitive_exam__exam_date',
                                                                                     'competitive_exam__start_date',
                                                                                     'competitive_exam__last_date',
                                                                                     'exam_total_amount',
                                                                                     'exam_amount',
                                                                                     'exam_tax')
    print(exam_obj)
    exam_list = []
    for i in exam_obj:
        exam_list.append(i)
        break
    print(exam_list, '______')
    if len(exam_list) != 0:
        exam_name = exam_list[0]['competitive_exam__exam_name']

        exam_desc = exam_list[0]['competitive_exam__exam_description']
        response_data = exam_list[0]['request_data']
        start_date = exam_list[0]['competitive_exam__start_date']
        last_date = exam_list[0]['competitive_exam__last_date']
        exam_date = exam_list[0]['competitive_exam__exam_date']
        amount = exam_list[0]['exam_amount']
        tax = exam_list[0]['exam_tax']
        total_amount = exam_list[0]['exam_total_amount']

        try:
            response_data = eval(response_data)
        except:
            response_data = None
        if response_data is not None:
            state = response_data['state']
            city = response_data['city']
            school = response_data['school']
            class_name = response_data['class_name']

            state_id_list = [int(i) for i in state]
            city_id_list = [int(i) for i in city]
            school_id_list = [int(i) for i in school]
            class_id_list = [int(i) for i in class_name]

            school_id_value = str(school_id_list).replace('[', '').replace(']', '')

            if len(school) == 1:
                school_state = school_models.School.objects.filter(id=(school_id_value)).values('id', 'school_state')
            else:
                school_state = school_models.School.objects.filter(id__in=school_id_list).values('id',
                                                                                                 'school_state')

            state_count = state_models.State.objects.filter().aggregate(Count('id'))
            state_name_list = []
            if state_count['id__count'] == len(school_state):
                all_state = 'All'
            else:
                for i in school_state:
                    state_name = state_models.State.objects.get(id=int(i['school_state'])).state_name
                    state_name_list.append(state_name)
                all_state = str(state_name_list).replace('[', '').replace(']', '').replace("'", "")
            if len(school) == 1:
                school_city = school_models.School.objects.filter(id=(school_id_value)).values('id', 'school_city')
            else:
                school_city = school_models.School.objects.filter(id__in=(school_id_list)).values('id', 'school_city')

            city_count = city_models.City.objects.filter().aggregate(Count('id'))

            city_name_list = []
            if city_count['id__count'] == len(school_city):
                all_city = 'All'
            else:
                for i in school_city:
                    city_name = city_models.City.objects.get(id=int(i['school_city'])).city_name
                    city_name_list.append(city_name)
                all_city = str(city_name_list).replace('[', '').replace(']', '').replace("'", "")

            if len(class_name) == 1:
                school_class = class_models.school_class_mapping.objects.filter(school_id=int(school_id_value)).values(
                    'class_id', 'class_id')
            else:
                school_class = class_models.school_class_mapping.objects.filter(school_id__in=(school_id_list)).values(
                    'id',
                    'class_id')
            class_count = class_models.school_class_mapping.objects.filter().aggregate(Count('id'))
            class_name_list = []
            if class_count['id__count'] == len(school_class):
                all_class = 'All'
            else:
                for i in class_name:
                    class_name = class_models.class_master.objects.get(id=int(i)).class_name
                    class_name_list.append(class_name)
                all_class = str(class_name_list).replace('[', '').replace(']', '').replace("'", "")

            school_count = school_models.School.objects.filter().aggregate(Count('id'))
            school_name_list = []
            if school_count['id__count'] == len(school):
                all_school = 'All'
            else:
                for i in school:
                    if str(i).find('_') >= 0:
                        i = (i.split('_'))[0]

                    else:
                        i = i

                    school_name = school_models.School.objects.get(id=int(i)).school_name
                    school_name_list.append(school_name)
                all_school = str(school_name_list).replace('[', '').replace(']', '').replace("'", "")
        else:
            all_class = 'All'
            all_school = 'All'
            all_city = 'All'
            all_state = 'All'

        exam_dtls = [exam_name, exam_desc, all_state, all_city, all_school, all_class,
                     str(start_date.strftime("%d/%m/%Y")), str(last_date.strftime("%d/%m/%Y")),
                     str(exam_date.strftime("%d/%m/%Y")), amount, tax, total_amount]
    else:
        exam_dtls = []

    if request.method == 'POST':
        print('__________poooost_____________')
        exam_models.Competitive_Exam_Transaction.objects.filter(id=pk).update(confirm_status=True)
        response = JsonResponse({'status': 'success'})
        return response

    else:
        print("Elseee")
        return render(request, 'post_competitive_exam.html',
                      {"country_data": country_data, "state_data": state_data, "city_data": city_data,
                       'school_data': school_data, 'medium_data': medium_data, 'module_data': module_data,
                       'exam_dtls': exam_dtls, 'id': pk})


@login_required
@csrf_exempt
def get_competitive_exam(request):
    data = []
    user_type = ""
    district = ""
    state = ""
    count = 0
    row = []
    user_info = exam_models.Competitive_Exam_Transaction.objects.filter(confirm_status=True).values_list('id',
                                                                                                         'competitive_exam__exam_name',
                                                                                                         'exam_school__school_name',
                                                                                                         'exam_class__class_name',
                                                                                                         'competitive_exam__start_date',
                                                                                                         'competitive_exam__last_date',
                                                                                                         'competitive_exam__exam_date',
                                                                                                         'exam_total_amount',
                                                                                                         'paid_by').order_by(
        '-id')
    for i in user_info:
        exam_name = str(i[1])
        school_name = str(i[2])
        class_name = str(i[3])
        start_date = i[4]
        formatedDate = start_date.strftime("%d-%m-%Y")
        last_date = i[5]
        formatedDate1 = last_date.strftime("%d-%m-%Y")
        exam_date = i[6]
        formatedDate2 = exam_date.strftime("%d-%m-%Y")
        exam_amount = i[7]
        paid_by = i[8]

        try:
            exam_obj = exam_models.Competitive_Exam_Transaction.objects.get(id=i[0])
        except:
            exam_obj = None

        response_data = exam_obj.request_data
        print(response_data)
        try:
            response_data = eval(response_data)
        except:
            response_data = None
        if response_data is not None:
            country = response_data['country']
            country_name = country_models.Country.objects.get(id=int(country[0])).country_name
            state = response_data['state']
            city = response_data['city']
            school = response_data['school']
            class_name = response_data['class_name']
            board = response_data['board']
            medium = response_data['board']

            class_count = class_models.class_master.objects.filter().aggregate(Count('id'))
            class_name_list = []
            if class_count['id__count'] == len(class_name):
                all_class = 'All'
            else:
                for i in class_name:
                    class_name = class_models.class_master.objects.get(id=int(i)).class_name
                    class_name_list.append(class_name)
                all_class = str(class_name_list).replace('[', '').replace(']', '').replace("'", "")

            medium_count = medium_models.Medium.objects.filter().aggregate(Count('id'))
            medium_name_list = []
            if medium_count['id__count'] == len(medium):
                all_medium = 'All'
            else:
                for i in medium:
                    medium_name = medium_models.Medium.objects.get(id=int(i)).medium_name
                    medium_name_list.append(medium_name)
                all_medium = str(medium_name_list).replace('[', '').replace(']', '').replace("'", "")

            board_count = board_models.Board.objects.filter().aggregate(Count('id'))
            board_name_list = []
            if board_count['id__count'] == len(board):
                all_board = 'All'
            else:
                for i in board:
                    board_name = board_models.Board.objects.get(id=int(i)).board_name
                    board_name_list.append(board_name)
                all_board = str(board_name_list).replace('[', '').replace(']', '').replace("'", "")

            school_count = school_models.School.objects.filter().aggregate(Count('id'))
            school_name_list = []
            if school_count['id__count'] == len(school):
                all_school = 'All'
            else:
                for i in school:
                    school_name = school_models.School.objects.get(id=int(i)).school_name
                    school_name_list.append(school_name)
                all_school = str(school_name_list).replace('[', '').replace(']', '').replace("'", "")

            state_count = state_models.State.objects.filter().aggregate(Count('id'))
            state_name_list = []
            if state_count['id__count'] == len(state):
                all_state = 'All'
            else:
                for i in state:
                    state_name = state_models.State.objects.get(id=int(i)).state_name
                    state_name_list.append(state_name)
                all_state = str(state_name_list).replace('[', '').replace(']', '').replace("'", "")

            city_count = city_models.City.objects.filter().aggregate(Count('id'))
            city_name_list = []
            if city_count['id__count'] == len(city):
                all_city = 'All'
            else:
                for i in city:
                    city_name = city_models.City.objects.get(id=int(i)).city_name
                    city_name_list.append(city_name)
                all_city = str(city_name_list).replace('[', '').replace(']', '').replace("'", "")

        else:
            all_city = 'All'
            all_state = 'All'
            country_name = 'All'
            all_school = 'All'
            all_class = 'All'
        count += 1

        # btn="<div class='editBut'><button class='btn btn-block btn-danger btn-sm delete' data-module_id="+str(school_id)+">Delete</button></div>"



        data.append(
            [count, str(exam_name), str(all_state), str(all_city), str(all_school), str(all_class), str(country_name),
             str(formatedDate), str(formatedDate1), str(formatedDate2), str(exam_amount), str(paid_by),
             "<a href='/competitive_exam/edit_competitive_exam/" + str(
                 exam_obj.id) + "' class='btn'><i class='fas fa-edit'></i> Edit</a>",
             "<a href='/competitive_exam/view_competitive_exam/" + str(
                 exam_obj.id) + "' class='btn'><i class='fas fa-eye'></i> View</a>"])

    return render(request, 'get_competitive_exam.html', {'data': (data)})


@csrf_exempt
def check_user_mobile(request):
    mobile_number = request.POST.get('mobile_number')
    user_id = request.POST.get('user_id')
    if mobile_number:
        if user_id:
            if User.objects.filter(~Q(id=user_id), username=mobile_number).exists():
                res = "false"
            else:
                res = "true"
        else:
            if User.objects.filter(username=mobile_number).exists():
                res = "false"
            else:
                res = "true"
    else:
        res = "false"
    return HttpResponse(res)


def get_group():
    group_data = []
    group_data1 = []

    gr_no = []
    first_name = ''
    last_name = ''
    city_name = ''
    state = ''
    data = {}

    user_type = Group.objects.all().values_list('id', 'name')
    for i in user_type:
        case = {'id': i[0], 'name': i[1]}
        group_data1.append(case)
        group_data = sorted(group_data1, key=itemgetter('name'))
    return group_data
