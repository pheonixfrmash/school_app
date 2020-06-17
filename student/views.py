from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
import json
from student import models

from django.db.models import Q
from django.utils.timezone import get_current_timezone
from datetime import datetime
import dateutil.parser
# from django.utils.encoding import smart_str, smart_unicode
import os
from operator import itemgetter
from datetime import timedelta
import io, csv
# from pyfcm import FCMNotification
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
from module_access import models as models_access
from class_master import models as models_class
from division import models as models_division
from student import models as models_student
from school.views import get_country, get_state, get_city, get_group, get_current_timezone
import pandas as pd
import re

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
def get_manage_student(request):
    data = []
    user_type = ""
    district = ""
    state = ""
    count = 0
    row = []
    request_user_profile=User.objects.filter(username=str(request.user))
    school_id=user_models.UserProfile.objects.filter(user=request_user_profile[0].id).values_list('school_id')
    user_info = models_student.Student.objects.filter(school_id=school_id[0][0]).values_list('id', 'class_name__class_name', 'division',
                                                                 'roll_number', 'date_of_birth', 'first_name',
                                                                 'last_name', 'student_address', 'parent__first_name',
                                                                 'parent__last_name', 'parent__username',
                                                                 'parent__email',
                                                                 'parent__userprofile__secondary_first_name',
                                                                 'parent__userprofile__secondary_last_name',
                                                                 'parent__userprofile__secondary_mobile_no',
                                                                 'parent__userprofile__secondary_email_id',
                                                                 'status').order_by(
        '-id')
    for i in user_info:
        count += 1
        studen_id = i[0]
        class_name = i[1]
        division = i[2]
        roll_no = i[3]
        student_dob = i[4]
        studen_name = i[5] + ' ' + i[6]
        student_address = i[7]
        p_parent_name = i[8] + ' ' + i[9]
        p_parent_mobile_no = i[10]
        p_parent_email = i[11]
        # s_parent_name = i[12] + ' ' + i[13]
        s_parent_name = ' '
        # s_parent_mobile_no = i[14]
        # s_parent_email = i[15]
        s_parent_mobile_no = ' '
        s_parent_email = ' '
        data.append([count, str(class_name), str(division), str(roll_no), str(studen_name), str(student_dob),
                     str(student_address), str(p_parent_name), str(p_parent_mobile_no), str(p_parent_email),
                     str(s_parent_name), str(s_parent_mobile_no), str(s_parent_email),
                     "<a href='/student/edit_student/" + str(
                         studen_id) + "' class='btn'><i class='fas fa-edit'></i> Edit</a>",
                     "<a href='/student/view_student/" + str(
                         studen_id) + "' class='btn'><i class='fas fa-eye'></i> View</a>",
                     ])
    # print("data",data)
    return render(request, 'get_manage_student.html', {'data': (data)})


