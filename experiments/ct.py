
from generalization_grid_games.envs import checkmate_tactic as ct

from sltp.util.misc import update_dict

from domains.generalized_grid_games.checkmate_tactic.domain import Domain
from domains.generalized_grid_games.checkmate_tactic.teach_policies import expert_checkmate_tactic_policy

from instances.ct_instances import four_four_instances, all_instances, \
    break_instances

from gpl.defaults import ct_names

DOMAIN_NAME = "checkmate_tactic"

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
        maxsat_timeout=None,

        distinguish_goals=False,
        use_incremental_refinement=False,

    )

    exps = dict()

    exps["1"] = update_dict(
        base,
        # instances=four_four_instances([1, 2, 3, 5, 6, 8, 9]) +
        #           all_instances([15, 16, 18]) +
        #           break_instances('a'),
        # test_instances=four_four_instances('a') +
        #                all_instances('a') +
        #                break_instances('a'),

        instances=four_four_instances([0]),
        test_instances=four_four_instances('a') +
                       all_instances('a') +
                       break_instances('a'),

        teach_policies=None,

        max_concept_size=2,
        distance_feature_max_complexity=5,
        concept_generation_timeout=120,

        parameter_generator=None,

        # rollouts
        num_episodes=5,
        num_rollouts=10,
        rollout_depth=10,

        # new
        expand_first_train_instance=False,
    )

    exps["2"] = update_dict(
        base,
        # instances=four_four_instances([1, 2, 3, 5, 6, 8, 9]) +
        #           all_instances([15, 16, 18]) +
        #           break_instances('a'),
        # test_instances=four_four_instances('a') +
        #                all_instances('a') +
        #                break_instances('a'),

        instances=four_four_instances([0]),
        test_instances=four_four_instances('a') +
                       all_instances('a') +
                       break_instances('a'),

        teach_policies=None,

        max_concept_size=2,
        distance_feature_max_complexity=5,
        concept_generation_timeout=120,

        parameter_generator=None,

        # rollouts
        num_episodes=2,
        num_rollouts=10,
        rollout_depth=10,

        # new
        expand_first_train_instance=False,
    )

    return exps



