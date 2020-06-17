from django.shortcuts import render,redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from resources.forms import adminForm,resourceForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from resources.models import admin,resource
from rest_framework.views import APIView
from django.utils import timezone
from resources.serializer import adminSerializer
from users.models import UserProfile,User
import json
import re
from django.core.exceptions import ObjectDoesNotExist
from resources.models import admin,resource,content_type
from state import models as state_models
from country import models as country_models
from city import models as city_models
from board.models import Board as board_models
from medium.models import Medium as medium_models
from school import models as school_models
from class_master import models as class_models
from division.models import Division as division_models
from subject.models import Subject as subject_models
from bank import models as bank_models
from users import models as user_models
from rest_framework import status
from operator import itemgetter
from django.template.defaulttags import register
from student import models as student

# Create your views here.
class Resources(APIView):
    @csrf_exempt
    def get_division():
        division_data=[]
        division_list=division_models.objects.all().values_list('id', 'division_name')
        for i in division_list:
            case2 = {'id': i[0], 'name': i[1].capitalize()}
            division_data.append(case2)
        division_data=sorted(division_data, key=itemgetter('name'))
        return division_data

    @csrf_exempt
    def get_subjects():
        subject_data=[]
        subject_list=country_models.Country.objects.all().values_list('id', 'name')
        for i in subject_list:
            case2 = {'id': i[0], 'name': i[1].capitalize()}
            subject_data.append(case2)
        subject_data=sorted(subject_data, key=itemgetter('name'))
        return subject_data

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
        state_list=state_models.State.objects.all().values_list('id', 'state_name','country')
        for i in state_list:
            case2 = {'id': i[0], 'name': i[1].capitalize(),'country':i[2]}
            state_data.append(case2)
        state_data=sorted(state_data, key=itemgetter('name'))
        print(type(state_data))
        return state_data


    @csrf_exempt
    def get_city():
        city_data=[]
        city_list=city_models.City.objects.all().values_list('id', 'city_name','state')
        print(city_list)
        for i in city_list:
            case2 = {'id': i[0], 'name': i[1],'state':i[2]}
            city_data.append(case2)
        print(city_data)
        return city_data

    @csrf_exempt
    def get_board():
        board_data=[]
        board_list=board_models.objects.all().values_list('id', 'board_name')
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
        school_list=school_models.School.objects.all().values_list('id', 'school_name')
        for i in school_list:
            case2 = {'id': i[0], 'name': i[1]}
            school_data.append(case2)
        return school_data

    @csrf_exempt
    def get_class():
        class_data=[]
        class_list=class_models.class_master.objects.all().values_list('id', 'class_name')
        for i in class_list:
            case2 = {'id': i[0], 'name': i[1]}
            class_data.append(case2)
        return class_data

    @csrf_exempt
    def get_resource():
        resource_data=[]
        class_list=resource.objects.all().values_list('id', 'title','content_type')
        for i in class_list:
            case2 = {'id': i[0], 'title': i[1],'content_type' : i[2]}
            resource_data.append(case2)
        return resource_data

    @csrf_exempt
    def get_content():
        content_data=[]
        content_list=content_type.objects.all().values_list('id', 'content_type')
        for i in content_list:
            case2 = {'id': i[0], 'name': i[1]}
            content_data.append(case2)
        content_data=sorted(content_data, key=itemgetter('name'))
        return content_data

    @register.filter
    def get_item(dictionary, key):
     return dictionary.get(key)

    @login_required
    def add_resource(request):
        user=user_models.User.objects.get(username=request.user.username)
        if user.has_perm('resources.add_resource'):    
            print(request)
            country_list=[]
            board_list=[]
            medium_list=[]
            school_list=[]
            state_list=[]
            city_list=[]
            class_list=[]
            division_list=[]
            subject_list=[]
            country_data=Resources.get_country
            state_data=Resources.get_state
            city_data=Resources.get_city
            board_data=Resources.get_board
            medium_data=Resources.get_medium
            school_data=Resources.get_schools
            class_data=Resources.get_class
            category = Resources.get_content
            subject_data = Resources.get_subjects
            division_data = Resources.get_division
            action_id_list=[]
            bank_deatils=[]
            jsonlist=[]
            school_data12=[]
            datajsonlist={}
            class_list1=[]
            if request.method =='POST':
                resource_name = request.POST.get('resource_name')
                resource_description = request.POST.get('resource_description')
                print(resource_description)
                file_media = request.FILES.get('file_media')
                content_type_id = request.POST.get('content_type')
                content_type_details = content_type.objects.get(id=content_type_id)
                print(content_type_details)
                print(request.user)
                print(type(request.user))
                user_id=user_models.User.objects.get(username=str(request.user))
                print(type(user_id))
                new_resource = resource.objects.create(title = resource_name,description = resource_description,file_media=file_media,content_type=content_type_details)
                resource_detail=new_resource.save()
                country = request.POST.getlist('country')
                print(country)
                for i in range(len(country)):
                    country_list.append(country_models.Country.objects.get(id=country[i]))

                board = request.POST.getlist('board')
                state = request.POST.getlist('state')
                city = request.POST.getlist('city')
                class_name = request.POST.getlist('class_master')
                school = request.POST.getlist('school')
                medium = request.POST.getlist('medium')
                division = request.POST.getlist('division')
                subject = request.POST.getlist('subject')
                serialised_data={'country_list':country,'state_list':state,'city_list':city,'board_list':board,'medium_list':medium,'class_list':class_name,'division_list':division,'subject_list':subject,'school_list':school}
                print(school)
                school_count=class_models.school_class_mapping.objects.all().count()
                school_count_front=class_models.school_class_mapping.objects.filter(school_id__in=school).count()
                print(len(school))
                if school_count_front==school_count:
                    school_id=''
                    class_id=''
                    try:
                        school=school_models.School.objects.get(id=school_id)
                    except:
                        school=None

                    try:
                        class_master=class_models.class_master.objects.get(id=class_id)
                    except:
                        class_master=None

                    new_admin = admin.objects.create(resource=new_resource,uploaded_by=user_id,class_master=class_master,school=school,resource_data=serialised_data)
                    admin_detail = new_admin.save()
                    # new_user = exam_models.Competitive_Exam_Transaction.objects.create(competitive_exam=exam_id,exam_school=school,exam_class=class_master,exam_amount=amount,exam_tax=per,exam_total_amount=total_amount,request_data=datarequest)                
                    # new_user.save()
                    print(new_admin)
                    print(admin_detail)
                    print("saveee two")

                    response=JsonResponse({'status':'success','admin_id':new_resource.id})
                    return response
                else:
                    print("schoolsss",school)
                    city_list=class_models.school_class_mapping.objects.filter(school_id__in=school).values_list('school_id','class_id')
                    for i in city_list:
                        school_list.append(str(i[0])+'_'+str(i[1]))
                        print("school_data",school_list)
                        #school_data=sorted(school_data, key=itemgetter('id'))
                    print("school_data",school_list)
                    for i in school_list:
                        print("iiiiiikkkkkkk",i)
                        school_id=i.split('_', 1)[0]
                        class_id=i.split('_', 1)[1]

                        #print("school_iddddd",school_id)
                        # q = Q()
                        # if school_id:
                        #     q &= Q(school_id=school_id)
                        # if class_id:
                        #     q &= Q(class_id__in=class_name)
                        class_list=class_models.school_class_mapping.objects.filter(school_id=school_id,class_id__in=class_name).values_list('class_id')
                        for i in class_list:
                            class_list1.append(str(i[0]))

                        #target_list = [6, 4, 8, 9, 10]
        
                        # initializing test list 
                        #test_list = [4, 6, 9]
                        
                        # printing lists
                        print("The target list : " + str(class_list1))
                        print("The test list : " + str(class_name))
                        
                        # Test if all elements are present in list
                        # Using list comprehension + all()
                        res = all(ele in class_list1 for ele in class_name)
                        s = set(class_list1)
                        class_not_persent= [x for x in class_name if x not in s]
                        #print("The test testtest : " + str(class))
                        
                        if res:
                            try:
                                school=school_models.School.objects.get(id=school_id)
                            except:
                                school=None
                            try:
                                class_master=class_models.class_master.objects.get(id=class_id)
                            except:
                                class_master=None

                            datasc=school_models.School.objects.filter(id=school_id).values_list('school_city','school_country','school_state')
                            for j in datasc:
                                city=j[0]
                                country=j[1]
                                state=j[2]
                                country=country_models.Country.objects.get(id=country)
                                state=state_models.State.objects.get(id=state)
                                city=city_models.City.objects.get(id=city)

                                print("school_idsssss",school_id,class_master)
                                exam_id=resource.objects.get(id=new_resource.id)
                                #print(school_id)
                                #input()
                                
                                new_user = admin.objects.create(resource=new_resource,uploaded_by=user_id,school=school,class_master=class_master,resource_data=serialised_data)
                                
                                new_user.save()
                        else:
                            #print("edddddddlseeeeeeeeeee")
                            class_list=class_models.class_master.objects.filter(id__in=class_not_persent).values_list('class_name')
                            for i in class_list:
                                class_name=i[0]

                            class_list1=school_models.School.objects.filter(id=school_id).values_list('school_name')
                            for i in class_list1:
                                school_name=i[0]

                                print("The test testtest : " + str(class_not_persent),class_name,school_name)
                                response=JsonResponse({'status':'error','msg':'Combination not exits for School '+school_name+' and Class '+class_name+''})
                                return response
                    # admin.objects.filter(pk=new_admin.id).update(resource_data= serialised_data)
                    response=JsonResponse({'status':'success'})
                    return response
            else:
                return render(request, 'add_resource.html', {"country_data":country_data ,"state_data":state_data,"city_data":city_data,'board_data':board_data,'medium_data':medium_data,'school_data':school_data,'class_data':class_data,'category':category,'division_data':division_data,'subject_data':subject_data })
        else:
            return render(request,'forbidden_page.html')
    
    @login_required
    def list_resources(request):
        user=user_models.User.objects.get(username=request.user.username)
        state_data=Resources.get_state
        city_data=Resources.get_city
        school_data=Resources.get_schools
        class_data=Resources.get_class
        resource_data=Resources.get_resource
        country_data=Resources.get_country 
        board_data=Resources.get_board
        medium_data=Resources.get_medium
        category = Resources.get_content
        subject_data = Resources.get_subjects
        division_data = Resources.get_division
        if 'role' in request.session:
         roles_used = request.session['role']
        ob = admin()
        resource_list = {}
        count = 1
        request_user_profile=User.objects.filter(username=str(request.user))
        request_user=UserProfile.objects.filter(user=request_user_profile[0].id)
        # user_group = request.user.groups.values_list('name', flat=True)
        if (roles_used=="Super Admin"):
            school_id=school_models.School.objects.all().values_list('pk')
            print(type(school_id))
        else:
          school_id=UserProfile.objects.filter(user=request_user_profile[0].id).values_list('school_id')
          print(type(school_id))
        if request.method == 'GET':
          print("call122222")
          data=[]
          user_type=""
          district=""
          state=""
          count=1
          row=[]
          print(roles_used)

          if (roles_used=="Parent"):
            pr=User.objects.filter(username=str(request.user))
            class_id=student.Student.objects.filter(parent=pr[0].id).values_list('class_name','division','id')
            class_details=class_id[0][0]
            division_details=class_id[0][1]
            student_id=class_id[0][2]
            user_info=admin.objects.filter(school_id=school_id[0][0],class_master=class_details).order_by('-id').values_list('resource')
          elif (roles_used=="Super Admin"):
              user_info=admin.objects.all().order_by('-id').values_list('resource')
          else:
            user_info=admin.objects.filter(school_id=school_id[0][0]).order_by('-id').values_list('resource')
          print(user_info)

          for i in user_info:
                school_list=[]
                class_list=[]
                state_list=[]
                country_list=[]
                city_list=[]

                resource_details=resource.objects.filter(pk=i[0]).values_list('title','content_type','updated_at','id')
                resource_title=resource_details[0][0]
                resource_content=content_type.objects.filter(pk=resource_details[0][1]).values_list('content_type')
                resource_posted_date= resource_details[0][2].strftime("%d-%m-%Y")
                print(resource_posted_date)

                admin_details=admin.objects.filter(resource_id=i)
                for i in admin_details:
                    posted_user = user_models.User.objects.filter(username=i.uploaded_by).values_list('first_name')
                    final_dictionary = eval(i.resource_data)
                    state_list=final_dictionary['state_list']
                    city_list=final_dictionary['city_list']
                    school_list=final_dictionary['school_list']
                    class_list=final_dictionary['class_list']
                    if not class_list:
                        class_name='All'
                    else:
                        class_name=repr(set(class_list))
                    school_name=""
                    if not school_list:
                        school_name='All'
                    else:
                        for j in school_list:
                            print(j)
                            i=school_models.School.objects.filter(id=j).values_list('school_name')
                            school_name+=str(i[0][0])+'####'
                        school_name=school_name.replace('####',',')
                        school_name=school_name.rstrip(',')
                        print(school_name)
                    state_name=""
                    if not state_list:
                        state_name='All'
                    else:
                        for j in state_list:
                            print(j)
                            i=state_models.State.objects.filter(id=j).values_list('state_name')
                            state_name+=str(i[0][0])+'####'
                        state_name=state_name.replace('####',',')
                        state_name=state_name.rstrip(',')
                        print(state_name)
                    city_name=''
                    if not city_list:
                            city_name='All'
                    else:
                        for j in city_list:
                            print(j)
                            i=city_models.City.objects.filter(id=j).values_list('city_name')
                            print(i)
                            city_name+=str(i[0][0])+'####'
                        city_name=city_name.replace('####',',')
                        city_name=city_name.rstrip(',')
                        print(city_name)
                    class_name=""
                    if not class_list:
                            class_name='All'
                    else:
                        for j in class_list:
                            print(j)
                            i=class_models.class_master.objects.filter(id=j).values_list('class_name')
                            print(i)
                            class_name+=str(i[0][0])+'####'
                        class_name=class_name.replace('####',',')
                        class_name=class_name.rstrip(',')
                        print(class_name)
                    country_name=''
                    ad_id=resource_details[0][3]
                    # btn="<div class='editBut'><button class='btn btn-block btn-danger btn-sm delete' data-module_id="+str(school_id)+">Delete</button></div>"
                    Edit='<div class="btn-group"><form action="/resources/edit/'+str(ad_id)+'" method="POST"><button style="margin:5px" class="btn btn-primary"><i class="fas fa-edit"></i> Edit</button></form>'
                    View='<form action="/resources/details/'+str(ad_id)+'" method="POST"><button style="margin:5px" class="btn btn-primary"><i class="fas fa-eye"></i>View</button></form>'
                    Delete='<form action="/module_manager/edit_module_manager/21" method="get"><button style="margin:5px" type="button" class="btn btn-primary"><i class="far fa-trash-alt"></i>Delete</button></form></div>'
                    if user.has_perm('resources.change_resource'):
                      if user.has_perm('resources.view_resource'):
                         actions = Edit+View
                      else:
                          actions = Edit
                    elif user.has_perm('resources.view_resource'):
                        actions= View
                    else:
                        actions=" "
                    serialised_data = [count,resource_title,school_name,resource_content[0][0],state_name,city_name,class_name,posted_user[0][0],str(resource_posted_date),actions]
                    data.append(serialised_data)
                    count=count+1
          context = {'data': data,"country_data":country_data ,"state_data":state_data,"city_data":city_data,'board_data':board_data,'medium_data':medium_data,'school_data':school_data,'class_data':class_data,'category':category }
          template = 'resource_list.html'
          return render(request,template,context)             

        else:
          response=JsonResponse({'status':'error','msg':'Bad Request'})
          return response

    @login_required
    def view_resources(request,id):
      user=user_models.User.objects.get(username=request.user.username)
      if user.has_perm('resources.view_resource'):
        print(request)
        print(id)
        try:
         ads = resource.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            # ad = resources.objects.get(pk= id)
            country_data=Resources.get_country
            state_data=Resources.get_state
            city_data=Resources.get_city
            board_data=Resources.get_board
            medium_data=Resources.get_medium
            school_data=Resources.get_schools
            class_data=Resources.get_class
            category_data = Resources.get_content
            print(class_data)
            print(city_data)
            print(country_data)
            print(medium_data)
            print(school_data)
            ad_id=id
            resource_details=resource.objects.filter(pk=id).values_list('title','content_type','updated_at','description','file_media')
            resource_title=resource_details[0][0]
            resource_description=resource_details[0][3]
            ad_image = resource_details[0][4]
            resource_category=content_type.objects.filter(pk=resource_details[0][1]).values_list('content_type')
            category=resource_details[0][1]
            resource_posted_date= resource_details[0][2].strftime("%d-%m-%Y")
            print(resource_posted_date)
            admin_details=admin.objects.filter(resource_id=id)
            print(admin_details)

            i=admin_details[0]
            posted_user = user_models.User.objects.filter(username=i.uploaded_by).values_list('first_name')
            print(posted_user)
            print(i)
            # print(i.school.id)
            # print(type(i.school))
            print(i.class_master)
            final_dictionary = eval(i.resource_data)
            print(final_dictionary['state_list'])
            print(final_dictionary)
            state_list=final_dictionary['state_list']
            city_list=final_dictionary['city_list']
            school_list=final_dictionary['school_list']
            class_list=final_dictionary['class_list']
            countries_list=final_dictionary['country_list']
            board_list=final_dictionary['board_list']
            medium_list=final_dictionary['medium_list']
            school_name=""
            country_name=""
            class_name=""
            board_name=""
            medium_name=""
            state_name=""
            city_name=""
            print(school_list)
            for i in countries_list:
                country_name+=str(i)+'####'
            country_name=country_name.replace('####',',')
            country_name=country_name.rstrip(',')
            print(country_name)
            for i in state_list:
                    state_name+=str(i)+'####'
            state_name=state_name.replace('####',',')
            state_name=state_name.rstrip(',')
            for i in class_list:
                    class_name+=str(i)+'####'
            class_name=class_name.replace('####',',')
            class_name=class_name.rstrip(',')
            for i in city_list:
                    city_name+=str(i)+'####'
            city_name=city_name.replace('####',',')
            city_name=city_name.rstrip(',')
            print(city_name)
            for i in school_list:
                school_name+=str(i)+'####'
            school_name=school_name.replace('####',',')
            school_name=school_name.rstrip(',')
            for i in board_list:
                    board_name+=str(i)+'####'
            board_name=board_name.replace('####',',')
            board_name=board_name.rstrip(',')
            for i in medium_list:
                    medium_name+=str(i)+'####'
            medium_name=medium_name.replace('####',',')
            medium_name=medium_name.rstrip(',')
            print(category)
            serialised_data = {'ad_id':ad_id,'resource_title':resource_title,'school_id':school_name,'content_type':category,'state_name':state_name,'city_name':city_name,'class_name':class_name,'board_name':board_name,'medium_name':medium_name,'country_name':country_name,'resource_description':resource_description,'ad_image':ad_image}
            return render(request,'view_resource.html',{'data':serialised_data,'country_data':country_data,'state_data':state_data, 'city_data':city_data,'board_data':board_data,'medium_data':medium_data,'school_data':school_data,'class_data':class_data,'category':category_data})
        else:
          response=JsonResponse({'status':'error','msg':'Bad Request'})
          return response
      else:
            return render(request,'forbidden_page.html')


    @login_required
    def edit_resources(request,id):
        try:
         ads = resource.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            # ad = resources.objects.get(pk= id)
            country_data=Resources.get_country
            state_data=Resources.get_state
            city_data=Resources.get_city
            board_data=Resources.get_board
            medium_data=Resources.get_medium
            school_data=Resources.get_schools
            class_data=Resources.get_class
            category_data = Resources.get_content
            ad_id=id
            resource_details=resource.objects.filter(pk=id).values_list('title','content_type','updated_at','description','file_media')
            resource_title=resource_details[0][0]
            resource_description=resource_details[0][3]
            ad_image = resource_details[0][4]
            resource_category=content_type.objects.filter(pk=resource_details[0][1]).values_list('content_type')
            category=resource_details[0][1]
            resource_posted_date= resource_details[0][2].strftime("%d-%m-%Y")
            # print(resource_posted_date)
            admin_details=admin.objects.filter(resource_id=id)
            # print(admin_details)

            i=admin_details[0]
            posted_user = user_models.User.objects.filter(username=i.uploaded_by).values_list('first_name')
            # print(posted_user)
            # print(i)
            # print(i.school.id)
            # print(type(i.school))
            # print(i.class_master)
            final_dictionary = eval(i.resource_data)
            # print(final_dictionary['state_list'])
            # print(final_dictionary)
            state_list=final_dictionary['state_list']
            city_list=final_dictionary['city_list']
            school_list=final_dictionary['school_list']
            class_list=final_dictionary['class_list']
            countries_list=final_dictionary['country_list']
            board_list=final_dictionary['board_list']
            medium_list=final_dictionary['medium_list']
            school_name=""
            country_name=""
            class_name=""
            board_name=""
            medium_name=""
            state_name=""
            city_name=""
            # print(school_list)
            for i in countries_list:
                country_name+=str(i)+'####'
            country_name=country_name.replace('####',',')
            country_name=country_name.rstrip(',')
            # print(country_name)
            for i in state_list:
                    state_name+=str(i)+'####'
            state_name=state_name.replace('####',',')
            state_name=state_name.rstrip(',')
            for i in class_list:
                    class_name+=str(i)+'####'
            class_name=class_name.replace('####',',')
            class_name=class_name.rstrip(',')
            for i in city_list:
                    city_name+=str(i)+'####'
            city_name=city_name.replace('####',',')
            city_name=city_name.rstrip(',')
            # print(city_name)
            for i in school_list:
                school_name+=str(i)+'####'
            school_name=school_name.replace('####',',')
            school_name=school_name.rstrip(',')
            for i in board_list:
                    board_name+=str(i)+'####'
            board_name=board_name.replace('####',',')
            board_name=board_name.rstrip(',')
            for i in medium_list:
                    medium_name+=str(i)+'####'
            medium_name=medium_name.replace('####',',')
            medium_name=medium_name.rstrip(',')
            # print(category)
            serialised_data = {'ad_id':ad_id,'resource_title':resource_title,'school_id':school_name,'content_type':category,'state_name':state_name,'city_name':city_name,'class_name':class_name,'board_name':board_name,'medium_name':medium_name,'country_name':country_name,'resource_description':resource_description,'ad_image':ad_image}
            return render(request,'edit_resource.html',{'data':serialised_data,'country_data':country_data,'state_data':state_data, 'city_data':city_data,'board_data':board_data,'medium_data':medium_data,'school_data':school_data,'class_data':class_data,'category':category_data})


    # @login_required
    # def edit_resources(request,id):
    #     print(request)
    #     print(id)
    #     try:
    #      ads = admin.objects.get(pk=id)
    #     except ObjectDoesNotExist:
    #      return Response(status=status.HTTP_404_NOT_FOUND)
    #     if request.method == 'POST':
    #         # ad = resources.objects.get(pk= id)
    #         country_data=Resources.get_country
    #         state_data=Resources.get_state
    #         city_data=Resources.get_city
    #         print(city_data)
    #         board_data=Resources.get_board
    #         medium_data=Resources.get_medium
    #         school_data=Resources.get_schools
    #         class_data=Resources.get_class
    #         category = Resources.get_content
    #         ad_id=ads.id
    #         resources=ads.resource
    #         resource_object=resource.objects.filter(pk=resources.id).values_list('title','description','content_type','file_media')
    #         resource_title = resource_object[0][0]
    #         resource_description = resource_object[0][1]
    #         resource_category = resource_object[0][2]
    #         resource_file = resource_object[0][3]
    #         state_name = ''
    #         class_name = ''
    #         school_name = ''
    #         city_name = ''
    #         country_name=''
    #         board_name=''
    #         medium_name=''
    #         final_dictionary = eval(ads.resource_data)
    #         state_list=final_dictionary['state_list']
    #         city_list=final_dictionary['city_list']
    #         school_list=final_dictionary['school_list']
    #         class_list=final_dictionary['class_list']
    #         countries_list=final_dictionary['country_list']
    #         board_list=final_dictionary['board_list']
    #         medium_list=final_dictionary['medium_list']
    #         print('city_list',city_list)
    #         print('state_list',state_list)
    #         for i in countries_list:
    #           country_name+=str(i[0])+'####'
    #         country_name=country_name.replace('####',',')
    #         country_name=country_name.rstrip(',')
    #         for i in state_list:
    #           state_name+=str(i[0])+'####'
    #         state_name=state_name.replace('####',',')
    #         state_name=state_name.rstrip(',')
    #         for i in class_list:
    #           class_name+=str(i[0])+'####'
    #         class_name=class_name.replace('####',',')
    #         class_name=class_name.rstrip(',')
    #         for i in city_list:
    #           city_name+=str(i[0])+'####'
    #         city_name=city_name.replace('####',',')
    #         city_name=city_name.rstrip(',')
    #         print(city_name)
    #         for i in school_list:
    #           school_name+=str(i[0])+'####'
    #         school_name=school_name.replace('####',',')
    #         school_name=school_name.rstrip(',')
    #         for i in board_list:
    #           board_name+=str(i[0])+'####'
    #         board_name=board_name.replace('####',',')
    #         board_name=board_name.rstrip(',')
    #         for i in medium_list:
    #           medium_name+=str(i[0])+'####'
    #         medium_name=medium_name.replace('####',',')
    #         medium_name=medium_name.rstrip(',')
    #         serialised_data = {'ad_id':ad_id,'resource_title':resource_title,'school_id':school_name,'content_type':resource_category,'state_name':state_name,'city_name':city_name,'class_name':class_name,'board_name':board_name,'medium_name':medium_name,'country_name':country_name}
            
    #         return render(request,'edit_resource.html',{'data':serialised_data,'country_data':country_data,'state_data':state_data, 'city_data':city_data,'board_data':board_data,'medium_data':medium_data,'school_data':school_data,'class_data':class_data,'category':category})

    @login_required    
    def save_resources(request,id):
        country_list=[]
        board_list=[]
        medium_list=[]
        school_list=[]
        state_list=[]
        city_list=[]
        class_list=[]
        division_list=[]
        subject_list=[]
        try:
         ads = admin.objects.get(resource=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method =='POST':
            resource_name = request.POST.get('resource_name')
            resource_description = request.POST.get('resource_description')
            file_media = request.FILES.get('file_media')
            content_type = request.POST.get('content_type')
            user_id=user_models.User.objects.get(username=str(request.user))
            country = request.POST.getlist('country')
            board = request.POST.getlist('board')
            state = request.POST.getlist('state')
            city = request.POST.getlist('city')
            class_id = request.POST.getlist('class_master')
            school_id = request.POST.getlist('school')
            medium = request.POST.getlist('medium')
            division = request.POST.getlist('division')
            subject = request.POST.getlist('subject')
            resource.objects.filter(pk=ads.resource.id).update(title= resource_name ,description=resource_description,content_type=content_type)
            final_dictionary = eval(ads.resource_data)
            # print(final_dictionary['state_list'])
            # print(final_dictionary)
            # state_list=final_dictionary['state_list']
            # city_list=final_dictionary['city_list']
            # school_list=final_dictionary['school_list']
            # class_list=final_dictionary['class_list']
            # countries_list=final_dictionary['country_list']
            # board_list=final_dictionary['board_list']
            # medium_list=final_dictionary['medium_list']
            for i in  range(len(board)):
                board_list.append(board[i])
            final_dictionary['board_list']=board_list
            
            for i in  range(len(state)):
                state_list.append(state[i])
            # ads.state.set(state_list)
            final_dictionary['state_list']=state_list

            for i in  range(len(city)):
                city_list.append(city[i])
            # ads.city.set(city_list)
            final_dictionary['city_list']=city_list

            for i in  range(len(medium)):
                medium_list.append(medium[i])
            # ads.medium.set(medium_list)
            final_dictionary['medium_list']=medium_list
 
            for i in  range(len(class_id)):
                class_list.append(class_id[i])
            # ads.class_master.set(class_list)
            final_dictionary['class_list']=class_list

            for i in  range(len(school_id)):
                school_list.append(school_id[i])
            # ads.school.set(school_list)
            final_dictionary['school_list']=school_list
            print(final_dictionary['school_list'])
            for i in  range(len(division)):
                division_list.append(division[i])
            # ads.division_master.set(division_list)
            final_dictionary['division_list']=division_list

            for i in  range(len(subject)):
                subject_list.append(subject[i] )
            # ads.subject_master.set(subject_list)
            final_dictionary['subject_list']=subject_list
            
            for i in range(len(country)):
                country_list.append(country[i])
            # ads.country.set(country_list)
            final_dictionary['country_list']=country_list
            updated_resource=admin.objects.filter(pk=ads.id).update(resource_data=final_dictionary)
            response=JsonResponse({'status':'success','msg':'Updated successfully'})
            return response
        else:
           response=JsonResponse({'status':'fail','error':'Invalid Request'})
           return response


 