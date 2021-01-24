from scipy import stats
import numpy as np

# OVERALL DATA
data.pH = data.pH.astype(float)

all_stats = stats.describe(data.pH)
all_stdev = np.std(data.pH)
all_linear = stats.linregress(data.sec, data.pH)


# STORMY PART OF DATA
storm = data_dict['2020-12-21_112915_NAPTRAM20206']
storm_stats = stats.describe(storm.pH)
storm_stdev = np.std(storm.pH)
storm_linear = stats.linregress(storm.sec, storm.pH)