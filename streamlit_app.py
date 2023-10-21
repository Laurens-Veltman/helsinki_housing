import streamlit as st
import pandas as pd

#path = "data/helsinki.geo.json"
path = "https://github.com/dhh16/helsinki/blob/master/osaalueet.geojson?short_path=c666dcd"
with open(path) as f:
  geojson_data = f.read()

st.json(geojson_data)
#st.map(geojson_data)


