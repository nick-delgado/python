import redis
import json
from geopy.point import Point

class Winds:
    def __init__(self, coord, month):
        self.coord = coord
        self.month = month

    def get_seasonal_wind(self):
        r = redis.Redis()
        result = r.georadius('winds.'+self.month, self.coord.latitude, self.coord.latitude, 100, 'mi', withdist=True,sort='ASC')
        j = json.loads(result[0][0])
        return j
        #return result[0]
