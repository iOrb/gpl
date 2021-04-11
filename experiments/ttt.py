
from generalization_grid_games.envs import checkmate_tactic as ct

from sltp.util.misc import update_dict

from domains.tictactoe.domain import Domain

from instances.ct_instances import four_four_instances, all_instances, \
    break_instances

from gpl.defaults import ct_names

DOMAIN_NAME = "tictactoe"

def experiments():
    base = dict(
        domain=Domain(DOMAIN_NAME),

        feature_namer=ct_names,
        maxsat_encoding="d2l",
        num_states="all",
        concept_generator=None,
        parameter_generator=None,
        v_slack=2,

        # concept_generation_timeout=120,  # in seconds
        # maxsat_timeout=None,

        distinguish_goals=True,
        use_incremental_refinement=False,
    )

    exps = dict()

    exps["1"] = update_dict(
        base,
        instances=['v0',],
        # test_instances=['v0', 'v1', 'v2', 'v3', 'v4', 'v5'],
        test_instances = ['v0'],

        max_concept_size=4,
        distance_feature_max_complexity=4,

        # concept_generation_timeout=120,
        # maxsat_timeout=1,
        maxsat_iter=6,

        parameter_generator=None,

        # rollouts
        num_episodes=1,
        num_rollouts=10,
        rollout_depth=10,

        expand_first_train_instance=True,
        # all_possible_successors=True,
    )

    return exps



