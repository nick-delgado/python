from geopy.distance import great_circle
from airport import Airport

CHA = Airport(35.11,-85.10)
DEN = Airport(32.55, -87.21)

dist = great_circle(CHA.geopoint, DEN.geopoint).miles
print(dist)
