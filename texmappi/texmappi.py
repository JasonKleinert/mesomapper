import json
import os
import webbrowser
import folium

from folium.plugins import MarkerCluster
from requests import get

# get weather station data
txmeso_url = 'https://www.texmesonet.org/api/CurrentData'
mesowest_url = 'http://api.mesowest.net/v2/stations/metadata?&state=tx&county=Travis&token=demotoken'
mesowest_data = get(mesowest_url).json()
txmeso_data = get(txmeso_url).json()

lons = []
lats = []
wsnames = []
airtemp = []

lons = [station['longitude'] for station in txmeso_data]
lats = [station['latitude'] for station in txmeso_data]
wsnames = [station['name'] for station in txmeso_data]
airtemp = [station['airTemp'] for station in txmeso_data]


# initialize the map
m = folium.Map(location=[30.334694,-97.781949],zoom_start=6, control_scale=True, tiles=None)

# add additional base maps
# folium.TileLayer('Stamen Terrain', name='Stamen Terrain').add_to(m)
# folium.TileLayer('Stamen Toner', name='Stamen Toner').add_to(m)
folium.TileLayer('Stamen Watercolor', name='Stamen Watercolor').add_to(m)
folium.TileLayer('https://{s}.tile.thunderforest.com/spinal-map/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='Spinal Map', attr='Thunderforest').add_to(m)
# folium.TileLayer('https://{s}.tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='Transport Dark', attr='Thunderforest').add_to(m)
folium.TileLayer('https://{s}.tile.thunderforest.com/pioneer/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='Pioneer', attr='Thunderforest').add_to(m)

# more basemaps
# folium.TileLayer('https://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='Outdoors', attr='Thunderforest').add_to(m)
# folium.TileLayer('https://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='Landscape', attr='Thunderforest').add_to(m)
# folium.TileLayer('https://{s}.tile.thunderforest.com/neighbourhood/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='neighbourhood', attr='Thunderforest').add_to(m)
# folium.TileLayer('https://{s}.tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='Transport', attr='Thunderforest').add_to(m)


counties_group =folium.FeatureGroup(name='Counties').add_to(m)
# add layers from geoserver pi
txdot_counties_detailed = get('http://10.10.11.66:8080/geoserver/tnris/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=tnris:txdot_2015_county_detailed_tx&maxFeatures=254&outputFormat=application%2Fjson').json()
for feature in txdot_counties_detailed['features']:
    county_name = feature['properties']['CNTY_NM']
    popup = folium.Popup(county_name + ' County')
    gj = folium.GeoJson(
            feature,
            style_function = lambda feature: {'color': '#545454', 'weight': 1.5,'dashArray': '5, 5'})
    gj.add_child(popup)
    gj.add_to(counties_group)

# state_parks = get('http://10.10.11.66:8080/geoserver/tnris/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=tnris:TPWD%20State%20Parks&maxFeatures=50&outputFormat=application%2Fjson').json()
# folium.GeoJson(state_parks,
#                name='State Parks').add_to(m)

# parks_group =folium.FeatureGroup(name='State Parks').add_to(m)
#
# state_parks = get('http://10.10.11.66:8080/geoserver/tnris/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=tnris:TPWD%20State%20Parks&maxFeatures=50&outputFormat=application%2Fjson').json()
# for feature in state_parks['features']:
#     park_name = feature['properties']['loname']
#     print(park_name)
#     popup = folium.Popup(park_name)
#     gj = folium.GeoJson(
#             feature)
#     # gj.add_child(popup)
#     gj.add_to(parks_group)

# gould_group =folium.FeatureGroup(name='Gould Eco Regions').add_to(m)
# # add layers from geoserver pi
# gould_ecoregions = get('http://10.10.11.66:8080/geoserver/tnris/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=tnris:Gould%20Eco-Regions&maxFeatures=50&outputFormat=application%2Fjson').json()
# for feature in gould_ecoregions['features']:
#     region_name = feature['properties']['name']
#     popup = folium.Popup(region_name)
#     gj = folium.GeoJson(
#             feature,
#             style_function = lambda feature: {'color': '#545454', 'weight': 1.5,'dashArray': '5, 5'})
#     gj.add_child(popup)
#     gj.add_to(gould_group)


# folium.GeoJson(
#     txdot_counties_detailed,
#     name='TX Counties',
#     style_function = lambda feature: {'fillColor': '#00ffffff','color': '#545454', 'weight': 1.5,'dashArray': '5, 5'},
#     highlight_function = lambda feature: {'fillColor': '#848484','color': 'green', 'weight': 3,'dashArray': '5, 5'}).add_child(folium.Popup('jason is the coolest')).add_to(m)

# get the mesowest stations for travis county
mesowest_url = 'http://api.mesowest.net/v2/stations/metadata?&state=tx&county=Travis&token=demotoken'
mesowest_data = get(mesowest_url).json()

marker_cluster = MarkerCluster(name='Travis County Mesowest Stations').add_to(m)

for station in mesowest_data['STATION']:
    if station['STATUS'] == 'ACTIVE':
        tooltip = station['NAME'] + ', Elevation: ' + station['ELEVATION'] + 'ft'
        folium.Marker([float(station['LATITUDE']),
                       float(station['LONGITUDE'])],
                       popup=tooltip,
                       icon=folium.Icon(icon = 'cloud')).add_to(marker_cluster)

off_leash_data = os.path.join(os.getcwd(), 'off-leash-areas.geojson')
f = open(off_leash_data).read()
data = json.loads(f)
for feature in data['features']:
    print(feature['geometry']['type'])
    print(feature['geometry']['coordinates'])


folium.LayerControl().add_to(m)


# save the map as html and open in the browser
CWD = os.getcwd()
m.save('texmappi.html')
webbrowser.open_new('file://' + CWD + '/' + 'texmappi.html')
