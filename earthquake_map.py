import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")

col1, col2 , col3 = st.columns([1,3,1])

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

# Create widgets for user input
starttime_param = col1.text_input("Enter the start time (e.g., 2023-01-01):",default_params['starttime'])
maxradiuskm_param = col1.number_input("Enter the max radius in kilometers (e.g., 100):",default_params['maxradiuskm'])
minmagnitude_param = col1.number_input("Enter the minimum magnitude (e.g., 2):",default_params['minmagnitude'])

# Check if any parameter has changed
input_changed = (
    starttime_param != default_params['starttime'] or
    maxradiuskm_param != default_params['maxradiuskm'] or
    minmagnitude_param != default_params['minmagnitude']
)

# Update parameters with user input
custom_params = {
    'starttime': starttime_param,
    'maxradiuskm': maxradiuskm_param,
    'minmagnitude': minmagnitude_param
}
params = default_params.copy()
params.update(custom_params)

# Fetch earthquake data only if any parameter has changed
if input_changed:
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        coordinates_list = [(feature["geometry"]["coordinates"][1], feature["geometry"]["coordinates"][0]) for feature in data["features"]]
        cl_df = pd.DataFrame(coordinates_list, columns=['lat', 'lon'])
        col2.map(cl_df, use_container_width=True)
        # col3.write(data)
        earthquakes_list = [(feature["properties"]["title"], feature["properties"]["time"], feature["properties"]["url"]) for feature in data["features"]]
        eq_df = pd.DataFrame(earthquakes_list, columns=['title','time','url'])
        col3.dataframe(eq_df)
    else:
        st.error(f"Error: Unable to fetch earthquake data. Status code {response.status_code}")


    
    


