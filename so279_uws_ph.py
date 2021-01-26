import pandas as pd
import os
import numpy as np
import time
import datetime
from datetime import timedelta
import PyCO2SYS as pyco2

# import spreadsheet
db = pd.read_excel('./data/UWS/UWS_datasheet.xlsx',
                   skiprows=[1])

# create list of files we want to keep
file_list = [file for file in os.listdir('./data/UWS') if 
                  '_'.join(file.split('_')) in db.pH_optN.values]

# create loop to extract data
data_dict = {} # tell python this is an empty dict so we can put the tables in
for file in file_list:
    fname = "./data/UWS/{}/{}.txt".format(file, file)
    data_dict[file] = pd.read_table(fname, skiprows=22, encoding="unicode_escape")

# rename headers of df inside dict and get rid off empty columns
rn = {
      "Date [A Ch.1 Main]":"date",
      "Time [A Ch.1 Main]":"time",
      " dt (s) [A Ch.1 Main]":"sec",
      "pH [A Ch.1 Main]":"pH",
      "Sample Temp. (°C) [A Ch.1 CompT]":"temp",
      "dphi (°) [A Ch.1 Main]":"dphi",
      "Signal Intensity (mV) [A Ch.1 Main]":"signal_intensity",
      "Ambient Light (mV) [A Ch.1 Main]":"ambient_light",
      "ldev (nm) [A Ch.1 Main]":"ldev",
      "Status [A Ch.1 Main]":"status_ph",
      "Status [A Ch.1 CompT]":"status_temp",
      }

for file in file_list:
    data_dict[file].rename(rn, axis=1, inplace=True)
    data_dict[file]['date_time'] = np.nan
    data_dict[file].date_time = data_dict[file].date + ' ' + data_dict[file].time
    data_dict[file].drop(columns=["Date [Comment]",
                    "Time [Comment]",
                    "Comment",
                    "date",
                    "time",
                    "pH (pH) [A Ch.1 Main]",
                    "Date [A Ch.1 CompT]",
                    "Time [A Ch.1 CompT]",
                    " dt (s) [A Ch.1 CompT]",
                    "Date [A T1]",
                    "Time [A T1]",
                    " dt (s) [A T1]",
                    "Sample Temp. (°C) [A T1]",
                    "Status [A T1]",
                    "Unnamed: 23",
                    "Unnamed: 24",
                    "Unnamed: 25",
                    "Unnamed: 26",
                    "Unnamed: 27",
                    "Unnamed: 28",
                    "Unnamed: 29"],
                    inplace=True)
    data_dict[file].dropna()
    data_dict[file] = data_dict[file][['date_time',
                                     'sec',
                                     'pH',
                                     'temp',
                                     'dphi',
                                     'signal_intensity',
                                     'ambient_light',
                                     'ldev',
                                     'status_ph',
                                     'status_temp']]

# FILES CLEAN UP
# only keep relevant data (apply cruise notes)
# file 1 - 2020-12-08_204002_SO279_STN1_test - real data only up to 91740 seconds,
# then CRM for 420 seconds, then pH2 until the end
L = data_dict['2020-12-08_204002_SO279_STN1_test'].sec <= 91740
data_dict['2020-12-08_204002_SO279_STN1_test'] = data_dict['2020-12-08_204002_SO279_STN1_test'][L]
# substract one hour to put data back in UTC
# This only needs to be done for this one file because the pH laptop time was adjusted
# after this point to be consistent with UTC.
sh = pd.Timedelta(1, unit='h')
data_dict['2020-12-08_204002_SO279_STN1_test']['date_time'] = pd.to_datetime(data_dict['2020-12-08_204002_SO279_STN1_test'].date_time,
                      format='%d-%m-%Y %H:%M:%S.%f') - sh

# file 2 - 2020-12-11_163148_NAPTRAM2020 - no end of sampling because problem 
# with pump which ruined the optode cap on 14/12
# data is unstable after 251791 seconds
L = data_dict['2020-12-11_163148_NAPTRAM2020'].sec <= 251791
data_dict['2020-12-11_163148_NAPTRAM2020'] = data_dict['2020-12-11_163148_NAPTRAM2020'][L]

# file 3 - 2020-12-15_214136_NAPTRAM20202 - NO end of sampling because problem
# with pump which ruined the optode cap on 16/12
# data is unstable after 79290.5 seconds
L = data_dict['2020-12-15_214136_NAPTRAM20202'].sec <= 79290.5
data_dict['2020-12-15_214136_NAPTRAM20202'] = data_dict['2020-12-15_214136_NAPTRAM20202'][L]

