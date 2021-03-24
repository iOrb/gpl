#!/usr/bin/env python3

import sys

from gpl.defaults import generate_experiment
from sltp.util import console
from sltp.util.bootstrap import setup_argparser
from sltp.util.runner import report_and_exit, import_experiment_file
from sltp.util.defaults import get_experiment_class
from sltp.steps import generate_pipeline

from .train_steps import TRAIN_STEPS

"""
TRAIN:
params:
    n-episodes

process:
    for _ in n-episodes:

        Train Steps:

        1. Rollouts:
            process:
                for _ in n-rollouts:
                    for _ in rollout-depth:
                        if d2l-policy exists:
                            if d2l-policy applies:
                                select action from d2l-policy
                        else:
                            select action from DFS

            params:
                n-rollouts
                rollout-depth

        2. With the saved Rollouts, update the graph AND/OR:

        3. Sampling:

        4. Generate Features:
            (keeping the previous ones (?))

        5. Compute d2l-policy using maxsat solver:
"""


def run(config, data, rng):
    return train(config, data, train_steps=[], show_steps_only=False)


def train(config, data, train_steps=[], show_steps_only=False):

    trainning = generate_train(config)

    if show_steps_only:
        print(f'Trainning is configured with the following steps:')
        print(trainning.print_description())
        return

    for _ in range(config.num_episodes):
        # TODO: check some policy convergence parameter
        trainning.run(train_steps)


def generate_train(config):

    config_ = config.to_dict()

    defaults = dict(
        pipeline=TRAIN_STEPS,

        experiment_class=get_experiment_class(config_)
    )

    parameters = {**config_, **defaults}  # Copy config, overwrite with train parameters

    steps = generate_pipeline(**parameters)
    exp = parameters["experiment_class"](steps, parameters)
    return exp










