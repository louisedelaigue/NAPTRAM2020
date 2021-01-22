import datetime
import random
import matplotlib.pyplot as plt

# keep data above 6.5
L = (data.pH == '<6.5')
data = data[~L]
data.pH = data.pH.astype(float)
data.sec = data.sec.astype(str)

data['testtime'] = data['date'] + data['time'] + data['sec']

# plot
plt.plot(data.testtime, data.pH)

# beautify the x-labels
# plt.gcf().autofmt_xdate()

plt.show()