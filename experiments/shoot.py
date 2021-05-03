
from sltp.util.misc import update_dict

from gpl.domains.fond_grid_games.domain import Domain

DOMAIN_NAME = "shoot"

def experiments():
    base = dict(
        domain=Domain(DOMAIN_NAME),
        maxsat_encoding="d2l",
        num_states="all",
        concept_generator=None,
        parameter_generator=None,
        v_slack=2,
        acyclicity='topological',
        discrete_action_space=False,
        use_incremental_refinement=False,
    )

    exps = dict()
    exps["1"] = update_dict(
        base,
        instances=[6, 7],
        test_instances=[0, 1, 2, 3, 4, 5, 6, 7],
        max_concept_size=2,
        distance_feature_max_complexity=4,
        concept_generation_timeout=15000,
        cond_feature_max_complexity=0,
        comparison_features=False,
        generate_goal_concepts=False,
        print_denotations=True,
        print_hstar_in_feature_matrix=False,

        verbosity=1,
        initial_sample_size=50,
        refinement_batch_size=10,
        maxsat_iter=3,

        allow_bad_states=False,
        decreasing_transitions_must_be_good=False,
        allow_cycles=False,
        use_action_ids=True,

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




