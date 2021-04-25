

from sltp.util.misc import update_dict

from gpl.domains.generalized_grid_games_2.checkmate_tactic.domain import Domain
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
        instances=break_instances([0]),
        # instances=four_four_instances([1, 2, 3, 5, 6, 8, 9]) +
        #           break_instances('a') +
        #           all_instances([15, 16, 17]),
        # instances=break_instances('a'),
        test_instances=four_four_instances('a') +
                       break_instances('a') +
                       all_instances('a'),
        # test_instances=all_instances([16]),

        max_concept_size=5,
        distance_feature_max_complexity=5,
        concept_generation_timeout=15000,

        allow_bad_states=True,
        decreasing_transitions_must_be_good=True,
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

    exps["2"] = update_dict(
        exps["1"],
        instances=all_instances([16]),
        # instances=four_four_instances([1, 2, 3, 5, 6, 8, 9]) +
        #           break_instances('a') +
        #           all_instances([15, 16, 17]),
        # instances=break_instances('a'),
        test_instances=four_four_instances('a') +
                       # all_instances('a') +
                       break_instances('a'),

        max_concept_size=5,
        distance_feature_max_complexity=5,
        concept_generation_timeout=15000,

        allow_bad_states=False,
        decreasing_transitions_must_be_good=True,
        allow_cycles=False,

        # skip_train_steps=[0, 1, 2],  # do not generate features twice!
        skip_train_steps=[],
        distinguish_goals=True,

        train_instances_to_expand=list(range(1000)),
    )



    exps["3"] = update_dict(
        exps["1"],
        instances=four_four_instances('a'),
        # instances=four_four_instances('a') +
        #           all_instances([0, 1, 2, 3, 4, 15, 16, 17, 20, 22]) +
        #           break_instances('a'),
        # instances=four_four_instances([1, 2, 3, 5, 6, 8, 9]) +
        #           break_instances('a') +
        #           all_instances([15, 16, 17]),
        # instances=break_instances('a'),
        test_instances=four_four_instances('a') +
                       all_instances('a') +
                       break_instances('a'),

        max_concept_size=5,
        distance_feature_max_complexity=5,
        concept_generation_timeout=15000,

        allow_bad_states=True,
        decreasing_transitions_must_be_good=True,
        allow_cycles=False,

        # skip_train_steps=[0, 1, 2],  # do not generate features twice!
        skip_train_steps=[],
        distinguish_goals=True,

        # rollouts
        num_episodes=1,
        num_rollouts=5,
        rollout_depth=5,

        train_instances_to_expand=[],
        # train_instances_to_expand=list(range(1000)),
    )
    return exps




