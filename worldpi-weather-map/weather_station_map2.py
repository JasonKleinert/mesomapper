import os
import webbrowser
import json
import folium
from requests import get

def colorgrad(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value - minimum) / (maximum - minimum)
    b = int(max(0, 255 * (1 - ratio)))
    g = int(max(0, 255 * (ratio - 1)))
    r = 255 - b - g
    hexcolor = '#%02x%02x%02x' % (r,g,b)
    return hexcolor

# get all world weather station data from the oracle
url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getalllastmeasurement'
station_data = get(url).json()
temps = []
tmin = 0.0
tmax = 100.0
lons = [data['weather_stn_long'] for data in station_data['items']]
lats = [data['weather_stn_lat'] for data in station_data['items']]
wsnames = [station['weather_stn_name'] for station in station_data['items']]
for data in station_data['items']:
    if 'ambient_temp' in data:
        t = data['ambient_temp']
        if t > 50 or t < -30:
            t = 20
        if t > tmax:
            tmax = t
        if t < tmin:
            tmin = t
        temps.append(str(t))

map_ws = folium.Map(location=[39.833333, -98.583333], tiles='Stamen Terrain', zoom_start=5)
for n in range(len(lons) - 1):
    #hcol = colorgrad(tmin, tmax, float(temps[n]))
    folium.Marker([lats[n], lons[n]],
                  icon=folium.Icon(color='green', icon='cloud'),
                  popup=wsnames[n] + ':' + temps[n]).add_to(map_ws)

CWD = os.getcwd()
map_ws.save('osm.html')
webbrowser.open_new('file://' + CWD + '/' + 'osm.html')

