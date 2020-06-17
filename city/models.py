from django.db import models
from state.models import State
from country.models import Country
# Create your models here.

class City(models.Model):
    city_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.ForeignKey(State,on_delete=models.PROTECT)
    country = models.ForeignKey(Country,on_delete=models.PROTECT)