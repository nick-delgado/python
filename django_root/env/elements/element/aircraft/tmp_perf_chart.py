import json
import pandas as pd

json_file = open('aircraft/ac.ea50.climb.perf.json')
json_str = json_file.read()
json_data = json.loads(json_str)
df_climb_perf = pd.DataFrame.from_dict(json_data)

json_file = open('aircraft/ac.ea50.cruise.perf.json')
json_str = json_file.read()
json_data = json.loads(json_str)
df_cruise_perf = pd.DataFrame.from_dict(json_data)

json_file = open('aircraft/ac.ea50.descent.perf.json')
json_str = json_file.read()
json_data = json.loads(json_str)
df_descent_perf = pd.DataFrame.from_dict(json_data)
