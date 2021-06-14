import copy
import math
from sltp.util.misc import update_dict
from gpl.domains.grid_games.domain import Domain
from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import CELL_S, COL_S, ROW_S, D1_S, D2_S
from gpl.domains.grid_games.envs.checkmate_tactic import CHECKMATE, STALEMATE, N_MOVE, CHECK, BLACK_HAS_ACTION


ct_params = Bunch({
    'domain_name': 'checkmate_tactic',
    'use_player_as_feature': True,
    'use_player_to_encode': True,
    'use_next_player_as_feature': False,
    'use_next_player_to_encode': False,
    'use_margin_as_feature': False,
    'use_verbose_margin_as_feature': False,
    'objects_to_ignore': set(),
    'map_cells': True,
    'use_diagonals_for_map_cells': True,
    'use_adjacency': {COL_S, ROW_S, CELL_S},
    'use_distance_2': {},
    'use_distance_more_than_1': {},
    'use_bidirectional': {},
    'sorts_to_use': {COL_S, ROW_S, CELL_S},
    'n_moves': 1000,
    'unary_predicates': {},
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
        use_weighted_tx=False,
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
    ct_params_v1.game_version = 0
    ct_params_v1.unary_predicates = {CHECKMATE, STALEMATE, CHECK, BLACK_HAS_ACTION}
    exps["1"] = update_dict(
        base,
        domain=Domain(ct_params_v1),
        instances=[103],
        # instances=[160],
        # test_instances=[0],
        test_instances=list(range(100, 200)),
        allow_bad_states=False,
        max_concept_size=5,
        # feature_generator=debug_features_checkmate_tactic_queen(),
        # validate_features=debug_validate_features(),
        skip_train_steps=[],
    )

    # version 2:
    # checkmate in 1 move
    # using tower
    ct_params_v2 = copy.deepcopy(ct_params)
    ct_params_v2.game_version = 1
    exps["2"] = update_dict(
        exps["1"],
        domain=Domain(ct_params_v2),
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
        instances=[22,],
        # test_instances=[0],
        test_instances=list(range(50000)),
        allow_bad_states=False,
        # feature_generator=debug_features_checkmate_tactic_rook,
    )

    # version 4:
    # checkmate in 1 move
    # using tower, and predicate checkmate
    ct_params_v4 = copy.deepcopy(ct_params)
    ct_params_v4.game_version = 1
    ct_params_v4.unary_predicates = {CHECK, BLACK_HAS_ACTION}
    exps["4"] = update_dict(
        exps["1"],
        domain=Domain(ct_params_v4),
        instances=[40, 12, 17],
        # instances=[160],
        # test_instances=[0],
        test_instances=list(range(50000)),
        allow_bad_states=True,
        max_concept_size=5,
        feature_generator=debug_features_checkmate_tactic_rook(),
        validate_features=debug_validate_features(),
        skip_train_steps=[],
    )

    # version 5:
    # checkmate in 1 move
    # using tower, and predicate checkmate
    exps["5"] = update_dict(
        exps["4"],
        instances=[300, 6, 60, 69],
    )

    # version 6:
    # checkmate in 1 move
    # using tower, and predicate checkmate
    exps["6"] = update_dict(
        exps["4"],
        instances=[1100],
    )

    # version 6:
    # checkmate in 1 move
    # using tower, and predicate checkmate
    exps["7"] = update_dict(
        exps["4"],
        instances=[200, 0, 32, 45, 500],
    )

    return exps


col_h_wk = 'col-has-white_king'
col_h_wr = 'col-has-white_rook'
col_h_bk = 'col-has-black_king'
row_h_wk = 'row-has-white_king'
row_h_wr = 'row-has-white_rook'
row_h_bk = 'row-has-black_king'
cell_h_wk = 'cell-has-white_king'
cell_h_wr = 'cell-has-white_rook'
cell_h_bk = 'cell-has-black_king'
adj_cell = 'adjacent_cell'
adj_col = 'adjacent_col'
adj_row = 'adjacent_row'

def debug_features_checkmate_tactic_rook():
    return [
        # "Atom[checkmate]",
        "Atom[check]",
        # "Atom[player-1]",
        # "Atom[stalemate]",
        f'Atom[{BLACK_HAS_ACTION}]',

        # "Num[cell-has-black_attacked]",
        # "Num[cell-has-white_attacked]",
        # "Bool[And(col-has-black_king,col-has-white_king)]",
        # "Bool[And(col-has-black_king,col-has-white_rook)]",
        # "Bool[And(row-has-black_king,row-has-white_king)]",
        # "Bool[And(row-has-black_king,row-has-white_rook)]",
        # "Bool[And(row-has-black_king,row-has-white_rook)]",
        # "Bool[And(row-has-black_king,row-has-white_rook)]",

        # "Bool[And(cell-has-black_attacked,cell-has-white_rook)]",
        # "Num[And(cell-has-black_attacked,cell-has-white_attacked)]",
        # "Bool[And(cell-has-white_attacked,cell-has-black_king)]",
        # "Num[And(Not(cell-has-black_attacked),cell-has-white_rook)]",
        # "Num[And(cell-has-white_attacked,cell-has-black_king)]",
        # "Num[And(Not(cell-has-white_attacked),cell-has-black_king)]",

        # "Dist[row-has-black_king;adjacent_row;row-has-white_rook]",
        # "Dist[row-has-black_king;adjacent_row;row-has-white_king]",
        # "Dist[col-has-black_king;adjacent_col;col-has-white_rook]",
        # "Dist[col-has-black_king;adjacent_col;col-has-white_king]",
        # "Dist[cell-has-black_king;adjacent_cell;cell-has-white_rook]",
        # "Bool[And(col-has-black_king,Exists(distance_2_col,col-has-white_rook))]",
        # "Bool[And(col-has-black_king,Exists(distance_2_col,col-has-white_king))]",
        # "Bool[And(row-has-black_king,Exists(distance_2_row,col-has-white_rook))]",
        # "Bool[And(row-has-black_king,Exists(distance_2_row,row-has-white_king))]",
        # "Bool[And(cell-has-black_king,Exists(distance_2_cell,cell-has-white_king))]",
        # "Bool[And(cell-has-black_king,Exists(distance_2_cell,cell-has-white_rook))]",
        # "Bool[And(row-has-black_king,Exists(adjacent_row,row-has-white_rook))]",
        # "Bool[And(row-has-black_king,Exists(adjacent_row,row-has-none))]",
        # "Bool[And(col-has-black_king,Exists(adjacent_col,col-has-white_rook))]",
        # "Bool[And(col-has-black_king,Exists(adjacent_col,col-has-none))]",
        # f"Bool[And({cell_h_wk},Exists({adj_cell},{cell_h_bk}))]",
        # f"Bool[And({cell_h_bk},Exists({adj_cell},{cell_h_wr}))]",
        # f"Bool[And({cell_h_wk},Exists({adj_cell},{cell_h_wr}))]",
        # "Bool[And(cell-has-white_king,Exists(adjacent_cell,cell-has-white_rook))]",
        # "Bool[And(cell-has-black_attacked,Exists(adjacent_cell,cell-has-white_king))]",
        # "Num[And(cell-has-white_attacked,Exists(adjacent_cell,cell-has-black_king))]",

        # "Num[And(cell-has-black_attacked,Exists(adjacent_cell,cell-has-white_rook))]",
        # "Num[And(Not(cell-has-black_attacked),Exists(adjacent_cell,cell-has-white_rook))]",
        # "Num[And(cell-has-white_attacked,Exists(adjacent_cell,cell-has-black_king))]",
        # "Num[And(Not(cell-has-white_attacked),Exists(adjacent_cell,cell-has-black_king))]",

        # "Num[Forall(adjacent_col,col-has-white_rook)]",
        # "Num[Forall(adjacent_col,col-has-white_king)]",
        # "Num[Forall(adjacent_col,col-has-black_king)]",
        # "Num[Forall(adjacent_row,row-has-white_rook)]",
        # "Num[Forall(adjacent_row,row-has-white_king)]",
        # "Num[Forall(adjacent_row,row-has-black_king)]",
        # "Num[Forall(adjacent_cell,cell-has-white_rook)]",
        # "Num[Forall(adjacent_cell,cell-has-white_rook)]",
        # "Num[Forall(adjacent_cell,cell-has-white_rook)]",
    ]

def debug_features_checkmate_tactic_queen():
    features = list()
    for s in debug_features_checkmate_tactic_rook():
        features.append(s.replace("rook", "queen"))
    return features

def debug_validate_features():
    return list(range(len(debug_features_checkmate_tactic_rook())))