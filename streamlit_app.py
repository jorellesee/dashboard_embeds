import streamlit as st
import pandas as pd
import requests


st.set_page_config(layout="wide")
col1, col2 = st.columns([1,3])
# col1, col2 , col3 = st.columns([1,3,2])

# Default parameters
default_params = {
    'format': 'geojson',
    'starttime': '2023-01-01',
    'latitude': 37.871960,
    'longitude': -122.259094,
    'maxradiuskm': 0,
    'orderby': 'time',
    'minmagnitude': 0.0
}
isFirstLoad = True
prevStartTime = default_params['starttime']
prevMaxRadius = default_params['maxradiuskm']
prevMinMag = default_params['minmagnitude']

# Create widgets for user input
starttime_param = col1.text_input("Enter the start time (e.g., 2023-01-01):",default_params['starttime'])
maxradiuskm_param = col1.number_input("Enter the max radius in kilometers (e.g., 100):",default_params['maxradiuskm'])
minmagnitude_param = col1.number_input("Enter the minimum magnitude (e.g., 2):",default_params['minmagnitude'])

isRefreshMap = col1.button("Refresh Map")
if isRefreshMap:
    col2.empty()
# Check if any parameter has changed
input_changed = (
    starttime_param != prevStartTime  or
    maxradiuskm_param != prevMaxRadius or
    minmagnitude_param != prevMinMag
)


# Update parameters with user input
custom_params = {
    'starttime': starttime_param,
    'maxradiuskm': maxradiuskm_param,
    'minmagnitude': minmagnitude_param
}
params = default_params.copy()

# Fetch earthquake data only if any parameter has changed
if isFirstLoad or input_changed:
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    if input_changed:
        params.update(custom_params)
        prevStartTime = params['starttime']
        prevMaxRadius = params['maxradiuskm']
        prevMinMag = params['minmagnitude']
    if isFirstLoad:
        isFirstLoad = False
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        coordinates_list = [(feature["geometry"]["coordinates"][1], feature["geometry"]["coordinates"][0]) for feature in data["features"]]
        cl_df = pd.DataFrame(coordinates_list, columns=['lat', 'lon'])
        col2.map(cl_df, use_container_width=True)

        # earthquakes_list = [(feature["properties"]["title"], feature["properties"]["time"], feature["properties"]["url"]) for feature in data["features"]]
        # eq_df = pd.DataFrame(earthquakes_list, columns=['title','time','url'])
        # col3.dataframe(eq_df)
    else:
        st.error(f"Error: Unable to fetch earthquake data. Status code {response.status_code}")



    


