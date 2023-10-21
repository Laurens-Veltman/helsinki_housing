import streamlit as st
import pandas as pd

import json
from shapely.geometry import Polygon, Point

#path = "data/helsinki.geo.json"
#path = "https://github.com/dhh16/helsinki/blob/master/osaalueet.geojson?short_path=c666dcd"
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


def main():
    file = "https://github.com/dhh16/helsinki/blob/master/osaalueet.geojson?short_path=c666dcd"
    districts = DistrictJSON(file)
    districts.load()
    print(districts.get_polygon(171))
    print(districts.get_polygon(171).contains(Point(24.92046539288323, 60.20190764575884)))
    #st.map(geojson_data)

if __name__ == '__main__':
    main()
