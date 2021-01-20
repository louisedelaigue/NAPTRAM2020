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
                     low_memory=False)

# create empty list to hold cleaned up chunks
smb_list = []

# rename temp_source column to python friendly, then only keep where 
# temp_source has data, then store cleaned up chunks into smb_list
for file in chunky:
    new = {
       "SMB.RSSMB.T_SBE38":"temp_source"
       }
    file.rename(new, axis=1, inplace=True)
    L = (file.temp_source == 9999)
    file = file[~L]
    #print(file.shape)
    smb_list.append(file)

# create 1 df holding all cleaned up smb data
smb = pd.concat(smb_list)

