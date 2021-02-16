import xarray as xr, pandas as pd, numpy as np
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from cartopy import crs as ccrs, feature as cfeature
import matplotlib.gridspec as gridspec
import cmocean 

# import GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT
sladat = xr.open_dataset('./data/dataset-duacs-nrt-global-merged-allsat-phy-l4_1612878616230.nc')

# import station coordinates
station_coord = pd.read_excel('./data/stations_coordinates.xlsx')

# import cruise data
so279_df = pd.read_csv('./data/so279_df.csv')

#%% make plot
# create figure
fig = plt.figure(figsize=(6, 11), dpi=300)
gs = gridspec.GridSpec(nrows=5, ncols=1)

# put datetime back in datetime format
so279_df['date_time'] = pd.to_datetime(so279_df.date_time)

# pick date range: 08/12/20 and 09/12/20
L = np.logical_or(so279_df['date_time'].dt.day == 8, so279_df['date_time'].dt.day == 9)

# FIRST PLOT =================================================================
# Map of SLA with transect time
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
sladat.sla.isel(time=[8]).plot(
    transform=ccrs.PlateCarree(),
    vmin=vmin,
    vmax=vmax,
    cmap='RdBu_r',
    ax=ax1
)

# add station to map
S = station_coord.station == 1
ax1.scatter(
    "lon",
    "lat",
    data=station_coord[S],
    c='xkcd:true blue',
    edgecolors='xkcd:true blue',
    marker='x',
    s=30,
    zorder=10,
    label='Station 1',
    transform=ccrs.PlateCarree()
)
ax1.text(20.1, 47.3, 'Station 1', c='xkcd:true blue')

# scatter ship track with time as cmap
st = ax1.scatter(
    "lon",
    "lat",
    data=so279_df[L],
    c="date_time",
    cmap='cmo.ice_r',
    s=0.5,
    zorder=1,
    transform=ccrs.PlateCarree()
)

# add colorbarfor time
cb = plt.colorbar(
    st,
    label='Time',
    ticks=[so279_df.date_time.dt.day.min(), so279_df.date_time.dt.day.max()],
    ax=[ax1]
)

# PLOT 2 =====================================================================
# plot pH
ax2 = fig.add_subplot(gs[1, 0])
ax2.scatter(
    'date_time',
    'pH_insitu',
    data=so279_df[L],
    s=2, 
    c='black'
)

ax2.set_ylabel('pH')
ax2.grid(alpha=0.3)
ax2.set_xlim('2020-12-08 18:00:00', '2020-12-10 00:00:00')
ax2.set_xticks([])

# PLOT 3 =====================================================================
# plot salinity
ax3 = fig.add_subplot(gs[2, 0])
ax3.scatter(
    'date_time',
    'SBE45_sal',
    data=so279_df[L],
    s=2, 
    c='black'
)
ax3.set_ylabel('Salinity')
ax3.grid(alpha=0.3)
ax3.set_xlim('2020-12-08 18:00:00', '2020-12-10 00:00:00')
ax3.set_xticks([])

# PLOT 4 =====================================================================
# plot temperature
ax4 = fig.add_subplot(gs[3, 0])
ax4.scatter(
    'date_time',
    'SBE38_water_temp',
    data=so279_df[L],
    s=2, 
    c='black'
)
ax4.set_ylabel('Temperature (°C)')
ax4.grid(alpha=0.3)
ax4.set_xlim('2020-12-08 18:00:00', '2020-12-10 00:00:00')
ax4.set_xticks([])

# PLOT 5 =====================================================================
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
ax5.set_xticks(['2020-12-08 18:00:00', '2020-12-09 00:00:00', '2020-12-09 12:00:00', '2020-12-10 00:00:00'])
fig.autofmt_xdate()


# loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
# ax5.xaxis.set_major_locator(loc)

# save fig
plt.savefig("figs/transect_1.png")
plt.show()