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

#%% Deal with SMB file
chunky = pd.read_csv('./data/UWS/smb_all_hr.csv',
                     chunksize=150000,
                     low_memory=False)

for file in chunky:
    new = {
       "SMB.RSSMB.T_SBE38":"temp"
       }
    file.rename(new, axis=1, inplace=True)
    L = (file.temp == 9999)
    file = file[~L]
    print(file.shape)
    
    # have it create one df for each chunk, then put a filter to remove 9999
    # in SMB.RSSMB.T_SBE38
    # then recombine to one df
    
    # if this doesnt work (still too many lines), then go through pH files first
    # only keep good data, and then go back to SMB file and only keep the right times