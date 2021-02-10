import xarray as xr
import pandas as pd
import os, imageio
from matplotlib import pyplot as plt
from cartopy import crs as ccrs, feature as cfeature
import cmocean

# import GLOBAL_ANALYSIS_FORECAST_PHY_001_024
satdat = xr.open_dataset('./data/global-analysis-forecast-phy-001-024_1612963010439.nc')

# import station coordinates
station_coord = pd.read_excel('./data/stations_coordinates.xlsx')

#%% create gif of entire study area throughout the month of December 2020

# counter for loop
ii = 0

# looping through satellite data and create a map for each day of data (01/12/2020 to 06/01/2021)
for ii in range(0, 37):
    
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
    
    # add axis labels and title
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # implement boundaries of colorbar and its ticks
    vmin, vmax = 30, 38
        
    # add sea level anomaly data to map
    cmap = cmocean.cm.haline_r
    satdat.so.isel(time=[ii]).plot(transform=ccrs.PlateCarree(),
                                    vmin=vmin,
                                    vmax=vmax,
                                    cmap=cmap,
                                    ax=ax)
    
    # add stations to map
    ax.scatter(
        "lon_dec",
        "lat_dec",
        data=station_coord,
        c='xkcd:black',
        marker='^',
        s=10,
        zorder=10,
        transform=ccrs.PlateCarree()
    )

    # tighten layout for homogeneous fig size    
    plt.tight_layout()

    # save figure in output path
    plt.savefig('./figs/gif_sal/{:02n}.png'.format(ii))
    plt.show()
    
# create gif
png_dir = './figs/gif_sal'
list_dir = os.listdir(png_dir)
list_dir.sort()
images=[]

for pic in (list_dir):
    if pic.endswith('.png'):
        file_path = os.path.join(png_dir, pic)
        images.append(imageio.imread(file_path))
imageio.mimsave('./figs/gif_sal/gif_sal.gif', images, duration=0.5)

