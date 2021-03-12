import pandas as pd, numpy as np
from matplotlib import pyplot as plt
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib import style
import statsmodels.api as sm
from termcolor import colored as cl

# import cruise data
so279_df = pd.read_csv('./data/so279_df.csv')

# remove rows with nan values (caused by SMB pump malfunctioning)
L = ~np.isnan(so279_df['pH_insitu'])
so279_df = so279_df[L]

# create list of days
so279_df['date_time'] = pd.to_datetime(so279_df.date_time)
days_list = so279_df['date_time'].dt.day.unique()

# create df with only variables for mlr
mlr_df = pd.DataFrame()
mlr_df['ph'] = so279_df['pH_insitu']
mlr_df['sss'] = so279_df['SBE45_sal']
mlr_df['sst'] = so279_df['SBE38_water_temp']
mlr_df['ta'] = so279_df['ta_est']
mlr_df['chl'] = so279_df['chl']

mlr_df['ph'] = mlr_df['ph'].astype(int)
mlr_df['sss'] = mlr_df['sss'].astype(int)
mlr_df['sst'] = mlr_df['sst'].astype(int)
mlr_df['ta'] = mlr_df['ta'].astype(int)
mlr_df['chl'] = mlr_df['chl'].astype(int)

# MLR model - stats model
# variables
X1_var = mlr_df[['sss','sst','ta','chl']] # independent variables
y_var = mlr_df['ph'] # dependent variable

# stats model
sm_X1_var = sm.add_constant(X1_var)

sm_X1_var = sm_X1_var.dropna()
mlr_df = mlr_df['ph'].values.reshape(-1,1)

mlr_model = sm.OLS(y_var, sm_X1_var)
mlr_reg = mlr_model.fit()

# model summary
print(cl(mlr_reg.summary(), attrs = ['bold']))

