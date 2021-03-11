import random
from datetime import datetime

# if set to 'now', it will be current time
timestamp = 'all'

# gin project absolute path
gin_dir = '../gin' #

generations = 10

population_size = 40

# run with evosuite generated test cases
evosuite_included = [
    False,
    # True
]

# fully random on seeds (overwrite below seeds)
repeat = 20

# random seeds [mutation, mutant selection]
default_seeds = [
    (111, 111),
    # (753, 753),
    # (1024, 1024),
]

# maximum time(ms) on running a test case
timeout = 1000

# GIN edit types
edits = [
    'STATEMENT',
    # 'MATCHED_STATEMENT',
     'MODIFY_STATEMENT',
    # 'INSERT_STATEMENT',
    # 'LINE'
]

# fitness function types
fitness_types = [
    'original',
     'decision',
     'arjae',
    # 'checkpoint' # only support LIS
]

# benchmark problems (17 in total, 2 have wrong method files)
problems = [
    # 'depth_first_search', # 79
    # 'detect_cycle',  # 350
    # 'find_in_sorted', # 117
    'get_factors', # 126
     'hanoi',  # wrong method file
    'is_valid_parenthesization', # 91
    'knapsack', # 417
    'levenshtein', # 183
    'lis',  # 69
    'mergesort', # 185
    'next_permutation', # 72
    'powerset', # 73
    'quicksort', # 2571 , found 50 identical fixes
    'rpn_eval', # 96, too many fixed patches
     'shortest_path_lengths',
    'sqrt'
    # 'sieve'
    # 'wrap' # slow
    ################ unrelated problems #################
    # 'bitcount',
    # 'to_base',
    # 'max_sublist_sum',
    # 'next_palindrome',
    
]

# gp search logging level
gp_log = [
     #'trace',
     #'debug',
     'info',
    # 'warning',
    'error'
]

# patch analyzer logging level
# must set be info to read the output of analysis
patch_analyser_log = [
    # 'trace',
    # 'debug',
    'info',
    # 'warning',
    # 'error'
]

# gin config: enable history patch records
record_patch = True

# enable patch analyzer for test-suite-adequate patches
# it is slow on RPN_EVAL because there are too many identical patches
analyze_patch = True


# return default seeds or generate random seeds
def get_seeds():
    global default_seeds
    # no repeat, use default seeds
    if repeat == 0:
        return default_seeds
    # create random seeds
    seeds = []
    for i in range(repeat):
        seeds.append((random.randint(1, 1000000), random.randint(1, 1000000)))
    return seeds


# return timestamp of the current experiment
def get_timestamp():
    global timestamp
    if timestamp == "now":
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return timestamp

