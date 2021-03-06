# Data processing for SO279

## Data
Data used in this repo comes from the SO279 cruise across the North Atlantic in the Azores Region (December 2020). Additional satellite data was downloaded from CMEMS.

## Raw processing
* _so279_uws_raw_processing.py_: processes raw data by assembling all underway Pyroscience optode pH files together, then imports the biogeochemical data from the SMB salinograph on board to match the exact dates and times of the pH data. Also converts degree coordinates to decimal coordinates. Renames columns in user-friendly headers. Saves output dataframe to .csv.

* _so279_carb_param_calc.py_: estimates Totalk Alkalinity (TA) on the cruise track from in-situ temperature and salinity (SMB salinograph on board) using Lee et al. (2006) equations. Recalculates in-situ pH from estimated TA and optode pH. Saves output dataframe to .csv.

## Further processing
* _so279_sal_compilation.py_: compiles salinity mean, min and max for each cruise day.

* _so279_satdat_interp.py_: interpolates satellite data along latitude, longitude and time to match cruise data.

## Graphs
* _so279_gif_X.py_: (X = sal, sla or sst) creates a gif of the evolution of sea level anomaliy, surface salinity or surface temperature throughout the duration of the cruise, in the study area.

* _so279_plotting_init.py_: creates a graph for:
    * Temperature from the optode sensor and in-situ temperature from the ships' SMB salinograph vs. time
    * In-situ temperature (SMB) and in-situ salinity (SMB) vs. time
    * In-situ pH (recalc) and in-situ temperature (SMB) vs. time

* _so279_track_phinsitu.py_: creates a map showing the ship's track with pH evolution.

* _so279_track_ship.py_: creates a map showing the ship's track with time indication.

* _so279_transect.py_: creates figure plotting transect on map, with four subsequent graphs of 1. in-situ pH, 2. surface salinity (SMB), 3. surface temperature (SMB) and 4. sea level anomaly (interpolated from CMEMS data) vs. time.
