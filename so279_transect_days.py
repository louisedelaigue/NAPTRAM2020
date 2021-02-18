import xarray as xr, pandas as pd, numpy as np
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from cartopy import crs as ccrs, feature as cfeature
import matplotlib.gridspec as gridspec
import cmocean 
import datetime

# import GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT
sladat = xr.open_dataset('./data/dataset-duacs-nrt-global-merged-allsat-phy-l4_1612878616230.nc')

# import station coordinates
station_coord = pd.read_excel('./data/stations_coordinates.xlsx')

# import cruise data
so279_df = pd.read_csv('./data/so279_df.csv')

# create list of days
so279_df['date_time'] = pd.to_datetime(so279_df.date_time)
days_list = so279_df['date_time'].dt.day.unique()

# make one figure per day showing the location of the data, the time and pH, salinity, temp and SLA
for day in days_list:
    L = so279_df['date_time'].dt.day == day
    
    # create figure
    fig = plt.figure(figsize=(6, 11), dpi=300)
    gs = gridspec.GridSpec(nrows=5, ncols=1)
    
    # put datetime back in datetime format
    so279_df['date_time'] = pd.to_datetime(so279_df.date_time)
     
    # FIRST PLOT ==============================================================
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
    ax1.set_extent((-40, -2, 25, 55))  # west, east, south, north limits
    
    # add gridlines
    ax1.gridlines(alpha=0.3)
    
    # implement boundaries of colorbar and its ticks
    vmin, vmax = -0.6, 0.6

    # add sea level anomaly data to map
    timenb = so279_df[L].date_time.dt.day.min() - 1
    sladat.sla.isel(time=[timenb]).plot(
        transform=ccrs.PlateCarree(),
        vmin=vmin,
        vmax=vmax,
        cmap='cmo.balance',
        ax=ax1
    )
    
    # add stations to map
    ax1.scatter(
        "lon",
        "lat",
        data=station_coord,
        c='xkcd:true blue',
        edgecolors='xkcd:true blue',
        marker='x',
        s=10,
        zorder=10,
        label='Station 1',
        transform=ccrs.PlateCarree()
    )
    
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
    
    # PLOT 2 ==================================================================
    hfmt = mdates.DateFormatter('%H:%M')
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
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval = 2))
    ax2.xaxis.set_major_formatter(hfmt)
    ax2.set_xlim([so279_df[L].date_time.min(), so279_df[L].date_time.max()])
    
    # PLOT 3 ==================================================================
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
    ax3.xaxis.set_major_locator(mdates.HourLocator(interval = 2))
    ax3.xaxis.set_major_formatter(hfmt)
    ax3.set_xlim([so279_df[L].date_time.min(), so279_df[L].date_time.max()])
    
    # PLOT 4 ==================================================================
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
    ax4.xaxis.set_major_locator(mdates.HourLocator(interval = 2))
    ax4.xaxis.set_major_formatter(hfmt)
    ax4.set_xlim([so279_df[L].date_time.min(), so279_df[L].date_time.max()])
    
    # PLOT 5 ==================================================================
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

    ax5.xaxis.set_major_locator(mdates.HourLocator(interval = 2))
    ax5.xaxis.set_major_formatter(hfmt)
    ax5.set_xlim([so279_df[L].date_time.min(), so279_df[L].date_time.max()])
    
    # save fig
    fig.autofmt_xdate()
    figname = 'figs/transect_days/{}.png'.format(day)
    plt.savefig(figname, dpi=300)
    plt.show