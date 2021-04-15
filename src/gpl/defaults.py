import os

from gpl import GPL_SRC_DIR
from gpl.pipeline_steps import GPL_PIPELINE
from sltp import SLTP_SRC_DIR
from sltp.steps import generate_pipeline
from sltp.util.command import create_experiment_workspace
from sltp.util.defaults import get_experiment_class
from sltp.util.misc import extend_namer_to_all_features

# from generalization_grid_games.envs import two_pile_nim as tpn
# from generalization_grid_games.envs import stop_the_fall as stf
# from generalization_grid_games.envs import chase as ec
# from generalization_grid_games.envs import checkmate_tactic as ct
# from generalization_grid_games.envs import reach_for_the_star as rfts

BASEDIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
BENCHMARK_DIR = os.path.join(BASEDIR, 'benchmarks')

GENERATORS = {
    'fond': os.path.join(os.path.dirname(GPL_SRC_DIR), "generators/fond"),
    'adv': os.path.join(os.path.dirname(GPL_SRC_DIR), "generators/adv"),
}

def generate_experiment(expid, **kwargs):
    """ """
    if "instances" not in kwargs or "domain" not in kwargs:
        raise RuntimeError("Please specify domain and instance when generating an experiment")

    # kwargs["instances"] = [os.path.join(BENCHMARK_DIR, i) for i in kwargs['instances']]
    # kwargs["test_instances"] = [os.path.join(BENCHMARK_DIR, i) for i in kwargs['test_instances']]

    defaults = dict(
        pipeline=GPL_PIPELINE,

        # Some directories of external tools needed by the pipeline
        # Note that we use our own generators, not SLTP's
        generators_path=GENERATORS['adv'],
        pyperplan_path=os.path.join(os.path.dirname(SLTP_SRC_DIR), "pyperplan"),

        # The directory where the experiment outputs will be left
        workspace=os.path.join(BASEDIR, 'workspace'),

        # Type of sampling. Accepted options are:
        # - "all" (default): Use all expanded states
        # - "random": Use only a random sample of the expanded states, of size given by the option "num_sampled_states"
        # - "optimal": Use those expanded states on some optimal path (only one arbitrary optimal path)
        # Note: ATM random sampling is deactivated
        sampling="all",

        # Number of states to be expanded in the sampling procedure. Either a positive integer, or the string
        # "until_first_goal", or the string "all", both with obvious meanings
        num_states="all",

        # Number randomly sampled states among the set of expanded states. The default of None means
        # all expanded states will be used
        num_sampled_states=None,

        # Max. size of the generated concepts
        max_concept_size=10,

        # Provide a special, handcrafted method to generate concepts, if desired.
        # This will override the standard concept generation procedure (default: None)
        concept_generator=None,

        # Or, alternatively, provide directly the features instead of the concepts (default: None)
        feature_generator=None,

        # A list of features the user wants to be in the abstraction (possibly along others).
        # Default is [], i.e. just run the generation process without enforcing anything
        enforce_features=[],

        # Max. allowed complexity for distance and conditional features (default: 0)
        distance_feature_max_complexity=0,
        cond_feature_max_complexity=0,

        # Whether to generate comparison features of the type F1 < F2
        comparison_features=False,

        # Method to generate domain parameters (goal or otherwise). If None, goal predicates will
        # be used (default: None)
        parameter_generator=None,

        # Whether to create goal-identifying features (e.g. of the form p_g AND not p_s for every unary predicate
        # apperaring in the goal)
        create_goal_features_automatically=False,

        # Optionally, use a method that gives handcrafted names to the features
        # (default: None, which will use their string representation)
        feature_namer=default_feature_namer,

        # Set a random seed for reproducibility (default: 1)
        random_seed=1,

        # the max-sat solver to use. Accepted: openwbo, openwbo-inc, wpm3, maxino
        maxsat_solver='openwbo',
        maxsat_timeout=None,

        # The Experiment class to be used (e.g. standard, or incremental)
        experiment_class=get_experiment_class(kwargs),

        # Reduce output to a minimum
        quiet=False,

        # Number of states to expand & test on the testing instances
        num_tested_states=50000,

        # The particular encoding to be used by the C++ CNF generator
        maxsat_encoding="d2l",

        # Some debugging help to print the denotations of all features over all states (expensive!)
        print_denotations=False,

        # By default don't timeout the concept generation process
        concept_generation_timeout=-1,

        # A function to manually provide a transition-classification policy that we want to test
        d2l_policy=None,

        # In the transition-separation encoding, whether we want to exploit the equivalence relation
        # among transitions given by the feature pool
        use_equivalence_classes=False,

        # In the transition-separation encoding, whether we want to exploit the dominance among features to ignore
        # dominated features and reduce the size of the encoding
        use_feature_dominance=False,

        # Whether to automatically generate goal-distinguishing concepts and roles
        generate_goal_concepts=False,

        # The slack value for the maximum allowed value for V_pi(s) = slack * V^*(s)
        v_slack=2,

        # In the transition-separation encoding, whether to use the incremental refinement approach
        use_incremental_refinement=False,

        # In the transition-separation encoding, whether to post constraints to ensure distinguishability of goals
        distinguish_goals=False,

        # In the transition-separation encoding, whether to post constraints to ensure distinguishability of goals
        # and transitions coming from different training instances
        cross_instance_constraints=True,

        # In the transition-separation encoding, whether to force any V-descending transition to be labeled as Good
        decreasing_transitions_must_be_good=False,

        # A function to create the FOL language, used to be able to parse the features.
        language_creator=programmatic_language_creator,

        # OTHERS:
        print_hstar_in_feature_matrix=False,
        initial_sample_size=0,
        # initial_sample_size=10,
        refinement_batch_size=2,
        # refinement_batch_size=20,
        seed=0,
        verbosity=0,
        # acyclicity='reachability',
        # acyclicity='topological',
        encodings_dir='~/Desktop/encodings_d2l',
        sampling_strategy='random',
        optimal_steps=3,
        consistency_bound=2,
        n_features=2,
        closed=True,
        solve=True,

        # New:
        expand_first_train_instance=False,
        provided_sample_file=None,
        maxsat_iter = 999,
    )

    parameters = {**defaults, **kwargs}  # Copy defaults, overwrite with user-specified parameters

    parameters['experiment_dir'] = os.path.join(parameters['workspace'], expid.replace(':', '_'))
    create_experiment_workspace(parameters["experiment_dir"], rm_if_existed=False)

    steps = generate_pipeline(**parameters)
    exp = parameters["experiment_class"](steps, parameters)

    # train_steps = generate_train(**parameters)
    # exp = generate_train(**parameters)
    return exp


