from lgp.defaults import tpn_names
from sltp.util.misc import update_dict

from lgp.teach_policies import expert_nim_policy
from instances.tpn_instances import all_instances


def experiments():
    base = dict(
        domain="two_pile_nim",
        feature_namer=tpn_names,
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
        # instances=all_instances([2, 3]),
        instances=all_instances([2, 3, 6, 11, 13, 15, 16]),
        # instances=all_instances([7]),
        # instances=all_instances('a'),
        test_instances=all_instances('a'),

        policies=None,

        policy_depth=1,

        max_concept_size=5,
        distance_feature_max_complexity=5,

        parameter_generator=None,
        use_equivalence_classes=True,
        # use_feature_dominance=True,
    )

    exps["2"] = update_dict(
        base,
        instances=all_instances([2, 3, 5]),
        # instances=all_instances([6, 15, 16]),
        # instances=all_instances([7]),
        # instances=all_instances('a'),
        test_instances=all_instances(list(range(22))),

        policies=None,

        policy_depth=1,

        max_concept_size=5,
        distance_feature_max_complexity=5,

        parameter_generator=None,
        use_equivalence_classes=True,
        # use_feature_dominance=True,
    )

    return exps
