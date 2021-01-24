from scipy import stats
data['pH'] = data.pH.astype(int)

for file in file_list:
    stats.describe(data[file].pH)
