from django.shortcuts import render,redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from advertisement.serializer import AdvertisementSerializer
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from advertisement.forms import DocumentForm,EditForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from advertisement.models import Advertisement as ads
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from advertisement.serializer import AdvertisementSerializer
from rest_framework.response import Response
import json
from django.core.exceptions import ObjectDoesNotExist
from state import models as state_models
from country import models as country_models
from city import models as city_models
from board.models import Board as board_models
from medium.models import Medium as medium_models
from school.models import School as school_models
from class_master.models import class_master as class_models
from advertisement.models import Ad_position
from bank import models as bank_models
from users import models as user_models
from operator import itemgetter
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
@csrf_exempt
class Advertisement(View):
    
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
        print(state_list)
        for i in state_list:
            case2 = {'id': i[0], 'name': i[1].capitalize(),'country':i[2]}
            state_data.append(case2)
        state_data=sorted(state_data, key=itemgetter('name'))
        return state_data


    @csrf_exempt
    def get_city():
        city_data=[]
        city_list=city_models.City.objects.all().values_list('id', 'city_name','state')

        for i in city_list:
            case2 = {'id': i[0], 'name': i[1],'state':i[2]}
            city_data.append(case2)
        city_data=sorted(city_data, key=itemgetter('name'))
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
        school_list=school_models.objects.all().values_list('id', 'school_name','school_board','school_medium')
    
        for i in school_list:
            case2 = {'id': i[0], 'name': i[1],'board':i[2],'medium':i[3]}
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

    @csrf_exempt
    def get_section():
        section_data=[]
        class_list=Ad_position.objects.all().values_list('id', 'position')
        for i in class_list:
            case2 = {'id': i[0], 'name': i[1]}
            section_data.append(case2)
        return section_data
   
    @login_required
    def add(request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                a=form.save()
                return render(request,'advertisement_list.html')
        else:
            response=JsonResponse({'status':'success','msg':'Advertisement not saved'})
            return response
    
    @login_required
    def add_ads(request):
     country_data=Advertisement.get_country
     state_data=Advertisement.get_state
     city_data=Advertisement.get_city
     board_data=Advertisement.get_board
     medium_data=Advertisement.get_medium
     school_data=Advertisement.get_schools
     class_data=Advertisement.get_class
     section_data=Advertisement.get_section

     if request.method=='POST':
        message = request.POST.get('message')
        ad_name = request.POST.get('ad_name')
        ad_from = request.POST.get('ad_from')
        ad_to = request.POST.get('ad_to')
        ad_position = request.POST.get('ad_position')
        country = request.POST.get('country')
        print(country)
        board = request.POST.get('board')
        state = request.POST.get('state')
        city = request.POST.get('city')
        class_id = request.POST.get('class_id')
        school_id = request.POST.getlist('school_id')
        medium = request.POST.get('school_medium')
        ad_image = request.FILES.get('ad_image')
        contact_number = request.POST.get('mobile_number')
        contact_name = request.POST.get('contact_name')
        ad_url = request.POST.get('ad_url')
        country_id = country_models.Country.objects.get(id=country)
        ad_position = Ad_position.objects.get(id=ad_position)
        new_advertisement = ads.objects.create(message = message,ad_name = ad_name,ad_from = ad_from ,ad_to = ad_to,ad_position = ad_position,country = country_id,ad_image = ad_image,contact_number = contact_number,contact_name = contact_name,ad_url = ad_url)

        ad_detail=new_advertisement.save()
        if board:
          board = board_models.objects.get(id=board)
          board_update = ads.objects.filter(pk=new_advertisement.id).update(board=board)
    
        if state:
          state = state_models.State.objects.get(id=state)
          state_update = ads.objects.filter(pk=new_advertisement.id).update(state=state)
         
        if city:
          city = city_models.City.objects.get(id=city)
          city_update = ads.objects.filter(pk=new_advertisement.id).update(city=city)
        
        if medium:
          school_medium = medium_models.objects.get(id=medium)
          medium_update = ads.objects.filter(pk=new_advertisement.id).update(school_medium=school_medium)
          
        if class_id:
          class_id = class_models.objects.get(id=class_id)
          class_update = ads.objects.filter(pk=new_advertisement.id).update(class_id=class_id)
          
        if school_id:
            for school_id in school_id:
               if len(school_id)==1:
                  school_name = school_models.objects.get(id=school_id[0]) 
                  new_ad=ads.objects.filter(pk=new_advertisement.id).update(school_id=school_name)
               elif len(school_id)==0 and not ad.school_id:
                  pass
               elif len(school_id)== 0 and ad.school_id:
                 new_ad=ads.objects.filter(pk=new_advertisement.id).update(school_id=None)
               else:
                 for i in range(len(school_id)):
                   if i == 0:
                      school_name = school_models.objects.get(id=school_id[0]) 
                      new_ad=ads.objects.filter(pk=new_advertisement.id).update(school_id=school_name)
                   else:
                        school_name = school_models.objects.get(id=school_id[i]) 
                        new_ad=ads.objects.create(message = message,ad_name = ad_name,ad_from = ad_from ,ad_to = ad_to,ad_position = ad_position,country = country_id,board = board,state = state,city = city,class_id = class_id,school_medium = school_medium,contact_number = contact_number,contact_name = contact_name,ad_url = ad_url,school_id=school_name,ad_image='media/advertisements/'+str(ad_image)) 
                        new_ad.save()
        response=JsonResponse({'status':'success'})
        return response
     else:
        return render(request, 'add_ads.html', {"country_data":country_data ,"state_data":state_data,"city_data":city_data,'board_data':board_data,'medium_data':medium_data,'school_data':school_data,'section_data':section_data,'class_data':class_data })
    
    @login_required
    def list_ads(request):
        data=[]
        ad_list={}
        ob = Advertisement()
        count=1
        if request.method == 'GET':
            ads_list = ads.objects.all()
            for ad in ads_list.filter(school_id__isnull=False):
              ad_id=ad.id
              ad_name=ad.ad_name
              ad_position=Ad_position.objects.filter(pk=ad.ad_position.id).values_list('position')
              ad_section=ad_position[0][0]
              school_id = ad
              #print("ad.school_idad.school_id",ad.school_id['id'])
              school_details = school_models.objects.filter(pk=ad.school_id.id).values_list('school_name')
              school_name = school_details[0][0]
              if (ad.class_id!=None):
                 class_details = class_models.objects.filter(pk=ad.class_id.id).values_list('class_name')
                 name = class_details[0][0]
              else:
                    name = ' '
              contact_name = ad.contact_name
              contact_number = ad.contact_number
              start_date = ad.ad_from
              end_date = ad.ad_to
              Edit='<div class="btn-group"><form class="span4 text-left" action="/advertisement/edit/'+str(ad_id)+'" method="POST"><button style="margin:5px" class="btn btn-primary"><i class="fas fa-edit"></i> Edit</button></form>'
              View='<form class="span4 text-center" action="/advertisement/details/'+str(ad_id)+'" method="POST"><button style="margin:5px" class="btn btn-primary"><i class="fas fa-eye"></i>View</button></form>'
              Delete='<form action="/module_manager/edit_module_manager/21" method="get"><button style="margin:5px" type="button" class="btn btn-primary"><i class="far fa-trash-alt"></i>Delete</button></form></div>'
              actions = Edit+View
              if ad.status != True:
                ad_status = 'Inactive'
                icon = 'fas fa-times'
              else:
                ad_status = 'Active'
                icon = 'fas fa-check'
              serialised_data = [count,ad_name,ad_section,school_name,name,contact_name,contact_number,str(start_date),str(end_date),ad_status,actions]
              data.append(serialised_data)
            for ad in ads_list.filter(school_id__isnull=True):
               ad_id=ad.id
               ad_name=ad.ad_name
               ad_position=Ad_position.objects.filter(pk=ad.ad_position.id).values_list('position')
               ad_section=ad_position[0][0]
               contact_name = ad.contact_name
               contact_number = ad.contact_number
               start_date = ad.ad_from
               end_date = ad.ad_to
               school_name = ' '
               name = ' '
               Edit='<div class="btn-group"><form class="span4 text-left" action="/advertisement/edit/'+str(ad_id)+'" method="POST"><button style="margin:5px" class="btn btn-primary"><i class="fas fa-edit"></i> Edit</button></form>'
               View='<form class="span4 text-center" action="/advertisement/details/'+str(ad_id)+'" method="POST"><button style="margin:5px" class="btn btn-primary"><i class="fas fa-eye"></i>View</button></form>'
               Delete='<form action="/module_manager/edit_module_manager/21" method="get"><button style="margin:5px" type="button" class="btn btn-primary"><i class="far fa-trash-alt"></i>Delete</button></form></div>'
               actions = Edit+View
               if ad.status != True:
                 ad_status = 'Inactive'
                 icon = 'fas fa-times'
               else:
                 ad_status = 'Active'
                 icon = 'fas fa-check'
               serialised_data = [count,ad_name,ad_section,school_name,name,contact_name,contact_number,str(start_date),str(end_date),ad_status,actions]
               data.append(serialised_data)
            context = {'data': data}
            template = 'advertisement_list.html'
            return render(request,template,context)
        else:
            response=JsonResponse({'status':'error','msg':'Bad Request'})
            return response

    @login_required
    def edit_ads(request,id):
        try:
         ad = ads.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            # ad = ads.objects.get(pk= id)
            country_data=Advertisement.get_country
            state_data=Advertisement.get_state
            city_data=Advertisement.get_city
            board_data=Advertisement.get_board
            medium_data=Advertisement.get_medium
            school_data=Advertisement.get_schools
            class_data=Advertisement.get_class
            section_data=Advertisement.get_section
            ad_id=ad.id
            ad_name=ad.ad_name
            ad_message=ad.message
            ad_country = country_models.Country.objects.filter(pk=ad.country.id).values_list('id')
            country_name=ad_country[0][0]
            ad_position = Ad_position.objects.filter(pk=ad.ad_position.id).values_list('id')
            ad_section=ad_position[0][0]
            contact_name = ad.contact_name
            contact_number = ad.contact_number
            start_date = ad.ad_from
            end_date = ad.ad_to
            ad_image = ad.ad_image
            ad_media = str(ad_image).replace(" ", "_")
            ad_url = ad.ad_url 
            serialised_data = {'ad_id':ad_id,'ad_name':ad_name,'ad_section':ad_section,'contact_name':contact_name,'mobile_number':contact_number,'start_date':str(start_date),'end_date':str(end_date),'ad_url':ad_url,'ad_image':ad_media,'ad_message':ad_message,'country_name':country_name}
            if ad.school_id is not None:
                if (ad.school_id.id!=None):
                    school_details = school_models.objects.filter(pk=ad.school_id.id).values_list('id')
                    school_name = school_details[0][0]
                    serialised_data['school_name']=school_name
                else:
                    school_name = 0
            if (ad.state_id!=None):
                state_details = state_models.State.objects.filter(pk=ad.state.id).values_list('id')
                state_name = state_details[0][0]
                serialised_data['state_name']=state_name
            else:
                state_name = 0
            if (ad.city_id!=None):
                class_details = city_models.City.objects.filter(pk=ad.city.id).values_list('id')
                city_name = class_details[0][0]
                serialised_data['city_name']=city_name
            else:
                city_name = 0
            if (ad.class_id!=None):
                class_details = class_models.objects.filter(pk=ad.class_id.id).values_list('id')
                class_name = class_details[0][0]
                serialised_data['class_name']=class_name
            else:
                class_name = 0
            if (ad.board!=None):
                board_details = board_models.objects.filter(pk=ad.board.id).values_list('id')
                board_name = board_details[0][0]
                serialised_data['board_name']=board_name
            else:
                board_name = 0
            if (ad.school_medium!=None):
                medium_details = medium_models.objects.filter(pk=ad.school_medium.id).values_list('id')
                medium_name = medium_details[0][0]
                serialised_data['medium_name']=medium_name
            else:
                medium_name = 0
            
            return render(request,'edit_ads.html',{'data':serialised_data,'country_data':country_data,'state_data':state_data, 'city_data':city_data,'board_data':board_data,'medium_data':medium_data,'school_data':school_data,'class_data':class_data,'section_data':section_data})

    @login_required    
    def view_ads(request,id):
        try:
         ad = ads.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            # ad = ads.objects.get(pk= id)
            country_data=Advertisement.get_country
            state_data=Advertisement.get_state
            city_data=Advertisement.get_city
            board_data=Advertisement.get_board
            medium_data=Advertisement.get_medium
            school_data=Advertisement.get_schools
            class_data=Advertisement.get_class
            section_data=Advertisement.get_section
            ad_id=ad.id
            ad_name=ad.ad_name
            ad_message=ad.message
            ad_country = country_models.Country.objects.filter(pk=ad.country.id).values_list('country_name')
            country_name=ad_country[0][0]
            ad_position = Ad_position.objects.filter(pk=ad.ad_position.id).values_list('position')
            ad_section=ad_position[0][0]
            if (ad.school_id!=None):
               school_details = school_models.objects.filter(pk=ad.school_id.id).values_list('id')
               school_name = school_details[0][0]
            else:
                school_name = ' '
            if (ad.state_id!=None):
                state_details = state_models.State.objects.filter(pk=ad.state.id).values_list('state_name')
                state_name = state_details[0][0]
            else:
                state_name = ' '
            if (ad.city_id!=None):
                city_details = city_models.City.objects.filter(pk=ad.city.id).values_list('city_name')
                city_name = city_details[0][0]
            else:
                city_name = ' '
            if (ad.class_id!=None):
                class_details = class_models.objects.filter(pk=ad.class_id.id).values_list('class_name')
                class_name = class_details[0][0]
            else:
                class_name = ' '
            if (ad.board!=None):
                board_details = board_models.objects.filter(pk=ad.board.id).values_list('board_name')
                board_name = board_details[0][0]
            else:
                board_name = ' '
            if (ad.school_medium!=None):
                medium_details = medium_models.objects.filter(pk=ad.school_medium.id).values_list('medium_name')
                medium_name = medium_details[0][0]
            else:
                medium_name = ' '
            contact_name = ad.contact_name
            contact_number = ad.contact_number
            start_date = ad.ad_from
            end_date = ad.ad_to
            ad_image = ad.ad_image
            ad_url = ad.ad_url 
            serialised_data = {'ad_id':ad_id,'ad_name':ad_name,'ad_section':ad_section,'school_name':school_name,'class_name':class_name,'contact_name':contact_name,'mobile_number':contact_number,'start_date':str(start_date),'end_date':str(end_date),'board_name':board_name,'medium_name':medium_name,'ad_url':ad_url,'ad_image':str(ad_image),'state_name':state_name,'city_name':city_name,'ad_message':ad_message,'country_name':country_name,'medium_name':medium_name}
            return render(request,'view_ads.html',{'data':serialised_data,'country_data':country_data,'state_data':state_data, 'city_data':city_data,'board_data':board_data,'medium_data':medium_data,'school_data':school_data,'class_data':class_data,'section_data':section_data})

    @login_required    
    def save_ads(request,id):
        try:
         ad = ads.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method =='POST':
            message = request.POST.get('message')
            ad_name = request.POST.get('ad_name')
            ad_from = request.POST.get('ad_from')

            ad_to = request.POST.get('ad_to')

            ad_position = request.POST.get('ad_position')

            country = request.POST.get('country')

            board = request.POST.get('board')

            state = request.POST.get('state')

            city = request.POST.get('city')

            class_id = request.POST.get('class_id')

            school_id = request.POST.getlist('school_id') 

            medium = request.POST.get('school_medium')

            ad_image = request.FILES.get('ad_image')

            contact_number = request.POST.get('mobile_number')
  
            contact_name = request.POST.get('contact_name')

            ad_url = request.POST.get('ad_url')
            if ad_image is None:
                ad_image = ad.ad_image
            else:
                ad_image = ad_image
            country_id = country_models.Country.objects.get(id=country)
            ad_position = Ad_position.objects.get(id=ad_position)
            ads.objects.filter(pk=ad.id).update(message = message,ad_name = ad_name,ad_from = ad_from ,ad_to = ad_to,ad_position = ad_position,country = country_id,contact_number = contact_number,contact_name = contact_name,ad_url = ad_url,ad_image=ad_image)

            if board:
                board = board_models.objects.get(id=board)
                board_update = ads.objects.filter(pk=ad.id).update(board=board)
            elif not board and ad.board:
                ad.board=None
        
            if state:
                state = state_models.State.objects.get(id=state)
                state_update = ads.objects.filter(pk=ad.id).update(state=state)
            
            elif not state and ad.state:
                pass
            
            if city:
                city = city_models.City.objects.get(id=city)
                city_update = ads.objects.filter(pk=ad.id).update(city=city)
            
            if medium:
                school_medium = medium_models.objects.get(id=medium)
                medium_update = ads.objects.filter(pk=ad.id).update(school_medium=school_medium)
                
            if class_id:
                class_id = class_models.objects.get(id=class_id)
                class_update = ads.objects.filter(pk=ad.id).update(class_id=class_id)
                
            if len(school_id)==1:
                  school_name = school_models.objects.get(id=school_id[0]) 
                  new_ad=ads.objects.filter(pk=ad.id).update(school_id=school_name)
            elif len(school_id)==0 and not ad.school_id:
                  pass
            elif len(school_id)== 0 and ad.school_id:
                 new_ad=ads.objects.filter(pk=ad.id).update(school_id=None)
            else:
                for i in range(len(school_id)):
                   if i == 0:
                      school_name = school_models.objects.get(id=school_id[0]) 
                      new_ad=ads.objects.filter(pk=id).update(school_id=school_name)
                   else:
                        school_name = school_models.objects.get(id=school_id[i]) 
                        new_ad=ads.objects.create(message = message,ad_name = ad_name,ad_from = ad_from ,ad_to = ad_to,ad_position = ad_position,country = country_id,board = board,state = state,city = city,class_id = class_id,school_medium = school_medium,contact_number = contact_number,contact_name = contact_name,ad_url = ad_url,school_id=school_name,ad_image='media/advertisements/'+str(ad_image)) 
                        new_ad.save()
              
            response=JsonResponse({'status':'success'})
            return response
        else:
           response=JsonResponse({'status':'fail','error':'Invalid Request'})
           return response


    @login_required
    def mobile_ads(request,id):
        try:
         ad = ads.objects.get(pk=id)
        except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            # ad = ads.objects.get(pk= id)
            serialiser=AdvertisementSerializer(ad)
            print(serialiser.data)
            input()
            form = EditForm(serialiser.data)
            print(form)
            input()
            if form.is_valid():
                return render(request,'edit_ads.html',{'form':form})
            else:
               response=JsonResponse(serialiser.data,safe=False)
               return response