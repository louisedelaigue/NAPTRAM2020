from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# read netCDF file
sat_dat_file = './data/dataset-duacs-nrt-global-merged-allsat-phy-l4_1612878616230.nc'
sat_dat = Dataset(sat_dat_file, mode='r')

# read data of variables inside netCDF file
sea_level_anomaly = sat_dat.variables['sla'][:]
lat = sat_dat.variables['latitude'][:]
lon = sat_dat.variables['longitude'][:]
time = sat_dat.variables['time'][:]

# close file
sat_dat.close

# create dict from sea level anomaly
dict_sla = {i:sea_level_anomaly for i, sea_level_anomaly in enumerate(sea_level_anomaly)}

