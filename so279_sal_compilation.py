import pandas as pd

# import cruise data
so279_df = pd.read_csv('./data/df_carb.csv')

# isolate date from date_time object
so279_df['date_time'] = pd.to_datetime(so279_df.date_time)
so279_df['only_date'] = [d.date() for d in so279_df['date_time']]

# get salinity mean, min and max
sal_min_max = so279_df.groupby('only_date').agg({'SBE45_sal': ['mean', 'min', 'max']}) 

# save
sal_min_max.to_csv('./data/salinity_compilation.csv')