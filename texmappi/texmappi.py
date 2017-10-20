from requests import get
import json
import folium
import os
import webbrowser

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
m = folium.Map(location=[30.334694,-97.781949],zoom_start=6, control_scale=True)

# add additional base maps
folium.TileLayer('Stamen Terrain', name='Stamen Terrain').add_to(m)
folium.TileLayer('Stamen Toner', name='Stamen Toner').add_to(m)
folium.TileLayer('https://{s}.tile.thunderforest.com/spinal-map/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='Spinal Map', attr='Thunderforest').add_to(m)
folium.TileLayer('https://{s}.tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='Transport Dark', attr='Thunderforest').add_to(m)
folium.TileLayer('https://{s}.tile.thunderforest.com/pioneer/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='Pioneer', attr='Thunderforest').add_to(m)

# more basemaps
# folium.TileLayer('Stamen Watercolor').add_to(m)
# folium.TileLayer('https://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='Outdoors', attr='Thunderforest').add_to(m)
# folium.TileLayer('https://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='Landscape', attr='Thunderforest').add_to(m)
# folium.TileLayer('https://{s}.tile.thunderforest.com/neighbourhood/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='neighbourhood', attr='Thunderforest').add_to(m)
# folium.TileLayer('https://{s}.tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey=47c1ac00fc2d4af9b0b9a6a4a5545341', name='Transport', attr='Thunderforest').add_to(m)


# add layers from geoserver pi
txdot_counties_detailed = get('http://10.10.11.66:8080/geoserver/tnris/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=tnris:txdot_2015_county_detailed_tx&maxFeatures=254&outputFormat=application%2Fjson').json()
for name, row in txdot_counties_detailed.items():
    print(name, row)
folium.GeoJson(
    txdot_counties_detailed,
    name='TX Counties',
    style_function = lambda feature: {'fillColor': '#848484','color': '#545454', 'weight': 1.5,'dashArray': '5, 5'},
    highlight_function = lambda feature: {'fillColor': '#CDCDCD','color': 'green', 'weight': 3,'dashArray': '5, 5'}).add_child(folium.Popup('jason is the coolest')).add_to(m)

tx_bathymetry = get('http://10.10.11.66:8080/geoserver/tnris/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=tnris:tx_coast_bathymetry&maxFeatures=200&outputFormat=application%2Fjson').json()
folium.GeoJson(
    tx_bathymetry,
    name='TX Coastal Bathymetry'
).add_to(m)

# tx_counties_wms = 'http://10.10.11.66:8080/geoserver/tnris/wms'
# folium.WmsTileLayer(url=tx_counties_wms, name='Counties WMS', layers='tnris:txdot_2015_county_detailed_tx', attr="TxDOT", fmt='image/png').add_to(m)

folium.LayerControl().add_to(m)

# add the mesonet weather stations to the map
# for station in mesowest_data['STATION']:
#     if station['STATUS'] == 'ACTIVE':
#         tooltip = station['NAME']
#         folium.Marker([float(station['LATITUDE']),
#                        float(station['LONGITUDE'])],
#                        popup=tooltip,
#                        icon=folium.Icon(icon = 'cloud')).add_to(m)

# add the texmesonet weather stations to the map
# for n in range(len(lons)):
#     folium.Marker([lats[n],
#                    lons[n]],
#                    popup=wsnames[n] + '\n' + str(airtemp[n]),
#                    icon=folium.Icon(icon = 'cloud', color = 'pink')).add_to(m)

# save the map as html and open in the browser
CWD = os.getcwd()
m.save('texmappi.html')
webbrowser.open_new('file://' + CWD + '/' + 'texmappi.html')
