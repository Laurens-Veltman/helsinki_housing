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

def clean_df(data):
    df = pd.DataFrame(data)
    def process_data(df, column_name='Toimipaikka'):
        def process_row(row):
            if ',' in row[column_name]:
                values = row[column_name].split(',')
                return [{column_name: val.strip(), **{col: row[col] for col in df.columns if col != column_name}} for val in values]
            else:
                return {column_name: row[column_name].strip(), **{col: row[col] for col in df.columns if col != column_name}}
        new_rows = df.apply(process_row, axis=1).tolist()
        if any(isinstance(item, list) for item in new_rows):
            new_rows = [item for sublist in new_rows for item in sublist]
        new_df = pd.DataFrame(new_rows, columns=df.columns)
        return new_df
    new_df = process_data(df)
    return new_df

def init_mask(geojson, data, m):
    selection = [i.lower() for i in data['Toimipaikka'].unique()]
    rejected = []
    with open(geojson) as f:
        json_file = json.loads(f.read())
    
        for shape in json_file['features']:
            name = shape['properties']['NIMI'].lower()
            if name in selection:
                folium.GeoJson(shape, name='geojson').add_to(m)
            else:
                rejected.append(name)
    st.write(len(rejected))
    st.write(len(selection))

def main():
    data = pd.read_csv("data/hhdata_csv.csv",header=4).iloc[0:83,:]
    data = clean_df(data)
    st.dataframe(data)
    geojson = "data/helsinki.geojson"
    m = folium.Map(location=[60.2019,24.9204], zoom_start=11, scrollWheelZoom=False, tiles='CartoDB positron')
    st.title('Helsinki housing prices through the years')
    init_mask(geojson, data, m)
    folium_static(m)


if __name__ == '__main__':
    main()
