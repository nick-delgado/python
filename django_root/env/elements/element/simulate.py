from airport.models import Airport
from aircraft.models import Aircraft
from geopy.distance import great_circle
from geopy.distance import EARTH_RADIUS
from geopy.point import Point
from importcsv import *
from tmp_winds import *
from winds_aloft import Winds
import math
import requests
from utils import E6B

def mins_to_hr_min(mins):
    hrs_frac = mins/60
    hr = math.floor(hrs_frac)
    minutes = math.ceil( (hrs_frac % 1) * 60 )
    return (hr, minutes)


##### AIRPORTS #####
AP1 = Airport(code='KCHA',LAT=35.035278,LONG=-85.203889,ALT=683)
############
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

class DATE(object):
    month = None

CREW = CREW()
CREW.weight = 250
PAYLOAD = PAYLOAD()
PAYLOAD.weight = 800

DATE = DATE()
DATE.month = 'jun'
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

def run_leg_sim(AP1, AP2, AC, CREW, PAYLOAD, DATE, CRITERIA=[]):
    # FACTUAL INFORMATION
    course = round(e6b.true_course(AP1.coord, AP2.coord),2) #Calculate course with E6B helper functions
    distance = round(great_circle(AP1.coord, AP2.coord).nm, 2) #Calculate distance with great_circle function from GeoPy Python package
    max_altitude = 410 # GET aircraft max climbing altitude based on operator
    #global SWDF_may
    # WINDS ALOFTS
    winds_json = Winds(AP1.coord, DATE.month).get_seasonal_wind()
    #ASK THE AIRCRAFT(S) TO RUN THE SIMULATIONS AT DIFFERENT ALTITUDES
    sim_result_chart = AC.calc_performances(distance, course, max_altitude, winds_json)

    #...At this point we have a DataFrame with the list of different flight levels and their respective flight time and fuel consumption
    # __________________________
    # | alt  |  time  |  fuel  |
    # --------------------------
    # | 30   |  24    |  148   |
    # | 50   |  26    |  142   |
    #  .....    ....     .....
    
    # !!!! CAUTION !!!!!! ---- Fuel reserved are not factored into the fuel weight on the above DataFrame

    # Can this flight be done with only one tank or will it have to have a fuel stop

    # ...now we need to select the optimal flight plan/altitude that will be the most cost effective
    sim_result_chart['time_cost'] = sim_result_chart.apply(lambda row: row.time * 13.33, axis=1)
    sim_result_chart['fuel_cost'] = sim_result_chart.apply(lambda row: row.fuel * 1.16, axis=1)
    sim_result_chart['total_cost'] = sim_result_chart.apply(lambda row: row.time_cost + row.fuel_cost, axis=1)
    sim_result_chart['dept'] = "CHA"
    sim_result_chart['arrv'] = AP2.code
    sim_result_chart['dist'] = distance
    sim_result_chart['course'] = course
    print(sim_result_chart)

    #...now select the row with the lowest total cost...that will be the most cost effective altitude
    sim_selected = sim_result_chart.loc[sim_result_chart['total_cost'] == sim_result_chart['total_cost'].min()]
    print("\n\n-----------------")
    print(sim_selected)

    # WEIGHT/BALANCE AND FUEL
    fuel = sim_selected['fuel']
    leg_min_fuel_req = int(fuel)/AC.fuel_weight
    fuel_reserve_lbs = 45 * AC.fuel_weight #...calculate the weight of the reserve fuel
    # ...now add it to the weight of the fuel burned at the optimal altitude
    leg_fuel_req = leg_min_fuel_req + 45 # ...so now need to add the fuel reserve
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
    max_tankering_fuel_lbs = min([avail_fuel_payload_atdept, avail_fuel_payload_atarrv, remaining_tank_lbs])
    if (max_tankering_fuel_lbs < 0 ): max_tankering_fuel_lbs = 0
    #...now calculate gallons based on fuel
    max_tankering_fuel_g = max_tankering_fuel_lbs / AC.fuel_weight
    print(max_tankering_fuel_g)
    sim_selected['RAMP'] = weight_onramp
    sim_selected['max_tankering_fuel'] = max_tankering_fuel_g
    #avail_tankering_fuel_g = AC.max_fuel_capacity - max_tankering_fuel_g
    return sim_selected


#@@@@@@ END OF run_leg_sim @@@@@@

###########################
#### SETUP SIMULATIONS ####
##########################

# Prepare Panda DataFrame for adding computations to it
#dfA = pd.DataFrame(columns=['dept_ap','arrv_ap','great_circle','course', \
#        'climb_alt', 'climb_tas','climb_time','climb_gs', 'climb_distC','climb_distL', \
#        'cruise_tas','cruise_timeC','cruise_timeL','cruise_gs','cruise_distC','cruise_distL', \
#        'flight_timeC', 'flight_timeL', 'min_fuel_req', 'fuel_req', \
#        'fuel_req_weight','remaining_tank_gl', 'zfw', 'weight_onramp', 'weight_ontakeoff','weight_onlanding','max_tankering_wgt', 'max_tankering_fuel'])

dfA = pd.DataFrame()
#def sim():
#    global dfA
#SOUTH BOUND
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KRMG'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KASN'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='11A'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KINF'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='MUSC'),AC,CREW,PAYLOAD, DATE), ignore_index = True)

#    #EAST BOUND
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='K1A3'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='K24A'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KCLT'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KEWN'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='TXKF'),AC,CREW,PAYLOAD, DATE), ignore_index = True)

#    #NORTH BOUND
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KCSV'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KEKQ'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KSDF'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KSBN'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='CYLD'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
#
#    #WEST BOUND
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KUOS'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='K2M2'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KMEM'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KRUE'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KAMA'),AC,CREW,PAYLOAD, DATE), ignore_index = True)
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KAPA'),AC,CREW,PAYLOAD, DATE), ignore_index = True)

#OTHERS
dfA = dfA.append(run_leg_sim(AP1,Airport.objects.get(code__exact='KAUO'),AC,CREW,PAYLOAD, DATE), ignore_index = True)

#(hour, mins) = mins_to_hr_min(flight_time)

def export_csv(filename):
    dfA.to_csv(filename, float_format='%.2f')

