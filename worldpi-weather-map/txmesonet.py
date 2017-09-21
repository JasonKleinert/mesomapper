from requests import get
import json
import folium
import os
import webbrowser

# get weather station data
txmeso_url = 'https://www.texmesonet.org/api/CurrentData'
url = 'http://api.mesowest.net/v2/stations/metadata?&state=tx&county=Travis&token=demotoken'
data = get(url).json()
txmeso_data = get(txmeso_url).json()
lons = []
lats = []
wsnames = []
lons = [station['longitude'] for station in txmeso_data]
lats = [station['latitude'] for station in txmeso_data]
wsnames = [station['name'] for station in txmeso_data]

# initialize the map
map_ws = folium.Map(location=[30.334694,-97.781949],zoom_start=10, tiles='Stamen Terrain')

# add the mesonet weather stations to the map
for station in data['STATION']:
    if station['STATUS'] == 'ACTIVE':
        tooltip = station['NAME']
        folium.Marker([float(station['LATITUDE']),
                       float(station['LONGITUDE'])],
                       popup=tooltip,
                       icon=folium.Icon(icon = 'cloud')).add_to(map_ws)

# add the texmesonet weather stations to the map
for n in range(len(lons)):
    folium.Marker([lats[n],
                   lons[n]],
                   popup=wsnames[n],
                   icon=folium.Icon(icon = 'cloud', color = 'pink')).add_to(map_ws)

# save the map as html and open in the browser
CWD = os.getcwd()
map_ws.save('mesomap.html')
webbrowser.open_new('file://' + CWD + '/' + 'mesomap.html')
