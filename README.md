# GPL: General Policy Learner
Learn and test generalized policies from planning examples.

Work in progress: Allow stochastic environments (FOND extension).

## Installation
Install the entire pipeline by running `pip install -e .`.
We recommend using a Python virtual environment.

install:\
https://github.com/iOrb/generalization_grid_games_2

## Experiments
The [experiments](experiments) folder contains experiment setups for some common domains.
You can run any of them with `./run.py <domain>:<experiment>`, where domain is the domain name,
and "experiment" a concrete experiment setup for that domain, e.g., `./run.py rfts:one`.
