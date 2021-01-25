# SMB DATE/TIME (metadata)
# date
smb['date'] = pd.to_datetime(smb['time'], format='%m/%d/%Y %H:%M').dt.date
smb['year'] = smb['date'].apply(lambda x: x.year)
smb['month'] = smb['date'].apply(lambda x: x.month)
smb['day'] = smb['date'].apply(lambda x: x.day)


# time
smb['hms'] = pd.to_datetime(smb['time'], format='%m/%d/%Y %H:%M').dt.time
smb['hour'] = smb['hms'].apply(lambda x: x.hour)
smb['hour'] = smb['hour'].map("{:02}".format)
smb['minute'] = smb['hms'].apply(lambda x: x.minute)

# create seconds ans ms column for smb time - TO EDIT WITH AN IF CONDITION (if less than 60 duplicates, then  fill with nan)
smb['second'] = smb.groupby('time').cumcount()+1
smb['second'] = smb['second'].map("{:02}".format)
smb['ms'] = '0'

# assemble above to match pyro date_time column
smb['time'] = smb['time'].astype(str)
smb['second'] = smb['second'].astype(str)
smb['date_time'] = smb['time']+':'+smb['second']+'.'+smb['ms']




# PYRO DATE/TIME (pH)
# split time into hours, minutes and seconds for pyro data
# date
data['date'] = pd.to_datetime(data['date'], format='%d-%m-%Y').dt.date
data['month'] = data['date'].apply(lambda x: x.month)
data['day'] = data['date'].apply(lambda x: x.day)

# time
data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S.%f').dt.time
data['hour'] = data['time'].apply(lambda x: x.hour)
data['minute'] = data['time'].apply(lambda x: x.minute)
data['second'] = data['time'].apply(lambda x: x.second)

_____________________

# data_dict['2020-12-08_204002_SO279_STN1_test']['date_time'] = datetime.datetime.strptime(data_dict['2020-12-08_204002_SO279_STN1_test']['date_time'], '%Y-%m-%d %H:%M:%S.%f')
# data_dict['2020-12-08_204002_SO279_STN1_test']['date_time'] = data_dict['2020-12-08_204002_SO279_STN1_test']['date_time'].strftime('%d-%m-%Y %H:%M:%S.%f')

# put back in right format
def date_convert(date_to_convert):
     return datetime.datetime.strptime(date_to_convert, '%Y-%m-%d %H:%M:%S.%f').strftime('%d-%m-%Y %H:%M:%S.%f')
data_dict['2020-12-08_204002_SO279_STN1_test']['date_time'] = data_dict['2020-12-08_204002_SO279_STN1_test']['date_time'].astype(str)
data_dict['2020-12-08_204002_SO279_STN1_test']['date_time'] = data_dict['2020-12-08_204002_SO279_STN1_test']['date_time'].apply(date_convert)

# redistribute substracted time to date and time columns respectively
# data_dict['2020-12-08_204002_SO279_STN1_test'].date_time = pd.to_datetime(data_dict['2020-12-08_204002_SO279_STN1_test'].date_time, format='%d-%m-%Y %H:%M:%S.%f')
# data_dict['2020-12-08_204002_SO279_STN1_test']['date'] = [d.date() for d in data_dict['2020-12-08_204002_SO279_STN1_test']['date_time']]
# data_dict['2020-12-08_204002_SO279_STN1_test']['time'] = [d.time() for d in data_dict['2020-12-08_204002_SO279_STN1_test']['date_time']]

# change date format to match rest of df
# def date_convert(date_to_convert):
#      return datetime.datetime.strptime(date_to_convert, '%Y-%m-%d').strftime('%d-%m-%Y')
# data_dict['2020-12-08_204002_SO279_STN1_test']['date'] = data_dict['2020-12-08_204002_SO279_STN1_test']['date'].astype(str)
# data_dict['2020-12-08_204002_SO279_STN1_test']['date'] = data_dict['2020-12-08_204002_SO279_STN1_test']['date'].apply(date_convert)

_________________________
# SMB DATE/TIME (metadata)
# only keep right time range to reduce file size
# L = 2020/12/08 00:00:01

# # date
# smb['date'] = pd.to_datetime(smb['time'], format='%Y/%m/%d %H:%M:%S').dt.date
# smb['year'] = smb['date'].apply(lambda x: x.year)
# smb['month'] = smb['date'].apply(lambda x: x.month)
# smb['day'] = smb['date'].apply(lambda x: x.day)

# # time
# smb['hms'] = pd.to_datetime(smb['time'], format='%m/%d/%Y %H:%M').dt.time
# smb['hour'] = smb['hms'].apply(lambda x: x.hour)
# smb['minute'] = smb['hms'].apply(lambda x: x.minute)
# smb['second'] = smb['hms'].apply(lambda x: x.second)

# create seconds column for smb time
# TO EDIT WITH AN IF CONDITION (if less than 60 duplicates, then  fill with nan)
# smb['second'] = smb.groupby('time').cumcount()+1


# ensure all have right format and convert to string for datetime
# smb['year'] = smb['year'].astype(str)
# smb['month'] = smb['month'].map("{:02}".format).astype(str)
# smb['day'] = smb['day'].map("{:02}".format).astype(str)
# smb['hour'] = smb['hour'].map("{:02}".format).astype(str)
# smb['minute'] = smb['minute'].astype(str)
# smb['second'] = smb['second'].map("{:02}".format).astype(str)

# combine all
smb['date_time'] = smb['day']+'-'+smb['month']+'-'+smb['year']+' '+smb['hour']+':'+smb['minute']+':'+smb['second']