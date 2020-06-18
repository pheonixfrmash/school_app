from django.db import models

# Create your models here.
class Board(models.Model):
    board_name = models.CharField(max_length=150)
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)