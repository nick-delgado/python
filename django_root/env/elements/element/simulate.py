from airport.models import Airport
from aircraft.models import Aircraft
from geopy.distance import great_circle
from geopy.distance import EARTH_RADIUS
from geopy.point import Point
import math



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
    
    def true_course(self, pointA, pointB):
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

    def wind_correction_angle(self, course, true_airspeed, wind_dir, wind_speed):
        wca = (180/math.pi) * math.asin((wind_speed / true_airspeed) *
            math.sin(math.pi * (wind_dir - course) / 180))
        # round to the nearest whole degree
        return round(wca, 2)

    def true_heading(self, course, true_airspeed, wind_dir, wind_speed):
        wca = course + (180/math.pi) * math.asin((wind_speed / true_airspeed) *
            math.sin(math.pi * (wind_dir - course) / 180))
        # round to the nearest whole degree
        return round(wca, 2)

    def density_altitude(self, pressure_alt, oat_cel, ISA):
        # return 145442.16 * (1 - (17.326 * pressure_alt / 459.67 + oat_cel) ** 0.235)
        return pressure_alt + 118.8 * (oat_cel - ISA)

    def ground_speed(self, course, true_airspeed, wind_dir, wind_speed, true_heading):
        return (true_airspeed*math.cos(math.radians(course-true_heading))) + ( wind_speed * math.cos( math.radians(course-wind_dir+180) ) )

    def flight_time(self, distance, climb_distance, climb_time, ground_speed, dept_ap_xtra_flt_time, arrv_ap_xtra_flt_time, global_xtra_flt_time):
        if (distance-climb_distance < 0):
            dist_travel_time = (distance / (groundspeed/2) ) * 60
        else:
            dist_travel_time = ( (distance-climb_distance) / ground_speed ) * 60
        total_flight_time = dept_ap_xtra_flt_time + climb_time + dist_travel_time + arrv_ap_xtra_flt_time + global_xtra_flt_time
        return total_flight_time

    def midpoint(self, pointA, pointB):
        if pointA.longitude == pointB.longitude: return Point((pointA.latitude+pointB.latitude)/2, pointA.longitude)
        if pointA.latitude == pointB.latitude: return Point(pointA.latitude, (pointA.longitude+pointB.longitude)/2)
        latA, lonA = math.radians(pointA.latitude), math.radians(pointA.longitude)
        latB, lonB = math.radians(pointB.latitude), math.radians(pointB.longitude)
        dLon = lonB-lonA
        Blon = math.cos(latB) * math.cos(dLon)
        Blat = math.cos(latB) * math.sin(dLon)
        latC = math.atan2(math.sin(latA)+math.sin(latB), math.sqrt((math.cos(latA)+Blon)*(math.cos(latA)+Blon) + Blat*Blat))
        lonC = lonA + math.atan2(Blat, math.cos(latA) + Blon)
        return Point(math.degrees(latC), math.degrees(lonC))

    def point_on_path(self, starting_point, heading, distance):
        R = EARTH_RADIUS
        distance = distance * 1.852 #convert from nautical miles to km
        lat2 = math.asin( math.sin(math.radians(starting_point.latitude))*math.cos(distance/R) + math.cos(math.radians(starting_point.latitude))*math.sin(distance/R)*math.cos(math.radians(heading)) )
        lon2 = math.radians(starting_point.longitude) + math.atan2(math.sin(math.radians(heading))*math.sin(distance/R)*math.cos(math.radians(starting_point.latitude)), math.cos(distance/R)-math.sin(math.radians(starting_point.latitude))*math.sin(lat2))
        return Point(math.degrees(lat2), math.degrees(lon2))

    def min_leg_fuel_req(self, ac_fuel_burn, ac_climb_burn, ac_taxi_fuel, ac_climb_time, leg_flight_time):
        return ac_taxi_fuel + ac_climb_burn + math.ceil(ac_fuel_burn * ((leg_flight_time - ac_climb_time)/60))

def mins_to_hr_min(mins):
    hrs_frac = mins/60
    hr = math.floor(hrs_frac)
    minutes = math.ceil( (hrs_frac % 1) * 60 )
    return (hr, minutes)

WIND_heading = 266
WIND_speed = 44

###########AIRPORT ONE
AP1 = Airport()
AP1.code = 'CHA'
AP1.LAT = 35.035278
AP1.LONG = -85.203889
AP1.ALT = 683
###########AIRPORT TWO
AP2 = Airport()
AP2.code = 'SFB'
AP2.LAT = 28.777778
AP2.LONG = -81.2375
AP2.ALT = 55
############ AIRCRAFT
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

course = e6b.true_course(AP1.coord, AP2.coord)
distance = great_circle(AP1.coord, AP2.coord)
wca = e6b.wind_correction_angle(course, AC.cruising_speed, WIND_heading, WIND_speed)
true_heading = wca + course
true_headingB = e6b.true_heading(course, AC.cruising_speed, WIND_heading, WIND_speed)
gs = e6b.ground_speed(course, AC.cruising_speed, WIND_heading, WIND_speed, true_heading)

flight_time = e6b.flight_time(distance.nm, AC.climb_dist, AC.climb_time, gs, 0, 0, 8)
(hour, mins) = mins_to_hr_min(flight_time)
min_fuel_required = e6b.min_leg_fuel_req(AC.cruising_fuel_burn_gph, AC.climb_fuel, AC.taxi_fuel, AC.climb_time, flight_time)
fuel_required = AC.cruising_fuel_reserve + min_fuel_required
fuel_required_weight = fuel_required * 6.84
#max_payload = AC.max_weight - AC.empty_weight - P.weight - fuel_required_weight
