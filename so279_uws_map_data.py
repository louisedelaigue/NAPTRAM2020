from cartopy import crs as ccrs, feature as cfeature
from matplotlib import pyplot as plt
import pandas as pd
import cmocean

# import data using so279_uws_ph.py

# initialize figure
fig = plt.figure(dpi=300)
ax = fig.add_subplot(projection=ccrs.Robinson(central_longitude=0))

# add more features
ax.add_feature(
    cfeature.NaturalEarthFeature("physical", "land", "10m"), facecolor="k",
)
ax.add_feature(
    cfeature.NaturalEarthFeature("physical", "lakes", "10m"), facecolor="w",
)
ax.add_feature(
    cfeature.NaturalEarthFeature("physical", "minor_islands", "10m"), facecolor="k",
)

# scatter data
splot = ax.scatter('lon',
                   'lat',
                   data=df,
                   transform=ccrs.PlateCarree())


