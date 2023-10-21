import streamlit as st
import pandas as pd
from streamlit_folium import folium_static

#path = "data/helsinki.geo.json"
path = "https://github.com/dhh16/helsinki/blob/master/osaalueet.geojson?short_path=c666dcd"
with open(path) as f:
  geojson_data = f.read()

st.map(geojson_data)


