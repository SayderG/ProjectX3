import folium
from geopy.geocoders import Nominatim
import os


def create_map(place):
    geolocator = Nominatim(user_agent="Maps")

    geo_loc = geolocator.geocode(place)
    location = [geo_loc.latitude, geo_loc.longitude]
    map = folium.Map(location=location, zoom_start=10)

    folium.TileLayer('openstreetmap').add_to(map)
    folium.TileLayer('Stamen Terrain').add_to(map)
    folium.TileLayer('Stamen Toner').add_to(map)
    folium.TileLayer('Stamen Water Color').add_to(map)
    folium.TileLayer('cartodbpositron').add_to(map)
    folium.TileLayer('cartodbdark_matter').add_to(map)
    folium.Marker(location, 'PROBKA').add_to(map)
    folium.LayerControl().add_to(map)
    path = os.getcwd()
    map_path = f'{path}\\Maps\\html_map\\map.html'
    map.save(map_path)
    with open(map_path, 'r') as file:
        read_file = file.read()
    return read_file
