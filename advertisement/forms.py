from django import forms
from advertisement.models import Advertisement

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        unwanted_field_list=['status','created_at','updated_at','ad_image','board','state','city','class_id','school_id','school_medium']
        model_fields=[]
        field_list = (f.name for f in Advertisement._meta.fields)
        
        for i in (field_list):
         if i not in unwanted_field_list:
          model_fields.append(i)
        fields = (model_fields)


class EditForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        unwanted_field_list=['status','created_at','updated_at']
        model_fields=[]
        field_list = (f.name for f in Advertisement._meta.fields)
        
        for i in (field_list):
         if i not in unwanted_field_list:
          model_fields.append(i)
        fields = (model_fields)