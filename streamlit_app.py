import streamlit as st
import pandas as pd
import requests

import json
from shapely.geometry import Polygon, Point

#path = "data/helsinki.geo.json"
#with open(path) as f:
#  geojson_data = f.read()

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
    file_name = 'output.geojson'
    geojson_data = requests.get(url).text
    with open(file_name, 'w') as f:
        json.dump(geojson_data, f)
    return file_name
            
def main():
    url = "https://github.com/dhh16/helsinki/blob/master/osaalueet.geojson"
    file = pull_file(url)
    #file = "data/helsinki.geo.json"
    st.json(file)
    #districts = DistrictJSON(file)
    #districts.load()
    #print(districts.get_polygon(171))
    #print(districts.get_polygon(171).contains(Point(24.92046539288323, 60.20190764575884)))
    #st.map(geojson_data)

if __name__ == '__main__':
    main()
