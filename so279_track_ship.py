import pandas as pd
from cartopy import crs as ccrs, feature as cfeature
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

# import data
so279_df = pd.read_csv('./data/UWS/so279_df.csv')
station_coord = pd.read_excel('./data/stations_coordinates.xlsx')

# convert datetime data to matplotlib format
so279_df["date_num"] = mdates.date2num(so279_df.date_time)

# plot ship track
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
    data=so279_df,
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

plt.savefig("figs/track_ship.png")
plt.show()
