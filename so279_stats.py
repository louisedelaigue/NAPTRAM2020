import pandas as pd, numpy as np
from matplotlib import pyplot as plt
import seaborn as sb
from matplotlib import style
from scipy import stats
from sklearn.preprocessing import StandardScaler

# import cruise data
so279_df = pd.read_csv('./data/so279_df.csv')

# remove rows with nan values (caused by SMB pump malfunctioning)
L = ~np.isnan(so279_df['pH_insitu'])
so279_df = so279_df[L]

# create list of days
so279_df['date_time'] = pd.to_datetime(so279_df.date_time)
days_list = so279_df['date_time'].dt.day.unique()

# create table to hold results per day
so279_stats = pd.DataFrame({'day':days_list})
so279_stats['n'] = np.nan
so279_stats['sss_mean'] = np.nan
so279_stats['sss_std'] = np.nan
so279_stats['sst_mean'] = np.nan
so279_stats['sst_std'] = np.nan
so279_stats['ta_mean'] = np.nan
so279_stats['ta_std'] = np.nan
so279_stats['ph_insitu_mean'] = np.nan
so279_stats['ph_insitu_std'] = np.nan
so279_stats['chl_mean'] = np.nan
so279_stats['chl_std'] = np.nan
so279_stats['r2_sss'] = np.nan
so279_stats['r2_sst'] = np.nan
so279_stats['r2_ta'] = np.nan
so279_stats['slope_sss'] = np.nan
so279_stats['slope_sst'] = np.nan
so279_stats['slope_ta'] = np.nan

# statistical summary
# stats_summary = so279_df.describe()

# statistical visualization summary 
# style.use('seaborn-whitegrid')
# plt.rcParams['figure.figsize'] = (20,10)
# sb.pairplot(so279_df)
# plt.tight_layout()
# plt.savefig('figs/stats_pairplot.png')

# compute mean and std stats
for day in days_list:
    L = so279_df['date_time'].dt.day == day
    so279_stats.loc[so279_stats.day==day, 'n'] = so279_df[L].SBE45_sal.count()
    so279_stats.loc[so279_stats.day==day, 'sss_mean'] = so279_df[L].SBE45_sal.mean()
    so279_stats.loc[so279_stats.day==day, 'sss_std'] = so279_df[L].SBE45_sal.std()
    so279_stats.loc[so279_stats.day==day, 'sst_mean'] = so279_df[L].SBE38_water_temp.mean()
    so279_stats.loc[so279_stats.day==day, 'sst_std'] = so279_df[L].SBE38_water_temp.std()
    so279_stats.loc[so279_stats.day==day, 'ta_mean'] = so279_df[L].ta_est.mean()
    so279_stats.loc[so279_stats.day==day, 'ta_std'] = so279_df[L].ta_est.std()
    so279_stats.loc[so279_stats.day==day, 'ph_insitu_mean'] = so279_df[L].pH_insitu.mean()
    so279_stats.loc[so279_stats.day==day, 'ph_insitu_std'] = so279_df[L].pH_insitu.std()
    so279_stats.loc[so279_stats.day==day, 'chl_mean'] = so279_df[L].chl.mean()
    so279_stats.loc[so279_stats.day==day, 'chl_std'] = so279_df[L].chl.std()
    so279_stats.loc[so279_stats.day==day, "r2_sss"] = stats.linregress(so279_df[L]['SBE45_sal'], so279_df[L]['pH_insitu'])[2]
    so279_stats.loc[so279_stats.day==day, "r2_sst"] = stats.linregress(so279_df[L]['SBE38_water_temp'], so279_df[L]['pH_insitu'])[2]
    so279_stats.loc[so279_stats.day==day, "r2_ta"] = stats.linregress(so279_df[L]['ta_est'], so279_df[L]['pH_insitu'])[2]
    so279_stats.loc[so279_stats.day==day, "slope_sss"] = stats.linregress(so279_df[L]['SBE45_sal'], so279_df[L]['pH_insitu'])[0]
    so279_stats.loc[so279_stats.day==day, "slope_sst"] = stats.linregress(so279_df[L]['SBE38_water_temp'], so279_df[L]['pH_insitu'])[0]
    so279_stats.loc[so279_stats.day==day, "slope_ta"] = stats.linregress(so279_df[L]['ta_est'], so279_df[L]['pH_insitu'])[0]
    print(day)

# compute pH uncertainty (weather/climate goal from ICOS)
pH_uncertainty = round(so279_stats.ph_insitu_std.median(),3)
ta_est_uncertainty = round(so279_stats.ta_std.median())


