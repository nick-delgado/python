import pandas as pd

ac_model = input("Aircraft Model: ")

df_tas = pd.read_csv("ac."+str(ac_model)+".climb.tas.csv")
df_time = pd.read_csv("ac."+str(ac_model)+".climb.time.csv")
newdf = df_tas.merge(df_time,on="alt")
df_fuel = pd.read_csv("ac."+str(ac_model)+".climb.fuel.csv")
newdf = newdf.merge(df_fuel,on="alt")
df_dist = pd.read_csv("ac."+str(ac_model)+".climb.dist.csv")
newdf = newdf.merge(df_dist,on="alt")
#dfTime = pd.read_csv("ac."+str(ac_model)+".climb.time.csv")
#dfSW = pd.read_csv("ac."+str(ac_model)+".tas.csv")
#dfSW = pd.read_csv("sw.cha."+str(ac_model)+".csv")
newdf.to_json("ac."+str(ac_model)+".climb.perf.json",orient="records",double_precision=2)
