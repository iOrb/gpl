#!/usr/bin/env python3
import os.path
import sys

from gpl.defaults import generate_experiment
from sltp.util import console
from sltp.util.bootstrap import setup_argparser
from sltp.util.runner import report_and_exit, import_experiment_file


def do(expid, steps=None, workspace=None, show_steps_only=False):
    name_parts = expid.split(":")
    if len(name_parts) != 2:
        report_and_exit(f'Wrong experiment ID syntax "{expid}". Expected format <domain>:<experiment_name>')

    scriptname, expname = name_parts
    mod = import_experiment_file(f"{scriptname}.py")

    experiments = None
    try:
        experiments = mod.experiments()
    except AttributeError:
        report_and_exit(f'Expected method "experiments" not found in script "{scriptname}"')

    if expname not in experiments:
        report_and_exit(f'No experiment named "{expname}" in current experiment script')

    parameters = experiments[expname]
    if workspace is not None:
        parameters["workspace"] = workspace

    experiment, _ = generate_experiment(expid, **parameters)

    if show_steps_only:
        console.print_hello()
        print(f'Experiment with id "{expid}" is configured with the following steps:')
        print(experiment.print_description())
        return

    experiment.run(steps)

if __name__ == "__main__":
    args = setup_argparser().parse_args(sys.argv[1:])
    do(args.exp_id, args.steps, args.workspace, args.show)








