import streamlit as st
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import json
import csv

st. set_page_config(layout="wide")

col1,col2 = st.columns(2)

default_params = {
}
#input params
custom_params = {
}


# variable to store the JWT token
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX3BrIjoiMTE1MjkiLCJpYXQiOjE2OTQwOTQ5OTIsImV4cCI6MTcyNTcxNzM5Mn0.K5lQTxGmkyMJtZXgB3pReJyXF1yAxlYSUzlcM1B9QOw'
# set the authorization header
headers = {'Authorization': 'Bearer ' + token} # set the request parameters

# make the GET request
ll_response = requests.get('https://www.mysmartcover.com/api/locations/list.php',headers=headers)
ll_data = ll_response.json()
coordinates_list = [(location['latitude'], location["longitude"]) for location in ll_data["locations"]]




st.sidebar.title("sidebar")

col1.write(ll_data)
df = pd.DataFrame(coordinates_list, columns=['lat', 'lon'])
col1.map(df)

hd_params = {'location': 22375,
          'start_time': '2022-12-31 23:59:59',
          'end_time': '2023-1-31 23:59:59',
          'data_type': '3'}
hd_response = requests.get('https://www.mysmartcover.com/api/locations/data.php',params=hd_params,headers=headers)
hd_data = hd_response.json()
col2.header("Historical Data ID: 22375")
col2.write(hd_data)
