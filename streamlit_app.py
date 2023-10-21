import streamlit as st
import pandas as pd

path = "/main/data/helsinki.geo.json"
with open(path) as f:
  geojson_data = f.read()

st.map(geojson_data)
