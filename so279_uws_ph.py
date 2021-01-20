import pandas as pd
import os
import numpy as np
from scipy import stats

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
    new = {
       'SMB.RSSMB.T_SBE38':'SBE38_water_temp'
       }
    file.rename(new, axis=1, inplace=True)
    file.dropna(subset=['temp_source'], inplace=True)
    smb_list.append(file)

# create 1 df holding all cleaned up smb data
smb = pd.concat(smb_list)
rn = {
      'date time':'time',
      'WeatherStation.PDWDC.Airtemperature':'WS_airtemp'
      'WeatherStation.PDWDC.Barometric':'WS_baro',
      'WeatherStation.PDWC.Course':'WS_course',
      'WeatherStation.PDWC.Date':'WS_date',
      'WeatherStation.PDWC.Heading':'WS_heading',
      'WeatherStation.PDWC.Humidity':'WS_humidity',
      'WeatherStation.PDWC.Latitude':'WS_lat',
      'WeatherStation.PDWC.Longitude':'WS_lon',
      'WeatherStation.PDWC.Longwave':'WS_longwave',
      'WeatherStation.PDWC.NormalizedTo':'WS_normto',
      'WeatherStation.PDWC.Pyrogeometer':'WS_pyrogeometer',
      'WeatherStation.PDWC.SensorValue':'WS_sensorvalue',
      'WeatherStation.PDWC.Sentence':'WS_sentence',
      'WeatherStation.PDWC.Shortwave':'WS_shortwave',
      'WeatherStation.PDWC.Speed':'WS_speed',
      'WeatherStation.PDWC.Timestamp':'WS_timestamp'
      'WeatherStation.PDWC.Watertemperature':'WS_watertemp',
      'WeatherStation.PDWC.Winddirection_rel':'WS_winddirection_rel',
      'WeatherStation.PDWC.Winddirection_true':'WS_winddirection_true',
      'WeatherStation.PDWC.Windspeed_rel':'WS_windspeed_rel',
      'WeatherStation.PDWC.Windspeed_true':'WS_windspeed_true',
      'WeatherStation.PDWC.Windspeed_true_Bft':'WS_windspeed_true_bft',
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

# subset smb df to open more easily
smb_small = smb[0:100]
smb_small.reset_index(inplace=True, drop=True)