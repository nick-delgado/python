import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyDV93OxljDchBbiBHjfjfbhpMMIyn3aYs8')

reverse_geocode_result = gmaps.reverse_geocode((35.10873, -86.11313))
geocode_result = gmaps.geocode('37363')
print(reverse_geocode_result)
print(geocode_result)

#API-KEY=  AIzaSyDV93OxljDchBbiBHjfjfbhpMMIyn3aYs8

