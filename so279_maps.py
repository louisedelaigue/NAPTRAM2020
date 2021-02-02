import pandas as pd
import numpy as np
import re
from cartopy import crs as ccrs, feature as cfeature
from matplotlib import pyplot as plt

# import data
df = pd.read_csv('./data/UWS/df.csv')

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

# convert lat/lon to decimals and assign back to df
lat_dd = df.lat.apply(dms_to_dd)
df['lat_dd'] = lat_dd
lon_dd = df.lon.apply(dms_to_dd)
df['lon_dd'] = lon_dd

#%% plot fig
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

# scatter data
# ax.scatter("LONGITUDE", "LATITUDE", data=rws, transform=ccrs.PlateCarree(), zorder=10)
splot = ax.scatter(
    "lon_dd",
    "lat_dd",
    data=df,
    transform=ccrs.PlateCarree()
)

plt.show()