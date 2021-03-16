# GPL: General Policy Learner
Learn and test generalized policies from planning examples.

Work in progress: Allow stochastic environments (FOND extension).

## Installation
We recommend using a Python virtual environment.\\
Install the entire pipeline by running `pip install -e .` and `pip install gpl`.\\
Then `cd src\d2l && pip install -e .`.

Install:\
https://github.com/tomsilver/generalization_grid_games

## Experiments
The [experiments](experiments) folder contains experiment setups for some common domains.
You can run any of them with `./run.py <domain>:<experiment>`, where domain is the domain name,
and "experiment" a concrete experiment setup for that domain, e.g., `./run.py rfts:one`.
