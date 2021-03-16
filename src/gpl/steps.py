import os

from sltp.driver import Step, check_int_parameter, InvalidConfigParameter
from sltp.returncodes import ExitCode
from sltp.steps import CPPMaxsatProblemGenerationStep
from sltp.util.naming import compute_sample_filenames, compute_test_sample_filenames, compute_info_filename


class StateSpaceExplorationStep(Step):
    """ Expand the entire state space """

    def get_required_attributes(self):
        return ["instances", "domain", "num_states", "test_instances",]

    def get_required_data(self):
        return []

    def process_config(self, config):
        config["sample_files"] = compute_sample_filenames(**config)
        config["test_sample_files"] = compute_test_sample_filenames(**config)
        return config

    def description(self):
        return "Expand the state space of the training instances"

    def get_step_runner(self):
        return state_space_expander


class TransitionSamplingStep(Step):
    """ Generate the sample of transitions from the set of solved planning instances """
    def get_required_attributes(self):
        return ["sample_files", "experiment_dir"]

    def get_required_data(self):
        return []

    def process_config(self, config):
        config["resampled_states_filename"] = os.path.join(config["experiment_dir"], 'sample.txt')
        config["transitions_info_filename"] = compute_info_filename(config, "transitions-info.io")

        ns = config["num_sampled_states"]
        if ns is not None:
            if isinstance(ns, int):
                ns = [ns]

            if len(config["instances"]) != len(ns):
                if len(ns) == 1:
                    ns = ns * len(config["instances"])
                else:
                    raise InvalidConfigParameter('"num_sampled_states" should have same length as "instances"')
            config["num_sampled_states"] = ns

        if config["sampling"] == "random" and config["num_sampled_states"] is None:
            raise InvalidConfigParameter('sampling="random" requires that option "num_sampled_states" is set')

        return config

    def description(self):
        return "Generation of the training sample"

    def get_step_runner(self):
        from sltp import sampling
        return sampling.run


class FeatureGenerationStep(Step):
    """ Generate the pool of candidate features """

    def get_required_attributes(self):
        return ["domain", "experiment_dir", "max_concept_size", "concept_generation_timeout"]

    def get_required_data(self):
        return ["sample"]

    def process_config(self, config):
        check_int_parameter(config, "max_concept_size")

        config["feature_matrix_filename"] = compute_info_filename(config, "feature-matrix.dat")
        config["parameter_generator"] = config.get("parameter_generator", None)
        config["concept_denotation_filename"] = compute_info_filename(config, "concept-denotations.txt")
        config["feature_denotation_filename"] = compute_info_filename(config, "feature-denotations.txt")
        config["serialized_feature_filename"] = compute_info_filename(config, "serialized-features.io")

        return config

    def description(self):
        return "Generate the pool of candidate features"

    def get_step_runner(self):
        from .features import run
        return run


class GPLPolicyTesting(Step):
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


def state_space_expander(config, data, rng):
    for i in range(0, len(config.instances)):
        config.domain.expand_state_space(instance_filename=config.instances[i],
                                         teach_policies=config.teach_policies,
                                         output=config.sample_files[i],)
    return ExitCode.Success, dict()


GPL_PIPELINE = [
    StateSpaceExplorationStep,
    TransitionSamplingStep,
    FeatureGenerationStep,
    CPPMaxsatProblemGenerationStep,
    GPLPolicyTesting
]