@csrf_exempt
@transaction.atomic
def student_upload(request):
    template = "import_student.html"
    response = ''
    if request.method == 'GET':
        return render(request, template)

    xlsx_file = request.FILES['file']
    if not xlsx_file.name.endswith('.xlsx'):
        response = JsonResponse({'status': 'error', 'msg': "Please upload a xlsx file"})
        return response

        # data_set = csv_file.read().decode('UTF-8')
    # io_string =io.StringIO(data_set)
    # next(io_string)
    count = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    usernameData = []
    districtData = []
    stateData = []
    userData = []
    import pandas as pd
    from pandas import ExcelWriter
    from pandas import ExcelFile
    import math
    df = pd.read_excel(xlsx_file)
    if ('Class' in df.columns) and ('Division' in df.columns) and ('Roll No' in df.columns) and (
                'Student First Name' in df.columns) and ('Student DOB' in df.columns) and (
                'School Name' in df.columns) and (
                'Student Address' in df.columns) and ('Country' in df.columns) and ('State' in df.columns) and (
                'City' in df.columns) and ('Pincode' in df.columns) and (
                'Primary Parent First Name' in df.columns) and (
                'Primary Parent Middle Name' in df.columns) and ('Primary Parent Last Name' in df.columns) and (
                'Primary Parent Mobile No' in df.columns) and ('Primary Parent Email Id' in df.columns) and (
                'Secondary Parent First Name' in df.columns) and ('Secondary Parent Middle Name' in df.columns) and (
                'Secondary Parent Last Name' in df.columns) and ('Secondary Parent Mobile No' in df.columns) and (
                'Secondary Parent Email Id' in df.columns) and (
                'Gender' in df.columns) and (
                'GR Number' in df.columns):

        for i in df.index:
            parent_username = df['Primary Parent Mobile No'][i]
            parent_password = df['Primary Parent Mobile No'][i]

            primary_parent_f_name = df['Primary Parent First Name'][i]
            primary_parent_m_name = df['Primary Parent Middle Name'][i]
            primary_parent_l_name = df['Primary Parent Last Name'][i]
            primary_parent_email = df['Primary Parent Email Id'][i]

            secondary_parent_mobile_no = df['Secondary Parent Mobile No'][i]
            secondary_parent_f_name = df['Secondary Parent First Name'][i]
            secondary_parent_m_name = df['Secondary Parent Middle Name'][i]
            secondary_parent_l_name = df['Secondary Parent Last Name'][i]
            secondary_parent_email = df['Secondary Parent Email Id'][i]

            student_f_name = df['Student First Name'][i]
            student_m_name = df['Primary Parent Middle Name'][i]
            student_l_name = df['Primary Parent Last Name'][i]
            gender = df['Gender'][i]
            gr_number = df['GR Number'][i]

            student_class = df['Class'][i]
            division = df['Division'][i]
            roll_no = df['Roll No'][i]
            student_dob = df['Student DOB'][i]
            school_name = df['School Name'][i]
            student_address = df['Student Address'][i]
            country = df['Country'][i]
            state = df['State'][i]
            city = df['City'][i]
            pincode = df['Pincode'][i]

            userData.append(
                [parent_username, parent_password, primary_parent_f_name, primary_parent_l_name, primary_parent_m_name,
                 primary_parent_email, secondary_parent_f_name, secondary_parent_m_name, secondary_parent_l_name,
                 secondary_parent_email, student_f_name, student_l_name, student_m_name, student_class, division,
                 student_dob, school_name, student_address, country, state, city, pincode, secondary_parent_mobile_no,
                 roll_no, gender, gr_number])

    else:
        response = JsonResponse({'status': 'error', 'msg': "Please check excel columns"})
        return response

    for i in userData:
        print(i[17])
        count1 += 1
        parent_username = i[0]
        primary_parent_f_name = i[2]
        primary_parent_l_name = i[3]
        primary_parent_m_name = i[4]
        primary_parent_email = i[5]
        secondary_parent_email = i[9]
        student_f_name = i[10]
        student_class = i[13]
        division = i[14]
        student_dob = i[15]
        school_name = i[16]
        country = i[18]
        state = i[19]
        city = i[20]
        pincode = i[21]
        secondary_parent_mobile_no = i[22]
        roll_no = i[23]
        gr_number = i[25]

        if user_models.User.objects.filter(username=parent_username).exists():
            response = JsonResponse(
                {'status': 'error', 'msg': "Mobile Number is Already Exits At Row:" + str(count1) + ""})
            return response

        if Group.objects.filter(name='parent').exists():
            response = JsonResponse({'status': 'error', 'msg': "Parent Group Not Exits In Application:"})
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

        if models_class.class_master.objects.filter(class_name=student_class).exists():
            class_obj = models_class.class_master.objects.get(class_name=student_class)
        else:
            class_obj = None
            response = JsonResponse({'status': 'error', 'msg': "Please Enter Correct Class At Row:" + str(count1) + ""})
            return response

        if models_division.Division.objects.filter(division_name=division).exists():
            models_division.Division.objects.get(division_name=division)
        else:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter Correct Division At Row:" + str(count1) + ""})
            return response
        print(school_name)
        if school_models.School.objects.filter(school_name=school_name).exists():
            print('___11111111111________')
            school_name = school_name
        else:
            print('___jgjhhkkhkjhkh________')
            school_name = None
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter Correct School Name At Row:" + str(count1) + ""})
            return response
        try:
            user_school_id = user_models.UserProfile.objects.get(user_id = request.user.id).school_id
            try:
                school_obj = school_models.School.objects.get(id=user_school_id)
            except:
                school_obj = None
        except:
            school_obj = None


        if models_student.Student.objects.filter(school_id=school_obj, class_name=class_obj, division=division,
                                                 roll_number=roll_no).exists():
            response = JsonResponse({'status': 'error', 'msg': "Duplicate Student Details At Row:" + str(count1) + ""})
            return response

        if models_student.Student.objects.filter(school_id=school_obj, gr_number=gr_number).exists():
            response = JsonResponse({'status': 'error', 'msg': "Duplicate GR Number At Row:" + str(count1) + ""})
            return response

        if len(str(parent_username)) == 0:
            response = JsonResponse({'status': 'error', 'msg': "Please Enter Parent Name At Row:" + str(count1) + ""})
            return response

        if len(str(student_dob)) == 0:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter Student Date Of Birth At Row:" + str(count1) + ""})
            return response

        if len(str(school_name)) == 0:
            response = JsonResponse({'status': 'error', 'msg': "Please Enter School Name At Row:" + str(count1) + ""})
            return response

        if len(str(roll_no)) == 0:
            response = JsonResponse({'status': 'error', 'msg': "Please Enter Roll Number At Row:" + str(count1) + ""})
            return response

        if len(str(gr_number)) == 0:
            response = JsonResponse({'status': 'error', 'msg': "Please Enter GR Number At Row:" + str(count1) + ""})
            return response

        if len(str(student_f_name)) == 0:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter Student First Name At Row:" + str(count1) + ""})
            return response

        if len(str(primary_parent_f_name)) == 0:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter Primary Parent First Name At Row:" + str(count1) + ""})
            return response

        if len(str(primary_parent_m_name)) == 0:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter Primary Parent Last Name At Row:" + str(count1) + ""})
            return response

        if len(str(primary_parent_l_name)) == 0:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter Primary Parent Middle Name At Row:" + str(count1) + ""})
            return response

        if len(str(parent_username)) != 10:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter 10 digit primary parent mobile no At Row:" + str(count1) + ""})
            return response

        if math.isnan(pincode):
            pincode = 0
        else:
            if len(str(pincode)) != 6:
                response = JsonResponse(
                    {'status': 'error', 'msg': "Please Enter 6 digit Pincode At Row:" + str(count1) + ""})
                return response

        try:
            int(parent_username)
            parent_username = True
        except:
            response = JsonResponse({'status': 'error',
                                     'msg': "Please Enter digits only in Primary Parent Mobile No At Row:" + str(
                                         count1) + ""})
            return response

        if secondary_parent_mobile_no != '':
            if len(str(secondary_parent_mobile_no)) != 10:
                response = JsonResponse(
                    {'status': 'error',
                     'msg': "Please Enter 10 digit secondary parent mobile no At Row:" + str(count1) + ""})
                return response
            try:
                int(secondary_parent_mobile_no)
                secondary_parent_mobile_no = True
            except:
                response = JsonResponse({'status': 'error',
                                         'msg': "Please Enter digits only in Secondary Parent Mobile No At Row:" + str(
                                             count1) + ""})
                return response

        if check(primary_parent_email) == True:
            school_admin_email = True
        else:
            response = JsonResponse(
                {'status': 'error', 'msg': "Please Enter valid email id At Row:" + str(count1) + ""})
            return response

        if secondary_parent_email != '':
            if check(secondary_parent_email) == True:
                secondary_parent_email = True
            else:
                response = JsonResponse(
                    {'status': 'error', 'msg': "Please Enter valid email id At Row:" + str(count1) + ""})
                return response

    countdata = 0
    for i in userData:

        countdata += 1
        parent_username = i[0]
        parent_password = i[1]
        primary_parent_f_name = i[2]
        primary_parent_l_name = i[3]
        primary_parent_m_name = i[4]
        primary_parent_email = i[5]
        secondary_parent_f_name = i[6]
        secondary_parent_m_name = i[7]
        secondary_parent_l_name = i[8]
        secondary_parent_email = i[9]
        student_f_name = i[10]
        student_l_name = i[11]
        student_m_name = i[12]
        student_class = i[13]
        division = i[14]
        student_dob = i[15]
        school_name = i[16]
        student_address = i[17]
        country = i[18]
        state = i[19]
        city = i[20]
        pincode = i[21]
        secondary_parent_mobile_no = i[22]
        roll_no = i[23]
        gender = i[24]
        gr_number = i[25]
        if models_class.class_master.objects.filter(class_name=student_class).exists():
            class_obj = models_class.class_master.objects.get(class_name=student_class)
        else:
            class_obj = None
            response = JsonResponse({'status': 'error', 'msg': "Please Enter Correct Class At Row:" + str(count1) + ""})
            return response

        try:
            user_school_id = user_models.UserProfile.objects.get(user_id = request.user.id).school_id
            try:
                school_obj = school_models.School.objects.get(id=user_school_id)
            except:
                school_obj = None
        except:
            school_obj = None

        if models_student.Student.objects.filter(school_id=school_obj, class_name=class_obj, division=division,
                                                 roll_number=roll_no).exists():
            response = JsonResponse({'status': 'error', 'msg': "Duplicate Student Details At Row:" + str(count1) + ""})
            return response

        if models_student.Student.objects.filter(school_id=school_obj, gr_number=gr_number).exists():
            response = JsonResponse({'status': 'error', 'msg': "Duplicate GR Number At Row:" + str(count1) + ""})
            return response

        school_obj = school_models.School.objects.get(school_name=school_name)
        class_obj = models_class.class_master.objects.get(class_name=student_class)
        state = state_models.State.objects.get(state_name=state.strip().capitalize())
        city = city_models.City.objects.get(city_name=city.strip().capitalize())
        country = country_models.Country.objects.get(country_name=country.strip().capitalize())

        new_user = User.objects.create(username=parent_username, password=parent_password,
                                       first_name=primary_parent_f_name, is_active=1, email=primary_parent_email,
                                       last_name=primary_parent_l_name)

        userprofile = user_models.UserProfile.objects.create(user=new_user,
                                                             secondary_first_name=secondary_parent_f_name,
                                                             secondary_middle_name=secondary_parent_m_name,
                                                             secondary_last_name=secondary_parent_l_name,
                                                             secondary_email_id=secondary_parent_email,
                                                             secondary_mobile_no=secondary_parent_mobile_no,
                                                             school_id=school_obj, created_at=datetime.now())

        student_obj = models_student.Student.objects.create(school=school_obj, class_name=class_obj,
                                                            division=division, first_name=student_f_name,
                                                            last_name=student_l_name, middle_name=student_m_name,
                                                            parent=new_user, gender=gender, date_of_birth=student_dob,
                                                            roll_number=roll_no, gr_number=gr_number,
                                                            student_address=student_address, student_country=country,
                                                            student_state=state, student_city=city, pincode=pincode)

        group_obj = Group.objects.get(name='Parent')

        user_roll_mappping_obj = user_models.UserRoleMapping.objects.create(user_id=new_user.id, group_id=group_obj.id,
                                                                            school_id=school_obj.id)

        user_roll_mappping_obj.save()
        group_obj.save()
        school_obj.save()
        userprofile.save()
        new_user.save()
        userprofile.save()
        student_obj.save()

    response = JsonResponse({'status': 'success', 'msg': " " + str(countdata) + " " + "User Added Successfully"})
    return response


