from rest_framework import serializers
from django.db import models
from class_master.models import class_master
from state.models import State
from city.models import City
from class_master.models import class_master
from school.models import School
from division.models import Division


class DivisionSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Division
        fields=[f.name for f in Division._meta.fields]
       