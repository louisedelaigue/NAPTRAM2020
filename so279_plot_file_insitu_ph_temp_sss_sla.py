import xarray as xr, pandas as pd, numpy as np
from matplotlib import pyplot as plt
from cartopy import crs as ccrs, feature as cfeature
import matplotlib.gridspec as gridspec

# import GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT
sladat = xr.open_dataset('./data/satdat/dataset-duacs-nrt-global-merged-allsat-phy-l4_1612878616230.nc')
# sladat = sladat.isel(time=9)
# sladat = sladat.sla
# L = np.where((sladat.latitude <= 48) & (46 <= sladat.latitude) & (sladat.longitude <= -8) & (-12 <= sladat.longitude))
# sladat = sladat[L]

# sladat = sladat.isel(time=9).to_dataframe().reset_index()
# L = (46 <= sladat.latitude) & (sladat.latitude <= 48) & (-12 <= sladat.longitude) & (sladat.longitude <= -8)
# sladat = sladat[L]

# import station coordinates
station_coord = pd.read_excel('./data/stations_coordinates.xlsx')

# import cruise data
so279_df = pd.read_csv('./data/so279_df.csv',
                   skiprows=[1])
L = so279_df['filename'] == '2020-12-08_204002_SO279_STN1_test'
file = so279_df[L]
so279_df['date_time'] = pd.to_datetime(so279_df.date_time)
 
#%% create figure
fig = plt.figure(figsize=(8, 5), dpi=300)
gs = gridspec.GridSpec(nrows=2, ncols=2)


# FIRST PLOT ==============================================================
# Map of SLA with transect time
ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())

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
ax1.set_extent((-12, -8, 46, 48))  # west, east, south, north limits

# add gridlines
ax1.gridlines(alpha=0.3)

# implement boundaries of colorbar and its ticks
vmin, vmax = 0.04, 0.17

# add sea level anomaly data to map
sladat.sla.isel(time=8).plot(transform=ccrs.PlateCarree(),
                                vmin=vmin,
                                vmax=vmax,
                                cmap='bwr',
                                ax=ax1)

# scatter ship track with time as cmap
st = ax1.scatter(
    "lon",
    "lat",
    data=so279_df[L],
    c='k',
    s=0.3,
    zorder=1,
    transform=ccrs.PlateCarree()
)

# add station to map
S = station_coord.station == 1
ax1.scatter(
    "lon",
    "lat",
    data=station_coord[S],
    c='xkcd:cyan',
    marker='x',
    s=70,
    zorder=10,
    label='Station 1',
    transform=ccrs.PlateCarree()
)
ax1.text(-9.5, 47.3, 'Station 1', c='k')

# PLOT 2 ==================================================================
# minx = so279_df[L].date_time.dt.day.min()
# maxx = so279_df[L].date_time.dt.day.max()
# plot pH
ax2 = fig.add_subplot(gs[0, 1])
ax2.scatter(
    'date_time',
    'pH_insitu',
    data=so279_df[L],
    s=2, 
    c='black'
)

ax2.set_ylabel('pH')
ax2.grid(alpha=0.3)
# ax2.set_xlim(minx, maxx)
ax2.set_xticks([])

# PLOT 3 ==================================================================
# plot salinity
ax3 = fig.add_subplot(gs[1, 0])
ax3.scatter(
    'date_time',
    'SBE45_sal',
    data=so279_df[L],
    s=2, 
    c='black'
)
ax3.set_ylabel('Salinity')
ax3.grid(alpha=0.3)
# ax3.set_xlim('2020-12-08 18:00:00', '2020-12-10 00:00:00')
ax3.set_xticks([])

# PLOT 4 ==================================================================
# plot temperature
ax4 = fig.add_subplot(gs[1, 1])
ax4.scatter(
    'date_time',
    'SBE38_water_temp',
    data=so279_df[L],
    s=2, 
    c='black'
)
ax4.set_ylabel('Temperature (°C)')
ax4.grid(alpha=0.3)
# ax4.set_xlim('2020-12-08 18:00:00', '2020-12-10 00:00:00')
ax4.set_xticks([])

# save fig
plt.subplots_adjust(wspace=0.5, hspace=0.2)
plt.savefig('figs/test.png')
plt.show