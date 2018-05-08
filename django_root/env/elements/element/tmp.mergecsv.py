import pandas as pd

month = input("Month: ")

df = pd.read_csv("dw.cha."+str(month)+".csv")
dfSW = pd.read_csv("sw.cha."+str(month)+".csv")
newdf = df.merge(dfSW,on="alt")
newdf.to_json("winds.cha."+str(month)+".json",orient="records",double_precision=2)
