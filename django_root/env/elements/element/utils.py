
class E6B(object):
    '''
    FUNCTIONS
        - true_course()
        - wind_correction_angle()
        - true_heading()
        - ground_speed()
        - midpoint()
        - flight_time()
        - leg_min_fuel_req()
    '''
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
        return round(compass_bearing, 2)

    def wind_correction_angle(self, course, true_airspeed, wind_dir, wind_speed):
        '''
        ARGUMENTS
            course          > true course of the leg between origin airport and destination airport
            true_airspeed   > True airspeed of aircraft at the selected optimal altitude
            wind_dir        > Direction in degrees the wind is coming from
            wind_speed      > Speeds in knots of the wind
        '''
        #wca = (180/math.pi) * math.asin((wind_speed / true_airspeed) * math.sin(math.pi * (wind_dir - course) / 180))
        wca = round(math.degrees(math.asin((wind_speed / true_airspeed)) * math.sin(math.radians(wind_dir - course+180))),2)
        # round to the nearest whole degree
        return round(wca, 2)

#    def true_heading(self, course, true_airspeed, wind_dir, wind_speed):
#        wca = course + (180/math.pi) * math.asin((wind_speed / true_airspeed) *
#            math.sin(math.pi * (wind_dir - course) / 180))
#        # round to the nearest whole degree
#        return round(wca, 2)

    def density_altitude(self, pressure_alt, oat_cel, ISA):
        # return 145442.16 * (1 - (17.326 * pressure_alt / 459.67 + oat_cel) ** 0.235)
        return pressure_alt + 118.8 * (oat_cel - ISA)

    def ground_speed(self, course, true_airspeed, wind_dir, wind_speed, true_heading):
        return round(((true_airspeed*math.cos(math.radians(course-true_heading))) + ( wind_speed * math.cos( math.radians(course-wind_dir+180) ) )), 2)

#    def flight_time(self, distance, climb_distance, climb_time, ground_speed, dept_ap_xtra_flt_time, arrv_ap_xtra_flt_time, global_xtra_flt_time):
#        if (distance-climb_distance < 0):
#            dist_travel_time = (distance / (groundspeed/2) ) * 60
#        else:
#            dist_travel_time = ( (distance-climb_distance) / ground_speed ) * 60
#        total_flight_time = dept_ap_xtra_flt_time + climb_time + dist_travel_time + arrv_ap_xtra_flt_time + global_xtra_flt_time
#        return total_flight_time


    def midpoint(self, pointA, pointB):
        '''
        ARGUMENTS
            pointA  > GeoPy Point class {lat, long,alt}; starting geo coordinates
            pointB  > GeoPy Point class {lat, long,alt}; ending geo coordinates

        RETURNS
            (Geopy.Data.Point) - Point coordinates at the middle of the great circle
        '''
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

    def leg_min_fuel_req(self, \
            ac_taxi_fuel_gl, \
            ac_climb_fuelburn_alt_lbs, \
            ac_fuel_type_lbs, \
            leg_flight_time_min, \
            leg_climb_time_alt_min, \
            ac_cruise_fuel_flow_alt_lb_hr):
        '''
        ARGUMENTS:
            ac_taxi_fuel_gl             > Aircraft taxi fuel amount required - user defined (gl)
            ac_climb_fuelburn_alt_lbs   > Aircraft's climb fuel burned to reach optimal altitude (lbs)
            ac_fuel_type_lbs            > Weight of fuel based on the type of fuel required by the aircraft (lbs/gl)
            leg_flight_time_min         > Overall flight time of the leg with optimal altitude (min)
            leg_climb_time_alt_min      > Climb time to optimal altitude (min)
            ac_cruise_fuel_flow_lb_hr   > Fuel flow of aircraft at a certain altitude (lb/hr)
        
        RETURNS:
            (float) -- Amount of fuel required [gl]
        '''
        #Compute minimum fuel required for the leg
        return round( \
                (ac_taxi_fuel_gl) + \
                ((ac_climb_fuelburn_alt_lbs/ac_fuel_type_lbs)) + \
                ((( (leg_flight_time_min - leg_climb_time_alt_min)/60 ) * ac_cruise_fuel_flow_alt_lb_hr)/ ac_fuel_type_lbs)\
                , 1)
