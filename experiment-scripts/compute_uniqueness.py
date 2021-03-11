import pandas as pd
from config import get_timestamp

# set base directory
base = 'output/{}'.format(get_timestamp())

df = pd.read_csv('{}/edits.csv'.format(base), index_col=0)

df = df.groupby(['program', 'fitness function'], as_index=False).agg({'Patch': ['count', 'nunique']})
df.reset_index(drop=True, inplace=True)
df.columns = ['program', 'fitness function', 'count', 'unique']

df['rate_unique'] = df['unique'].divide(df['count']).map("{:.2%}".format)

df.to_csv('{}/{}'.format(base, 'uniqueness.csv'))

print(df)