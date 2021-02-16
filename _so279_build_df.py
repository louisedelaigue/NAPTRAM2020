import pickle

# Save some variables (data, stations and groups)
with open("pickles/data_stations_groups_v9.pkl", "wb") as f:
    pickle.dump((data, stations, groups), f)
    
# Import them (in a different script)
with open("pickles/data_stations_groups_v9.pkl", "rb") as f:
    data, stations, groups = pickle.load(f)