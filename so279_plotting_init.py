import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# import spreadsheet
db = pd.read_csv('./data/UWS/df_carb.csv',
                   skiprows=[1])

#%% plot pt-100 temp vs. SBE38
fig, ax = plt.subplots(
    dpi=300, figsize=(8, 4), nrows=1
) 
sns.set_style("darkgrid")
sns.set_context("paper", font_scale=2)
sns.set(font="Verdana", font_scale=1)

ax.scatter(db.index, db.temp, label='optode_temp', c='xkcd:blue', s=2)
ax.scatter(db.index, db.SBE38_water_temp, label='smb_temp', c='xkcd:aquamarine', s=2)
ax.set_xticklabels([])
ax.set_xlabel('Time')
ax.set_ylabel('Temperature (°C)')
ax.legend()

plt.savefig('./figs/compare_temps.png', bbox_inches='tight', format = 'png')
plt.show()

#%% plot temp and sal
color='xkcd:aquamarine'
fig, ax1 = plt.subplots(dpi=300, figsize=(8, 4))
ax1.scatter(df.index, df.SBE38_water_temp, s=2, color=color)
ax1.set_xlabel('Time')
ax1.set_ylabel('Temperature (°C)', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticklabels([])

ax2 = ax1.twinx() # command for second y axis for temp

color='tab:blue'
ax2.scatter(df.index, df.SBE45_sal, s=2, color=color)
ax2.set_ylabel('Salinity', color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.tight_layout()
plt.savefig('./figs/temp_sal.png', bbox_inches='tight', format = 'png')
plt.show()

#%% plot pH_insitu w/ SBE38_water_temp
color='xkcd:aquamarine'
fig, ax1 = plt.subplots(dpi=300, figsize=(8, 4))
ax1.scatter(df.index, df.pH_insitu, s=2, color=color)
ax1.set_xlabel('Time')
ax1.set_ylabel('pH', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticklabels([])

ax2 = ax1.twinx() # command for second y axis for temp

color='tab:blue'
ax2.scatter(df.index, df.SBE38_water_temp, s=2, color=color)
ax2.set_ylabel('Temperature (°C)', color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.tight_layout()
plt.savefig('./figs/insitu_pH_temp.png', bbox_inches='tight', format = 'png')
plt.show()
