import os

from sltp.driver import Step, check_int_parameter, InvalidConfigParameter
from sltp.returncodes import ExitCode
from sltp.steps import CPPMaxsatProblemGenerationStep
from sltp.util.naming import compute_sample_filenames, compute_test_sample_filenames, compute_info_filename


class TrainStep(Step):
    """ Expand the entire state space """

    def get_required_attributes(self):
        return ["instances",
                "domain",
                "num_episodes",
                "num_rollouts",
                "rollout_depth"]

    def get_required_data(self):
        return []

    def process_config(self, config):
        config["sample_files"] = compute_sample_filenames(**config)
        return config

    def description(self):
        return "Explore the state space of the training instances"

    def get_step_runner(self):
        from .train import run
        return run


class PolicyTesting(Step):
    """ Test the policy """
    def get_required_attributes(self):
        return ["experiment_dir", "test_instances"]

    def process_config(self, config):
        if any(not os.path.isfile(i) for i in config["test_instances"]):
            raise InvalidConfigParameter('"test_instances" must point to existing files')
        return config

    def get_required_data(self):
        return ["d2l_policy"]

    def description(self):
        return "Testing of the D2L policy"

    def get_step_runner(self):
        from . import tester
        return tester.test_d2l_policy_on_gym_env


GPL_PIPELINE = [
    TrainStep,
    PolicyTesting,
]




