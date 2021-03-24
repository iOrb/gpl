
from generalization_grid_games.envs import checkmate_tactic as ct

from sltp.util.misc import update_dict

from domains.generalized_grid_games.checkmate_tactic.domain import Domain
from domains.generalized_grid_games.checkmate_tactic.teach_policies import expert_checkmate_tactic_policy

from .instances.ct_instances import four_four_instances, all_instances, \
    break_instances

from gpl.defaults import ct_names

DOMAIN_NAME = "checkmate_tactic"

def get_config(id):
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

        # new
        epochs=2,
        num_rollouts=1,
        rollout_depth=5,
    )

    exps = dict()
    exps[1] = update_dict(
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

    return exps[id]
