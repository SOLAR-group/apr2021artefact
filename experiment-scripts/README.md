# Refining Fitness Functions for Searched-Based Program Repair

This repository contains the experiment scripts of the "Refining Fitness Functions for Searched-Based Program Repair" paper by Zhiqiang Bian, Aymeric Blot and Justyna Petke.
The Gin repository used for this experiment is https://github.com/SOLAR-group/apr2021gin.

## quixbugs
We use [quixbugs](https://github.com/jkoppel/QuixBugs) dataset as the benchmark. `quixbugs/` contains the refactored quixbugs java classes that suit our experiment scripts.

## Get started
All data will be generated under `output/<timestamp>` folder.
1. Update the `config.py` to configure the experiments. 
2. Execute `fix.py` to start the program repair process. Gin outputs will be generated and stored at `/results/`.
3. Execute `analyze.py` to start the analysis. `/analysis.csv` will be generated. The fixed patches will be stored at `/fixed_patches/`.
4. Execute `integrate.py` to generate integrated results for all experiments. `/result.csv` will be generated.
5. Execute `collect_all_edits.py` and then `compute_uniqueness.py` to check the uniqueness of the fixed patches. `/edits.csv` and `/uniqueness.csv` will be generated.
6. Execute `collect_all_fitness.py` and then `compute_plateau.py` to check the diversities of the fitness values. `/fitness.csv` and `/plateaus.csv`will be generated.