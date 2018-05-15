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
        possible_alt_lvl = []
        # Run various simulations/calculations
        #...for a given distance and heading
        #...to figure out which cruising altitude 
        #...will be the best based on data from the A/C performance charts.
        #...Course between [000-179] >> Odd Flight Levels (ie. FL230,FL250,FL270)
        #...Course between [180-359] >> Even Flight Levels (ie. FL220,FL240,FL260)
        #
        # Eliminate altitudes in climb/cruise performance chart if the overall
        #...distance is less than twice the climbing distance
        #cutoff_dist = dist/2 #TODO WHICH ONE TO SELECT
        # 
        cutoff_dist = dist
        #...now need to check what max altitude that would correlate to in the climb chart
        #...or generate a new DataFrame with the filtered rows that exclude max travel dist
        filter_climb_perf = df_climb_perf.loc[df_climb_perf['dist'] < cutoff_dist]
        max_climbing_alt_lvl = int(filter_climb_perf.loc[filter_climb_perf.index[-1]]['alt'])
        #...make sure that the simulation doesn't go above the maximum allowed altitude set
        #...by the operator for this aircraft
        #...which of the altitude levels is the least? Use that as the limit
        limit_alt_lvl = max_climbing_alt_lvl if (max_climbing_alt_lvl-max_cruising_alt_lvl < 0) else max_cruising_alt_lvl
        filter_climb_perf = df_climb_perf.loc[df_climb_perf['alt'] <= limit_alt_lvl]
        #print(filter_climb_perf)
        filter_cruise_perf = df_cruise_perf.loc[df_cruise_perf['alt'] <= limit_alt_lvl]
        #print(filter_cruise_perf)
        #...now get descent chart performance
        filter_descent_perf = df_descent_perf.loc[df_descent_perf['alt']<=limit_alt_lvl]
        #...now we have a table with the list of all the altitudes up to either (1) the max climbing altitude set by the 
        #...operator (ie.FL 410) or (2) the max climbing altitude based on max distance needed to climb to a certain altitude
        #...(ie. if total distance is 21nm, then we can only climb up to the max FL 150)
        #
        # Eliminate altitudes in climb/cruise performance chart based on whether
        #...the course is to the East or to the West
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
        # Remaining altitude profiles will be simulated, both climbing and cruise

        e6b = E6B() # Initialize E6B computing utility
        for alt_lvl in possible_alt_lvl:

            # CLIMB SECTION -- LOOKUP
            sim_climb_time = float(filter_climb_perf.loc[filter_climb_perf['alt']==alt_lvl]['time'])
            sim_climb_dist = float(filter_climb_perf.loc[filter_climb_perf['alt']==alt_lvl]['dist'])
            sim_climb_fuel = float(filter_climb_perf.loc[filter_climb_perf['alt']==alt_lvl]['fuel'])

            # DESCENT SECTION -- LOOKUP
            sim_descent_time = float(filter_descent_perf.loc[filter_descent_perf['alt']==alt_lvl]['time'])
            sim_descent_dist = float(filter_descent_perf.loc[filter_descent_perf['alt']==alt_lvl]['dist'])
            sim_descent_fuel = float(filter_descent_perf.loc[filter_descent_perf['alt']==alt_lvl]['fuel'])
            
            # Eliminate altitudes for which the distance to climb + distance to descent is greater than the total dist
            if (sim_climb_dist + sim_descent_dist < dist):
                #CRUISE SECTION -- COMPUTE
                sim_cruise_dist = dist - sim_climb_dist - sim_descent_dist
                sim_cruise_tas = float(filter_cruise_perf.loc[filter_cruise_perf['alt']==alt_lvl]['tas'])
                sim_cruise_flow = float(filter_cruise_perf.loc[filter_cruise_perf['alt']==alt_lvl]['flow'])
                sim_cruise_wca = e6b.wind_correction_angle(course, sim_cruise_tas, \
                        float(winds_df.loc[winds_df['alt']==alt_lvl]['dir']), \
                        float(winds_df.loc[winds_df['alt']==alt_lvl]['speed']))
                #sim_cruise_wca = e6b.wind_correction_angle(course, sim_cruise_tas, \
                #        270, \
                #        40)
                #sim_cruise_wca = 0
                sim_cruise_true = sim_cruise_wca + course
                sim_cruise_gs = e6b.ground_speed(course, sim_cruise_tas, \
                        float(winds_df.loc[winds_df['alt']==alt_lvl]['dir']), \
                        float(winds_df.loc[winds_df['alt']==alt_lvl]['speed']), \
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
                #...based on the total fuel, can the flight be made in one leg?
                #...check wether the fuel weight in lbs, to gallons, is more than
                #...max fuel capacity-reserve fuel qty (in lbs.)
                # ie. fuel_lbs < (251 gal x 6.77lbs/gal) - (45 gal x 6.77 lbs/gal)

                #...if not, return false

                #...now that we have the flight time and total fuel consumed then append it to the table
                ROW = pd.Series([alt_lvl,sim_flight_time, sim_total_fuel, sim_cruise_gs, sim_climb_time, sim_cruise_time,sim_descent_time],\
                       ['alt', 'time', 'fuel','cruise_gs','climb_time','cruise_time','desc_time'])
                RESULT = RESULT.append(ROW,ignore_index=True)
                #----END OF FOR LOOP ---

        return RESULT

    def to_json(self):
        pass
