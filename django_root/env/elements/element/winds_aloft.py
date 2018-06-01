import redis
import json

class Winds:
    def __init__(self, lat, lon, month):
        self.latitude = lat
        self.longitude = lon
        self.month = month

    def get_seasonal_wind(self):
        r = redis.Redis()
        result = r.georadius('winds.'+self.month,self.longitude, self.latitude, 100, 'mi', withdist=True,sort='ASC')
        j = json.loads(result[0][0])
        return j
        #return result[0]
