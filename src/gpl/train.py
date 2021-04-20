#!/usr/bin/env python3

import sys

from gpl.defaults import generate_experiment
from sltp.util import console
from sltp.returncodes import ExitCode

from .utils import Bunch, _create_exception_msg, print_important_message, save_local_object, load_local_object, \
    get_sampling_class
from .train_steps import TRAIN_STEPS


def run(config, data, rng):
    exitcode, output = train(config, data, rng, train_steps=[], show_steps_only=False)
    return exitcode, output


def train(config, data, rng, train_steps=[], show_steps_only=False):

    data = pre_process_data(config, data)

    for episode in range(config.num_episodes):
        # TODO: check some policy convergence parameter

        print_important_message('(START Episode {})'.format(episode))

        for i, step in enumerate(TRAIN_STEPS):
            step = step()
            print_important_message("({}) {}:".format(episode, step.description()))

            # Process the requirements of the trainning step
            config, data = process_requirements(step, config, data)

            if i in config.skip_train_steps:
                continue

            # Run the trainnin step
            exitcode, config, data = run_step(step, config, data, rng)

            if exitcode != ExitCode.Success:
                return exitcode, data

        print_important_message('(END Episode {})'.format(episode))

    data = post_process_data(config, data)

    return exitcode, data.to_dict()


def run_step(step, config, data, rng):
    exitcode, data_ = step.get_step_runner(config)(config, data, rng)
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


def pre_process_data(config, data):
    data = Bunch(dict(sample=None, d2l_policy=None, tasks=None))
    if config.provided_sample_file is not None:
        data.sample = load_local_object(config.provided_sample_file)
    else:
        data.sample = get_sampling_class(config)
    if config.d2l_policy is not None:
        data.d2l_policy=config.d2l_policy
    return data


def post_process_data(config, data):
    save_local_object(data.sample, config.sample_file)
    data.sample = None
    return data