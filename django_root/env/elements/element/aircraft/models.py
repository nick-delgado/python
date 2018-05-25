from django.db import models
import pandas as pd
from aircraft.tmp_perf_chart import *
from utils import E6B


class Aircraft(models.Model):
    tailnumber = models.CharField(max_length=30)
    cruising_speed = models.IntegerField(default=0)
    cruising_altitude = models.IntegerField(default=3500)
    # BASICS
    make = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    type = models.CharField(max_length=40)
    serial = models.CharField(max_length=40)
    classification = models.CharField(max_length=40)

    # WEIGHT & BALANCE
    max_fuel_capacity = models.IntegerField(default=130)
    cruising_fuel_burn_gph = models.IntegerField(default=60)
    cruising_fuel_reserve = models.IntegerField(default=60)
    empty_weight = models.IntegerField(default=2000)
    empty_weight_cg = models.IntegerField(default=150)
    maximum_zero_fuel_weight = models.IntegerField(default=4000)
    ramp_max_weight = models.IntegerField(default=6000)
    max_takeoff_weight = models.IntegerField(default=6000)
    max_landing_weight = models.IntegerField(default=5600)

    fuel_weight = models.FloatField(default=6.77)
    # AIRPORT REQUIREMENTS
    
    # PERFORMANCE
    taxi_fuel = models.IntegerField(default=4.5)
    climb_time = models.IntegerField(default=25)
    climb_fuel = models.IntegerField(default=25)
    climb_dist = models.IntegerField(default=80)
    # PERFORMANCE CHARTS
    # ...store them as JSON files and then load them into Pandas DataFrame
    #climb_chart = models.JSONField()
    #cruise_chart = models.JSONField()


    def calc_performances(self, dist, course, MAX_CRUISING_ALT_LVL, WINDS_DF, time_cost_min=13.33, fuel_cost_lbs=1.16):
        '''
        NOTE
            This function takes simulates the aircraft flight time and fuel consumption based on arguments provided
            and applying them to several altitude possibilities, which are then returned as a table

        ARGUMENTS
            dist    > Great-circle distance in nm
            course  > Course heading in normalized degrees
            winds   > NumPy array / DataFrame array

        RETURNS
            (Integer)   > The altitude flight level (FL250)
        '''
        global DF_CLIMB_PERF #TODO  <--- pull from db
        global DF_CRUISE_PERF #TODO <--- pull from db
        global DF_DESCENT_PERF
        #init RESULT dataframe
        RESULT = pd.DataFrame(columns=['alt','time','fuel'])
        possible_alt_lvl = []
        # Run various simulations/calculations
        #...for a given distance and heading
        #...to figure out which cruising altitude 
        #...will be the best based on data from the A/C performance charts.
        
        # Eliminate altitudes in climb/cruise performance chart if the overall
        #...distance is less than twice the climbing distance or some factor
        #
        # Technically, we should eliminate all altitudes that based on the distance to CLIMB
        # and then DESCEND would be further than the distance we need to cover
        #cutoff_dist = dist/2 #TODO WHICH ONE TO SELECT
        # 
        cutoff_dist = dist
        #...now need to check what altitude that cutoff_dist would equate to in the climb chart
        #...and return it as a filtered DataFrame
        filtered_climb_perf = DF_CLIMB_PERF.loc[DF_CLIMB_PERF['dist'] < cutoff_dist]
        #...get the last altitude of the last row in filtered DataFrame
        max_climb_chart_alt_lvl = int(filtered_climb_perf.loc[filtered_climb_perf.index[-1]]['alt'])
        #...make sure that the simulation doesn't go above the maximum allowed altitude set
        #...by the operator for this aircraft
        #...which of the altitude levels is the least? 
        #...The one from the filtered DataFrame chart or the one provided by the operator. Use that as the limit
        limit_alt_lvl = max_climb_chart_alt_lvl if (max_climb_chart_alt_lvl - MAX_CRUISING_ALT_LVL < 0) else MAX_CRUISING_ALT_LVL
        #...now get the filtered performance charts in a DataFrame UP TO THE LIMIT ALTITUDE
        filtered_climb_perf = DF_CLIMB_PERF.loc[DF_CLIMB_PERF['alt'] <= limit_alt_lvl]
        filtered_cruise_perf = DF_CRUISE_PERF.loc[DF_CRUISE_PERF['alt'] <= limit_alt_lvl]
        filtered_descent_perf = DF_DESCENT_PERF.loc[DF_DESCENT_PERF['alt']<=limit_alt_lvl]
        #...now we have a table with the list of all the altitudes up to either (1) the max climbing altitude set by the 
        #...operator (ie.FL 410) or (2) the max altitude based on distance needed to climb to a certain altitude
        #...(ie. if total distance is 21nm, then we can only climb up to the max FL 150)
        
        # Eliminate altitudes in climb/cruise performance chart based on whether
        #...the course is to the East or to the West
        #...Course between [000-179] >> Odd Flight Levels (ie. FL230,FL250,FL270)
        #...Course between [180-359] >> Even Flight Levels (ie. FL220,FL240,FL260)
        use_odd_alt = True if (round(course,0) < 180) else False
        for alt_lvl in range(30,limit_alt_lvl+10,10):
            if (alt_lvl%20 == 0): #...the altitude is even
                if use_odd_alt: #...and we are using odd altitudes
                    pass
                else: #...here we are using even altitudes
                    possible_alt_lvl.append(alt_lvl) #...concatenate it
            else: #...the altitude level is odd
                if use_odd_alt: #...and we are using odd altitudes
                    possible_alt_lvl.append(alt_lvl) #...concatenate it
                else:
                    pass

        # Now we have the possible altitude levels that we can travel on
        # Remaining altitudes will be simulated, for climbing, cruise and descent

        e6b = E6B() # Initialize E6B computing utility
        for alt_lvl in possible_alt_lvl:

            # CLIMB SECTION -- LOOKUP
            sim_climb_time = float(filtered_climb_perf.loc[filtered_climb_perf['alt']==alt_lvl]['time'])
            sim_climb_dist = float(filtered_climb_perf.loc[filtered_climb_perf['alt']==alt_lvl]['dist'])
            sim_climb_fuel = float(filtered_climb_perf.loc[filtered_climb_perf['alt']==alt_lvl]['fuel'])

            # DESCENT SECTION -- LOOKUP
            sim_descent_time = float(filtered_descent_perf.loc[filtered_descent_perf['alt']==alt_lvl]['time'])
            sim_descent_dist = float(filtered_descent_perf.loc[filtered_descent_perf['alt']==alt_lvl]['dist'])
            sim_descent_fuel = float(filtered_descent_perf.loc[filtered_descent_perf['alt']==alt_lvl]['fuel'])
            
            # Eliminate altitudes for which the distance to climb + distance to descent is greater than the total dist
            if (sim_climb_dist + sim_descent_dist < dist):
                #CRUISE SECTION -- COMPUTE
                sim_cruise_dist = dist - sim_climb_dist - sim_descent_dist
                sim_cruise_tas = float(filtered_cruise_perf.loc[filtered_cruise_perf['alt']==alt_lvl]['tas'])
                sim_cruise_flow = float(filtered_cruise_perf.loc[filtered_cruise_perf['alt']==alt_lvl]['flow'])
                sim_cruise_wca = e6b.wind_correction_angle(course, sim_cruise_tas, \
                        float(WINDS_DF.loc[WINDS_DF['alt']==alt_lvl]['dir']), \
                        float(WINDS_DF.loc[WINDS_DF['alt']==alt_lvl]['speed']))
                #sim_cruise_wca = e6b.wind_correction_angle(course, sim_cruise_tas, \
                #        270, \
                #        40)
                sim_cruise_true = sim_cruise_wca + course
                sim_cruise_gs = e6b.ground_speed(course, sim_cruise_tas, \
                        float(WINDS_DF.loc[WINDS_DF['alt']==alt_lvl]['dir']), \
                        float(WINDS_DF.loc[WINDS_DF['alt']==alt_lvl]['speed']), \
                        sim_cruise_true) 
                #sim_cruise_gs = e6b.ground_speed(course, sim_cruise_tas, \
                #        270, \
                #        40, \
                #        sim_cruise_true) 
                sim_cruise_time_hr = float(sim_cruise_dist / sim_cruise_gs)
                sim_cruise_fuel = round(sim_cruise_flow * sim_cruise_time_hr,2)
                sim_cruise_time = int(round(sim_cruise_time_hr*60,2))

                #OVERALL FLIGHT
                sim_flight_time = float(round(sim_climb_time + sim_cruise_time + sim_descent_time, 2))
                sim_total_fuel = float(round(sim_climb_fuel + sim_cruise_fuel + sim_descent_fuel, 2))
                #TODO -----------------------
                #...based on the total fuel, can the flight be made in one leg?
                #...check wether the fuel weight in lbs, to gallons, is more than
                #...max fuel capacity-reserve fuel qty (in lbs.)
                # ie. fuel_lbs < (251 gal x 6.77lbs/gal) - (45 gal x 6.77 lbs/gal)

                #...if not, return false   .... or should this be checked by the simulator??? will the aircraft be smart by itself?
                #--------------------

                #...now that we have the flight time and total fuel consumed then append it to the table
                ROW = pd.Series([alt_lvl,sim_flight_time, sim_total_fuel, sim_cruise_gs, sim_climb_time, sim_cruise_time,sim_descent_time],\
                       ['alt', 'time', 'fuel','cruise_gs','climb_time','cruise_time','desc_time'])
                RESULT = RESULT.append(ROW,ignore_index=True)
            #----END OF if
        #----END OF for alt_lvl LOOP ---

        return RESULT
    # END OF calc_performance

    def to_json(self):
        pass