@csrf_exempt
def edit_student(request, student_id_pk):
    data = {}
    action_url_list = []
    action_name_list = []
    action_id_list = []
    action_name = ''
    action_url = ''
    user_photo = "/media/default/placeholder.png"
    country_data = get_country()
    state_data = get_state()
    city_data = get_city()
    action_id_list = []
    bank_deatils = []
    jsonlist = []
    datajsonlist = {}

    try:
        student_obj = models_student.Student.objects.get(id=student_id_pk)
    except:
        student_obj = None

    if student_obj is not None:
        student_details = [str(student_obj.first_name), str(student_obj.last_name), str(student_obj.middle_name),
                           str(student_obj.student_address), str(student_obj.student_country.id),
                           str(student_obj.student_state.id),
                           str(student_obj.student_city.id), str(student_obj.pincode), str(student_obj.roll_number),
                           str(student_obj.gr_number), str(student_obj.profile_picture),
                           str(student_obj.class_name.class_name),
                           str(student_obj.gender.capitalize()), str(student_obj.date_of_birth),
                           str(student_obj.school.school_name), str(student_obj.division)]
    else:
        student_details = []

    try:
        user_obj = user_models.User.objects.get(username=student_obj.parent)
    except:
        user_obj = None

    if user_obj is not None:

        parent_mobile_no = user_obj.username
        parent_f_name = user_obj.first_name
        parent_l_name = user_obj.last_name
        email = user_obj.email

        primary_parent_dtl = [parent_mobile_no, parent_f_name, parent_l_name, email]
        try:
            userprofile_obj = user_models.UserProfile.objects.get(user=user_obj)
        except:
            userprofile_obj = None

        if userprofile_obj is not None:
            print(userprofile_obj)
            parent_mobile_no = userprofile_obj.secondary_mobile_no
            parent_f_name = userprofile_obj.secondary_first_name
            parent_m_name = userprofile_obj.secondary_middle_name
            parent_l_name = userprofile_obj.secondary_last_name
            email = userprofile_obj.secondary_email_id
            secondary_parent_dtl = [parent_mobile_no, parent_f_name, parent_m_name, parent_l_name, email]
        else:
            secondary_parent_dtl = []
    else:
        primary_parent_dtl = []
        secondary_parent_dtl = []

    if request.method == 'POST':
        data = {}
        user_photo = ''
        student_f_name = request.POST.get('student_first_name')
        student_dob = request.POST.get('student_dob')
        student_gender = request.POST.get('gender')
        roll_no = request.POST.get('roll_no')
        gr_number = request.POST.get('gr_no')
        student_address = request.POST.get('student_address')
        p_parent_f_name = request.POST.get('p_parent_first_name')
        p_parent_l_name = request.POST.get('p_parent_last_name')
        p_parent_email_id = request.POST.get('p_parent_email_id')
        s_parent_f_name = request.POST.get('s_parent_first_name')
        s_parent_m_name = request.POST.get('s_parent_middle_name')
        s_parent_l_name = request.POST.get('s_parent_last_name')
        s_parent_mobile_no = request.POST.get('s_parent_mobile_no')
        s_parent_email_id = request.POST.get('s_parent_email_id')
        date_of_birth = request.POST.get('dob')
        class_name = request.POST.get('class_label')
        division_name = request.POST.get('division_label')

        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        if request.FILES.get('user_photo'):
            user_photo = request.FILES['user_photo']
        try:
            student_obj = models_student.Student.objects.get(id=student_id_pk)
        except:
            student_obj = None

        if student_obj is not None:
            student_obj.first_name = student_f_name
            student_obj.last_name = p_parent_f_name
            student_obj.middle_name = p_parent_l_name
            student_obj.student_address = student_address
            student_obj.student_country.id = country
            student_obj.student_state.id = state
            student_obj.student_city.id = city
            student_obj.pincode = pincode
            student_obj.roll_number = roll_no
            student_obj.gr_number = gr_number
            student_obj.profile_picture = user_photo
            student_obj.class_name.id = class_name
            student_obj.gender = student_gender
            student_obj.date_of_birth = student_dob
            student_obj.date_of_birth = date_of_birth
            student_obj.division = division_name
            student_obj.save()

        try:
            user_obj = user_models.User.objects.get(username=student_obj.parent)
        except:
            user_obj = None

        if user_obj is not None:
            user_obj.first_name = p_parent_f_name
            user_obj.last_name = p_parent_l_name
            user_obj.email = p_parent_email_id
            user_obj.save()

        try:
            userprofile_obj = user_models.UserProfile.objects.get(user=user_obj)
        except:
            userprofile_obj = None

        if userprofile_obj is not None:
            userprofile_obj.secondary_mobile_no = s_parent_mobile_no
            userprofile_obj.secondary_first_name = s_parent_f_name
            userprofile_obj.secondary_middle_name = s_parent_m_name
            userprofile_obj.secondary_last_name = s_parent_l_name
            userprofile_obj.secondary_email_id = s_parent_email_id
            userprofile_obj.save()
        
        response = JsonResponse({'status': 'success', 'msg': "School Updated Successfully"})
        return response

    return render(request, 'edit_student.html',
                  {'data': data, "country_data": country_data, "state_data": state_data, "city_data": city_data,
                   'student_details': student_details, 'primary_parent_dtl': primary_parent_dtl,
                   'secondary_parent_dtl': secondary_parent_dtl, 'student_id_pk': student_id_pk,
                   'user_photo': user_photo})


