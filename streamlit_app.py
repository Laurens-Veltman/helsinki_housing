import streamlit as st
import pandas as pd
from streamlit_folium import folium_static

path = "data/helsinki.geo.json"
with open(path) as f:
  geojson_data = f.read()

#st.map(geojson_data)

# Create a folium map centered at a specific location
m = folium.Map(location=[0, 0], zoom_start=2)

# Add the GeoJSON data to the map
folium.GeoJson(geojson_data, name='geojson').add_to(m)

# Display the map using Streamlit
st.title('GeoJSON Visualization with Folium in Streamlit')
folium_static(m)
