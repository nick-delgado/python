from geopy.distance import great_circle
from airport import Airport
from wind import Wind

CHA = Airport(35.11,-85.10)
DEN = Airport(32.55, -87.21)

CHA_weather = Wind(CHA.geopoint)
DEN_weather = Wind(DEN.geopoint)

dist = great_circle(CHA.geopoint, DEN.geopoint).miles
print(dist)
