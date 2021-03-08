from lgp.defaults import stf_names
from sltp.util.misc import update_dict

from lgp.teach_policies import expert_stf_policy, general_stf_policy_fill_all, \
    general_stf_policy_0, general_stf_policy_1

from instances.stf_instances import all_instances,five_five_instances

def experiments():
    base = dict(
        domain="stop_the_fall",
        feature_namer=stf_names,
        maxsat_encoding="d2l",
        num_states="all",
        concept_generator=None,
        parameter_generator=None,
        v_slack=2,

        # concept_generation_timeout=120,  # in seconds
        maxsat_timeout=None,

        distinguish_goals=False,
        # distinguish_goals=True,
        use_incremental_refinement=False,
    )

    exps = dict()

    exps["1"] = update_dict(
        base,
        instances=all_instances([20, 23]),
        # instances=all_instances([17, 18, 19, 21, 20, 22]),
        test_instances=five_five_instances('a') + all_instances('a'),
        # test_instances=all_instances([2]),

        max_concept_size=4,
        distance_feature_max_complexity=4,

        policies=[general_stf_policy_0],

        policy_depth=1,

        parameter_generator=None,
        use_equivalence_classes=True,
        # use_feature_dominance=True,
    )

    exps["2"] = update_dict(
        base,
        instances=all_instances([20, 23]),
        # instances=all_instances([17, 18, 19, 21, 20, 22]),
        test_instances=five_five_instances('a') +
                       all_instances('a'),
        # test_instances=all_instances([2]),

        max_concept_size=4,
        distance_feature_max_complexity=4,

        policies=[general_stf_policy_0],

        policy_depth=1,

        parameter_generator=None,
        use_equivalence_classes=True,
        # use_feature_dominance=True,
    )

    return exps
