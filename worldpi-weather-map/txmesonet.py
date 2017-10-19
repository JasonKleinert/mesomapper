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
m = folium.Map(location=[30.334694,-97.781949],zoom_start=10, tiles='Stamen Terrain')

# add additional base maps
folium.TileLayer('Stamen Toner').add_to(m)
folium.TileLayer('openstreetmap').add_to(m)

folium.LayerControl().add_to(m)

# add the mesonet weather stations to the map
for station in mesowest_data['STATION']:
    if station['STATUS'] == 'ACTIVE':
        tooltip = station['NAME']
        folium.Marker([float(station['LATITUDE']),
                       float(station['LONGITUDE'])],
                       popup=tooltip,
                       icon=folium.Icon(icon = 'cloud')).add_to(m)

# add the texmesonet weather stations to the map
for n in range(len(lons)):
    folium.Marker([lats[n],
                   lons[n]],
                   popup=wsnames[n] + '\n' + str(airtemp[n]),
                   icon=folium.Icon(icon = 'cloud', color = 'pink')).add_to(m)

# save the map as html and open in the browser
CWD = os.getcwd()
m.save('mesomap.html')
webbrowser.open_new('file://' + CWD + '/' + 'mesomap.html')
