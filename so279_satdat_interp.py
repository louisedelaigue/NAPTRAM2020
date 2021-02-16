import xarray as xr, pandas as pd
from scipy.interpolate import interpn
from matplotlib import dates as mdates
from matplotlib import pyplot as plt

# import GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT
sla = xr.open_dataset('./data/dataset-duacs-nrt-global-merged-allsat-phy-l4_1612878616230.nc')


# import GLOBAL_ANALYSIS_FORECAST_PHY_001_024
bgcdat = xr.open_dataset('./data/global-analysis-forecast-phy-001-024_1612963010439.nc')

# import cruise data
so279_df = pd.read_csv('./data/so279_df.csv')

# put data into matplotlib time friendly format
so279_df['date_time'] = pd.to_datetime(so279_df.date_time)
so279_df['datenum'] = mdates.date2num(so279_df.date_time)


# phx = (
#     ph[["lat_dd", "lon_dd"]]
#     .rename(columns={"lat_dd": "latitude", "lon_dd": "longitude"})
#     .to_xarray()
# )

# phx = xr.Dataset(coords={
#     "latitude": ph.lat_dd.to_numpy(),
#     "longitude": ph.lon_dd.to_numpy(),
# })

# 2D interpolation along latitude and longitude
# sla.isel(time=0).sla.plot()
# sla.isel(time=0).sla.interp(latitude=[40, 41], longitude=[-20, -21, -20.5])

# 3D linear interpolation along latitude, longitude and time
so279_df['sla'] = interpn(
    (mdates.date2num(sla.time.data), sla.latitude.data, sla.longitude.data), # this needs to be same order as dimensions order in xarray
    sla.sla.data,
    (so279_df.datenum, so279_df.lat_dd, so279_df.lon_dd), # this needs to match above order
)

