from django.db import models

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
