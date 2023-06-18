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


def get_place_by_points(latitude, longitude, language='ru'):
    geolocator = Nominatim(user_agent="test")
    coordinates = f"{latitude}, {longitude}"
    return geolocator.reverse(coordinates, language=language, addressdetails=True).raw


def get_place_by_name(place):
    geolocator = Nominatim(user_agent="test")
    geo_loc = geolocator.geocode(place)
    return [geo_loc.latitude, geo_loc.longitude]


def graph():
    import osmnx as ox
    import networkx as nx

    ox.config(log_console=True, use_cache=True)

    # start_latlng = (45.094605, 39.00194)
    # end_latlng = (45.055292, 39.002459)
    start_latlng = (45.10826, 39.046196)
    end_latlng = (45.055267, 38.934072)
    place = "краснодар, улица московская"
    mode = 'walk'  # 'drive', 'bike', 'walk'
    optimizer = 'time'  # 'length','time'
    graph = ox.graph_from_address(place, network_type=mode)
    orig_node = ox.nearest_nodes(graph, X=start_latlng[0], Y=start_latlng[-1])
    dest_node = ox.nearest_nodes(graph, *end_latlng)
    shortest_route = nx.shortest_path(graph, orig_node, dest_node, weight=optimizer)
    print(shortest_route)


if __name__ == '__main__':
    print(graph())
