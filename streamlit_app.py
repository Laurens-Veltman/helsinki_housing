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

def pull_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        geojson_data = json.loads(response.text)
        return geojson_data
    else:
        # Print an error message if the request was not successful
        print(f"Failed to fetch the file. Status Code: {response.status_code}")
        return None
            
def main():
    file = "data/helsinki.geojson"
    districts = DistrictJSON(file)
    #print(districts.get_polygon(171))
    #print(districts.get_polygon(171).contains(Point(24.92046539288323, 60.20190764575884)))
    
    m = folium.Map(location=[60.2019,24.9204], zoom_start=11)
    folium.GeoJson(districts._poly_dict, name='geojson').add_to(m)
    
    # Display the map using Streamlit
    st.title('Helsinki housing prices through the years')
    folium_static(m)

if __name__ == '__main__':
    main()