# file 4 - 2020-12-17_134828_NAPTRAM20203 - stopped working on 18/12 at 11am 
# BUT no need to use logical array as stopped optode on time

# file 5 - 2020-12-18_222759_NAPTRAM20204 - in pH2 after 16h50 on 20/12
# data real data only up to 152521 seconds
L = data_dict['2020-12-18_222759_NAPTRAM20204'].sec <= 152521
data_dict['2020-12-18_222759_NAPTRAM20204'] = data_dict['2020-12-18_222759_NAPTRAM20204'][L]

# file 6 - 2020-12-20_182318_NAPTRAM20205 - membrane pump needed maintenance
# BUT no need to use logical array as stopped optode on time

# file 7 - 2020-12-21_112915_NAPTRAM20206 - didn't recalibrate as left optode 
# in UWS seawater - after optode stabilization, values look fine 27/12 - 9h30ish,
# VTD turned the pump off without telling me
# running a CRM6 as a sample to try and estimate drift [NEXT FILE]
# data real data only up to 511263 seconds
L = data_dict['2020-12-21_112915_NAPTRAM20206'].sec <= 511263
data_dict['2020-12-21_112915_NAPTRAM20206'] = data_dict['2020-12-21_112915_NAPTRAM20206'][L]

# file 8 - 2020-12-27_101200_NAPTRAM2020CRM6 - VTD turned pump off
# this file is a unique CRM to try and estimate drift in previous file

# file9 - 2020-12-28_151321_NAPTRAM20207 - in pH2 after 20h40 on 30/12
# data real data only up to 195991 seconds
L = data_dict['2020-12-28_151321_NAPTRAM20207'].sec <= 195991
data_dict['2020-12-28_151321_NAPTRAM20207'] = data_dict['2020-12-28_151321_NAPTRAM20207'][L]

# for all files, ignore first 20 min for optode stabilization
for file in file_list:
    L = (data_dict[file].sec > 1200)
    data_dict[file] = data_dict[file][L]
    data_dict[file]['date_time'] = pd.to_datetime(data_dict[file].date_time,
                      format='%d-%m-%Y %H:%M:%S.%f')

# turn dict into single df
data = pd.concat(data_dict.values(), ignore_index=True)

# drop ms
data['date_time'] = data['date_time'].apply(lambda x: x.strftime('%d-%m-%Y %H:%M:%S'))

# clean-up the SMB file to only keep where temp_source contains data
# load smb in chunks
chunky = pd.read_csv('./data/UWS/smb_all_hr.dat',
                     chunksize=150000,
                     na_values=9999,
                     delimiter='\t',
                     encoding= 'unicode_escape',
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
    # file.dropna(subset=['SBE38_water_temp'], inplace=True)
    smb_list.append(file)

# create 1 df holding all cleaned up smb data
smb = pd.concat(smb_list)

# rename headers with python friendly names
rn = {
      'date time':'date_time',
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

# convert SMB date format to match PyroSci date format
def date_convert(date_to_convert):
     return datetime.datetime.strptime(date_to_convert, '%Y/%m/%d %H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')
smb['date_time'] = smb['date_time'].apply(date_convert)

# merge SMB w/ PyroSci data
df = data.merge(right=smb, 
                how='inner',
                on=['date_time'])

# Convert column formats to be more useful for analysis
df["date_time"] = pd.to_datetime(df.date_time)
df["pH"] = np.float64(df.pH)

# estimate TA for the North Atlantic Ocean from S and T according to Lee et al. (2006)
def ta_nao(sss, sst):
    """Estimate TA in the North Atlantic Ocean."""
    return (
        2305 
        + (53.97 * (sss - 35)) 
        + (2.74 * ((sss - 35)**2)) 
        - (1.16 * (sst - 20)) 
        + (0.040 * ((sst - 20)**2)) 
        )

# create new column with results in dataset
df['ta_est'] = ta_nao(df.SBE45_sal, df.SBE38_water_temp)

# recalculate pH at in-situ temperature (SBE38) using estimated TA
carb_dict = pyco2.CO2SYS_nd(df.ta_est, df.pH, 1, 3, 
                      salinity=df.SBE45_sal,
                      temperature=df.temp,
                      temperature_out=df.SBE38_water_temp,
                      pressure=0,
                      pressure_out=3,
                      opt_pH_scale=1,
                      opt_k_carbonic=16,
                      opt_total_borate=1
                      )

# save in-situ pH to df
df['pH_insitu'] = carb_dict['pH_total_out']