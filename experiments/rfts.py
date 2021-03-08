import random

from lgp.defaults import rfts_names
from lgp.teach_policies import expert_rfts_policy, expert_rfts_policy_original, \
    general_policy_rfts_cell_bunch, general_policy_rfts_single_cell_deterministic, \
    general_policy_rfts_single_cell_random, expert_rfts_policy_two_stairs_bunch, \
    build_and_advance_rfts_policy, expert_rfts_policy_two_stairs_deterministic, \
    climb_the_pilar_rfts_policy_deterministic_0, climb_the_pilar_rfts_policy_deterministic_1, \
    climb_the_pilar_rfts_policy_random_0, climb_the_pilar_rfts_policy_random_1
    # climb_from_down_policy_random
    # climb_from_down_policy_deterministic

from sltp.util.misc import update_dict

from instances.rfts_instances import \
    six_x_six_instances, four_five_instances, \
    three_four_instances, all_instances, \
    original_instances, five_five_instances, \
    climb_from_left, climb_from_right, \
    climb_the_pilar_instances, climb_the_pilar_tiny_instances

# TEST_INSTANCES = three_four_instances('a') + four_five_instances('a') + \
#                  five_five_instances('a') + six_x_six_instances('a') + \
#                  climb_from_left('a') + \
#                  climb_from_right('a') + \
#                  original_instances(list(range(3)) + list(range(18, 20))) + \
#                  all_instances(list(range(7)) + list(range(31, 62)))

TEST_INSTANCES = three_four_instances('a') + four_five_instances('a') + \
                 five_five_instances('a') + six_x_six_instances('a') + \
                 climb_from_left('a') + \
                 climb_from_right('a') + \
                 original_instances('a') + \
                 all_instances('a') + \
                 climb_the_pilar_tiny_instances('a') + \
                 climb_the_pilar_instances('a')



def experiments():

    base = dict(
        domain="reach_for_the_star",
        feature_namer=rfts_names,
        maxsat_encoding="d2l",
        num_states="all",
        concept_generator=None,
        parameter_generator=None,
        v_slack=2,

        # concept_generation_timeout=120,  # in seconds
        maxsat_timeout=None,

        # distinguish_goals=True,
        distinguish_goals=False,
        use_incremental_refinement=False,
    )

    exps = dict()

    exps["one"] = update_dict(
        base,
        instances=["reach_for_the_star/layout_3x3_1.json"],
        test_instances=["reach_for_the_star/layout_3x3_1.json"],

        policies=[expert_rfts_policy],

        concept_generation_timeout=120,
        maxsat_timeout=120,

        max_concept_size=5,
        distance_feature_max_complexity=5,
        parameter_generator=None,
        use_equivalence_classes=True,
        # use_feature_dominance=True,
        # use_incremental_refinement=True
    )

    exps["test1"] = update_dict(
        base,
        instances=climb_the_pilar_instances('a'),
        test_instances=TEST_INSTANCES,

        policies=[climb_the_pilar_rfts_policy_random_0],

        concept_generation_timeout=300,
        maxsat_timeout=300,

        policy_depth=1,

        max_concept_size=5,
        distance_feature_max_complexity=5,
        parameter_generator=None,
        use_equivalence_classes=True,
    )

    exps["2"] = update_dict(
        base,
        instances=climb_the_pilar_tiny_instances('a'),
        test_instances=TEST_INSTANCES,

        policies=[climb_the_pilar_rfts_policy_random_0],

        concept_generation_timeout=300,
        maxsat_timeout=300,

        policy_depth=2,

        max_concept_size=5,
        distance_feature_max_complexity=5,
        parameter_generator=None,
        use_equivalence_classes=True,
    )

    exps["test2"] = update_dict(
        base,
        instances=climb_the_pilar_instances('a'),
        test_instances=TEST_INSTANCES,

        policies=[climb_the_pilar_rfts_policy_random_1],

        concept_generation_timeout=300,
        maxsat_timeout=300,

        policy_depth=1,

        max_concept_size=5,
        distance_feature_max_complexity=5,
        parameter_generator=None,
        use_equivalence_classes=True,
    )

    exps["test3"] = update_dict(
        base,
        # instances=climb_from_left([0]),
        instances=climb_the_pilar_tiny_instances('a'),
        test_instances=TEST_INSTANCES,

        policies=[climb_the_pilar_rfts_policy_deterministic_0],

        concept_generation_timeout=300,
        maxsat_timeout=300,

        policy_depth=1,

        max_concept_size=5,
        distance_feature_max_complexity=5,
        parameter_generator=None,
        use_equivalence_classes=True,
    )

    return exps

