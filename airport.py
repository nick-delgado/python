from geopy.point import Point as gp

class Airport():
    def __init__(self, latitude, longitude, altitude=0):
        self.geopoint = gp(latitude, longitude, altitude)


