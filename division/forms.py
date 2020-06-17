from django import forms
from division.models import Division

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Division
        unwanted_field_list=['status','created_at','updated_at']
        model_fields=[]
        division_list = (f.name for f in Division._meta.fields )
        for i in set(division_list):
         if i not in unwanted_field_list:
          model_fields.append(i)
        fields = (model_fields)