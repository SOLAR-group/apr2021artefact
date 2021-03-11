import pandas as pd
from config import get_timestamp

# set base directory
base = 'output/{}'.format(get_timestamp())

df = pd.read_csv('{}/fitness.csv'.format(base), index_col=0)

plateaus = pd.DataFrame(columns=['program', 'fitness function', 'mutation seed', 'selection seed' 'ratio'])
for columns, run in df.groupby(['program', 'fitness function', 'mutation seed', 'selection seed'], as_index=False):
    scores = run['fitness score'].value_counts().to_frame()
    total = scores['fitness score'].sum()
    matched = scores[scores['fitness score'] > 1]['fitness score'].sum()
    ratio = matched / total
    plateaus = plateaus.append({'program': columns[0], 'fitness function': columns[1], 'mutation seed': columns[2],
                                'selection seed': columns[3], 'ratio': ratio}, ignore_index=True)

x = plateaus.groupby(['program', 'fitness function'], as_index=False).agg({'ratio': ['mean', 'std']})
x.columns = ['program', 'fitness function', 'mean', 'std']

x['mean'] = x['mean'].astype(float).map("{:.2%}".format)
x['std'] = x['std'].astype(float).map("{:.2%}".format)

x.to_csv('{}/{}'.format(base, 'plateaus.csv'))
