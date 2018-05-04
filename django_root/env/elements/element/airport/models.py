from django.db import models
from geopy.point import Point
import requests
from airport.airport_db import airports_df

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    LAT = models.FloatField()
    LONG = models.FloatField()
    ALT = models.FloatField(default=0)

    #def __init__(self, code, latitude, longitude, alt=0):
    #    self.code = code
    #    self.LAT = latitude
    #    self.LONG = longitude
    #    self.ALT = alt

    @property
    def coord(self):
        return Point([self.LAT, self.LONG, self.ALT])

    def fetchData(self, iata):
        prms = {'lat'}

    def fetch_ap_ext(self):
        data = requests.get('http://www.airport-data.com/api/ap_info.json?icao='+self.code).json()
        #self.code = data['icao']
        self.LAT = float(data['latitude'])
        self.LONG = float(data['longitude'])
        print(str(self.LAT) + " / " + str(self.LONG))
        
    def fetch_ap(self):
        #self.code = airports_df.loc[airports_df.ident==code].ident
        self.LAT = airports_df.loc[airports_df.ident==self.code].latitude_deg
        self.LONG = airports_df.loc[airports_df.ident==self.code].longitude_deg
        #return airports_df.loc[airports_df.ident == code]

    def getCurrentWind(self):
        prms = {'lat':self.LAT, 'lon':self.LONG, 'appid':'123e753779880e258c4045b786f0b107'}
        data = requests.get('http://api.openweathermap.org/data/2.5/weather', params=prms).json()
        return data

    def __str__(self):
        return self.code
