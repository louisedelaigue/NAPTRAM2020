import pandas as pd
import os

# import spreadsheet
db = pd.read_excel('./data/UWS/UWS_datasheet.xlsx',
                   skiprows=[1])

# create list of files we want to keep
file_list = [file for file in os.listdir('./data/UWS') if 
                  '_'.join(file.split('_')) in db.pH_optN.values]

# create loop to extract data
data_dict = {} # tell python this is an empty dict so we can put the tables in
for file in file_list:
    fname = "./data/UWS/{}/{}.txt".format(file,file)
    data_dict[file] = pd.read_table(fname, skiprows=22, encoding="unicode_escape")

# rename headers of df inside dict and get rid off empty columns
rn = {
      "Date [A Ch.1 Main]":"date",
      "Time [A Ch.1 Main]":"time",
      " dt (s) [A Ch.1 Main]":"sec",
      "pH [A Ch.1 Main]":"pH",
      "Fixed Temp (?C) [A Ch.1 CompT]":"temp"
      }

for file in file_list:
    data_dict[file].rename(rn, axis=1, inplace=True)
    data_dict[file].drop(columns=["Date [Comment]",
                    "Time [Comment]",
                    "Comment",
                    "Unnamed: 23",
                    "Unnamed: 24",
                    "Unnamed: 25",
                    "Unnamed: 26",
                    "Unnamed: 27",
                    "Unnamed: 28",
                    "Unnamed: 29"],
                    inplace=True)
    data_dict[file].dropna()
    
# turn dict into single df
data = pd.concat(data_dict.values(), ignore_index=True)

# clean-up the SMB file to only keep where temp_source contains data
# load smb in chunks
chunky = pd.read_csv('./data/UWS/smb_all_hr.csv',
                     chunksize=150000,
                     na_values=9999,
                     low_memory=False)

# create empty list to hold cleaned up chunks
smb_list = []

# rename temp_source column to python friendly, then only keep where 
# temp_source has data, then store cleaned up chunks into smb_list
for file in chunky:
    file = file.drop([file.index[0], file.index[1]])
    file.reset_index(drop=True)
    rn = {
       'SMB.RSSMB.T_SBE38':'SBE38_water_temp'
       }
    file.rename(rn, axis=1, inplace=True)
    file.dropna(subset=['SBE38_water_temp'], inplace=True)
    smb_list.append(file)

# create 1 df holding all cleaned up smb data
smb = pd.concat(smb_list)

# rename headers with python friendly names
rn = {
      'date time':'time',
      'Weatherstation.PDWDC.Airtemperature':'WS_airtemp',
      'Weatherstation.PDWDC.Barometric':'WS_baro',
      'Weatherstation.PDWDC.Course':'WS_course',
      'Weatherstation.PDWDC.Date':'WS_date',
      'Weatherstation.PDWDC.Heading':'WS_heading',
      'Weatherstation.PDWDC.Humidity':'WS_humidity',
      'Weatherstation.PDWDC.Latitude':'WS_lat',
      'Weatherstation.PDWDC.Longitude':'WS_lon',
      'Weatherstation.PDWDC.Longwave':'WS_longwave',
      'Weatherstation.PDWDC.NormalizedTo':'WS_normto',
      'Weatherstation.PDWDC.Pyrogeometer':'WS_pyrogeometer',
      'Weatherstation.PDWDC.SensorValue':'WS_sensorvalue',
      'Weatherstation.PDWDC.Sentence':'WS_sentence',
      'Weatherstation.PDWDC.Shortwave':'WS_shortwave',
      'Weatherstation.PDWDC.Speed':'WS_speed',
      'Weatherstation.PDWDC.Timestamp':'WS_timestamp',
      'Weatherstation.PDWDC.Watertemperature':'WS_watertemp',
      'Weatherstation.PDWDC.Winddirection_rel':'WS_winddirection_rel',
      'Weatherstation.PDWDC.Winddirection_true':'WS_winddirection_true',
      'Weatherstation.PDWDC.Windspeed_rel':'WS_windspeed_rel',
      'Weatherstation.PDWDC.Windspeed_true':'WS_windspeed_true',
      'Weatherstation.PDWDC.Windspeed_true_Bft':'WS_windspeed_true_bft',
      'SMB.RSSMB.Chl':'chl',
      'SMB.RSSMB.C_SBE45':'SBE_45_C',
      'SMB.RSSMB.Date':'date',
      'SMB.RSSMB.Delay':'delay',
      'SMB.RSSMB.Depth':'depth',
      'SMB.RSSMB.EW':'ew',
      'SMB.RSSMB.Flow':'flow',
      'SMB.RSSMB.Latitude':'lat',
      'SMB.RSSMB.Longitude':'lon',
      'SMB.RSSMB.Name':'smb_name',
      'SMB.RSSMB.NS':'ns',
      'SMB.RSSMB.RVK':'system',
      'SMB.RSSMB.Sal_SBE45':'SBE45_sal',
      'SMB.RSSMB.Sentence':'sentence',
      'SMB.RSSMB.SN':'sn',
      'SMB.RSSMB.SV_SBE45':'SBE45_sv',
      'SMB.RSSMB.SV_insito':'insitu_sv',
      'SMB.RSSMB.Status':'smb_status',
      'SMB.RSSMB.SV_AML':'smb_sv_aml',
      'SMB.RSSMB.T_SBE45':'SBE45_water_temp',
      'SMB.RSSMB.Time':'smb_time',
      'SMB.RSSMB.Tur':'smb_tur'
      }

smb.rename(rn, axis=1, inplace=True)

# SMB DATE/TIME (metadata)
# date
smb['date'] = pd.to_datetime(smb['time'], format='%m/%d/%Y %H:%M').dt.date
smb['month'] = smb['date'].apply(lambda x: x.month)
smb['day'] = smb['date'].apply(lambda x: x.day)

# time
smb['hms'] = pd.to_datetime(smb['time'], format='%m/%d/%Y %H:%M').dt.time
smb['hour'] = smb['hms'].apply(lambda x: x.hour)
smb['minute'] = smb['hms'].apply(lambda x: x.minute)

# create seconds column for smb time - TO EDIT WITH AN IF CONDITION (if less than 60 duplicates, then  fill with nan)
smb['second'] = smb.groupby('time').cumcount()+1

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

# merge SMB w/ PYRO
df = data.merge(right=smb, 
               how='inner',
               on=['day','month','hour','minute','second'])


# first plot only the PYRO data to see where gaps are, and where buffers/CRMs are
# then figure out why only 12000 lines in df vs. 50000 in PYRO data













