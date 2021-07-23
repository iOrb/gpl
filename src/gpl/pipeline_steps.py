import os

from sltp.driver import Step, check_int_parameter, InvalidConfigParameter
from sltp.returncodes import ExitCode
from sltp.util.naming import compute_sample_filenames, compute_test_sample_filenames, compute_info_filename


class TrainStep(Step):
    """ Expand the entire state space """

    def get_required_attributes(self):
        return ["instances",
                "domain",
                # "num_episodes",
                # "num_rollouts",
                # "rollout_depth",
                # "val_isntances",
        ]

    def get_required_data(self):
        return []

    def process_config(self, config):
        if "num_episodes" not in config:
            config["num_episodes"] = 1
        # config["sample_files"] = compute_sample_filenames(**config)
        config["sample_file"] = compute_info_filename(config, "sample.pickle")
        return config

    def description(self):
        return "Train: Explore the state space of the training instances"

    def get_step_runner(self):
        from .train import run
        return run


class PolicyTesting(Step):
    """ Test the policy """
    def get_required_attributes(self):
        return ["experiment_dir", "test_instances"]

    def process_config(self, config):
        # if any(not os.path.isfile(i) for i in config["test_instances"]):
        #     raise InvalidConfigParameter('"test_instances" must point to existing files')
        self.config = config
        return self.config

    def get_required_data(self):
        return ["d2l_policy"]

    def description(self):
        return "Testing of the D2L policy"

    def get_step_runner(self):
        if self.config['interactive_demo']:
            from .demo import run
        else:
            from .tester import run
        return run


GPL_PIPELINE = [
    TrainStep,
    PolicyTesting,
]




