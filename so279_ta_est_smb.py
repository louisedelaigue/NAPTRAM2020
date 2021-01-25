#  Estimate TA for the North Atlantic Ocean from S and T according to Lee et al. (2006)
def ta_nao(sss, sst):
    """Estimate TA in the Indian Ocean."""
    return (
        2305 
        + (53.97 * (sss - 35)) 
        + (2.74 * ((sss - 35)**2)) 
        - (1.16 * (sst - 20)) 
        + (0.040 * ((sst - 20)**2)) 
        )

# create new column with results in dataset
smb['ta_est'] = ta_nao(SBE45_sal, SBE38_water_temp)
