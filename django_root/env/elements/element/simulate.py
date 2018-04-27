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


class E6B(object):
    def __init__(self):
        pass

    def time(self, speed, distance):
        return distance / speed

    def speed(self, time, distance):
        return distance / time

    def distance(self, time, speed):
        return speed * time

    def true_airspeed(self, indicated_altitude, altimeter_setting, oat_cel, indicated_airspeed):
        pass

    def cel_to_fahr(self, degrees_cel):
        return (degrees_cel * 9/5) + 32

    def fahr_to_cel(self, degrees_fahr):
        return (degrees_fahr - 32) * 5/9

    def nautical_to_statute(self, nautical):
        return round(nautical * 1.1507794, 2)

    def statute_to_nautical(self, statute):
        return round(statute / 1.1507794, 2)

    def wind_correction_angle(self, course, true_airspeed, wind_dir, wind_speed):
        wca = (180/math.pi) * math.asin((wind_speed / true_airspeed) *
            math.sin(math.pi * (wind_dir - course) / 180))
        # round to the nearest whole degree
        return round(wca, 0)

    def true_heading(self, course, true_airspeed, wind_dir, wind_speed):
        wca = course + (180/math.pi) * math.asin((wind_speed / true_airspeed) *
            math.sin(math.pi * (wind_dir - course) / 180))
        # round to the nearest whole degree
        return round(wca, 0)

    def density_altitude(self, pressure_alt, oat_cel, ISA):
        # return 145442.16 * (1 - (17.326 * pressure_alt / 459.67 + oat_cel) ** 0.235)
        return pressure_alt + 118.8 * (oat_cel - ISA)



WIND_heading = 266
WIND_speed = 44

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

e6b = E6B()
wca = e6b.wind_correction_angle(bearing, AC.cruising_speed, WIND_heading, WIND_speed)
true_heading = e6b.true_heading(bearing, AC.cruising_speed, WIND_heading, WIND_speed)
