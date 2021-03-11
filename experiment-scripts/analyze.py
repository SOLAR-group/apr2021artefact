import os
import shutil
import subprocess

import pandas as pd
import re
from config import patch_analyser_log
from config import analyze_patch
from config import get_timestamp

df_analysis = pd.DataFrame(
    columns=['fitness type',
             'problem name',
             'run with evosuite',
             'mutation seed',
             'selection seed',
             'number of fixed patch',
             'number of unique fixed patch',
             'number of unique fixed patch passed evosuite',
             'number of evaluations to find first fixed patch',
             'minimum number of edits to find a fix',
             'number of better patches',
             'ratio of better patches',
             'number of equal patches',
             'ratio of equal patches'])

# base directory of results
base = 'PLACEHOLDER'


# analyze file with input file name
def analyze_file(f_name):
    global df_analysis

    # parse file name
    info = re.findall("(\w+)-(\w+)-(\d+)-(\d+)-(\w+).csv", f_name)[0]
    fitness = info[0]
    problem = info[1]
    m_seed = info[2]
    s_seed = info[3]
    postfix = info[4]
    with_evosuite = (postfix == 'True')

    # read file content
    df = pd.read_csv(f_name)
    init_fit_value = df.iloc[0]['Fitness']
    num_patch = len(df)

    # number of fixed patch
    fix_df = df[df['AllTestsPassed']]
    num_fix = len(fix_df)

    # number of evaluations to find the first fix; -1 if no fix is found
    min_edits = 999999
    num_fix_evo = 0
    edit_dict = {}
    if num_fix == 0:
        first_fix = 999999
    else:
        first_fix = fix_df.index.values[0]
        # number of edits of each fix
        for patch in fix_df['Patch']:
            num_edits = patch.count('|') - 1
            min_edits = min(min_edits, num_edits)
        # execute PatchAnalyser to get fixed patch
        if analyze_patch:
            # file that save analyze cmds
            f = open('{}/patch_analyser_cmds.txt'.format(base), 'w')
            # create folder for fixed patch
            path = '{}/fixed_patches'.format(base)
            if not os.path.exists(path):
                os.makedirs(path)
            # remove duplicate
            count = 0
            for patch in fix_df['Patch']:
                count += 1
                if patch in edit_dict:
                    edit_dict[patch] += 1
                else:
                    edit_dict[patch] = 1
            # analyze each fixed patch
            i = 0
            for edit in edit_dict.keys():
                i += 1
                id = '{fitness}-{problem}-{mut}-{sel}-{i}.java'.format(
                    fitness=fitness,
                    problem=problem,
                    mut=m_seed,
                    sel=s_seed,
                    i=i)
                cmd = 'java -Dtinylog.level={log} -cp gin.jar gin.PatchAnalyser -f quixbugs/faulty_programs/{problem}.java -c {class_name} -t {test_class_name} -cp {classpath} -d {project} -p "{edits}" -b {base} -id {id}'.format(
                    log=patch_analyser_log[0],
                    problem=problem.upper(),
                    edits=edit,
                    base=path,
                    id=id,
                    class_name='faulty_programs.{}'.format(problem.upper()),
                    classpath='quixbugs',
                    test_class_name='faulty_programs.{}_TEST'.format(problem.upper()),
                    project='quixbugs'
                )
                # execute patch analyser and collect result
                f.write(cmd + '\n')
                f.flush()
                result = subprocess.check_output(cmd, shell=True)
                # look for all test successful meesage
                if re.search(b'true', result) is not None:
                    num_fix_evo += 1  # valid
                    valid = 'passed'
                else:
                    valid = 'failed'
                # rename generated patch
                path = '{}/fixed_patches/'.format(base)
                new_file_name = '{path}/{fitness}-{problem}-{mut}-{sel}-{count}-{valid}.java'.format(
                    path=path,
                    fitness=fitness,
                    problem=problem,
                    mut=m_seed,
                    sel=s_seed,
                    count=i,
                    valid=valid)
                os.rename('{}/{}'.format(path, id), new_file_name)

    # number/percentage of better fitness patches
    better_df = df[df['Fitness'] > init_fit_value]
    num_better = len(better_df)
    portion_better = num_better / num_patch

    # number/percentage of same fitness patches
    same_df = df[df['Fitness'] == init_fit_value]
    num_same = len(same_df)
    portion_same = num_same / num_patch

    num_fix_unique = len(edit_dict)

    # save on main df
    save_df = pd.Series(
        [fitness, problem, with_evosuite, m_seed, s_seed, num_fix, num_fix_unique, num_fix_evo,
         first_fix, min_edits,
         num_better,
         portion_better,
         num_same,
         portion_same],
        index=df_analysis.columns)

    df_analysis = df_analysis.append(save_df, ignore_index=True)


# analyze all files in results folder
def analyze_results():
    # create fixed patch directory
    path = '{}/fixed_patches'.format(base)
    if os.path.exists(path):
        shutil.rmtree(path)
    # analyze each result patch file
    f_names = os.listdir('{}/results'.format(base))
    for f_name in f_names:
        print('analyzing: ' + f_name)
        analyze_file('{}/results/{}'.format(base, f_name))


def analyze():
    global base
    base = 'output/{}'.format(get_timestamp())
    # run analysis
    analyze_results()
    df_analysis.to_csv('{}/analysis.csv'.format(base), encoding='utf-8', index=False)
    print('analysis.csv saved to {}'.format(base))


# main function
if __name__ == '__main__':
    analyze()
