from airport.models import Airport
from aircraft.models import Aircraft
from geopy.distance import great_circle
from geopy.distance import EARTH_RADIUS
from geopy.point import Point
from importcsv import *
import math
import requests

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
            leg_flight_time_min     > Overall flight time of the leg with optimal altitude (min)
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

def mins_to_hr_min(mins):
    hrs_frac = mins/60
    hr = math.floor(hrs_frac)
    minutes = math.ceil( (hrs_frac % 1) * 60 )
    return (hr, minutes)

#OPTIMAL CLIMBING ALTITUDE FOR A CERTAIN DISTANCE based on Aircraft Performance Chart of T.F.D. to Climb
def opt_climb_alt(distance, tfdc_chart_df):
    #Optimal Climb Altitude
    oca = distance/6 #Dividing the total distance by a factor of 6 seems to approximate to the max climbing distance for chart lookup
    altitude_prof= 0
    for index,row in tfdc_chart_df.iterrows():
        altitude_prof = index
        if math.ceil(oca) - row.dist <= 0:
            break
    return altitude_prof

WIND_heading = 266
WIND_speed = 44

##### AIRPORTS #####
AP1 = Airport(code='KCHA',LAT=35.035278,LONG=-85.203889,ALT=683)
#AP2 = Airport()
#AP2.code = 'SFB'
#AP2.LAT = 28.777778
#AP2.LONG = -81.2375
#AP2.ALT = 55
################
#AP3 = Airport()
#AP3.code = 'RMG'
#AP3.LAT = 34.3507778
#AP3.LONG = -85.1586667
#AP3.ALT = 644
##################
#AP4 = Airport()
#AP4.code = 'ORL'
#AP4.LAT = 28.5454722
#AP4.LONG = -81.3329167
#AP4.ALT = 112
##################
#AP5 = Airport()
#AP5.code = '0G7'
#AP5.LAT = 42.8835556
#AP5.LONG = -76.7811667
#AP5.ALT = 491
##################
#AP6 = Airport()
#AP6.code = 'TYS'
#AP6.LAT = 35.8093739
#AP6.LONG = -83.9953214
#AP6.ALT = 979
##################
#AP7 = Airport()
#AP7.code = 'MEM'
#AP7.LAT = 35.0424167
#AP7.LONG = -89.9766667
#AP7.ALT = 979
##################
#AP8 = Airport()
#AP8.code = 'VGT'
#AP8.LAT = 36.2106944
#AP8.LONG = -115.1944444
#AP8.ALT = 979
#####
#AP9 = Airport()
#AP9.code = 'JLN'
#AP9.LAT = 37.1531683
#AP9.LONG = -94.4988078
#AP9.ALT = 977
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
AC.fuel_weight = 6.77
AC.empty_weight = 3754
AC.maximum_zero_fuel_weight = 4922
AC.max_takeoff_weight = 6000
AC.max_landing_weight = 5600
AC.ramp_max_weight = 6034

class CREW (object):
    weight = 0

class PAYLOAD(object):
    weight = 0

CREW = CREW()
CREW.weight = 250
PAYLOAD = PAYLOAD()
PAYLOAD.weight = 800
e6b = E6B() # Init E6B core computing functions tool

#midpoint = e6b.midpoint(AP1.coord, AP2.coord)
#point200m_away = e6b.point_on_path(AP1.coord, course, 200)

#figure out the payload (1-2 pilots, pax weight, baggage weight)
# pilots = [ {'pic_lbs':180, 'pic_bag_lbs':35} , {'sic_lbs':175, 'sic_bag_lbs':35} ]
# pax = [ {'seat_num':1, 'lbs':200, 'bag_lbs':40} , {'seat_num':2, 'lbs':165, 'bag_lbs':30}
#         {'seat_num':3, 'lbs':175, 'bag_lbs':20} ]
def load_aircraft(AC, pilots=[], pax=[], pax_bag=[] ):
    pass

