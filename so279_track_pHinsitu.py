import pandas as pd
from matplotlib import pyplot as plt
from cartopy import crs as ccrs, feature as cfeature
import cmocean

# import pH and SMB data
so279_df = pd.read_csv('./data/so279_df.csv')

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
vmin, vmax = so279_df.pH_insitu.min(), so279_df.pH_insitu.max()

# plot pH data
pH_plot = ax.scatter(
       'lon_dd',
       'lat_dd',
       c='pH_insitu',
       data=so279_df,
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
plt.savefig("figs/track_pHinsitu.png")
plt.show()

