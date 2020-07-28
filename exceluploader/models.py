from django.db import models
from postgres_copy import CopyManager

# Create your models here.

class ExcelData(models.Model):
    name = models.CharField(max_length=100,primary_key=True)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    objects = CopyManager()