#run the simulations with orig, dept, aircraft, and payload (whether estimative or true)
#this will give us the total payload on the a/c and so we can figure out tankering

def run_leg_sim(AP1, AP2, AC, CREW, PAYLOAD):
    #### CALCULATE FLIGHT TIME BASED ON NEW MODEL AND CALCULATIONS
    # FACTUAL INFORMATION
    course = round(e6b.true_course(AP1.coord, AP2.coord),2) #Calculate course with E6B helper functions
    distance = round(great_circle(AP1.coord, AP2.coord).nm, 2) #Calculate distance with great_circle function from GeoPy Python package
    #df - pandas data frame with csv data from T.F.D.C @ ISA chart
    altitude_prof = opt_climb_alt(distance, df) # Find optimal crusing altitude profile for the aircraft based on the leg distance
    ##### CLIMB SECTION
    climb_sect_tas = df.ix[altitude_prof].tas #Retrieve True AirSpeed from Aircraft Performance Chart (Climb section)
    climb_sect_wca = e6b.wind_correction_angle(course, climb_sect_tas, WIND_heading, WIND_speed*0.5)
    climb_sect_true_heading = climb_sect_wca + course
    climb_sect_gs = e6b.ground_speed(course, df.ix[altitude_prof].tas, WIND_heading, WIND_speed*0.5, climb_sect_true_heading)
    climb_sect_alt = df.ix[altitude_prof].alt
    climb_sect_time = df.ix[altitude_prof].time
    climb_sect_dist_lookup = df.ix[altitude_prof].dist
    climb_sect_dist_calc = round(climb_sect_gs * (climb_sect_time/60),1)
    climb_sect_dist_diff = climb_sect_dist_calc - climb_sect_dist_lookup
    climb_sect_fuel_burn = df.ix[altitude_prof].fuel
    
    ##### CRUISE SECTION
    cruise_sect_tas = cruise_df.ix[climb_sect_alt].tas
    cruise_sect_wca = e6b.wind_correction_angle(course, cruise_sect_tas, WIND_heading, WIND_speed)
    cruise_sect_true_heading = cruise_sect_wca + course
    cruise_sect_gs = e6b.ground_speed(course, cruise_sect_tas, WIND_heading, WIND_speed, cruise_sect_true_heading) # this ground speed is wind adjusted
    cruise_sect_dist_lookup = distance-climb_sect_dist_lookup
    cruise_sect_dist_calc = distance-climb_sect_dist_calc
    cruise_sect_time_lookup = round((cruise_sect_dist_lookup/cruise_sect_gs) * 60, 2)
    cruise_sect_time_calc = round((cruise_sect_dist_calc/cruise_sect_gs) * 60, 1)
    cruise_sect_time_diff = cruise_sect_time_calc - cruise_sect_time_lookup
    cruise_sect_fuel_flow = cruise_df.ix[climb_sect_alt].fuel_flow
    flight_time_lookup = climb_sect_time + cruise_sect_time_lookup
    flight_time_calc = climb_sect_time + cruise_sect_time_calc
    
    #Compute fuel consumption calculations
    leg_min_fuel_req = e6b.leg_min_fuel_req(4.5, climb_sect_fuel_burn, AC.fuel_weight, flight_time_calc, climb_sect_time, cruise_sect_fuel_flow )
    leg_fuel_req = leg_min_fuel_req + 45
    leg_fuel_req_lbs = round(leg_fuel_req * AC.fuel_weight , 2)
    if (leg_fuel_req > AC.max_fuel_capacity):
        print('Maximum Fuel Capacity limit exceeded: '+str(leg_fuel_req))

    # Calculate weight limitation and allowances for take-off and landing
    weight_basic_operating = CREW.weight + AC.empty_weight    #sum of all the pilot(s) and crew
    weight_zero_fuel_weight = weight_basic_operating + PAYLOAD.weight
    #...now need to check if the the zero-fuel-weight exceeds the Maximum Zero Fuel Weight of the A/C
    if (weight_zero_fuel_weight > AC.maximum_zero_fuel_weight):
        print('Maximum Zero Fuel Weight limit exceeded')

    #...now add the required-fuel-weight to the zero-fuel-weight to get the weight of the A/C on the ramp
    weight_onramp = weight_zero_fuel_weight + leg_fuel_req_lbs
    if (weight_onramp > AC.ramp_max_weight):
        print('Maximum Ramp Weight limit exceeded')

    #...now subtract taxi fuel burned weight
    weight_ontakeoff = weight_onramp - (AC.taxi_fuel*AC.fuel_weight)
    if (weight_ontakeoff > AC.max_takeoff_weight):
        print('Maximum TakeOff Weight limit exceeded')

    #...after taking off and flying, calculate the fuel burned (don't include reserve)
    weight_onlanding = weight_ontakeoff - (leg_min_fuel_req*AC.fuel_weight)
    if (weight_onlanding > AC.max_landing_weight):
        print('Maximum Landing Weight limit exceeded')

    #...this is the weight of the A/C, pilots, paxs, bags and remaining fuel when the engine shuts down
    weight_atshutdown = weight_onlanding - (AC.taxi_fuel*AC.fuel_weight) 
    #...calculate available extra weight that the A/C that will allow it to takeoff or land
    avail_fuel_payload_atdept = AC.max_takeoff_weight - weight_ontakeoff # Lbs
    avail_fuel_payload_atarrv = AC.max_landing_weight - weight_onlanding # Lbs
    # ...what capacity is possible for this aircraft in terms of lbs and gl
    remaining_tank_gl = AC.max_fuel_capacity - leg_fuel_req # ...How many gallons more could be added in lbs
    remaining_tank_lbs = remaining_tank_gl * AC.fuel_weight # ...how many gallons more could be added in gallons

    #...the least of the 3 fuel payloads is the maximum tankering (in lbs) that can be added to the leg
    max_tankering_fuel_lbs = min([avail_fuel_payload_atdept, avail_fuel_payload_atarrv,remaining_tank_lbs])
    if (max_tankering_fuel_lbs < 0 ): max_tankering_fuel_lbs = 0
    #...now calculate gallons based on fuel
    max_tankering_fuel_g = max_tankering_fuel_lbs / AC.fuel_weight
    #avail_tankering_fuel_g = AC.max_fuel_capacity - max_tankering_fuel_g

    #GENERATE PANDA DATAFRAME Data
    flight_data = {'dept_ap':AP1.code, 'arrv_ap':AP2.code,'great_circle':distance, 'course':course, \
            'climb_alt': climb_sect_alt, 'climb_tas':df.ix[altitude_prof].tas, \
            'climb_time':climb_sect_time, 'climb_gs':climb_sect_gs, 'climb_distC':climb_sect_dist_calc, 'climb_distL':climb_sect_dist_lookup,\
            'cruise_tas':cruise_sect_tas, 'cruise_timeC':cruise_sect_time_calc, 'cruise_timeL':cruise_sect_time_lookup, 'cruise_gs':cruise_sect_gs, \
            'cruise_distC':cruise_sect_dist_calc, 'cruise_distL':cruise_sect_dist_lookup, 'flight_timeC':flight_time_calc, 'flight_timeL':flight_time_lookup, \
            'min_fuel_req':leg_min_fuel_req, 'fuel_req':leg_fuel_req, 'fuel_req_weight':leg_fuel_req_lbs,'remaining_tank_gl':remaining_tank_gl,\
            'zfw':weight_zero_fuel_weight,'weight_onramp':weight_onramp, 'weight_ontakeoff':weight_ontakeoff, 'weight_onlanding':weight_onlanding,'max_tankering_wgt':max_tankering_fuel_lbs, \
            'max_tankering_fuel':max_tankering_fuel_g}
    return flight_data