@csrf_exempt
def view_student(request, student_id_pk):
    data = {}
    action_url_list = []
    action_name_list = []
    action_id_list = []
    action_name = ''
    action_url = ''
    user_photo = "/media/default/placeholder.png"
    country_data = get_country()
    state_data = get_state()
    city_data = get_city()
    action_id_list = []
    bank_deatils = []
    jsonlist = []
    datajsonlist = {}

    try:
        student_obj = models_student.Student.objects.get(id=student_id_pk)
    except:
        student_obj = None

    if student_obj is not None:
        student_details = [str(student_obj.first_name), str(student_obj.last_name), str(student_obj.middle_name),
                           str(student_obj.student_address), str(student_obj.student_country.id),
                           str(student_obj.student_state.id),
                           str(student_obj.student_city.id), str(student_obj.pincode), str(student_obj.roll_number),
                           str(student_obj.gr_number), str(student_obj.profile_picture),
                           str(student_obj.class_name.class_name),
                           str(student_obj.gender.capitalize()), str(student_obj.date_of_birth),
                           str(student_obj.school.school_name), str(student_obj.division)]
    else:
        student_details = []

    try:
        user_obj = user_models.User.objects.get(username=student_obj.parent)
    except:
        user_obj = None

    if user_obj is not None:

        parent_mobile_no = user_obj.username
        parent_f_name = user_obj.first_name
        parent_l_name = user_obj.last_name
        email = user_obj.email

        primary_parent_dtl = [parent_mobile_no, parent_f_name, parent_l_name, email]
        try:
            userprofile_obj = user_models.UserProfile.objects.get(user=user_obj)
        except:
            userprofile_obj = None

        if userprofile_obj is not None:
            print(userprofile_obj)
            parent_mobile_no = userprofile_obj.secondary_mobile_no
            parent_f_name = userprofile_obj.secondary_first_name
            parent_m_name = userprofile_obj.secondary_middle_name
            parent_l_name = userprofile_obj.secondary_last_name
            email = userprofile_obj.secondary_email_id
            secondary_parent_dtl = [parent_mobile_no, parent_f_name, parent_m_name, parent_l_name, email]
        else:
            secondary_parent_dtl = []
    else:
        primary_parent_dtl = []
        secondary_parent_dtl = []

    return render(request, 'view_student.html',
                  {'data': data, "country_data": country_data, "state_data": state_data, "city_data": city_data,
                   'student_details': student_details, 'primary_parent_dtl': primary_parent_dtl,
                   'secondary_parent_dtl': secondary_parent_dtl, 'user_photo': user_photo})


