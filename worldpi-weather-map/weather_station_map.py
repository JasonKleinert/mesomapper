from requests import get
import json
import folium
import os
import webbrowser

# get all world weather station data from the oracle
url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallstations'
stations = get(url).json()
lons = [station['weather_stn_long'] for station in stations['items']]
lats = [station['weather_stn_lat'] for station in stations['items']]
wsnames = [station['weather_stn_name'] for station in stations['items']]

# initialize the map
map_ws = folium.Map(location=[39.833333,-98.583333],zoom_start=5)

# add the weather stations to the map
for n in range(len(lons)):
    folium.Marker([lats[n],
                   lons[n]],
                   icon = folium.Icon(icon = 'cloud', color = 'green')).add_to(map_ws)

# save the map as html and open in the browser
CWD = os.getcwd()
map_ws.save('wsmap1.html')
webbrowser.open_new('file://' + CWD + '/' + 'wsmap1.html')
