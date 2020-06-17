from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
# Create your views here.
from django.conf import settings
from django.contrib.auth.models import User,Group,Permission
from users import models as user_models
from roles import models as role_models
@csrf_exempt
def get_all_permissions():
  permissions_data=[]
  permissions = Permission.objects.all().order_by('id').values_list('id','name','content_type')
  for i in permissions:
    case2 = {'id': i[0], 'name': i[1],'content':i[2]}
    permissions_data.append(case2)
    permissions_data=sorted(permissions_data, key=itemgetter('id'))
  return permissions_data

@login_required
def get_user_permissions(request):
  user=request.user
  permissions_data=[]
  user_permissions = Permission.objects.filter(Q(user=user) | Q(group__user=user)).all().order_by('id').values_list('id','name','content_type')
  #user_permissions=user.get_all_permissions()
  for i in user_permissions:
    case2 = {'id': i[0], 'name': i[1],'content':i[2]}
    permissions_data.append(case2)
  permissions_list=sorted(permissions_data, key=itemgetter('id'))
  permissions_data=list({v['id']:v for v in permissions_list}.values())
  return permissions_data

@login_required
def get_user_groups(request):
  user_names=[]
  data=[]
  role_name=''
  user_id=request.user.id
  my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
  for i in my_user_type:
    role_name=i[0]

  if role_name=="Ignite Admin":
    user_type=Group.objects.all().values_list('id', 'name').order_by('-id')
  else:
    user_type=role_models.SchoolRoleMapping.objects.filter(posted_by=request.user.id).values_list('group', 'group__name').order_by('-id')
    user_groups11 =  user_models.User.objects.filter(pk=request.user.id).values_list('groups','groups__name').order_by('-id')
  print(user_groups11)
  for i in user_groups11:
    name=i[1]
    name = name.split("-", 1)[0]
    data.append([str(i[0]),name])
  for i in data:
      case2 = {'id':i[0],'name': i[1]}
      user_names.append(case2)
  user_groups=sorted(user_names,key=itemgetter('id'))
  groups_data=list({v['id']:v for v in user_groups}.values())
  return groups_data

@login_required
def assign_user_permissions(request):
  user_names=[]
  # user_id   = user_models.User.objects.get(username=request.user.username)
  # print(user_id.id)
  # print(type(user_id.id))
  # print(user_models.UserProfile.objects.get(user__username=request.user.username))
  # input()
  school_id = user_models.UserProfile.objects.get(user__username=request.user.username)
  user_list = user_models.UserProfile.objects.filter(school_id=school_id.school_id).values_list('user__first_name','user__last_name','id')
  for i in user_list:
      case2 = {'id':i[2],'name': i[0] + " " + i[1]}
      user_names.append(case2)
  if request.method=='POST':
    permissions_list=request.POST.getlist('permission')
    user_list=request.POST.getlist('users')
    if user_list:
      for users in user_list:
        user_profile=user_models.UserProfile.objects.filter(pk=int(users)).values_list('user')
        user=user_models.User.objects.filter(pk=user_profile[0][0])
        for permission in permissions_list:
          permissions=Permission.objects.get(id=int(permission))
          user[0].user_permissions.add(permissions)
      response=JsonResponse({'status':'success','msg':'Permissions Granted to users'})
    else:
      response=JsonResponse({'status':'error','msg':'Please select a User'})
    return response

  else:
    permissions_data=[]
    content_data=[]
    content=[]
    app_list=[]
    data = get_user_permissions(request)
    for i in data:
      content.append(i['content'])
    content_list = ContentType.objects.filter(pk__in=content).values_list('id','model','app_label')
    for i in content_list:
      case2 = {'id': i[0], 'name': i[1] ,'app':i[2]}
      app_list.append(i[2])
      content_data.append(case2)
    all_apps=list(set(app_list))
    content_data=sorted(content_data, key=itemgetter('id'))
    context = {'data': data,"app_list":all_apps,"content_list":content_data,'user_list':user_names}
    template = 'assign_permission.html'
    return render(request,template,context)

@login_required
def assign_group_users(request):
  user_names=[]
  data=[]
  user_id   = user_models.User.objects.get(username=request.user.username)
  school_id = user_models.UserProfile.objects.get(user=user_id.id)
  user_list = user_models.UserProfile.objects.filter(school_id=school_id.school_id).values_list('user__first_name','user__last_name','id')
  for i in user_list:
      case2 = {'id':i[2],'name': i[0] + " " + i[1]}
      user_names.append(case2)
  if request.method=='POST':
    groups_list=request.POST.getlist('groups')
    user_list=request.POST.getlist('users')
    if user_list:
      for users in user_list:
        user_profile=user_models.UserProfile.objects.filter(pk=int(users)).values_list('user')
        user=user_models.User.objects.filter(pk=user_profile[0][0])
        for group in groups_list:
          groups_details=Group.objects.get(id=int(group))
          user[0].groups.add(groups_details)
      response=JsonResponse({'status':'success','msg':'Groups Assigned to the users'})
    else:
      response=JsonResponse({'status':'error','msg':'Please select a User'})
    return response

  else:
    permissions_data=[]
    content_data=[]
    group_name=[]
    app_list=[]
    data = get_user_groups(request)
    context = {"content_list":data,'user_list':user_names}
    template = 'assign_groups.html'
    return render(request,template,context)


@login_required
def assign_group_permissions(request):
  user_names=[]
  data=[]
  permissions_data=[]
  content_data=[]
  content=[]
  app_list=[]
  user_id   = user_models.User.objects.get(username=request.user.username)
  school_id = user_models.UserProfile.objects.get(user=user_id.id)
  user_list = user_models.UserProfile.objects.filter(school_id=school_id.school_id).values_list('user__first_name','user__last_name','id')
  data = get_user_permissions(request)
  for i in data:
     content.append(i['content'])
  content_list = ContentType.objects.filter(pk__in=content).values_list('id','model','app_label')
  for i in content_list:
    case2 = {'id': i[0], 'name': i[1] ,'app':i[2]}
    app_list.append(i[2])
    content_data.append(case2)
  all_apps=list(set(app_list))
  content_data=sorted(content_data, key=itemgetter('id'))
  for i in user_list:
      case2 = {'id':i[2],'name': i[0] + " " + i[1]}
      user_names.append(case2)
  if request.method=='POST':
    groups_list=request.POST.getlist('groups')
    permissions_list=request.POST.getlist('permission')
    if groups_list:
      for group in groups_list:
        groups_details=Group.objects.get(id=int(group))
        for permission in permissions_list:
          permissions=Permission.objects.get(id=int(permission))    
          # permissions_data.append(permissions)
          groups_details.permissions.add(permissions) 
        response=JsonResponse({'status':'success','msg':'Permissions granted to groups'})   
    else:
      response=JsonResponse({'status':'error','msg':'Please select a Group'})
    return response

  else:
    groups_list = get_user_groups(request)
    context = {"groups":groups_list,'user_list':user_names,"app_list":all_apps,"content_list":content_data,"data":data}
    template = 'assign_groups_permissions.html'
    return render(request,template,context)

@login_required
def assign_permissions(request):
  return render(request, "permissions.html") 