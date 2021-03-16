import pandas as pd, numpy as np
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from scipy import interpolate

# import spreadsheet
so279_df = pd.read_csv('./data/pH/so279_df.csv',
                   skiprows=[1])

# only keep first file
L = so279_df['filename'] == '2020-12-08_204002_SO279_STN1_test'
file = so279_df[L]

# plot in-situ pH
fig, ax1 = plt.subplots(dpi=300, figsize=(8, 5))
ax1.scatter(
    file.datenum,
    file.pH_insitu,
    s=2,
    color='#00B0F0',
    label='pH'
)

ax1.set_xlabel('Time')
ax1.set_ylabel('pH')
x_date = DateFormatter("%d-%m %H:%M")
ax1.xaxis.set_major_formatter(x_date)
ax1.grid(alpha=0.3)

# plot in-situ temperature (SBE38)
ax2 = ax1.twinx()
ax2.scatter(file.datenum,
            file.SBE38_water_temp,
            s=2,
            color='#003DB9',
            label='Temperature (°C)'
)

ax2.set_ylabel('Temperature (°C)')

fig.legend(markerscale=3,
           bbox_to_anchor=(-0.17, 0.47, 0.5, 0.5)
)

plt.xlim(file.datenum.min(), file.datenum.max())


# tight layout and save plot
plt.tight_layout()
plt.savefig('./figs/file_insitu_pH_temp.png', bbox_inches='tight', format = 'png')
plt.show()

