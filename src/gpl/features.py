import copy
import logging
import os
from pathlib import Path

from sltp.featuregen import print_sample_info, transform_generator_output, invoke_cpp_generator
from sltp.features import InstanceInformation, create_model_cache
from sltp.returncodes import ExitCode
from sltp.util.misc import compute_universe_from_pddl_model, state_as_atoms, types_as_atoms
from tarski.dl import compute_dl_vocabulary


def run(config, data, rng):
    return generate_feature_pool(config, data.sample)


def generate_feature_pool(config, sample):
    logging.info(f"Starting generation of feature pool. State sample used to detect redundancies: {sample.info()}")

    model_cache = prepare_generator_input(config, sample)

    # If user provides handcrafted features, no need to go further than here
    # if config.feature_generator is not None:
    #     features = deal_with_serialized_features(language, config.feature_generator, config.serialized_feature_filename)
    #     generate_output_from_handcrafted_features(sample, config, features, model_cache)
    #     return ExitCode.Success, dict(enforced_feature_idxs=[], in_goal_features=[],
    #                                   model_cache=model_cache)

    if invoke_cpp_generator(config) != 0:
        return ExitCode.FeatureGenerationUnknownError, dict()

    # Read off the output of the module and transform it into the numpy matrices to be consumed
    # by the next pipeline step
    transform_generator_output(
        config, sample,
        os.path.join(config.experiment_dir, "feature-matrix.io"),
    )

    return ExitCode.Success, dict(model_cache=model_cache, in_goal_features=None)


def prepare_generator_input(config, sample):
    """ Prepare the input for the C++ feature generator. This essentially boils down to printing information
     about the DL primitive predicates that we will use, the DL nominals, etc.
    """

    all_objects = []  # We'll collect here the set of objects used in each instance
    infos = []

    for instance in sample.representative_instances.values():
        lang, static_predicates = config.domain.generate_language()
        vocabulary = compute_dl_vocabulary(lang)

        # We interpret as DL nominals all constants that are defined on the entire domain, i.e. instance-independent
        nominals = lang.constants()
        static_predicates |= {s.name for s in lang.sorts}  # Add unary predicates coming from types!

        # For our DL grammar we'll use all predicates declared in the problem, plus type predicates
        dl_predicates = {(p.name, p.arity) for p in lang.predicates if not p.builtin} | \
                        {(p.name, 1) for p in lang.sorts if not p.builtin and p != lang.Object}

        # We clone the language so that objects from different instances don't get registered all in the same language;
        # if that happened, we'd be unable to properly compute the universe of each instace.
        pl = copy.deepcopy(lang)
        problem = config.domain.generate_problem(pl, instance)

        # Compute the universe of each instance: a set with all objects in the universe
        universe = compute_universe_from_pddl_model(problem.language)

        # Compute the set of all static atoms in the instance, including those stemming from types
        static_atoms = {atom for atom in state_as_atoms(problem.init) if atom[0] in static_predicates} |\
                       {atom for atom in types_as_atoms(problem.language)}

        infos.append(InstanceInformation(universe, static_atoms, static_predicates, {}, {}))

        all_objects.append(set(c.symbol for c in problem.language.constants()))

    model_cache = create_model_cache(vocabulary, sample.states, sample.instance, nominals, infos)
    # Write out all input data for the C++ feature generator code
    print_sample_info(sample, infos, model_cache, dl_predicates, set(), nominals, all_objects, set(), config)
    return model_cache
