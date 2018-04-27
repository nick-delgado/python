from airport.models import Airport
from aircraft.models import Aircraft
from geopy.distance import great_circle
import math

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """

    lat1 = math.radians(pointA.latitude)
    lat2 = math.radians(pointB.latitude)

    diffLong = math.radians(pointB.longitude - pointA.longitude)

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing



AP1 = Airport()
AP1.code = 'CHA'
AP1.LAT = 35.035278
AP1.LONG = -85.203889
AP1.ALT = 683

AP2 = Airport()
AP2.code = 'SFB'
AP2.LAT = 28.777778
AP2.LONG = -81.2375
AP2.ALT = 55

bearing = calculate_initial_compass_bearing(AP1.coord, AP2.coord)
distance = great_circle(AP1.coord, AP2.coord)

AC = Aircraft('N32RT')
AC.cruising_speed = 340
AC.cruising_altitude = 35000
AC.max_fuel_capacity = 251
AC.cruising_fuel_reserve = 45
AC.cruising_fuel_burn_gph = 60
AC.taxi_fuel = 4.5
AC.climb_time = 25
AC.climb_fuel = 50
AC.climb_dist = 87
