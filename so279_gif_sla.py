import xarray as xr
import pandas as pd
import os, imageio
from matplotlib import pyplot as plt
from cartopy import crs as ccrs, feature as cfeature

# import GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT
satdat = xr.open_dataset('./data/dataset-duacs-nrt-global-merged-allsat-phy-l4_1612878616230.nc')

# import station coordinates
station_coord = pd.read_excel('./data/stations_coordinates.xlsx')

#%% create gif of entire study area throughout the month of December 2020

# looping through satellite data and create a map for each day of data (01/12/2020 to 06/01/2021)
for ii in range(37):
    # create figure
    fig = plt.figure(dpi=300, figsize=[12, 12])
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
    ax.gridlines(alpha=0.3, draw_labels=True)  # to show lat/lon values // MPH
    
    # # add axis labels and title
    # ax.set_xlabel('Longitude') 
    # ax.set_ylabel('Latitude')  
    # ^ stick to the object-oriented approach, not the MATLAB-style state-based approach
    #   (plt.xlabel) --- although you may have noticed that these labels don't appear?
    #   This is because of the cartopy transformation.  If you want xlabel/ylabels then
    #   you need to add them manually with ax.text().  See the top answer here:
    #   https://stackoverflow.com/questions/35479508/cartopy-set-xlabel-set-ylabel-not-ticklabels
    #   But I really don't think writing 'longitude' and 'latitude' on the sides this
    #   map is at all necessary // MPH
    
    # implement boundaries of colorbar and its ticks
    vmin, vmax = -0.6, 0.6
        
    # add sea level anomaly data to map
    satdat.sla.isel(time=[ii]).plot(transform=ccrs.PlateCarree(),
                                    vmin=vmin,
                                    vmax=vmax,
                                    cmap='RdBu_r',
                                    ax=ax)
    
    # add stations to map
    ax.scatter(
        "lon",
        "lat",
        data=station_coord,
        c='k',  # a simpler way to get black // MPH
        marker='^',
        s=10,
        zorder=10,
        transform=ccrs.PlateCarree()
    )  # stations look essentially the same as islands // MPH


    # save figure in output path
    plt.savefig('./figs/gif_sla/{:02n}.png'.format(ii))
    plt.show()
    
# create gif
png_dir = './figs/gif_sla'
list_dir = os.listdir(png_dir)
list_dir.sort()
images=[]

for pic in (list_dir):
    if pic.endswith('.png'):
        file_path = os.path.join(png_dir, pic)
        images.append(imageio.imread(file_path))
imageio.mimsave('./figs/gif_sla/gif_sla.gif', images, duration=0.5)

