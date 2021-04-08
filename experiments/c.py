
from sltp.util.misc import update_dict

from domains.chess_.domain import Domain


DOMAIN_NAME = "chess"

def experiments():
    base = dict(
        domain=Domain(DOMAIN_NAME),

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
        instances=['v0',],
        test_instances=['v0',],

        max_concept_size=4,
        distance_feature_max_complexity=4,
        concept_generation_timeout=120,

        parameter_generator=None,
        # maxsat_timeout=5,
        maxsat_iter=2,

        # rollouts
        num_episodes=1,
        num_rollouts=4,
        rollout_depth=3,

        # expand_first_train_instance=True,
        # all_player1_possible_successors=True,
    )

    return exps



