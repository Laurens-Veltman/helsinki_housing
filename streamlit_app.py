import streamlit as st
import pandas as pd
import requests
import folium

import json
from shapely.geometry import Polygon, Point
from streamlit_folium import folium_static

class DistrictJSON:
    def __init__(self, filename):
        self._filename = filename
        self._poly_dict = {}

        self.load()

    def load(self):
        with open(self._filename) as f:
            data = json.loads(f.read())

            for shape in data['features']:
                id = int(shape['properties']['TUNNUS'])
                coords = shape['geometry']['coordinates'][0]
                self._poly_dict[id] = Polygon(coords)

    def get_polygon(self, id):
        return self._poly_dict[id]

def clean_data(file, selection):
    with open(file) as f:
        data = json.loads(f.read())
    
        for shape in data['features']:
            st.write(shape)
            #id = int(shape['properties']['TUNNUS'])
            filtered_data = [row for row in data if row.get('NIMI') not in selection]

            
def main():
    geojson = "data/helsinki.geojson"
    data = pd.read_csv("data/hhdata_csv.csv",header=4).iloc[0:81,:]
    m = folium.Map(location=[60.2019,24.9204], zoom_start=11, scrollWheelZoom=False, tiles='CartoDB positron')
    folium.GeoJson(geojson, name='geojson').add_to(m)
    st.title('Helsinki housing prices through the years')
    folium_static(m)

    st.dataframe(data)

    #clean_data(file)

if __name__ == '__main__':
    main()
