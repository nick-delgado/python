from django.db import models
from aircraft.tmp_perf_chart import *
from tmp_winds import *
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


    def optimal_altitude(self, dist, course):
        '''
        ARGUMENTS
            dist    > Great-circle distance in nm
            course  > Course heading in normalized degrees

        RETURNS
            (Integer)   > The altitude flight level (FL250)
        '''
        global df_climb_perf
        global df_cruise_perf
        global SWDF_may
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
        #cutoff_dist = dist/2
        cutoff_dist = dist
        #print(cutoff_dist)
        #...now need to check what max altitude that would correlate to in the climb chart
        #...or generate a new DataFrame with the filtered rows that exclude max travel dist
        filter_climb_perf = df_climb_perf.loc[df_climb_perf['dist'] < cutoff_dist]
        #print(filter_climb_perf)
        max_climbing_alt_lvl = int(filter_climb_perf.loc[filter_climb_perf.index[-1]]['alt'])
        print(max_climbing_alt_lvl)
        #...make sure that the simulation doesn't go above the maximum allowed altitude set
        #...by the operator for this aircraft
        max_cruising_alt_lvl = 350 #TODO PULL FROM DATABASE <<<!!!>>>
        #...which of the altitude levels is the least? Use that as the limit
        limit_alt_lvl = max_climbing_alt_lvl if (max_climbing_alt_lvl-max_cruising_alt_lvl < 0) else max_cruising_alt_lvl
        filter_climb_perf = df_climb_perf.loc[df_climb_perf['alt'] <= limit_alt_lvl]
        #print(filter_climb_perf)
        filter_cruise_perf = df_cruise_perf.loc[df_cruise_perf['alt'] <= limit_alt_lvl]
        print(limit_alt_lvl)
        # Remaining altitude profiles will be simulated, both climbing and cruise
        #...and the altitude with the best flight time  will be selected/returned
        possible_alt_lvl = []
        for alt_lvl in range(90,limit_alt_lvl+10,10):
            if (alt_lvl%20 == 0): #...the altitude is even
                if use_odd_alt: #...and we are using odd altitudes
                    pass
                else:
                    possible_alt_lvl.append(alt_lvl)
            else: #...the altitude level is odd
                if use_odd_alt: #...and we are using odd altitudes
                    possible_alt_lvl.append(alt_lvl)
                else:
                    pass

        #Now we have the possible altitude levels that we can travel on
        #...compute all the possible flight times and see which one results in the shortest
        shortest_flight_time = 100000000000000 # ..an insanely large number (mins)
        optimal_altitude = 0
        print(possible_alt_lvl)

        e6b = E6B()
        for alt_lvl in possible_alt_lvl:
            # CLIMB SECTION
            sim_climb_time = float(filter_climb_perf.loc[filter_climb_perf['alt']==alt_lvl]['time'])
            sim_climb_dist = float(filter_climb_perf.loc[filter_climb_perf['alt']==alt_lvl]['dist'])
            sim_climb_fuel = float(filter_climb_perf.loc[filter_climb_perf['alt']==alt_lvl]['fuel'])
            
            #CRUISE SECTION
            sim_cruise_dist = dist - sim_climb_dist
            sim_cruise_tas = float(filter_cruise_perf.loc[filter_cruise_perf['alt']==alt_lvl]['tas'])
            sim_cruise_flow = float(filter_cruise_perf.loc[filter_cruise_perf['alt']==alt_lvl]['flow'])
            sim_cruise_wca = e6b.wind_correction_angle(course, sim_cruise_tas, SWDF_mar.loc[SWDF_mar['alt']==alt_lvl]['dir'], SWDF_mar.loc[SWDF_mar['alt']==alt_lvl]['speed'])
            sim_cruise_true = sim_cruise_wca + course
            sim_cruise_gs = e6b.ground_speed(course, sim_cruise_tas, SWDF_mar.loc[SWDF_mar['alt']==alt_lvl]['dir'], SWDF_mar.loc[SWDF_mar['alt']==alt_lvl]['speed'], sim_cruise_true) # this ground speed is wind adjusted
            sim_cruise_time_hr = float(sim_cruise_dist / sim_cruise_gs)
            sim_cruise_fuel = sim_cruise_flow * sim_cruise_time_hr
            sim_cruise_time = sim_cruise_time_hr*60

            #OVERALL FLIGHT
            sim_flight_time = sim_climb_time + sim_cruise_time
            sim_total_fuel = sim_climb_fuel + sim_cruise_fuel
            # ... now that we have the simulation flight time and fuel burned, weight those two variables
            
            if (sim_flight_time < shortest_flight_time):
                shortest_flight_time = sim_flight_time
                optimal_altitude = alt_lvl

            print("[ALT "+str(alt_lvl)+"] (Climb: "+ str(sim_climb_time) + " min | "+str(sim_climb_dist)+" nm | "+str(sim_climb_fuel)+" lbs)  >> "\
                    +"(Cruise: "+str(sim_cruise_time)+" min | "+str(sim_cruise_dist)+" nm | "+str(sim_cruise_fuel)+" lbs | "\
                    +str(sim_cruise_tas)+" nmph) \n     ===> "+str(sim_flight_time) + "min  \n     ===> "+str(sim_total_fuel)+" lbs")

        print("RECOMMENDED ALTITUDE: " + str(optimal_altitude) + "  FLIGHT TIME="+str(shortest_flight_time))
