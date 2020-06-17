from rest_framework import serializers
from resources.models import admin,resource

class adminSerializer(serializers.ModelSerializer):  
    class Meta:
        model = admin
        unwanted_field_list=['status','created_at','updated_at']
        model_fields=[]
        field_list = (f.name for f in admin._meta.fields )
        for i in set(field_list):
         if i not in unwanted_field_list:
          model_fields.append(i)
        fields = (model_fields)

class resourceSerializer(serializers.ModelSerializer):  
    class Meta:
        model = resource
        unwanted_field_list=['status','created_at','updated_at']
        model_fields=[]
        field_list = (f.name for f in resource._meta.fields)
        
        for i in set(field_list):
         if i not in unwanted_field_list:
          model_fields.append(i)
        fields = (model_fields)