import random

from lgp.defaults import ec_names
from sltp.util.misc import update_dict

from lgp.teach_policies import expert_ec_policy, expert_ec_policy_original, \
    fill_agent_column_ec_policy

from instances.ec_instances import bunch_instances, six_seven_instances, \
    nine_ten_instances, nine_nine_instances, \
    eight_nine_instances, all_eight_nine_instances, \
    all_seven_eight_instances, all_six_seven_instances, \
    all_five_six_instances, all_four_five_instances, \
    all_four_six_instances, all_five_five_instances,\
    break_point_instances

TEST_INSTACES = bunch_instances('a') + six_seven_instances('a') + \
    nine_ten_instances('a') + nine_nine_instances('a') + \
    eight_nine_instances('a') + all_eight_nine_instances('a') + \
    all_seven_eight_instances('a') + all_six_seven_instances('a') + \
    all_five_six_instances('a') + all_four_five_instances('a') + \
    all_four_six_instances('a') + all_five_five_instances('a') + \
    break_point_instances('a')

def experiments():
    base = dict(
        domain="chase",
        feature_namer=ec_names,
        maxsat_encoding="d2l",
        num_states="all",
        concept_generator=None,
        parameter_generator=None,
        v_slack=2,

        # concept_generation_timeout=120,  # in seconds
        maxsat_timeout=None,

        distinguish_goals=False,
        # use_incremental_refinement=False,
    )

    exps = dict()

    exps["1"] = update_dict(
        base,
        instances=all_four_six_instances('a') +
                  six_seven_instances([61, 62, 63, 64]),
        test_instances=TEST_INSTACES,

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policies=[expert_ec_policy_original,],

        policy_depth=1,

        # concept_generation_timeout=600,  # in seconds
        maxsat_timeout=10000,

        parameter_generator=None,
        use_equivalence_classes=True,
    )

    exps["2"] = update_dict(
        base,
        # instances=all_four_six_instances('a') +
        #           six_seven_instances([61, 62, 63, 64]),
        instances=all_four_six_instances([0, 2, 4, 5]),
        test_instances=TEST_INSTACES,

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policies=[expert_ec_policy_original,],

        policy_depth=2,

        # concept_generation_timeout=600,  # in seconds
        maxsat_timeout=10000,

        parameter_generator=None,
        use_equivalence_classes=True,
    )

    exps["3"] = update_dict(
        base,
        instances=all_four_six_instances('a'),
        # instances=all_four_five_instances([1]) + six_seven_instances([3]),
        test_instances=TEST_INSTACES,

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policies=[expert_ec_policy_original,],

        policy_depth=1,

        # concept_generation_timeout=600,  # in seconds
        maxsat_timeout=10000,

        parameter_generator=None,
        use_equivalence_classes=True,
    )

    exps["4"] = update_dict(
        base,
        instances=six_seven_instances([61, 62, 63, 64]),
        test_instances=TEST_INSTACES,

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policies=[expert_ec_policy_original,],

        policy_depth=1,

        # concept_generation_timeout=600,  # in seconds
        maxsat_timeout=10000,

        parameter_generator=None,
        use_equivalence_classes=True,
    )

    return exps

