import xarray as xr, pandas as pd, numpy as np
from scipy.interpolate import interpn
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from cartopy import crs as ccrs, feature as cfeature
import matplotlib.gridspec as gridspec

# import GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT
sladat = xr.open_dataset('./data/dataset-duacs-nrt-global-merged-allsat-phy-l4_1612878616230.nc')

# import station coordinates
station_coord = pd.read_excel('./data/stations_coordinates.xlsx')

# import cruise data
so279_df = pd.read_csv('./data/so279_df.csv')

# put data into matplotlib time friendly format
so279_df['date_time'] = pd.to_datetime(so279_df.date_time)
so279_df['datenum'] = mdates.date2num(so279_df.date_time)

# 3D linear interpolation along latitude, longitude and time
so279_df['sla'] = interpn(
    (mdates.date2num(sladat.time.data), sladat.latitude.data, sladat.longitude.data), # this needs to be same order as dimensions order in xarray
    sladat.sla.data,
    (so279_df.datenum, so279_df.lat_dd, so279_df.lon_dd), # this needs to match above order
)

#%% make plot
# create figure
fig = plt.figure(figsize=(6, 11), dpi=300)
gs = gridspec.GridSpec(nrows=5, ncols=1)

# first plot with map
ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree(central_longitude=-30))

# add Earth features (land, lakes and minor islands)
ax1.add_feature(
    cfeature.NaturalEarthFeature("physical", "land", "10m"), facecolor="k",
)
ax1.add_feature(
    cfeature.NaturalEarthFeature("physical", "lakes", "10m"), facecolor="w",
)
ax1.add_feature(
    cfeature.NaturalEarthFeature("physical", "minor_islands", "10m"), facecolor="k",
)

# set extent of map to study area
ax1.set_extent((-13, -8, 46, 48))  # west, east, south, north limits

# add gridlines
ax1.gridlines(alpha=0.3)

# implement boundaries of colorbar and its ticks
vmin, vmax = -0.6, 0.6
    
# add sea level anomaly data to map
sladat.sla.isel(time=[8]).plot(transform=ccrs.PlateCarree(),
                                vmin=vmin,
                                vmax=vmax,
                                cmap='RdBu_r',
                                ax=ax1)

# loc = mdates.AutoDateLocator()
# scbar = plt.colorbar(st, ticks=loc,
#                   format=mdates.AutoDateFormatter(loc))
# scbar.ax.yaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))

# add stations to map
ax1.scatter(
    "lon",
    "lat",
    data=station_coord,
    c='xkcd:true blue',
    edgecolors='xkcd:true blue',
    marker='x',
    s=30,
    zorder=10,
    label='Station 1',
    transform=ccrs.PlateCarree()
)  


# plot track of continuous pH for 08/12/20 and 09/12/20
L = np.logical_or(so279_df['date_time'].dt.day == 8, so279_df['date_time'].dt.day == 9)

# ax1.scatter(
#     'lon_dd',
#     'lat_dd',
#     data=ph[L],
#     c='xkcd:bright green',
#     s=0.1,
#     transform=ccrs.PlateCarree()
#     )

st = ax1.scatter(
    "lon_dd",
    "lat_dd",
    data=so279_df[L],
    c="datenum",
    cmap='cmo.ice_r',
    s=0.5,
    zorder=1,
    transform=ccrs.PlateCarree()
)

loc = mdates.AutoDateLocator()
scbar = plt.colorbar(st, ticks=loc,
                  format=mdates.AutoDateFormatter(loc))
scbar.ax.yaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))

# plot pH
ax2 = fig.add_subplot(gs[1, 0])
ax2.scatter(
    'date_time',
    'pH_insitu',
    data=so279_df[L],
    s=2, 
    c='xkcd:cyan'
)

ax2.set_ylabel('pH')
ax2.grid(alpha=0.3)
ax2.set_xlim('2020-12-08 18:00:00', '2020-12-10 00:00:00')
ax2.set_xticks([])

# plot salinity
ax3 = fig.add_subplot(gs[2, 0])
ax3.scatter(
    'date_time',
    'SBE45_sal',
    data=so279_df[L],
    s=2, 
    c='xkcd:true blue'
)
ax3.set_ylabel('Salinity')
ax3.grid(alpha=0.3)
ax3.set_xlim('2020-12-08 18:00:00', '2020-12-10 00:00:00')
ax3.set_xticks([])

# plot temperature
ax4 = fig.add_subplot(gs[3, 0])
ax4.scatter(
    'date_time',
    'SBE38_water_temp',
    data=so279_df[L],
    s=2, 
    c='xkcd:light red'
)
ax4.set_ylabel('Temperature (°C)')
ax4.grid(alpha=0.3)
ax4.set_xlim('2020-12-08 18:00:00', '2020-12-10 00:00:00')
ax4.set_xticks([])

# plot SLA
ax5 = fig.add_subplot(gs[4,0])
ax5.scatter(
    'date_time',
    'sla',
    data=so279_df[L],
    s=2,
    c='black')
ax5.set_ylabel('Sea level anomaly (m)')
ax5.grid(alpha=0.3)
ax5.set_xlim('2020-12-08 18:00:00', '2020-12-10 00:00:00')
loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
ax5.xaxis.set_major_locator(loc)

# save fig
plt.savefig("figs/transect.png")
plt.show()