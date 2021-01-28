import pandas as pd

# import data
# df = pd.read_csv('./data/UWS/df.csv')

# format lat and lon columns (remove space)
df['lat'] = df['lat'].apply(lambda x: ''.join(filter(None, x.split(' '))))
df['lon'] = df['lon'].apply(lambda x: ''.join(filter(None, x.split(' '))))


df['lat_dd'] = np.nan
df['lon_dd'] = np.nan

# convert coordinates DMS to DD
def dms_dd(degrees, minutes=0, seconds=0):
    if degrees >= 0:
        decimal = degrees + minutes/60.0 + seconds/3600.0
    else:
        decimal = degrees - minutes/60.0 - seconds/3600.0
    return decimal

def convert_line(data):
    return data[0], dms_dd(*map(float,data[1].split())), dms_dd(*map(float, data[2].split()))

df['lat_dd'] = convert_line(df.lat)
