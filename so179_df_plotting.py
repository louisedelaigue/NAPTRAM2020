import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# import spreadsheet
db = pd.read_table('./data/UWS/df_processed.txt',
                   skiprows=[1])

#%% plot pt-100 temp vs. SBE38
fig, ax = plt.subplots(
    dpi=300, figsize=(8, 4), nrows=1
) 
sns.set_style("darkgrid")
sns.set_context("paper", font_scale=2)
sns.set(font="Verdana", font_scale=1)

ax.scatter(db.index, db.temp, label='optode_temp', c='xkcd:blue', s=3)
ax.scatter(db.index, db.SBE38_water_temp, label='smb_temp', c='xkcd:aquamarine', s=3)
ax.set_xticklabels([])
ax.set_xlabel('Time')
ax.set_ylabel('Temperature (°C)')
ax.legend()

plt.savefig('./figs/compare_temps.png', bbox_inches='tight', format = 'png')
plt.show()