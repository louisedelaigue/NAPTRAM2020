data_small = data[0:150]
data_small.reset_index(inplace=True, drop=True)
smb_small = smb[0:150]
smb_small.reset_index(inplace=True, drop=True)

# SMB TIME
# date
smb_small['date'] = pd.to_datetime(smb_small['time'], format='%m/%d/%Y %H:%M').dt.date
smb_small['month'] = smb_small['date'].apply(lambda x: x.month)
smb_small['day'] = smb_small['date'].apply(lambda x: x.day)

# time
smb_small['hms'] = pd.to_datetime(smb_small['time'], format='%m/%d/%Y %H:%M').dt.time
smb_small['hour'] = smb_small['hms'].apply(lambda x: x.hour)
smb_small['minute'] = smb_small['hms'].apply(lambda x: x.minute)

# create seconds column for smb time - TO EDIT WITH AN IF CONDITION (if less than 60 duplicates, then  fill with nan)
smb_small['second'] = smb_small.groupby('time').cumcount()+1

# PYRO TIME
# split time into hours, minutes and seconds for pyro data
# date
data_small['date'] = pd.to_datetime(data_small['date'], format='%d-%m-%Y').dt.date
data_small['month'] = data_small['date'].apply(lambda x: x.month)
data_small['day'] = data_small['date'].apply(lambda x: x.day)


# time
data_small['time'] = pd.to_datetime(data_small['time'], format='%H:%M:%S.%f').dt.time
data_small['hour'] = data_small['time'].apply(lambda x: x.hour)
data_small['minute'] = data_small['time'].apply(lambda x: x.minute)
data_small['second'] = data_small['time'].apply(lambda x: x.second)

