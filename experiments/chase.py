

from sltp.util.misc import update_dict

from gpl.domains.fond_grid_games.chase.domain import Domain

from instances.ct_instances import four_four_instances, all_instances, \
    break_instances


DOMAIN_NAME = "chase"

def experiments():
    base = dict(
        domain=Domain(DOMAIN_NAME),
        maxsat_encoding="d2l",
        num_states="all",
        concept_generator=None,
        parameter_generator=None,
        v_slack=2,
        maxsat_iter=1,
        teach_policies=None,
        initial_sample_size=1,
        refinement_batch_size=1,
        verbosity=1,
        acyclicity='topological',
        discrete_action_space=False,
        use_incremental_refinement=False,
    )

    exps = dict()

    exps["1"] = update_dict(
        base,
        instances=four_four_instances([0, 2, 4]),
        # instances=four_four_instances([1, 2, 3, 5, 6, 8, 9]) +
        #           break_instances('a') +
        #           all_instances([15, 16, 17]),
        # test_instances=four_four_instances([0]),
        test_instances=four_four_instances('a') +
                       break_instances('a') +
                       all_instances('a'),
        # test_instances=all_instances([16]),
        max_concept_size=5,
        distance_feature_max_complexity=5,
        concept_generation_timeout=15000,
        allow_bad_states=False,
        decreasing_transitions_must_be_good=False,
        allow_cycles=True,
        # skip_train_steps=[0, 1, 2],  # do not generate features twice!
        skip_train_steps=[],
        distinguish_goals=True,
        # rollouts
        # num_episodes=1,
        # num_rollouts=1,
        # rollout_depth=2,
        # train_instances_to_expand=[],
        train_instances_to_expand=list(range(1000)),
    )

    exps["2"] = update_dict(
        base,
        instances=all_instances([15]),
        # instances=four_four_instances([1, 2, 3, 5, 6, 8, 9]) +
        #           break_instances('a') +
        #           all_instances([15, 16, 17]),
        # test_instances=four_four_instances([0]),
        test_instances=four_four_instances('a') +
                       break_instances('a') +
                       all_instances('a'),
        # test_instances=all_instances([16]),
        max_concept_size=5,
        distance_feature_max_complexity=5,
        concept_generation_timeout=15000,
        allow_bad_states=True,
        decreasing_transitions_must_be_good=False,
        allow_cycles=False,
        # skip_train_steps=[0, 1, 2],  # do not generate features twice!
        skip_train_steps=[],
        distinguish_goals=True,
        # rollouts
        # num_episodes=1,
        # num_rollouts=1,
        # rollout_depth=2,
        # train_instances_to_expand=[],
        train_instances_to_expand=list(range(1000)),
    )

    return exps




