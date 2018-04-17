from geopy.distance import great_circle
from airport import Airport
from wind import Wind
from aircraft import Aircraft

N32RT = Aircraft()
N32RT.name = "jetone"
N32RT.cruising_speed = 430

CHA = Airport(35.11,-85.10)
DEN = Airport(32.55, -87.21)

CHA_weather = Wind(CHA.geopoint).getCurrent()
#for item in CHA_weather:
#    print(item)
print(CHA_weather['wind']['speed'])
DEN_weather = Wind(DEN.geopoint)

dist = great_circle(CHA.geopoint, DEN.geopoint).miles
print(dist)
