import xarray as xr, pandas as pd
from scipy.interpolate import interpn
from matplotlib import dates as mdates

# import GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT
sla = xr.open_dataset('./data/dataset-duacs-nrt-global-merged-allsat-phy-l4_1612878616230.nc')
ph = pd.read_csv('./data/UWS/df_carb.csv')
ph['date_time'] = pd.to_datetime(ph.date_time)
ph['datenum'] = mdates.date2num(ph.date_time)

# # import GLOBAL_ANALYSIS_FORECAST_PHY_001_024
# bgcdat = xr.open_dataset('./data/global-analysis-forecast-phy-001-024_1612963010439.nc')

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

ph['sla'] = interpn(
    (mdates.date2num(sla.time.data), sla.latitude.data, sla.longitude.data),
    sla.sla.data,
    (ph.datenum, ph.lat_dd, ph.lon_dd),
)
