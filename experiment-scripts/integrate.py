import pandas as pd

from config import get_timestamp


def compute_average():
    # base directory
    base = 'output/{}'.format(get_timestamp())

    df = pd.read_csv("{}/analysis.csv".format(base))

    df['ratio of unique fixed patch'] \
        = df['number of unique fixed patch'] / df['number of fixed patch']

    df['ratio of unique fixed patch passed evosuite'] \
        = df['number of unique fixed patch passed evosuite'] / df['number of unique fixed patch']

    df = df.groupby(['problem name',
                     'fitness type'], as_index=False) \
        .agg({'number of fixed patch': [lambda x: x[x > 0].count(),
                                        'sum',
                                        'mean'],  # run with fix, sum of fixed patch, average fixed patch
              'ratio of unique fixed patch': ['sum'],  # need post-process
              'ratio of unique fixed patch passed evosuite': ['sum'],  # need post-process
              'number of evaluations to find first fixed patch': ['min'],
              'minimum number of edits to find a fix': ['min'],
              'ratio of better patches': ['mean'],
              'ratio of equal patches': ['mean']})

    # df.columns = df.columns.droplevel(level=1)

    new_column_names = ['problem',
                        'fitness type',
                        'run with fix',
                        'number of all fixed patch',
                        'average number of fix patch per run',
                        'average ratio of fixed patch is unique',
                        'average ratio of unique patch can pass evosuite',
                        'number of evaluations to find first fixed patch',
                        'minimum number of edits to find a fix',
                        'ratio of better fitness patches',
                        'ratio of same fitness patches']
    # print(len(new_column_names))

    df.columns = new_column_names

    print(df.columns)

    df['average ratio of fixed patch is unique'] /= df['run with fix']
    df['average ratio of unique patch can pass evosuite'] /= df['run with fix']

    # float to percentage
    df['ratio of better fitness patches'] = df['ratio of better fitness patches'].astype(float).map("{:.2%}".format)
    df['ratio of same fitness patches'] = df['ratio of same fitness patches'].astype(float).map("{:.2%}".format)
    df['average number of fix patch per run'] = df['average number of fix patch per run'].map('{:.2f}'.format)
    df['average ratio of fixed patch is unique'] = df['average ratio of fixed patch is unique'].astype(
        float).map("{:.2%}".format)
    df['average ratio of unique patch can pass evosuite'] = df[
        'average ratio of unique patch can pass evosuite'].astype(
        float).map("{:.2%}".format)

    # output file
    filename = 'result'
    df.to_csv('{}/{}.csv'.format(base, filename), encoding='utf-8', index=False)
    print('{}.csv saved to {}'.format(filename, base))


if __name__ == '__main__':
    compute_average()
