from django.db import models

# Create your models here.
class Aircraft(models.Model):
    tailnumber = models.CharField(max_length=30)

