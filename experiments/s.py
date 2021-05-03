

from sltp.util.misc import update_dict

from gpl.domains.shoot.domain import Domain

from instances.ct_instances import four_four_instances, all_instances, \
    break_instances


DOMAIN_NAME = "shoot"

DOMAIN_TYPE = 'adv'  # could be one of {'fond', 'adv'}

def experiments():
    base = dict(
        domain=Domain(DOMAIN_NAME),
        domain_type=DOMAIN_TYPE,

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
        discrete_action_space=True,

        use_incremental_refinement=False,
    )

    exps = dict()
    exps["1"] = update_dict(
        base,
        instances=four_four_instances([0]),
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
        cond_feature_max_complexity=0,
        comparison_features=True,
        generate_goal_concepts=True,
        print_denotations=True,
        print_hstar_in_feature_matrix=True,

        allow_bad_states=False,
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




