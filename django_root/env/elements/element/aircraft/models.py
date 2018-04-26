from django.db import models

# Create your models here.
class Aircraft(models.Model):
    tailnumber = models.CharField(max_length=30)
    cruising_speed = models.IntegerField(default=0)
    cruising_altitude = models.IntegerField(default=3500)
    # BASICS
    make = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    type = models.CharField(max_length=40)
    serial = models.CharField(max_length=40)
    classification = models.CharField(max_length=40)


    # WEIGHT & BALANCE
    max_fuel_capacity = models.IntegerField(default=130)
    cruising_fuel_burn_gph = models.IntegerField(default=60)
    cruising_fuel_reserve = models.IntegerField(default=60)
    # AIRPORT REQUIREMENTS
    # PERFORMANCE

    taxi_fuel = models.IntegerField(default=4.5)
    climb_time = models.IntegerField(default=25)
    climb_fuel = models.IntegerField(default=25)
    climb_dist = models.IntegerField(default=80)
