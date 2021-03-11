import os
import shutil

from config import fitness_types
from config import problems
from config import get_seeds
from config import generations
from config import population_size
from config import edits
from config import timeout
from config import evosuite_included
from config import gp_log
from config import record_patch
from config import get_timestamp

from time import perf_counter
from pathlib import Path

# file that contains all fix cmds
fix_cmds = 'gin_fix_cmds.txt'

# base directory of results
base = 'PLACEHOLDER'


# generate fix cmds and write into a file
def write_fix_cmds():
    global fix_cmds
    fix_cmds = '{base}/{filename}'.format(base=base, filename=fix_cmds)
    f = open(fix_cmds, "w")
    for fit_type in fitness_types:
        for problem in problems:
            for with_evosuite in evosuite_included:
                for seed in get_seeds():
                    f.write(constr_fix_cmd(fit_type, problem, seed[0], seed[1], with_evosuite) + '\n')
    f.close()


# construct a fix cmd
def constr_fix_cmd(fitness_type, problem, mutation_seed, selection_seed, with_evosuite):
    # set gp fix type
    if fitness_type == 'original':
        gp_class = 'gin.util.GPFix'
    elif fitness_type == 'decision':
        gp_class = 'gin.util.GPNovelFix'
    elif fitness_type == 'arjae':
        gp_class = 'gin.util.GPArjaEFix'
    elif fitness_type == 'checkpoint':
        gp_class = 'gin.util.GPCheckpointFix'
    else:
        raise ValueError("Illegal fitness type.")

    # method file name
    if with_evosuite:
        method_file = 'quixbugs/quixbugs_method_files/{problem}-evosuite.csv'.format(problem=problem)
    else:
        method_file = 'quixbugs/quixbugs_method_files/{problem}.csv'.format(problem=problem)

    # result file name
    result_file = '{dir}/{fitness}-{problem}-{mut}-{sel}-{evo}.csv'.format(
        dir='output/{}/results'.format(get_timestamp()),
        fitness=fitness_type,
        problem=problem,
        mut=mutation_seed,
        sel=selection_seed,
        evo=with_evosuite)

    # construct cmd
    cmd = 'java -Dtinylog.level={gp_log} -cp gin.jar {class_name} -d quixbugs -c quixbugs -gn {gen} -in {pop} -m {method} -o {result} -et {edits} -x {timeout} -ms {mut} -is {sel} -rec {rec} -j'.format(
        gp_log=gp_log[0],
        class_name=gp_class,
        gen=generations,
        pop=population_size,
        method=method_file,
        result=result_file,
        edits=','.join(edits),
        timeout=timeout,
        mut=mutation_seed,
        sel=selection_seed,
        rec=record_patch
    )

    # append reference method file if checkpoint
    if fitness_type == 'checkpoint':
        cmd = '{} -M quixbugs/quixbugs_method_files/{}_correct.csv'.format(cmd, problem)

    return cmd


# read fix cmds from file
def read_fix_cmds():
    f = open(fix_cmds, 'r')
    lines = f.readlines()
    cmds = []
    for line in lines:
        cmds.append(line)
    return cmds


# run fix cmds
def run_fix_cmds():
    global base
    base = 'output/{}'.format(get_timestamp())
    # create and overwrite result directory
    result_dir = '{}/results'.format(base)
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    Path(result_dir).mkdir(parents=True)
    # generate and log fix cmds
    write_fix_cmds()
    # read and run fix cmds
    fix_cmds = read_fix_cmds()
    # save run time
    f = open('{}/time.txt'.format(base), 'w')
    for cmd in fix_cmds:
        t_start = perf_counter()
        print(cmd)
        os.system(cmd)
        t_end = perf_counter()
        duration = t_end - t_start
        f.write(cmd + 'time elapsed: ' + str(duration) + '\n')


# main function
if __name__ == '__main__':
    run_fix_cmds()
