from django.db import models

# Create your models here.
class AirportProfile(models.Model):
    name = models.CharField(max_length=40)
    max_cargo_weight = models.IntegerField(default=0)
