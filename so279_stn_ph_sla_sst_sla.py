import pandas as pd
import xarray as xr
from matplotlib import pyplot as plt

# import pH and SMB data
df = pd.read_csv('./data/UWS/df_carb.csv')

# import satellite data for sea level anomaly
sladat = xr.open_dataset('./data/dataset-duacs-nrt-global-merged-allsat-phy-l4_1612878616230.nc')

# import satellite data for sst and sal
bgcdat = xr.open_dataset('./data/global-analysis-forecast-phy-001-024_1612963010439.nc')

#%% make plot
# create figure
fig, axs = plt.subplots(
    dpi=300, figsize=(6,6), nrows=2, ncols=2
    )

