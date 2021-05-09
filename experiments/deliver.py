import math

from sltp.util.misc import update_dict


from gpl.domains.grid_games.domain import Domain

from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import CELL_S, COL_S, ROW_S

deliver_params = Bunch({
    'domain_name': 'deliver',
    'use_player_as_feature': False,
    'map_cells': True,
    'use_diagonals_for_map_cells': True,
    'use_adjacency': True,
    'sorts_to_use': {CELL_S, COL_S, ROW_S},
})

def experiments():
    base = dict(
        domain=Domain(deliver_params),
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
        # instances=[5,],
        instances=[0, 2, 3, 4, 5,],
        test_instances=[0, 2, 3, 4, 5, 6],
        max_concept_size=5,
        distance_feature_max_complexity=4,
        concept_generation_timeout=15000,
        cond_feature_max_complexity=0,
        comparison_features=False,
        generate_goal_concepts=True,
        print_denotations=True,
        print_hstar_in_feature_matrix=False,

        verbosity=1,
        initial_sample_size=10,
        refinement_batch_size=20,
        maxsat_iter=10,

        allow_bad_states=False,
        decreasing_transitions_must_be_good=False,
        allow_cycles=False,
        use_action_ids=True,
        use_weighted_tx=False,
        use_state_novelty=True,
        distinguish_goals=True,
        sampling_strategy="full",

        # skip_train_steps=[0, 1, 2],  # do not generate features twice!
        skip_train_steps=[],
        # rollouts
        # num_episodes=1,
        # num_rollouts=1,
        # rollout_depth=2,
        # train_instances_to_expand=[],
        train_instances_to_expand=list(range(1000)),
        max_states_expanded=math.inf,
    )

    return exps



