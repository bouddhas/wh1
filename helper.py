import requests
import pandas as pd

data = pd.read_csv('new_data.csv')
url = 'http://127.0.0.1:5000/api'
#r = requests.post(url,data)
r = requests.post(url,json=(data.loc[0].to_json()))

print(r.json())