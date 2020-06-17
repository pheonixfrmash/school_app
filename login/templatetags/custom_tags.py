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

#link = "http://www.somesite.com/details.pl?urn=2344"
# f = open("/home/dev04/workspace/school_app/school_app/urls.py", "r")
# print(f.read())

# from django.contrib.auth.models import Group
# listgroup=[]
# @register.simple_tag
# #@register.tag(name='request')
# def number_of_messages(request):
#     role_id=""
#     models_list12=[]
#     role_list12=[]
#     url_list=[]
#     print("request.pathrequest.path",request.path)
#     models_list=models_manage.Master.objects.all().values_list('module_name','id')
#     for j in models_list:
#         module_id=j[1]
#         models_list12.append(module_id)
        
#     user_info=models_user.UserProfile.objects.filter(user=request.user.id).values_list("user_type__id")
#     for i in user_info:
#         role_id=i[0]
#         role_list12.append(i[0])

#     access_info=models_access1.Role_Mapping.objects.filter(module_id__in=models_list12,role_id__in=role_list12).values_list('module_id')
#     for kl in access_info:
#         models_list=models_manage.Master.objects.filter(id=kl[0]).values_list('module_name')
#         for p in models_list:
#             module_name=p[0]
#             if module_name not in listgroup:
#                 #module_dict={"module_name":module_name,"module_path":request.path}
#                 listgroup.append(module_name)
#                 #url_list.append(request.path)
        
#     print("Final",listgroup)
#     return listgroup

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


from django.template.defaultfilters import linebreaksbr, urlize

@register.filter(needs_autoescape=True)
def module_access_role(request, autoescape=True):
    role_id=""
    models_list12=[]
    role_list12=[]
    url_list=[]
    listgroup=[]
    url_list1=[]
    models_list=models_manage.Master.objects.all().values_list('module_name','id')
    for j in models_list:
        module_id=j[1]
        models_list12.append(module_id)

    print("ModuleLittt",models_list12)
        
    user_info=models_user.UserRoleMapping.objects.filter(user=request.user.id).values_list("group")
    for i in user_info:
        role_id=i[0]
        role_list12.append(i[0])

    print("role_list12",role_list12)
    print("models_list12",models_list12)

    access_info=models_access1.Role_Mapping.objects.filter(module_id__in=models_list12,role_id__in=role_list12).values_list('module_id')
    for kl in access_info:
        models_list=models_manage.Master.objects.filter(id=kl[0]).values_list('module_name','id','module_path')
        for p in models_list:
            module_name=p[0]
            module_id=p[1]
            url='/'+p[2]+'/'
            #print("module_path",module_path)
            models_list=models_manage.Action.objects.filter(module=module_id,action_name='View').values_list('action_url')
            for url1 in models_list:
                re_direct_path=url1[0]
                
                print("module_name1111",module_name,re_direct_path,url)    
                
                module_dict={"module_name":module_name,"re_direct_path":re_direct_path,'url':url,'module_id':module_id}
                listgroup.append(module_dict)
                listgroup=sorted(listgroup, key=itemgetter('module_id'))
                #print("listgroup",listgroup)
            
    

    return listgroup



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