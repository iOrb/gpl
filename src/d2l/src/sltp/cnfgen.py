import logging
import os

from tarski.dl import FeatureValueChange

from sltp.separation import TransitionClassificationPolicy, TransitionActionClassificationPolicy, StateActionClassificationPolicy, DNFAtom

from .util.tools import load_selected_features, IdentifiedFeature
from .util.command import execute, read_file
from .returncodes import ExitCode


def invoke_cpp_module(config, data, validate_features=None):
    logging.info('Calling C++ MaxSAT module')
    cmd = os.path.realpath(os.path.join(config.generators_path, "cnfgen"))
    args = ["--workspace", config.experiment_dir]
    args += ["--validate-features", ",".join(map(str, validate_features))] if validate_features is not None else []
    args += ["--use-equivalence-classes"] if config.use_equivalence_classes else []
    args += ["--use-feature-dominance"] if config.use_feature_dominance else []
    args += ["--v_slack", str(config.v_slack)]
    args += ["--distinguish-goals"] if config.distinguish_goals else []
    args += ["--initial-sample-size", str(config.initial_sample_size)]
    args += ["--refinement-batch-size", str(config.refinement_batch_size)]
    args += ["--seed", str(config.seed)]
    args += ["--verbosity", str(config.verbosity)]
    args += ["--acyclicity", str(config.acyclicity)]
    args += ["--encodings_dir", str(config.encodings_dir)]
    args += ["--sampling_strategy", str(config.sampling_strategy)]
    args += ["--optimal_steps", str(config.optimal_steps)]
    args += ["--consistency_bound", str(config.consistency_bound)]
    args += ["--n_features", str(config.n_features)]
    args += ["--closed"] if config.closed else []
    args += ["--maxsat_iter", str(config.maxsat_iter)]
    args += ["--allow_bad_states"] if config.allow_bad_states else []
    args += ["--decreasing_transitions_must_be_good"] if config.decreasing_transitions_must_be_good else []
    args += ["--allow_cycles"] if config.allow_cycles else []
    args += ["--use_action_ids"] if config.use_action_ids else []
    args += ["--use_weighted_tx"] if config.use_weighted_tx else []
    retcode = execute([cmd] + args)

    return {  # Let's map the numeric code returned by the c++ app into an ExitCode object
        0: ExitCode.Success,
        1: ExitCode.MaxsatModelUnsat,
        2: ExitCode.IterativeMaxsatApproachSuccessful
    }.get(retcode, ExitCode.CNFGenerationUnknownError)


def run(config, data, rng):
    try:
        exitcode = invoke_cpp_module(config, data, config.validate_features)
    except:
        exitcode = invoke_cpp_module(config, data)
    if exitcode != ExitCode.Success:
        # return exitcode, dict(d2l_policy=None) # keep trying
        return ExitCode.Success, dict(d2l_policy=None) # keep trying

    # Parse the DNF transition-classifier and transform it into a policy
    # policy = parse_dnf_policy(config)
    policy = parse_dnfa_policy(config)

    policy.minimize()
    # if config.use_action_ids:
    #     print("Policy (with actions):")
    #     policy.print()
    # print("\nPOLICY:")
    # policy.print_aaai20()

    return exitcode, dict(d2l_policy=policy)


def parse_dnf_policy(config):
    fval_map = {
        "=0": False,
        ">0": True,
        "INC": FeatureValueChange.INC,
        "DEC": FeatureValueChange.DEC,
        "NIL": FeatureValueChange.NIL,
    }
    # language = config.domain.generate_language()
    language = config.language_creator(config)
    policy = None
    fmap = {}
    for i, line in enumerate(read_file(config.experiment_dir + "/classifier.dnf"), 0):
        if i == 0:  # First line contains feature IDs only
            fids = list(map(int, line.split()))
            fs = load_selected_features(language, fids, config.serialized_feature_filename)
            fmap = {i: IdentifiedFeature(f, i, config.feature_namer(str(f))) for i, f in zip(fids, fs)}
            policy = TransitionClassificationPolicy(list(fmap.values()))
            continue

        clause = []
        for lit in line.split(', '):
            f, val = lit.split(' ')
            fid = int(f[2:-1])
            clause.append(DNFAtom(fmap[fid], fval_map[val]))
        policy.add_clause(frozenset(clause))
    return policy


def parse_dnfa_policy(config):
    fval_map = {
        "=0": False,
        ">0": True,
        "INC": FeatureValueChange.INC,
        "DEC": FeatureValueChange.DEC,
        "NIL": FeatureValueChange.NIL,
    }
    # language = config.domain.generate_language()
    language = config.language_creator(config)
    policy = None
    fmap = {}
    for i, line in enumerate(read_file(config.experiment_dir + "/classifier.dnf"), 0):
        if i == 0:  # First line contains feature IDs only
            fids = list(map(int, line.split()))
            fs = load_selected_features(language, fids, config.serialized_feature_filename)
            fmap = {i: IdentifiedFeature(f, i, config.feature_namer(str(f))) for i, f in zip(fids, fs)}
            policy = TransitionActionClassificationPolicy(list(fmap.values()))
            continue

        clause = []
        line.split()
        do_a, lits = line.split(' if ')
        a = int(do_a[3:-1])
        for lit in lits.split(', '):
            f, val = lit.split(' ')
            fid = int(f[2:-1])
            clause.append(DNFAtom(fmap[fid], fval_map[val]))
        policy.add_clause(frozenset(clause), (a,))
    return policy