# import toolbox
import PyCO2SYS as pyco2
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# import spreadsheet (cheat one)
db = pd.read_excel('./data/check__CRM_drift_stn1.xlsx',
                   skiprows=[1])

# rename headers of df inside dict and get rid off empty columns
rn = {
      "Date [A Ch.1 Main]":"date",
      "Time [A Ch.1 Main]":"time",
      " dt (s) [A Ch.1 Main]":"sec",
      "pH":"pH",
      "Fixed Temp (?C) [A Ch.1 CompT]":"temp"
      }

db.rename(rn, axis=1, inplace=True)
db.drop(columns=["Date [Comment]",
                    "Time [Comment]",
                    "Comment"],
                    inplace=True)

# create new column t0 calc CRM pH at in situ temp
db['CRM_expect'] = np.nan
db['talk'] = 2205.26
db['dic'] = 2009.48
db['sp'] = 33.494
db['phos'] = 0.45
db['si'] = 2.1
db['press'] = 0

# calc CRM at in situ temp
CRM = pyco2.CO2SYS_nd(db.talk, db.dic, 1, 2, 
                      salinity=db.sp,
                      temperature_out=db.temp,
                      pressure_out=db.press,
                      total_phosphate=db.phos,
                      total_silicate=db.si,
                      opt_pH_scale=1,
                      opt_k_carbonic=16,
                      opt_total_borate=1
                      )

db['CRM_expect'] = CRM['pH_total_out']

# calc drift between optode ph and CRM over 24 hours
db['ph_diff'] = db['pH'] - db['CRM_expect']

AVERAGE_drift = np.mean(db.ph_diff)