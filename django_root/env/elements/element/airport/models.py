from django.db import models
from geopy.point import Point

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    LAT = models.FloatField()
    LONG = models.FloatField()
    ALT = models.FloatField()

    @property
    def coord(self):
        return Point([self.LAT, self.LONG, self.ALT])