###########################
#### SETUP SIMULATIONS ####
##########################

# Prepare Panda DataFrame for adding computations to it
dfA = pd.DataFrame(columns=['dept_ap','arrv_ap','great_circle','course', \
        'climb_alt', 'climb_tas','climb_time','climb_gs', 'climb_distC','climb_distL', \
        'cruise_tas','cruise_timeC','cruise_timeL','cruise_gs','cruise_distC','cruise_distL', \
        'flight_timeC', 'flight_timeL', 'min_fuel_req', 'fuel_req', \
        'fuel_req_weight','remaining_tank_gl', 'zfw', 'weight_onramp', 'weight_ontakeoff','weight_onlanding','max_tankering_wgt', 'max_tankering_fuel'])

def sim():
    #SOUTH BOUND
    dfA.loc[0] = run_leg_sim(AP1,Airport.objects.get(code__exact='KRMG'),AC,CREW,PAYLOAD)
    dfA.loc[1] = run_leg_sim(AP1,Airport.objects.get(code__exact='KASN'),AC,CREW,PAYLOAD)
    dfA.loc[2] = run_leg_sim(AP1,Airport.objects.get(code__exact='11A'),AC,CREW,PAYLOAD)
    dfA.loc[3] = run_leg_sim(AP1,Airport.objects.get(code__exact='KINF'),AC,CREW,PAYLOAD)
    dfA.loc[4] = run_leg_sim(AP1,Airport.objects.get(code__exact='MUSC'),AC,CREW,PAYLOAD)
    
    #EAST BOUND
    dfA.loc[5] = run_leg_sim(AP1,Airport.objects.get(code__exact='K1A3'),AC,CREW,PAYLOAD)
    dfA.loc[6] = run_leg_sim(AP1,Airport.objects.get(code__exact='K24A'),AC,CREW,PAYLOAD)
    dfA.loc[7] = run_leg_sim(AP1,Airport.objects.get(code__exact='KCLT'),AC,CREW,PAYLOAD)
    dfA.loc[8] = run_leg_sim(AP1,Airport.objects.get(code__exact='KEWN'),AC,CREW,PAYLOAD)
    dfA.loc[9] = run_leg_sim(AP1,Airport.objects.get(code__exact='TXKF'),AC,CREW,PAYLOAD)
    #NORTH BOUND
    dfA.loc[10] = run_leg_sim(AP1,Airport.objects.get(code__exact='KCSV'),AC,CREW,PAYLOAD)
    dfA.loc[11] = run_leg_sim(AP1,Airport.objects.get(code__exact='KEKQ'),AC,CREW,PAYLOAD)
    dfA.loc[12] = run_leg_sim(AP1,Airport.objects.get(code__exact='KSDF'),AC,CREW,PAYLOAD)
    dfA.loc[13] = run_leg_sim(AP1,Airport.objects.get(code__exact='KSBN'),AC,CREW,PAYLOAD)
    dfA.loc[14] = run_leg_sim(AP1,Airport.objects.get(code__exact='CYLD'),AC,CREW,PAYLOAD)

    #WEST BOUND
    dfA.loc[15] = run_leg_sim(AP1,Airport.objects.get(code__exact='KUOS'),AC,CREW,PAYLOAD)
    dfA.loc[16] = run_leg_sim(AP1,Airport.objects.get(code__exact='K2M2'),AC,CREW,PAYLOAD)
    dfA.loc[17] = run_leg_sim(AP1,Airport.objects.get(code__exact='KMEM'),AC,CREW,PAYLOAD)
    dfA.loc[18] = run_leg_sim(AP1,Airport.objects.get(code__exact='KRUE'),AC,CREW,PAYLOAD)
    dfA.loc[19] = run_leg_sim(AP1,Airport.objects.get(code__exact='KAMA'),AC,CREW,PAYLOAD)
    dfA.loc[20] = run_leg_sim(AP1,Airport.objects.get(code__exact='KAPA'),AC,CREW,PAYLOAD)

#(hour, mins) = mins_to_hr_min(flight_time)

def export_csv():
    dfA.to_csv('simulation.csv',float_format='%.2f')

