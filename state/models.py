from django.db import models
from country.models import Country

class State(models.Model):
    state_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = models.ForeignKey(Country,on_delete=models.PROTECT)

    def __str__(self):
        return self.state_name
