#A custom django has_group conditional tag
#  usage:
#
#      {% if request.user|has_group:"Manager" %}  {% endif %}
#
# Developer: Thanos Vassilakis, 2002


import re, string
from django import template
from module_manager import models as models_manage
from module_access import models as models_access
from users import models as models_user
from module_access import models as models_access1
from school_app import urls as urlset
from django.contrib.auth.models import User,Group
register = template.Library()
from operator import itemgetter
from users import models as user_models
from django.contrib.contenttypes.models import ContentType
from permissions.views import get_user_permissions,get_all_permissions
from django.template.defaultfilters import linebreaksbr, urlize

@register.filter(name='has_group')
def has_group(user, group_name):
    #groupList=[]
    #print("group_namev",group_name)
    #groupList.append(group_name)
    # print("group_namegroup_namegroup_name",group_name)
    #print("userid",request.user.id)
    try:
        group = Group.objects.get(name=group_name)
        return True if group in user.groups.all() else False
    except Group.DoesNotExist:
        return False

@register.filter(needs_autoescape=True)
def action_role(request, autoescape=True):
    role_id=""
    models_list12=[]
    role_list12=[]
    url_list=[]
    listgroup=[]
    url_list1=[]
    module_id12_list=[]
    add=0
    edit=0
    delete=0
    view=0
    print("request",request.path)
    models_list=models_manage.Master.objects.all().values_list('module_name','id')
    for j in models_list:
        module_id=j[1]
        models_list12.append(module_id)
        
    user_info=models_user.UserRoleMapping.objects.filter(user=request.user.id).values_list("group")
    for i in user_info:
        role_id=i[0]
        role_list12.append(i[0])

    access_info=models_access1.Role_Mapping.objects.filter(module_id__in=models_list12,role_id__in=role_list12).values_list('module_id')
    for kl in access_info:
        models_list=models_manage.Master.objects.filter(id=kl[0]).values_list('module_name')
        for p in models_list:
            module_name=p[0]
            if module_name not in listgroup:
                if request.path=='/users/':
                    module_name="Manage User"
                    
                    models_list1=models_manage.Master.objects.filter(module_name=module_name).values_list('id')
                    for j in models_list1:
                        module_id12=(j[0])     
                        module_id12_list.append(module_id12)
                   
                    if models_manage.Action.objects.filter(action_name="add",module__in=module_id12_list)[:1]:
                        add=1
                    if models_manage.Action.objects.filter(action_name="edit",module__in=module_id12_list)[:1]:
                        edit=1
                    if models_manage.Action.objects.filter(action_name="delete",module__in=module_id12_list)[:1]:
                        delete=1
                    if models_manage.Action.objects.filter(action_name="view",module__in=module_id12_list)[:1]:
                        view=1
                    

                    module_dict={"add":add,"edit":edit,'delete':delete,'view':view}
                    if module_dict not in listgroup:
                        listgroup.append(module_dict)
                    
    return listgroup



@register.filter(name='addstr')
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter(needs_autoescape=True)
def module_access_role(request, autoescape=True):
  user_names=[]
  data=[]
  permissions_data=[]
  content_data=[]
  content=[]
  app_list=[]
  listgroup1=[]
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
  print(content_data)
#   print(all_apps)
  module_name="Dashboard"
  url='/dashboard/'
  re_direct_path='dashboard'
  print("module_path",module_name)
  module_dict={"module_name":module_name,"re_direct_path":re_direct_path ,'url':url}
  listgroup1.append(module_dict)
  for p in all_apps:
    #module_list=[i for i in content_data if i['app'] == p]
    for p in all_apps:
      if p in ['users','class_master','auth','module_access','medium']:
          pass
    #   elif p =='division':
    #       url='/'+p+'_list/'
    #       module_dict={"module_name":p+'_list',"re_direct_path":p+'_list' ,'url':url}
      else:
        module_name=p.capitalize()
        url='/'+p+'/'
        re_direct_path=p
        print("module_path",module_name)
        module_dict={"module_name":module_name,"re_direct_path":re_direct_path ,'url':url}
        if module_dict not in listgroup1:
         listgroup1.append(module_dict)
  listgroup=listgroup1
  return listgroup