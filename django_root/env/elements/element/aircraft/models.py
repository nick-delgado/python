from django.db import models
import pandas as pd
from aircraft.tmp_perf_chart import *
from utils import E6B



# Create your models here.
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


    def calc_performances(self, dist, course, max_cruising_alt_lvl, winds_df, time_cost_min=13.33, fuel_cost_lbs=1.16):
        '''
        ARGUMENTS
            dist    > Great-circle distance in nm
            course  > Course heading in normalized degrees
            winds   > NumPy array

        RETURNS
            (Integer)   > The altitude flight level (FL250)
        '''
        global df_climb_perf
        global df_cruise_perf
        RESULT = pd.DataFrame(columns=['alt','time','fuel'])
        # Run various simulations/calculations
        #...for a given distance and heading
        #...to figure out which cruising altitude 
        #...will be the best based on data from the A/C performance charts.
        #...Course between [000-179] >> Odd Flight Levels (ie. FL230,FL250,FL270)
        #...Course between [180-359] >> Even Flight Levels (ie. FL220,FL240,FL260)
        #
        # Eliminate altitudes in climb/cruise performance chart based on whether
        #...the course is to the East or to the West
        use_odd_alt = True if (round(course,0) < 180) else False
        #print(use_odd_alt)
        # Eliminate altitudes in climb/cruise performance chart if the overall
        #...distance is less than twice the climbing distance
        #cutoff_dist = dist/2 #TODO WHICH ONE TO SELECT
        cutoff_dist = dist
        #...now need to check what max altitude that would correlate to in the climb chart
        #...or generate a new DataFrame with the filtered rows that exclude max travel dist
        filter_climb_perf = df_climb_perf.loc[df_climb_perf['dist'] < cutoff_dist]
        #print(filter_climb_perf)
        max_climbing_alt_lvl = int(filter_climb_perf.loc[filter_climb_perf.index[-1]]['alt'])
        #print(max_climbing_alt_lvl)
        #...make sure that the simulation doesn't go above the maximum allowed altitude set
        #...by the operator for this aircraft
        #max_cruising_alt_lvl = 410 
        #...which of the altitude levels is the least? Use that as the limit
        limit_alt_lvl = max_climbing_alt_lvl if (max_climbing_alt_lvl-max_cruising_alt_lvl < 0) else max_cruising_alt_lvl
        filter_climb_perf = df_climb_perf.loc[df_climb_perf['alt'] <= limit_alt_lvl]
        #print(filter_climb_perf)
        filter_cruise_perf = df_cruise_perf.loc[df_cruise_perf['alt'] <= limit_alt_lvl]
        #print(limit_alt_lvl)
        # Remove altitude levels based on whether they are odd or even and based on course
        possible_alt_lvl = []
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

        # Remaining altitude profiles will be simulated, both climbing and cruise
        #Now we have the possible altitude levels that we can travel on
        #...compute all the possible flight times and see which one results in the shortest
        shortest_flight_time = 100000000000000 # ..an insanely large number (mins)
        least_cost = 10000000000000000
        least_fuel_usage = 10000000000000
        optimal_altitude = 0
        #print(possible_alt_lvl)

        e6b = E6B() # Initialize E6B computing utility
        for alt_lvl in possible_alt_lvl:
            # CLIMB SECTION
            sim_climb_time = float(filter_climb_perf.loc[filter_climb_perf['alt']==alt_lvl]['time'])
            sim_climb_dist = float(filter_climb_perf.loc[filter_climb_perf['alt']==alt_lvl]['dist'])
            sim_climb_fuel = float(filter_climb_perf.loc[filter_climb_perf['alt']==alt_lvl]['fuel'])
            
            #CRUISE SECTION
            sim_cruise_dist = dist - sim_climb_dist
            sim_cruise_tas = float(filter_cruise_perf.loc[filter_cruise_perf['alt']==alt_lvl]['tas'])
            sim_cruise_flow = float(filter_cruise_perf.loc[filter_cruise_perf['alt']==alt_lvl]['flow'])
            sim_cruise_wca = e6b.wind_correction_angle(course, sim_cruise_tas, \
                    float(winds_df.loc[winds_df['alt']==alt_lvl]['dir']), \
                    float(winds_df.loc[winds_df['alt']==alt_lvl]['speed']))
            sim_cruise_true = sim_cruise_wca + course
            sim_cruise_gs = e6b.ground_speed(course, sim_cruise_tas, \
                    float(winds_df.loc[winds_df['alt']==alt_lvl]['dir']), \
                    float(winds_df.loc[winds_df['alt']==alt_lvl]['speed']), \
                    sim_cruise_true) 
            sim_cruise_time_hr = float(sim_cruise_dist / sim_cruise_gs)
            sim_cruise_fuel = round(sim_cruise_flow * sim_cruise_time_hr,2)
            sim_cruise_time = int(round(sim_cruise_time_hr*60,2))

            #OVERALL FLIGHT
            sim_flight_time = float(round(sim_climb_time + sim_cruise_time, 2))
            sim_total_fuel = float(round(sim_climb_fuel + sim_cruise_fuel, 2))
            #...now that we have the total flight time and total fuel consumed at that altitude do a cost indexing
            sim_flight_time_cost = float(round(sim_flight_time * time_cost_min,2))
            sim_total_fuel_cost = float(round(sim_total_fuel * fuel_cost_lbs,2))
            sim_cost = float(round(sim_flight_time_cost + sim_total_fuel_cost,2))
            #...now that we have the flight time and total fuel consumed then append it to the table
            #RESULT = np.append(RESULT, [[alt_lvl, sim_flight_time, sim_total_fuel]], axis=0)
            ROW = pd.Series([alt_lvl,sim_flight_time, sim_total_fuel], ['alt', 'time', 'fuel'])
            RESULT = RESULT.append(ROW,ignore_index=True)


            if (sim_cost <= least_cost):
                least_cost = sim_cost
                shortest_flight_time = sim_flight_time
                least_fuel_usage = sim_total_fuel
                optimal_altitude = alt_lvl

            #print("[ALT "+str(alt_lvl)+"] (Climb: "+ str(sim_climb_time) + "min | "+str(sim_climb_dist)+"nm | "+str(round(sim_climb_fuel,2))+"lbs) / "\
            #        +"(Cruise: "+str(sim_cruise_time)+"min | "+str(sim_cruise_dist)+"nm | "+str(sim_cruise_fuel)+"lbs | "\
            #        +str(sim_cruise_tas)+"nmph) \n     ===> "+str(sim_flight_time) + "min  \n     ===> "+str(sim_total_fuel)+" lbs" \
            #        +"\n    ==========>> COST: "+str(sim_cost)) 

        print("RECOMMENDED ALTITUDE: " + str(optimal_altitude) + "  FLIGHT TIME="+str(shortest_flight_time)+"min  >  FUEL BURNED: "+str(least_fuel_usage))
        return RESULT
