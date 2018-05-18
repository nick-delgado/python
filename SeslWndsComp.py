import numpy as np
import xarray as xr
import math

ds_u = xr.open_dataset('uwnd.mon.mean.nc')
ds_v = xr.open_dataset('vwnd.mon.mean.nc')
ds_temp = xr.open_dataset('air.mon.mean.nc')

# PRESSURE ALTITUDE
# NOAA formula from converting millibars (mb) to pressure altitude in feet (ft)
#
#     FT = 145366.45 * ( 1 - ( ( Station pressure in mb / 1013.25 )^0.190284  ) ) 
#

# DATA SET/ARRAY FORMAT
#
# LEVEL  [ 0 to 16 ]  - 1000.0 millibar

#iterate through a time period (YEARLY!!!!)
#  -------------------------------------------------------------------------------------
# [768] -> 2012-01-01       [769] -> 2012-02-01     [770] -> 2012-03 ...    [779] -> 2012-12
# [780] -> 2013-01-01       [781] -> 2013-02-01     [782] -> 2013-03 ...    [827] -> 2013-12
# ...                       ...                     ...              ...    ...
# [828] -> 2017-01-01       [829] -> 2017-02-01     [830] -> 2017-03        [839] -> 2017-12
# [840] -> 2018-01          [841] -> 2018-02

# so roughly 5 years
# Start from 2017 backwards to include full-year monthly data (2018 only partial)

MONTH_jan_ix = np.array([]) # this is the ix of all the January months over a 5 year gap which start at start=768
MONTH_feb_ix = np.array([])
MONTH_mar_ix = np.array([])
MONTH_apr_ix = np.array([])
MONTH_may_ix = np.array([])
MONTH_jun_ix = np.array([])
MONTH_jul_ix = np.array([])
MONTH_aug_ix = np.array([])
MONTH_sep_ix = np.array([])
MONTH_oct_ix = np.array([])
MONTH_nov_ix = np.array([])
MONTH_dec_ix = np.array([])
start = 828
NUM_YRS = 10

################# RESULT ###############
RESULT_jan_u = np.array([])
RESULT_jan_v = np.array([])
RESULT_jan_wdir_10000ft = np.array([])
RESULT_jan_wspd_10000ft = np.array([])


for year_ct in range(0,NUM_YRS):
    MONTH_jan_ix = np.append(MONTH_jan_ix, (start+0) - (12*year_ct) )
    MONTH_feb_ix = np.append(MONTH_feb_ix, (start+1) - (12*year_ct) )
    MONTH_mar_ix = np.append(MONTH_mar_ix, (start+2) - (12*year_ct) )
    MONTH_apr_ix = np.append(MONTH_apr_ix, (start+3) - (12*year_ct) )
    MONTH_may_ix = np.append(MONTH_may_ix, (start+4) - (12*year_ct) )
    MONTH_jun_ix = np.append(MONTH_jun_ix, (start+5) - (12*year_ct) )
    MONTH_jul_ix = np.append(MONTH_jul_ix, (start+6) - (12*year_ct) )
    MONTH_aug_ix = np.append(MONTH_aug_ix, (start+7) - (12*year_ct) )
    MONTH_sep_ix = np.append(MONTH_sep_ix, (start+8) - (12*year_ct) )
    MONTH_oct_ix = np.append(MONTH_oct_ix, (start+9) - (12*year_ct) )
    MONTH_nov_ix = np.append(MONTH_nov_ix, (start+10) - (12*year_ct) )
    MONTH_dec_ix = np.append(MONTH_dec_ix, (start+11) - (12*year_ct) )

    
# Now we have the indeces of all the months for a range of years, separated per month
# ...we need to now start at one geographical point or line and go through the datas for each month
# ...for that particular point

# Start with a fixed latitude
#
#   CHANGE FROM 0-360 DEG TO ....    
#
#     >>> 360|0 >>>
#        --------
#       / /  |  \ \
#     / /    |    \ \
#   / /   ---|---   \ \
#   | |             | |
#   | |----EARTH--- | |
#   | |      |      | |
#   \ \      |      / /
#     \ \ -- | --  / /
#       \ \  | / /
#         --------
# -180       0      180
#
#   ...... -180 > 180 FORMAT

LAT90_ix = 22 # This translates to the 35 deg lat in the dataset

