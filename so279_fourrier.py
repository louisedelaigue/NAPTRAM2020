import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt

# import cruise data
so279_df = pd.read_csv('./data/so279_df.csv',
                   skiprows=[1])

prd = signal.periodogram(so279_df.pH_insitu)

plt.plot(prd)