def default_feature_namer(s):
    return str(s)


def rfts_names(feature):
    base = {
        'Forall(down,Exists(hv,Nominal(empty)))': 'if-below-exists-empty',
    }
    base.update({f'Exists(hv,Nominal({t}))': f'num-{t}s' for t in rfts.ALL_TOKENS})
    base.update({
        'Exists(hv,Nominal(star))': 'star-unreached',
        'Exists(hv,Nominal(agent))': 'agent-exists',
    })

    s = str(feature)
    return extend_namer_to_all_features(base).get(s, s)


def stf_names(feature):
    base = {f'Exists(hv,Nominal({t}))': f'cell-with-{t}' for t in stf.ALL_TOKENS}
    s = str(feature)
    return extend_namer_to_all_features(base).get(s, s)


def ec_names(feature):
    base = {f'Exists(hv,Nominal({t}))': f'cell-with-{t}' for t in ec.ALL_TOKENS}
    s = str(feature)
    return extend_namer_to_all_features(base).get(s, s)


def tpn_names(feature):
    base = {f'Exists(hv,Nominal({t}))': f'cell-with-{t}' for t in tpn.ALL_TOKENS}
    s = str(feature)
    return extend_namer_to_all_features(base).get(s, s)


def ct_names(feature):
    from generalization_grid_games_2.envs.checkmate_tactic import ALL_TOKENS
    base = {f'Exists(hv,Nominal({t}))': f'cell-with-{t}' for t in ALL_TOKENS}
    s = str(feature)
    return extend_namer_to_all_features(base).get(s, s)


def programmatic_language_creator(config):
    lang, _ = config.domain.generate_language()
    return lang