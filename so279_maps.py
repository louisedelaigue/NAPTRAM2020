import pandas as pd
import numpy as np
import re
from cartopy import crs as ccrs, feature as cfeature
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import cmocean

# import data
df = pd.read_csv('./data/UWS/df.csv')
station_coord = pd.read_excel('./data/stations_coordinates.xlsx')

# format lat and lon columns (remove space)
df['lat'] = df['lat'].apply(lambda x: ''.join(filter(None, x.split(' '))))
df['lon'] = df['lon'].apply(lambda x: ''.join(filter(None, x.split(' '))))


def dms_to_dd(lat_or_lon):
    """Convert coordinates from degrees to decimals."""
    deg, minutes, seconds, direction =  re.split('[°\.\'\"]', lat_or_lon)
    ans = (
        (float(deg) + float(minutes)/60) + float(seconds)/(60*60)
    ) * (-1 if direction in ['W', 'S'] else 1)
    return pd.Series({'decimals': ans})
# ^ Use function docstrings to document what they do, rather than comments above them.
#   Of course, still use comments within a function to explain what's going on, where
#   necessary. // MPH

# # create columns to hold converted coordinates in decimals
# df['lat_dd'] = np.nan
# df['lon_dd'] = np.nan
# ^ You only need to create empty columns first if you're going to fill in the values
#   one at a time, row-by-row.  That is not the case here --- df.apply() creates the
#   entire new column in one go.  So this pre-allocation doesn't do anything. // MPH

# convert lat/lon to decimals and assign back to df ######## I THINK THIS COULD BE BETTER
df['lat_dd'] = df.lat.apply(dms_to_dd)
df['lon_dd'] = df.lon.apply(dms_to_dd)
# ^ No need to create intermediate lat_dd and lon_dd variables here // MPH
#
# convert datetime data to matplotlib format
# mpl = [mdates.date2num(datetime.strptime(i, '%d-%m-%Y %H:%M:%S')) for i in df.date_time]
df["date_time"] = pd.to_datetime(df.date_time, format='%d-%m-%Y %H:%M:%S')
df["date_num"] = mdates.date2num(df.date_time)
# ^ Use datetimes! // MPH
#
# The lat/lon and datetime conversions should be in your main processing script where df
# is created, not here in a figure script. // MPH

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

# scatter data
st = ax.scatter(
    "lon_dd",
    "lat_dd",
    data=df,
    c="date_num",  # we can do this, as it's now a column in the dataframe // MPH
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
