from geopy.point import Point as gp
from noaa_sdk import noaa

class Airport():
    def __init__(self, latitude, longitude, altitude=0):
        self.geopoint = gp(latitude, longitude, altitude)

    def weather(self):
        n = noaa.NOAA()
        n.points_forecast(self.geopoint.latitude, self.geopoint.longitude, hourly=False)
        return n
