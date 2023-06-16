import folium
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Maps")

place = 'Краснодар, ул будённого'
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

map.save("map1.html")
