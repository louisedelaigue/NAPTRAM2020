import pandas as pd
import os
import numpy as np
import time
import datetime
from datetime import timedelta

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
sh = pd.Timedelta(1, unit='h')
data_dict['2020-12-08_204002_SO279_STN1_test'].date_time = pd.to_datetime(data_dict['2020-12-08_204002_SO279_STN1_test'].date_time,
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
    data_dict[file].date_time = pd.to_datetime(data_dict[file].date_time,
                      format='%d-%m-%Y %H:%M:%S.%f')

# turn dict into single df
data = pd.concat(data_dict.values(), ignore_index=True)

# drop ms
data['date_time'] = data['date_time'].apply(lambda x: x.strftime('%d-%m-%Y %H:%M:%S'))