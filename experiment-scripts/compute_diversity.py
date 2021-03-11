import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from config import get_timestamp

# problem to analyze density
program = 'quicksort'

# set base directory
base = 'output/{}'.format(get_timestamp())

df = pd.read_csv('{}/fitness.csv'.format(base), index_col=0)

# select program
df = df.loc[df['program'] == program]

# decision fitness
df_decision = df.loc[df['fitness function'] == 'decision']
decision_max = df_decision['fitness score'].max()
df_decision['fitness score'] = df_decision['fitness score'].div(decision_max)

# genprog
df_genprog = df.loc[df['fitness function'] == 'original']
original_max = df_genprog['fitness score'].max()
df_genprog['fitness score'] = df_genprog['fitness score'].div(original_max)

# arjae
df_arjae = df.loc[df['fitness function'] == 'arjae']
arjae_max = df_arjae['fitness score'].max()
df_arjae['fitness score'] = df_arjae['fitness score'].div(arjae_max)

df = pd.concat([df_genprog, df_decision, df_arjae])

sns.set(style="whitegrid", palette="pastel", color_codes=True)
ax = sns.violinplot(x="fitness function", y="fitness score", data=df)

plt.savefig('{}/diversity/{}.png'.format(base, program))
