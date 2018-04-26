from django.db import models

# Create your models here.
class AircraftProfile(models.Model):
    name = models.CharField(max_length=40)
    max_cargo_weight = models.IntegerField(default=0)
    max_pax = models.IntegerField(default=2)
    max_weight_per_seat = models.IntegerField(default=280)
