#!/usr/bin/env python3

import sys

from gpl.defaults import generate_experiment
from sltp.util import console
from sltp.returncodes import ExitCode

from .utils import Bunch, _create_exception_msg, print_important_message
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
    return train(config, data, rng, train_steps=[], show_steps_only=False)


def train(config, data, rng, train_steps=[], show_steps_only=False):

    for episode in range(config.num_episodes):
        # TODO: check some policy convergence parameter

        print_important_message('(START Episode {})'.format(episode))

        for step in TRAIN_STEPS:
            step = step()
            print_important_message("{}:".format(step.description()))

            # Process the requirements of the trainning step
            config, data = process_requirements(step, config, data)

            # Run the trainnin step
            exitcode, config, data = run_step(step, config, data, rng)

        print_important_message('(END Episode {})'.format(episode))


def run_step(step, config, data, rng):
    exitcode, data_ = step.get_step_runner()(config, data, rng)
    if exitcode is not ExitCode.Success:
        raise RuntimeError(_create_exception_msg(step, exitcode))
    data.update(data_)
    return exitcode, config, data


def process_requirements(step, config, data):
    config = config.to_dict()
    data = data.to_dict() if data else dict()

    # Check if the requirements of the step are satisfied
    check_requirements(step, config, data)

    config = Bunch(step.process_config(config))
    data = Bunch(data)
    return config, data


def check_requirements(step, config, data):
    attributes = step.get_required_attributes()
    for att in attributes:
        if att not in config:
            raise RuntimeError(_create_exception_msg(step, "Missing attribute {}".format(att)))

    data = step.get_required_data()
    for d in data:
        if d not in data:
            raise RuntimeError(_create_exception_msg(step, "Missing data {}".format(d)))
