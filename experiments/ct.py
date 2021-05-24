import math
from sltp.util.misc import update_dict
from gpl.domains.grid_games.domain import Domain
from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import CELL_S, COL_S, ROW_S, D1_S, D2_S
from gpl.domains.grid_games.envs.checkmate_tactic import CHECKMATE, STALEMATE, N_MOVE, CHECK


ct_params = Bunch({
    'domain_name': 'checkmate_tactic',
    'use_player_as_feature': True,
    'map_cells': True,
    'use_diagonals_for_map_cells': True,
    'use_adjacency': {CELL_S},
    'use_bidirectional': {},
    'sorts_to_use': {COL_S, ROW_S, CELL_S},
    'n_moves': 1,
    'unary_predicates': {},
    # 'unary_predicates': {"{}_{}".format(N_MOVE, i) for i in range(CHECKMATE_IN_N + 1)},
    # 'unary_predicates': {STALEMATE, CHECKMATE}
    'game_version': 0,
})

def experiments():
    base = dict(
        domain=Domain(ct_params),
        maxsat_encoding="d2l",
        num_states="all",
        concept_generator=None,
        parameter_generator=None,
        v_slack=2,
        acyclicity='topological',
        discrete_action_space=False,
        use_incremental_refinement=False,

        max_concept_size=5,
        distance_feature_max_complexity=4,
        concept_generation_timeout=15000,
        cond_feature_max_complexity=0,
        comparison_features=False,
        generate_goal_concepts=False,
        print_denotations=True,
        print_hstar_in_feature_matrix=False,

        verbosity=0,
        initial_sample_size=20,
        refinement_batch_size=50,
        maxsat_iter=4,

        allow_bad_states=False,
        decreasing_transitions_must_be_good=False,
        allow_cycles=False,
        use_action_ids=False,
        use_weighted_tx=False,
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
        use_state_novelty=True,
    )

    # version 1:
    # checkmate in 1 move
    # using queen
    exps = dict()
    exps["1"] = update_dict(
        base,
        instances=list(range(50)) + [74, 76, 77, 79, 86, 50, 52, 118, 142, 147, 159, 169, 187, 200, 201, 202, 206, 208,
                                     221, 223, 233, 235, 242, 244, 78, 80, 81, 83, 90, 92, 96, 98, 327, 56, 222, 224,
                                     228, 230, 243, 245, 255, 257, 264, 266, 267, 269, 294, 296, 309, 311, 315],
        test_instances=list(range(2000)),
    )

    # version 2:
    # checkmate in 1 move
    # using tower
    ct_params.game_version = 1
    exps["2"] = update_dict(
        exps["1"],
    )

    # version 3:
    # checkmate in 1 move
    # using two bishops
    # ct_params.game_version = 1
    exps["3"] = update_dict(
        exps["1"],
    )

    return exps
