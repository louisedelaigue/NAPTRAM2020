# Data processing for SO279.

## Data
Data used in this repo comes from the SO279 cruise across the North Atlantic in the Azores Region (December 2020).

## Raw processing
* _so279_uws_raw_processing.py_: processes raw data by assembling all underway Pyroscience optode pH files together, then imports the biogeochemical data from the SMB salinograph on board to match the exact dates and times of the pH data. Also converts degree coordinates to decimal coordinates. Renames columns in user-friendly headers. Saves output dataframe to .csv.

* _so279_carb_param_calc.py_: estimates Totalk Alkalinity (TA) on the cruise track from in-situ temperature and salinity (SMB salinograph on board) using Lee et al. (2006) equations. Recalculates in-situ pH from estimated TA and optode pH. Saves output dataframe to .csv.
