#A custom django has_group conditional tag
#  usage:
#
#      {% if request.user|has_group:"Manager" %}  {% endif %}
#
# Developer: Thanos Vassilakis, 2002


import re, string
from django import template

register = template.Library()


from django.contrib.auth.models import Group
listgroup=[]
@register.simple_tag
def number_of_messages(request):
    print("request.user.id",request.user.id)
    for g in request.user.groups.all():
        listgroup.append(g.name)
    # my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
    # for i in my_user_type:
    #     name=i[0]
    #     print(my_user_type[0][0])
    #     listgroup.append(name)

    # group = Group.objects.filter(user=request.user.id).values_list('name')
    # for i in group:
    #     name=i[0]
    #     listgroup.append(name)
    return listgroup

@register.filter(name='has_group')
def has_group(user, group_name):
    #groupList=[]
    #print("group_namev",group_name)
    #groupList.append(group_name)
    # print("group_namegroup_namegroup_name",group_name)
    try:
        group = Group.objects.get(name=group_name)
        return True if group in user.groups.all() else False
    except Group.DoesNotExist:
        return False
