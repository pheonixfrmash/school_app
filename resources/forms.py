from django import forms
from .models import admin,resource

class adminForm(forms.ModelForm):
    class Meta:
        model = admin
        unwanted_field_list=['status','created_at','updated_at','resource','uploaded_by']
        model_fields=[]
        field_list = (f.name for f in admin._meta.fields )
        for i in (field_list):
         if i not in unwanted_field_list:
          model_fields.append(i)
          fields = (model_fields)
class resourceForm(forms.ModelForm):
     class Meta:
        model = resource
        unwanted_field_list=['status','created_at','updated_at','file_media']
        model_fields=[]
        resource_list = (f.name for f in resource._meta.fields )
        for i in set(resource_list):
         if i not in unwanted_field_list:
          model_fields.append(i)
        fields = (model_fields)



       