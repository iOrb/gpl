import copy
import math
from sltp.util.misc import update_dict
from gpl.domains.grid_games.domain import Domain
from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import CELL_S, COL_S, ROW_S, D1_S, D2_S
from gpl.domains.grid_games.envs.checkmate_tactic import CHECKMATE, STALEMATE, N_MOVE, CHECK


ct_params = Bunch({
    'domain_name': 'checkmate_tactic',
    'use_player_as_feature': True,
    'use_player_to_encode': True,
    'use_next_player_as_feature': False,
    'use_next_player_to_encode': False,
    'use_margin_as_feature': False,
    'objects_to_ignore': set(),
    'map_cells': True,
    'use_diagonals_for_map_cells': True,
    'use_adjacency': {COL_S, ROW_S},
    'use_distance_2': {COL_S, ROW_S},
    'use_distance_more_than_1': {COL_S, ROW_S},
    'use_bidirectional': {},
    'sorts_to_use': {COL_S, ROW_S},
    'n_moves': 1000,
    'unary_predicates': {},
    # 'unary_predicates': {"{}_{}".format(N_MOVE, i) for i in range(CHECKMATE_IN_N + 1)},
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

        verbosity=2,
        initial_sample_size=20,
        refinement_batch_size=50,
        maxsat_iter=4,

        allow_bad_states=False,
        decreasing_transitions_must_be_good=False,
        allow_cycles=False,
        use_action_ids=False,
        use_weighted_tx=True,
        distinguish_goals=True,
        sampling_strategy="full",

        # skip_train_steps=[0, 1, 2, 3],  # do not generate features twice!
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
    exps = dict()

    # version 1:
    # checkmate in 1 move
    # using queen
    ct_params_v1 = copy.deepcopy(ct_params)
    ct_params_v1.game_version = 1
    exps["1"] = update_dict(
        base,
        # instances=[1, 9, 11, 43, 45, 47, 48, 49, 50, 56, 57, 62, 63, 65, 68, 69, 71, 77, 78, 80, 81, 83, 89, 90, 93, 98,
        #            99, 15, 18, 19, 23, 24, 25, 26, 28, 30, 32, 82, 84, 101, 110, 111, 112, 113, 124, 125, 126, 128, 13, 35,
        #            52, 54, 58, 60, 64, 66, 70, 72, 73, 75, 85, 87, 95, 100, 102, 103, 106, 108, 115, 117, 225, 228, 236,
        #            239, 240, 243, 257, 260, 265, 268, 284, 296, 301, 315, 319, 327, 348, 351, 358, 360, 361, 362,
        #            403, 405, 406, 408, 415, 417],
        # test_instances=list(range(500)),
        instances=[0],
        test_instances=list(range(100)),
    )

    # version 2:
    # checkmate in 1 move
    # using tower
    ct_params_v1 = copy.deepcopy(ct_params)
    ct_params_v1.game_version = 1
    exps["2"] = update_dict(
        exps["1"],
        domain=Domain(ct_params_v1),
        instances=[0, 97],
        # test_instances=[0],
        max_concept_size=7,
        test_instances=list(range(100)),
        allow_bad_states=False,
    )

    # version 3:
    # checkmate in 1 move
    # using tower, and predicate checkmate
    ct_params_v3 = copy.deepcopy(ct_params)
    ct_params_v3.game_version = 1
    ct_params_v3.unary_predicates = {CHECKMATE}
    exps["3"] = update_dict(
        exps["1"],
        domain=Domain(ct_params_v3),
        instances=[22, 29],
        # test_instances=[0],
        test_instances=list(range(100)),
        allow_bad_states=False,
        feature_generator=debug_features_checkmate_tactic_rook,
    )

    # version 4:
    # checkmate in 1 move
    # using tower, and predicate checkmate
    ct_params_v4 = copy.deepcopy(ct_params)
    ct_params_v4.game_version = 1
    ct_params_v4.unary_predicates = {CHECKMATE}
    exps["4"] = update_dict(
        exps["1"],
        domain=Domain(ct_params_v4),
        instances=[31],
        # test_instances=[0],
        test_instances=list(range(100)),
        allow_bad_states=False,
        max_concept_size=5,
        feature_generator=debug_features_checkmate_tactic_rook,
    )

    return exps


def debug_features_checkmate_tactic_rook(lang):
    checkmate = a = "Atom[checkmate]"
    same_col_bk_wk = b = "Bool[And(col-has-black_king,col-has-white_king)]"
    same_row_bk_wk = c = "Bool[And(row-has-black_king,row-has-white_king)]"
    distance_row_bk_wr = d = "Dist[row-has-black_king;adjacent_row;row-has-white_rook]"
    distance_col_bk_wr = e = "Dist[col-has-black_king;adjacent_col;col-has-white_rook]"
    distance_2_col_bk_wr = f = "Bool[And(col-has-black_king,Exists(distance_2_col,col-has-white_rook))]"
    distance_2_col_bk_wk = g = "Bool[And(col-has-black_king,Exists(distance_2_col,col-has-white_king))]"
    distance_2_row_bk_wr = h = "Bool[And(row-has-black_king,Exists(distance_2_row,col-has-white_rook))]"
    distance_2_row_bk_wk = i = "Bool[And(row-has-black_king,Exists(distance_2_row,row-has-white_king))]"
    return [a, b, c, d, e, f, g, h, i]