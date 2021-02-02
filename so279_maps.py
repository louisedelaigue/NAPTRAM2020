import pandas as pd
import numpy as np
import re
from cartopy import crs as ccrs, feature as cfeature
from matplotlib import pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import cmocean

# import data
df = pd.read_csv('./data/UWS/df.csv')
station_coord = pd.read_excel('./data/stations_coordinates.xlsx')

# format lat and lon columns (remove space)
df['lat'] = df['lat'].apply(lambda x: ''.join(filter(None, x.split(' '))))
df['lon'] = df['lon'].apply(lambda x: ''.join(filter(None, x.split(' '))))

# create fx to convert coordinates from degrees to decimals
def dms_to_dd(lat_or_lon):
    deg, minutes, seconds, direction =  re.split('[°\.\'\"]', lat_or_lon)
    ans = ((float(deg) + float(minutes)/60) + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1)
    return pd.Series({
        'decimals':ans
        })

# create columns to hold converted coordinates in decimals
df['lat_dd'] = np.nan
df['lon_dd'] = np.nan

# convert lat/lon to decimals and assign back to df ######## I THINK THIS COULD BE BETTER
lat_dd = df.lat.apply(dms_to_dd)
df['lat_dd'] = lat_dd
lon_dd = df.lon.apply(dms_to_dd)
df['lon_dd'] = lon_dd

#%% plot ship track
fig = plt.figure(dpi=300)
ax = fig.add_subplot(projection=ccrs.Robinson(central_longitude=-30))

ax.add_feature(
    cfeature.NaturalEarthFeature("physical", "land", "10m"), facecolor="k",
)
ax.add_feature(
    cfeature.NaturalEarthFeature("physical", "lakes", "10m"), facecolor="w",
)
ax.add_feature(
    cfeature.NaturalEarthFeature("physical", "minor_islands", "10m"), facecolor="k",
)

ax.set_extent((-40, -2, 25, 55))  # west, east, south, north limits
ax.gridlines(alpha=0.3)

# convert datetime data to matplotlib format
mpl = [mdates.date2num(datetime.strptime(i, '%d-%m-%Y %H:%M:%S')) for i in df.date_time]

# scatter data
st = ax.scatter(
    "lon_dd",
    "lat_dd",
    data=df,
    c=mpl,
    cmap='cmo.ice_r',
    s=0.5,
    zorder=1,
    transform=ccrs.PlateCarree()
)

loc = mdates.AutoDateLocator()
scbar = plt.colorbar(st, ticks=loc,
                 format=mdates.AutoDateFormatter(loc))

scbar.ax.yaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))

ax.scatter(
    "lon_dec",
    "lat_dec",
    data=station_coord,
    c='r',
    s=5,
    zorder=10,
    transform=ccrs.PlateCarree()
)

plt.savefig("figs/ship_track.png")
plt.show()
