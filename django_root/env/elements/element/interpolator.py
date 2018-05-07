from scipy import interpolate
import numpy as np
import pandas as pd
import sys,os


def step_interpolate(flag):
    try:
        X1 = int(input("Starting altitude: "))
        X2 = int(input("Ending altitude: "))
        Y1 = int(input("Starting point for Y: "))
        Y2 = int(input("Ending point for Y: "))
    except KeyboardInterrupt:
        print("---INTERRUPTED---")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    global intp_df, inc
    xdata = [X1,X2]
    ydata = [Y1,Y2]

    intp_df = intp_df.append(pd.DataFrame({'alt':[X1], 'val':[Y1]}), ignore_index=True)
    f = interpolate.interp1d(xdata,ydata)
    for xval in range(X1+inc,X2,inc):
        yval = f(int(xval))
        intp_df = intp_df.append(pd.DataFrame({'alt':[xval], 'val':[yval]}), ignore_index=True)

    if (flag):
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
intp_df.to_csv(str(OF),index=False)
