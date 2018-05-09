import pandas as pd

ac_model = input("Aircraft Model: ")

df_tas = pd.read_csv("ac."+str(ac_model)+".cruise.tas.csv")
df_flow = pd.read_csv("ac."+str(ac_model)+".cruise.flow.csv")
newdf = df_tas.merge(df_flow,on="alt")
#df_fuel = pd.read_csv("ac."+str(ac_model)+".cruise.fuel.csv")
#newdf = newdf.merge(df_fuel,on="alt")
#df_dist = pd.read_csv("ac."+str(ac_model)+".cruise.dist.csv")
#newdf = newdf.merge(df_dist,on="alt")
newdf.to_json("ac."+str(ac_model)+".cruise.perf.json",orient="records",double_precision=2)
