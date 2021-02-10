import pandas as pd
import xarray as xr
from matplotlib import pyplot as plt
from cartopy import crs as ccrs, feature as cfeature
import cmocean

# import pH and SMB data
df = pd.read_csv('./data/UWS/df_carb.csv')

#%% make plot
# create figure
fig = plt.figure(dpi=300)
ax = fig.add_subplot(projection=ccrs.Robinson(central_longitude=-30))

# add Earth features (land, lakes and minor islands)
ax.add_feature(
    cfeature.NaturalEarthFeature("physical", "land", "10m"), facecolor="k",
)
ax.add_feature(
    cfeature.NaturalEarthFeature("physical", "lakes", "10m"), facecolor="w",
)
ax.add_feature(
    cfeature.NaturalEarthFeature("physical", "minor_islands", "10m"), facecolor="k",
)

# set extent of map to study area
ax.set_extent((-40, -2, 25, 55))  # west, east, south, north limits

# add gridlines
ax.gridlines(alpha=0.3)

# prep colorbar
cmap = cmocean.cm.dense

# implement boundaries of colorbar and its ticks
vmin, vmax = df.pH_insitu.min(), df.pH_insitu.max()

# plot pH data
pH_plot = ax.scatter(
       'lon_dd',
       'lat_dd',
       c='pH_insitu',
       data=df,
       cmap=cmap,
       vmin=vmin,
       vmax=vmax,
       s=2,
       transform=ccrs.PlateCarree()
       )

# add colorbar to plot
cbar = plt.colorbar(pH_plot)
cbar.ax.set_ylabel('pH')

# save plot
plt.savefig("figs/pHinsitu_track.png")
plt.show()

