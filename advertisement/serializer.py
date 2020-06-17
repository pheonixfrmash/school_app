from rest_framework import serializers
from django.db import models
from class_master.models import class_master
from state.models import State
from city.models import City
from school.models import School
from advertisement.models import Advertisement,Ad_position


class AdvertisementSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Advertisement
        unwanted_field_list=['created_at','updated_at']
        model_fields=[]
        field_list = (f.name for f in Advertisement._meta.fields)
        
        for i in set(field_list):
         if i not in unwanted_field_list:
          model_fields.append(i)
        fields = (model_fields)
       