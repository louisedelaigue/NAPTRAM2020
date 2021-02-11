import xarray as xr

# import GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT
sladat = xr.open_dataset('./data/dataset-duacs-nrt-global-merged-allsat-phy-l4_1612878616230.nc')

# import GLOBAL_ANALYSIS_FORECAST_PHY_001_024
bgcdat = xr.open_dataset('./data/global-analysis-forecast-phy-001-024_1612963010439.nc')

#%% 2D interpolation along latitude and longitude

