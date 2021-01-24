import matplotlib.pyplot as plt

# keep data above 6.5
L = (data.pH == '<6.5')
data = data[~L]
data.pH = data.pH.astype(float)

# plot
plt.scatter(data.index, data.pH)
plt.show()