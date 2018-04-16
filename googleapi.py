import googlemaps
from datetime import datetime

#API-KEY=  AIzaSyDV93OxljDchBbiBHjfjfbhpMMIyn3aYs8

gmaps = googlemaps.Client(key='AIzaSyDV93OxljDchBbiBHjfjfbhpMMIyn3aYs8')

reverse_geocode_result = gmaps.reverse_geocode((35.10873, -86.11313))
#what is returned? 
#what can be parsed? 
#is it always consistent? 
#does it change based on location? 
# in higher concentration areas of POI is there a filtering system to decrease results or to filter results to what we need?

geocode_result = gmaps.geocode('37363')
#can i return an geolocation from this?
#then use that geopoint to find airports within that radius?
#what about very  large zip code areas? 
#what about doing a functions that if no top 10 airports are found then increase the mileage radius search?
print(reverse_geocode_result)
print(geocode_result)


