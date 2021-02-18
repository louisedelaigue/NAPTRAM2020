# MLR not working
# # perform linear regression on each variable pair with pH (eg. pH vs chl)
# for day in days_list:
#     L = so279_df['date_time'].dt.day == day
#     so279_stats.loc[so279_stats.day==day,
#         "r2_sss"] = stats.linregress(so279_df[L]['SBE45_sal'],
#                                            so279_df[L]['pH_insitu'])[2]
#     so279_stats.loc[so279_stats.day==day,
#     "r2_sst"] = stats.linregress(so279_df[L]['SBE45_sal'],
#                                        so279_df[L]['pH_insitu'])[2]
#     so279_stats.loc[so279_stats.day==day,
#     "r2_ta"] = stats.linregress(so279_df[L]['ta_est'],
#                                        so279_df[L]['pH_insitu'])[2]                                          
#     so279_stats.loc[so279_stats.day==day,
#             "r2_chl"] = stats.linregress(so279_df[L]['chl'],
#                                                so279_df[L]['pH_insitu'])[2]

# # find covariance for each variable pair with pH (eg. pH vs chl)
# for day in days_list:
#     L = so279_df['date_time'].dt.day == day
#     so279_stats.loc[so279_stats.day==day,
#         "cov_sss"] = cov(so279_df[L]['SBE45_sal'],
#                                            so279_df[L]['pH_insitu'])
#     so279_stats.loc[so279_stats.day==day,
#     "r2_sst"] = stats.linregress(so279_df[L]['SBE45_sal'],
#                                        so279_df[L]['pH_insitu'])
#     so279_stats.loc[so279_stats.day==day,
#     "r2_ta"] = stats.linregress(so279_df[L]['ta_est'],
#                                        so279_df[L]['pH_insitu'])                                
#     so279_stats.loc[so279_stats.day==day,
#             "r2_chl"] = stats.linregress(so279_df[L]['chl'],
#                                                so279_df[L]['pH_insitu'])
                            

# WORKING BUT NOT DETAILED ENOUGH
# # perform log transformation of data
# so279_df['log_ph'] = np.log2(so279_df['pH_insitu'])
# so279_df['log_sss'] = np.log2(so279_df['SBE45_sal'])
# so279_df['log_sst'] = np.log2(so279_df['SBE38_water_temp'])
# so279_df['log_ta'] = np.log2(so279_df['ta_est'])

# # perform standardization so mean = 0 std deviation = 1
# so279_df['std_ph'] = preprocessing.scale(so279_df['log_ph'])
# so279_df['std_sss'] = preprocessing.scale(so279_df['log_sss'])
# so279_df['std_sst'] = preprocessing.scale(so279_df['log_sst'])
# so279_df['std_ta'] = preprocessing.scale(so279_df['log_ta'])

# standardize the data to remove bias of different scales on which variables were measured
# normalize variables individually so that μ = 0 and σ = 1 before doing MLR
# test with ph and sst data
X = np.array([so279_df['pH_insitu'], so279_df['SBE45_sal']])

# the scaler object (model)
scaler = StandardScaler()

# fit and transform the data
scaled_data = scaler.fit_transform(X) 

# check on mean and std
mean = scaled_data.mean(axis = 0)
std = scaled_data.std(axis = 0)