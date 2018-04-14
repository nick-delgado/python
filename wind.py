from geopy.point import Point
import requests

class Wind():
    def __init__(self, geopoint):
        self.gp = Point(geopoint)
        
    def getCurrent():
        prms = {lat:self.gp.latitude, lon:self.gp.longitude, appid:'123e753779880e258c4045b786f0b107'}
        data = requests.get('http://api.openweathermap.org/data/2.5/weather', params=prms).json()
        return data
