from scipy import interpolate
import numpy as np
import pandas as pd



def step_interpolate():
    X1 = int(input("Starting altitude: "))
    X2 = int(input("Ending altitude: "))
    Y1 = int(input("Starting point for Y: "))
    Y2 = int(input("Ending point for Y: "))
    inc = int(input("Increments: "))

    global intp_df
    xdata = [X1,X2]
    ydata = [Y1,Y2]

    new_df = pd.DataFrame({'alt':[X1], 'val':[Y1]})
    intp_df = intp_df.append(new_df, ignore_index=True)
    f = interpolate.interp1d(xdata,ydata)
    for xval in range(X1+inc,X2,inc):
        yval = f(int(xval))
        new_df = pd.DataFrame({'alt':[xval], 'val':[yval]})
        intp_df = intp_df.append(new_df, ignore_index=True)
        #intp_df = intp_df.append({'alt':xval,'val':yval}, ignore_index=True)
        #print(str(yval))

intp_df = pd.DataFrame(columns=['alt','val'])
steps = int(input("Number of levels: "))

for step in range(0,int(steps)):
    step_interpolate()

print(intp_df)
