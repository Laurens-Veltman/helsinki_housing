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

def clean_df(df):
    def split_commas(df,column_name):
        new_df = pd.DataFrame(columns=df.columns)
        indices_to_drop = []
        for index, row in df.iterrows():
            if ',' in row[column_name]:
                names = row[column_name].split(',')
                row1,row2 = row.copy(),row.copy()
                row1[column_name],row2[column_name] = names[0].strip(),names[1].strip()
                out = pd.DataFrame([row1,row2]).reset_index(drop=True)
                new_df = pd.concat([new_df,out],ignore_index=True)
                indices_to_drop.append(index)
        return pd.concat([df.drop(labels=indices_to_drop),new_df],ignore_index=True)
    new_df = split_commas(df,'Toimipaikka')

    def remove_dashes(row):
        row["Toimipaikka"].replace("-", " ")
                
    new_df = new_df.apply(remove_dashes)
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
    st.write(rejected)
    st.write(selection)

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
