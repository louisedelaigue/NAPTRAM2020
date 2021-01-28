# pH = -log(H+)
# H+ = 10^pH

df["pH"] = np.float64(df.pH)

#%%
min_hplus = 10**(df.pH_insitu.min())
max_hplus = 10**(df.pH_insitu.max())
mean_hplus = 10**(df.pH_insitu.mean())

ans = 100 * ((min_hplus - max_hplus)/mean_hplus)

range_pH = df.pH_insitu.max() - df.pH_insitu.min()