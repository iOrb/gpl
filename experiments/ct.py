
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

        distinguish_goals=True,
        use_incremental_refinement=False,

    )

    exps = dict()
    exps["1"] = update_dict(
        base,
        instances=four_four_instances([1, 2, 3, 5, 6, 8, 9]) +
                  all_instances([15, 16, 18]) +
                  break_instances('a'),
        test_instances=four_four_instances('a') +
                       all_instances('a') +
                       break_instances('a'),

        teach_policies=[expert_checkmate_tactic_policy],

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policy_depth=1,

        parameter_generator=None,
    )

    exps["2"] = update_dict(
        base,
        instances=four_four_instances('a') +
                  all_instances([15, 16, 17]) +
                  break_instances('a'),
        test_instances=four_four_instances('a') +
                       all_instances('a') +
                       break_instances('a'),

        teach_policies=[expert_checkmate_tactic_policy],

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policy_depth=1,

        parameter_generator=None,
    )

    exps["2."] = update_dict(
        base,
        instances=four_four_instances([1, 2, 3, 6, 8]),
        test_instances=four_four_instances('a') + all_instances('a'),

        policies=[expert_checkmate_tactic_policy],

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policy_depth=1,

        parameter_generator=None,
        use_equivalence_classes=True,
        # use_feature_dominance=True,
    )# 80%

    exps["3"] = update_dict(
        base,
        instances=four_four_instances([1, 2, 3, 6, 8]) + all_instances([15, 16]),
        test_instances=four_four_instances('a') + all_instances('a'),

        policies=[expert_checkmate_tactic_policy],

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policy_depth=1,

        parameter_generator=None,
        use_equivalence_classes=True,
    ) # 90%

    exps["4"] = update_dict(
        base,
        instances=four_four_instances([1, 2, 3, 6, 8]) + all_instances([16]),
        test_instances=four_four_instances('a') + all_instances('a'),

        policies=[expert_checkmate_tactic_policy],

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policy_depth=1,

        parameter_generator=None,
        use_equivalence_classes=True,
    ) # 100%

    exps["5"] = update_dict(
        base,
        instances=four_four_instances([1,]),
        # instances=four_four_instances([1, 2]) + all_instances([16]),
        test_instances=four_four_instances('a') + all_instances('a'),

        policies=[expert_checkmate_tactic_policy],

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policy_depth=1,

        parameter_generator=None,
        use_equivalence_classes=True,
    ) # 100%

    exps["6"] = update_dict(
        base,
        instances=four_four_instances([1]) + all_instances([16]),
        test_instances=four_four_instances('a') + all_instances('a'),

        policies=[expert_checkmate_tactic_policy],

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policy_depth=1,

        parameter_generator=None,
        use_equivalence_classes=True,
    ) # 60%

    exps["7"] = update_dict(
        base,
        instances=four_four_instances([1]),
        test_instances=four_four_instances('a') + all_instances('a'),

        policies=[expert_checkmate_tactic_policy],

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policy_depth=1,

        parameter_generator=None,
        use_equivalence_classes=True,
    ) # 42.42%

    exps["8"] = update_dict(
        base,
        instances=four_four_instances([1, 2, 3]),
        test_instances=four_four_instances('a') + all_instances('a'),

        policies=[expert_checkmate_tactic_policy],

        max_concept_size=5,
        distance_feature_max_complexity=5,

        policy_depth=1,

        parameter_generator=None,
        use_equivalence_classes=True,
    ) # 93.94%

    return exps



