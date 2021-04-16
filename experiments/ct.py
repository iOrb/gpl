

from sltp.util.misc import update_dict

from domains.generalized_grid_games_2.checkmate_tactic.domain import Domain
# from domains.generalized_grid_games.checkmate_tactic.teach_policies import expert_checkmate_tactic_policy

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

        distinguish_goals=True,
        use_incremental_refinement=False,
    )

    exps = dict()

    exps["1"] = update_dict(
        base,
        instances=break_instances('a'),
        # instances=four_four_instances([1, 2, 3, 5, 6, 8, 9]) +
        #           all_instances([15, 16]) +
        #           break_instances('a'),
        test_instances=four_four_instances('a') +
                       all_instances('a') +
                       break_instances('a'),

        teach_policies=None,

        initial_sample_size=5,
        refinement_batch_size=10,
        verbosity=0,

        acyclicity='topological',
        # acyclicity='reachability',

        max_concept_size=5,
        distance_feature_max_complexity=5,
        concept_generation_timeout=120,

        parameter_generator=None,
        maxsat_iter=100,

        # rollouts
        # num_episodes=1,
        # num_rollouts=2,
        # rollout_depth=2,

        train_instances_to_expand=list(range(1000)),
    )

    exps["2"] = update_dict(
        base,
        instances=four_four_instances([1, 2, 3, 5, 6, 8, 9]) +
                  all_instances([15, 16]) +
                  break_instances('a'),
        test_instances=four_four_instances('a') +
                       all_instances('a') +
                       break_instances('a'),

        teach_policies=None,

        max_concept_size=5,
        distance_feature_max_complexity=5,
        concept_generation_timeout=120,

        parameter_generator=None,

        # rollouts
        num_episodes=1,
        num_rollouts=1,
        rollout_depth=1,

        expand_first_train_instance=False,
    )

    return exps



