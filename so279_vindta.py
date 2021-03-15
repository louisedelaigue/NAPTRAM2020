import copy
import numpy as np, pandas as pd
from matplotlib import pyplot as plt
import PyCO2SYS as pyco2, koolstof as ks, calkulate as calk

# Import logfile and dbs file
logfile = ks.read_logfile(
    "data/VINDTA/logfile.bak",
    methods=[
        "3C standard separator",
        "3C standard separator modified LD",
        "3C standard separator modified LD temp",
    ],
)
dbs = ks.read_dbs("data/VINDTA/SO279.dbs", logfile=logfile)

# Drop weird first row
dbs.drop(index=dbs.index[dbs.bottle == "03/02/21"], inplace=True)

# Create empty metadata columns
for meta in [
    "salinity",
    "dic_certified",
    "alkalinity_certified",
    "total_phosphate",
    "total_silicate",
    "total_ammonia",
]:
    dbs[meta] = np.nan

# Assign metadata values for CRMs
dbs["crm"] = dbs.bottle.str.startswith("CRM-")
dbs["crm_batch_189"] = dbs.bottle.str.startswith("CRM-189-")
dbs.loc[dbs.crm_batch_189, "dic_certified"] = 2009.48  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "alkalinity_certified"] = 2205.26  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "salinity"] = 33.494
dbs.loc[dbs.crm_batch_189, "total_phosphate"] = 0.45  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "total_silicate"] = 2.1  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "total_ammonia"] = 0  # micromol/kg-sw

# ---------------------------------------------------------vvv- UPDATE BELOW HERE! -vvv-
# Assign metadata values for samples (nutrients and salinity)
dbs.loc[~dbs.crm, "salinity"] = 35.0
dbs.loc[~dbs.crm, "total_phosphate"] = 0
dbs.loc[~dbs.crm, "total_silicate"] = 0
dbs.loc[~dbs.crm, "total_ammonia"] = 0

# Assign alkalinity metadata
dbs["analyte_volume"] = 95.0  # TA pipette volume in ml
dbs["file_path"] = "data/VINDTA/SO279/"

# Fix DIC cell ID column
# dbs.loc[..., "dic_cell_id"] = ...

# Assign TA acid batches
dbs["analysis_batch"] = 0

# Select which DIC CRMs to use for calibration --- only fresh bottles
dbs["k_dic_good"] = dbs.crm & dbs.bottle.str.endswith("-1")

# Select which TA CRMs to use for calibration
dbs["reference_good"] = ~np.isnan(dbs.alkalinity_certified)
dbs.loc[np.isin(dbs.bottle, ["CRM-189-0963-1"]), "reference_good"] = False
# ---------------------------------------------------------^^^- UPDATE ABOVE HERE! -^^^-

# Get blanks and apply correction
dbs.get_blank_corrections()
dbs.plot_blanks(figure_path="figs/vindta/dic_blanks/")

# Calibrate DIC and plot calibration
dbs.calibrate_dic()
dic_sessions = copy.deepcopy(dbs.sessions)
dbs.plot_k_dic(figure_path="figs/vindta/")
dbs.plot_dic_offset(figure_path="figs/vindta/")

# Calibrate and solve alkalinity and plot calibration
calk.io.get_VINDTA_filenames(dbs)
calk.dataset.calibrate(dbs)
calk.dataset.solve(dbs)
calk.plot.titrant_molinity(dbs, figure_fname="figs/vindta/titrant_molinity.png")
calk.plot.alkalinity_offset(dbs, figure_fname="figs/vindta/alkalinity_offset.png")

# Demote dbs to a standard DataFrame
dbs = pd.DataFrame(dbs)

# Compare initial pH measurement with PyCO2SYS value from TA & DIC
dbs["pH_alk_dic_25"] = pyco2.sys(
    dbs.alkalinity.to_numpy(),
    dbs.dic.to_numpy(),
    1,
    2,
    temperature=dbs.temperature_initial.to_numpy(),
    salinity=dbs.salinity.to_numpy(),
    total_phosphate=dbs.total_phosphate.to_numpy(),
    total_silicate=dbs.total_silicate.to_numpy(),
    total_ammonia=dbs.total_ammonia.to_numpy(),
)["pH_free"]

# Plot pH comparison
fig, ax = plt.subplots(dpi=300)
ax.scatter("pH_alk_dic_25", "pH_initial", data=dbs, s=20, alpha=0.5)
ax.set_aspect(1)
ax.grid(alpha=0.3)
ax.set_xlabel("pH from DIC and alkalinity")
ax.set_ylabel("pH from electrode")
pH_range = [
    min(dbs.pH_alk_dic_25.min(), dbs.pH_initial.min()),
    max(dbs.pH_alk_dic_25.max(), dbs.pH_initial.max()),
]
ax.plot(pH_range, pH_range, lw=0.8)
plt.savefig("figs/vindta/pH_comparison.png")
