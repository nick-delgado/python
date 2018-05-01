import pandas as pd

df = pd.read_csv('ea500.perf.tfdc.csv')

cruise_df = pd.read_csv('ea500.perf.cruise.csv', index_col=0)
