import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter

# import spreadsheet
so279_df = pd.read_csv('./data/so279_df.csv',
                   skiprows=[1])

# plot in-situ pH
# color = pygame.Color("#1CFF82")
fig, ax1 = plt.subplots(dpi=300, figsize=(8, 5))
ax1.scatter(
    so279_df.datenum,
    so279_df.pH_insitu,
    s=2,
    color='#00B0F0',
    label='pH'
)

ax1.set_xlabel('Time')
ax1.set_ylabel('pH')
x_date = DateFormatter("%d-%m")
ax1.xaxis.set_major_formatter(x_date)
ax1.grid(alpha=0.3)

# plot in-situ temperature (SBE38)
ax2 = ax1.twinx()
ax2.scatter(so279_df.datenum,
            so279_df.SBE38_water_temp,
            s=2,
            color='#003DB9',
            label='Temperature (°C)'
)

ax2.set_ylabel('Temperature (°C)')

fig.legend(markerscale=3,
           bbox_to_anchor=(-0.17, 0.47, 0.5, 0.5)
)

plt.xlim(so279_df.datenum.min(), so279_df.datenum.max())

# draw lines to locate storm
L = so279_df['filename'] == '2020-12-21_112915_NAPTRAM20206'
xmin = so279_df['datenum'][L].min()
xmax = so279_df['datenum'][L].max()

ax1.axvline(x=xmin, linestyle='--', c='#de0c62')
ax1.axvline(x=xmax, linestyle='--', c='#de0c62')    
ax1.text(737782.5, 8.07, 'STORM', fontweight='bold')

# tight layout and save plot
plt.tight_layout()
plt.savefig('./figs/insitu_pH_temp.png', bbox_inches='tight', format = 'png')
plt.show()