def send_file_student(request):
    file_path = "C:/Users/ANAND/Downloads/student.xlsx"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

# @csrf_exempt
# def check_roll_no(request, roll_no, class_name, division, student_id_pk):
#     try:
#         school_id = models_student.Student.objects.get(id=student_id_pk).school_id
#     except:
#         school_id = None

#     if school_id is not None:
#         try:
#             school_obj = school_models.School.objects.get(id=school_id)
#         except:
#             school_obj = None
#         try:
#             class_obj = models_class.class_master.objects.get(id=class_name)
#         except:
#             class_obj = None
#         if (school_obj is not None) and (class_obj is not None):
#             try:
#                 roll_no_obj = models_student.Student.objects.get(id=student_id_pk, school_id=school_obj.id,
#                                                                  class_name_id=class_name, division=division,
#                                                                  roll_number=roll_no).roll_number
#             except:
#                 roll_no_obj = None
#             if roll_no_obj is not None:
#                 if roll_no_obj.gr_number != roll_no:
#                     res = "false"
#                 else:
#                     res = "true"
#                 return HttpResponse(res)
#             res = "true"
#             return HttpResponse(res)
#         res = "true"
#         return HttpResponse(res)
#     res = "true"
#     return HttpResponse(res)


# @csrf_exempt
# def check_gr_no(request, gr_no, student_id_pk):
#     print(gr_no, student_id_pk)
#     try:
#         school_id = models_student.Student.objects.get(id=student_id_pk).school_id
#     except:
#         school_id = None

#     if school_id is not None:
#         try:
#             school_obj = school_models.School.objects.get(id=school_id)
#         except:
#             school_obj = None
#         if school_obj is not None:
#             try:
#                 gr_no_obj = models_student.Student.objects.get(id=student_id_pk, school_id=school_obj.id).gr_number
#             except:
#                 gr_no_obj = None
#             if gr_no is not None:
#                 if gr_no_obj.gr_number != gr_no:
#                     res = "false"
#                 else:
#                     res = "true"
#                 return HttpResponse(res)
#             res = "true"
#             return HttpResponse(res)
#         res = "true"
#         return HttpResponse(res)
#     res = "true"
#     return HttpResponse(res)
