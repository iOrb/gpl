import math

from sltp.util.misc import update_dict
from gpl.domains.grid_games.domain import Domain
from domain_params import pick_package_params

def experiments():
    base = dict(
        domain=Domain(pick_package_params),
        maxsat_encoding="d2l",
        num_states="all",
        concept_generator=None,
        parameter_generator=None,
        v_slack=2,
        acyclicity='topological',
        use_incremental_refinement=False,
    )

    exps = dict()
    exps["1"] = update_dict(
        base,
        instances=[0, 1, 2],
        # instances=[0, 1, 2, 3],
        test_instances=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        max_concept_size=5,
        distance_feature_max_complexity=4,
        concept_generation_timeout=15000,
        cond_feature_max_complexity=0,
        comparison_features=False,
        generate_goal_concepts=False,
        print_denotations=True,
        print_hstar_in_feature_matrix=False,

        verbosity=1,
        initial_sample_size=10,
        refinement_batch_size=50,
        maxsat_iter=10,

        allow_bad_states=False,
        decreasing_transitions_must_be_good=False,
        allow_cycles=False,
        use_action_ids=True,
        use_weighted_tx=False,
        use_state_novelty=True,

        sampling_strategy="full",

        # skip_train_steps=[0, 1, 2],  # do not generate features twice!
        skip_train_steps=[],
        distinguish_goals=True,
        # rollouts
        # num_episodes=1,
        # num_rollouts=10,
        # rollout_depth=10,
        # train_instances_to_expand=[],
        train_instances_to_expand=list(range(1000)),
        max_states_expanded=math.inf,
    )

    return exps



