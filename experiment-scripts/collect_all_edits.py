import os
import pandas as pd
import re
from config import get_timestamp

# set base directory
base = 'output/{}'.format(get_timestamp())

# collect all result files name
f_names = os.listdir('{}/results'.format(base))

# store the tmp dataframes
frames = []

for f_name in f_names:
    # parse file name
    info = re.findall("(\w+)-(\w+)-(\d+)-(\d+)-(\w+).csv", f_name)[0]
    fitness = info[0]
    problem = info[1]
    m_seed = info[2]
    s_seed = info[3]
    postfix = info[4]
    with_evosuite = (postfix == 'True')

    # dataframe for single file
    df = pd.read_csv('{}/results/{}'.format(base, f_name))
    df = df[df['AllTestsPassed']]
    df = df['Patch'].to_frame()
    df['program'] = problem
    df['fitness function'] = fitness
    df['run with evosuite'] = with_evosuite
    df['mutation seed'] = m_seed
    df['selection seed'] = s_seed
    frames.append(df)

df = pd.concat(frames)

df.to_csv('{}/{}'.format(base, 'edits.csv'))
