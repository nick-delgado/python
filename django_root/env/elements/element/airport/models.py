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
    ALT = models.FloatField()

    @property
    def coord(self):
        return Point([self.LAT, self.LONG, self.ALT])

    def fetchData(self, iata):
        prms = {'lat'}

    def fetch_ap_ext(self, code):
        data = requests.get('http://www.airport-data.com/api/ap_info.json?icao='+code).json()
        self.code = data['icao']
        self.LAT = data['latitude']
        self.LONG = data['longitude']
        
    def fetch_ap(self, code):
        self.code = airports_df.loc[airports_df.ident==code].ident
        self.LAT = airports_df.loc[airports_df.ident==code].latitude_deg
        self.LONG = airports_df.loc[airports_df.ident==code].longitude_deg
        #return airports_df.loc[airports_df.ident == code]

    def getCurrentWind(self):
        prms = {'lat':self.LAT, 'lon':self.LONG, 'appid':'123e753779880e258c4045b786f0b107'}
        data = requests.get('http://api.openweathermap.org/data/2.5/weather', params=prms).json()
        return data