LON360_ix = 110 #At this lon[110] index is the normalized latitude -85.000 deg  (originally '275'degrees)
LON360 = float(ds_u.lon[LON360_ix])
NORM_LONG = ( (LON360 + 180) % 360 ) - 180
    

LEVEL_MB_ix = 3 # This translates to 700 millibars which is roughly 10,000ft


# ... now we start iterating over the different levels as well
for level_ix in range(0,5): 
    level_ft = 145366.45 * ( 1 - ( ( ds_u.level[level_ix] / 1013.25 )**0.190284  ) ) 
    #level_ft = 145366.45 * ( 1 - ( ( level_mb / 1013.25 )**0.190284  ) ) 
    norm_level_ft = int(round(float(level_ft),0))  # Normalize levels to 1000 ft increments 1000,2000,...,18000,...43000
    flight_level_ft = norm_level_ft / 100  # Convert altitude to Flight Level standard

    #zero out all arrays temporarily used for this level
    RESULT_jan_u = np.array([])
    RESULT_jan_v = np.array([])
    RESULT_jan_wdir = np.array([])
    RESULT_jan_wspd = np.array([])
    for year_ct in range(0,NUM_YRS):
        #month to month querying
        # u-wind vector (monthly mean) for this particular lat,long,alt
        u_vect = ds_u.uwnd[int(MONTH_jan_ix[year_ct]), level_ix, LAT90_ix, LON360_ix]
        v_vect = ds_v.vwnd[int(MONTH_jan_ix[year_ct]), level_ix, LAT90_ix, LON360_ix]
        # now.. we append it to the array which holds the mean for that month
        RESULT_jan_u = np.append(RESULT_jan_u, u_vect)
        RESULT_jan_v = np.append(RESULT_jan_v, v_vect)
        # we need to calculate the mean of the angles 
        wdir = ( 270 - round(math.degrees(math.atan2(- v_vect, - u_vect)),2)+180 ) % 360
        wspd = round( (math.sqrt( (u_vect**2) + (v_vect**2) )) * 1.943844, 2)
        RESULT_jan_wdir = np.append( RESULT_jan_wdir, wdir)
        RESULT_jan_wspd = np.append( RESULT_jan_wspd, wspd)
        print(str(norm_level_ft)+"ft = DIR: "+str(wdir) + " @ "+ str(wspd) + "   >  u,v = [ "+str(float(u_vect))+" , " + str(float(v_vect))+" ]")

    wdir_avg = RESULT_jan_wdir.mean() # This is not going to work since we are dealing with a circular mean
    sin_func = np.vectorize(lambda angle: math.sin( math.radians( angle ) ) )
    cos_func = np.vectorize(lambda angle: math.cos( math.radians( angle ) ) )
    RESULT_jan_wdir_sin = sin_func(RESULT_jan_wdir)
    RESULT_jan_wdir_cos = cos_func(RESULT_jan_wdir)
    wdir_mean = ( 270 - round( math.degrees( math.atan2(RESULT_jan_wdir_sin.mean(), RESULT_jan_wdir_cos.mean() ) ), 2) ) % 360
    wdir_max = RESULT_jan_wdir.max()
    wdir_min = RESULT_jan_wdir.min()
    wdir_std = RESULT_jan_wdir.std()
    wspd_avg = RESULT_jan_wspd.mean()
    wspd_max = RESULT_jan_wspd.max()
    wspd_min = RESULT_jan_wspd.min()
    wspd_std = RESULT_jan_wspd.std()
    print("--------WIND\n" +\
            "AVG="+str(wdir_avg) + "\n"+ \
            "MEAN="+str(wdir_mean) + "\n"+ \
            "MAX="+str(wdir_max) + "\n"+ \
            "MIN="+str(wdir_min) + "\n"+\
            "RANGE="+str(wdir_max - wdir_min) + "\n"+\
            "STD="+str(wdir_std) + "\n"\
            )
    print("--------SPEED\n" +\
            "AVG="+str(wspd_avg) + "\n"+ \
            "MAX="+str(wspd_max) + "\n"+ \
            "MIN="+str(wspd_min) + "\n"+\
            "RANGE="+str(wspd_max - wspd_min) + "\n"+\
            "STD="+str(wspd_std) + "\n"\
            )

#print(RESULT_jan_u)
#print(RESULT_jan_v)
