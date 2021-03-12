import pandas as pd
from cartopy import crs as ccrs, feature as cfeature
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

# import data
so279_df = pd.read_csv('./data/so279_df.csv')
station_coord = pd.read_excel('./data/stations_coordinates.xlsx')

# convert datetime data to matplotlib format
so279_df["date_num"] = mdates.date2num(so279_df.date_time)

# plot ship track
fig = plt.figure(dpi=300, figsize=(5, 5))
ax = fig.add_subplot(projection=ccrs.PlateCarree(central_longitude=-30))

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
ax.gridlines(alpha=0.3, draw_labels=True)

# scatter data
st = ax.scatter(
    "lon",
    "lat",
    data=so279_df,
    # c="date_num",  # we can do this, as it's now a column in the dataframe // MPH
    # cmap='cmo.ice_r',
    c='xkcd:blue violet',
    marker='.',
    s=1,
    zorder=1,
    transform=ccrs.PlateCarree()
)

# scatter station coordinates
ax.scatter(
    "lon",
    "lat",
    data=station_coord,
    c='xkcd:cyan',
    s=30,
    zorder=10,
    transform=ccrs.PlateCarree()
)

# make it pretty
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

plt.savefig("figs/track_ship.png")
plt.show()
