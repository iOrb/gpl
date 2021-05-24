import copy
import math

from sltp.util.misc import update_dict

from gpl.domains.grid_games.domain import Domain

from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import CELL_S, COL_S, ROW_S, D1_S, D2_S
from gpl.domains.grid_games.envs.nim import ONLY_ONE_LEFT


nim_params = Bunch({
    'domain_name': 'nim',
    'use_player_as_feature': True,
    'map_cells': True,
    'use_diagonals_for_map_cells': True,
    'use_adjacency': {CELL_S},
    'use_bidirectional': {CELL_S},
    'sorts_to_use': {CELL_S},
    'last_player_win': True,
    'unary_predicates': {},
    'predicates_arity_1': {},
    'mark_top_token': False,
    'mark_bottom_token': False,
    'game_version': 0,
})

def experiments():
    base = dict(
        domain=Domain(nim_params),
        maxsat_encoding="d2l",
        num_states="all",
        concept_generator=None,
        parameter_generator=None,
        v_slack=2,
        acyclicity='topological',
        use_incremental_refinement=False,
        max_concept_size=5,
        distance_feature_max_complexity=4,
        concept_generation_timeout=15000,
        cond_feature_max_complexity=0,
        comparison_features=True,
        generate_goal_concepts=True,
        print_denotations=True,
        print_hstar_in_feature_matrix=False,

        verbosity=2,
        initial_sample_size=50,
        refinement_batch_size=10,
        maxsat_iter=3,

        sampling_strategy='full',

        allow_bad_states=True,
        decreasing_transitions_must_be_good=False,
        allow_cycles=False,
        use_action_ids=False,
        use_weighted_tx=False,
        use_state_novelty=True,
        distinguish_goals=True,

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

    exps = dict()

    # version 1:
    # two piles
    nim_params_v1 = copy.deepcopy(nim_params)
    nim_params_v1.game_version = 0
    exps["1"] = update_dict(
        base,
        domain=Domain(nim_params_v1),
        instances=[11, 13],
        test_instances=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
    )

    # version 2:
    # 3 piles
    nim_params_v2 = copy.deepcopy(nim_params)
    nim_params_v2.game_version = 1
    nim_params_v2.mark_bottom_token = True
    nim_params_v2.mark_top_token = True
    exps["2"] = update_dict(
        exps["1"],
        domain=Domain(nim_params_v2),
        max_concept_size=8,
        instances=[0],
        test_instances=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    )

    # version 3:
    # 3 piles
    nim_params_v3 = copy.deepcopy(nim_params)
    nim_params_v3.game_version = 1
    exps["3"] = update_dict(
        exps["1"],
        domain=Domain(nim_params_v3),
        instances=[5],
        test_instances=[0, 1, 2, 3, 4, 5],
    )

    return exps




