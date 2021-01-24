from scipy import stats
data['pH'] = data.pH.astype(float)
stats.describe(data.pH)