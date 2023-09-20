import streamlit as st
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import json

st. set_page_config(layout="wide")

col1,col2 = st.columns(2)

default_params = {
    'format': 'geojson',  # Default format
    'starttime': '2023-01-01',  # Default starttime
    'latitude': 37.871960,  # Default latitude
    'longitude': -122.259094,  # Default longitude
    'maxradiuskm': 100,  # Default maxradiuskm
    'orderby': 'time',  # Default orderby
    'minmagnitude': 0.0  # Default minmagnitude
}

format_param = col1.text_input("Enter the format (e.g., geojson):")
starttime_param = col1.text_input("Enter the start time (e.g., 2023-01-01):")
maxradiuskm_param = col1.number_input("Enter the max radius in kilometers (e.g., 100):")
minmagnitude_param = col1.number_input("Enter the minimum magnitude (e.g., 2):")



custom_params = {
        'format': format_param,
        'starttime': starttime_param,
        'latitude': 37.871960,
        'longitude': -122.259094,
        'maxradiuskm': maxradiuskm_param,
        'orderby': 'time',
        'minmagnitude': minmagnitude_param
    }

params = default_params.copy()
params.update(custom_params)

base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
response = requests.get(base_url, params=params)
data = response.json()
coordinates_list = [(feature["geometry"]["coordinates"][1], feature["geometry"]["coordinates"][0]) for feature in data["features"]]

df = pd.DataFrame(coordinates_list, columns=['lat', 'lon'])
col2.map(df)
col2.write(coordinates_list)

