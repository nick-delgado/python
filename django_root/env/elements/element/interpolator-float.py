#############################
# Interpolator : 
# Program used to interpolate data between different 'levels' or 'steps'
# of a chart      

#i          FL350  ____________
#                 /
# FL250 _________/     <<<<
#      /                <<<
#     /                  <<
#    / FL180             << WINDS
# 
# In this project it is used for interpolating seasonal winds from different
# data sources where not all the flight levels (FL) are defined
# and also to interpolate the performance data of an aircraft
# based on the data from the Time, Fuel, and Distance to Climb chart
# as well as the Cruise Performance chart
#############################
from scipy import interpolate
import numpy as np
import pandas as pd
import sys,os


def step_interpolate(flag):
    try:
        X1 = int(input("Starting altitude: "))
        Y1 = float(input("Starting value: "))
        X2 = int(input("Ending altitude: "))
        Y2 = float(input("Ending value: "))
    except KeyboardInterrupt:
        print("\n\r---INTERRUPTED---")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    global intp_df, inc
    xdata = [X1,X2]
    ydata = [Y1,Y2]

    #Add the first first row
    intp_df = intp_df.append(pd.DataFrame({'alt':[X1], 'val':[Y1]}), ignore_index=True)
    f = interpolate.interp1d(xdata,ydata)
    for xval in range(X1+inc,X2,inc):
        yval = f(int(xval))
        intp_df = intp_df.append(pd.DataFrame({'alt':[xval], 'val':[yval]}), ignore_index=True)

    if (flag):
        #Add the last row
        intp_df = intp_df.append(pd.DataFrame({'alt':[X2], 'val':[Y2]}), ignore_index=True)

intp_df = pd.DataFrame(columns=['alt','val'])
steps = int(input("Number of levels: "))
inc = int(input("Increments: "))

for step in range(0,int(steps)):
    if (step==int(steps)-1):
        step_interpolate(True)
    else:
        step_interpolate(False)

print(intp_df)
OF = input("File Name:")
intp_df.to_csv(str(OF),index=False,float_format='%.2f')