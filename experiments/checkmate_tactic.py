import copy
import math
from sltp.util.misc import update_dict
from gpl.domains.grid_games.domain import Domain
from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import *
from gpl.domains.grid_games.envs.checkmate_tactic import \
    CHECKMATE, STALEMATE, N_MOVE, CHECK, BLACK_HAS_ACTION, WHITE_KING, WHITE_TOWER, BLACK_KING, WHITE, BLACK


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
    'use_distance_2': {COL_S, ROW_S, CELL_S},
    'use_distance_more_than_1': {COL_S, ROW_S, CELL_S},
    'use_bidirectional': {COL_S, ROW_S, CELL_S},
    'sorts_to_use': {COL_S, ROW_S, CELL_S},
    'n_moves': 70,
    'unary_predicates': {CHECKMATE, STALEMATE, CHECK, BLACK_HAS_ACTION},
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
    # using tower
    ct_params_v1 = copy.deepcopy(ct_params)
    ct_params_v1.game_version = 1
    exps["1"] = update_dict(
        base,
        domain=Domain(ct_params_v1),
        instances=[500],
        # test_instances=[0],
        allow_bad_states=True,
        test_instances=list(range(0, -1000, -1)),  # using negative keys for test instances
        # test_instances=[-1, -2, -3],
        feature_generator=debug_features_checkmate_tactic_rook(),
        validate_features=debug_validate_features(),
        # skip_train_steps=[0, 1, 2, 3],
    )

    exps["2"] = update_dict(
        exps["1"],
        instances=[0],
    )

    return exps


# % % % % % % % % %
#    FEATURES
# % % % % % % % % %

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
cell_h_c_att_by_w = CELL_HAS_COLOR_ATTAKED_BY(WHITE)
cell_h_c_att_by_b = CELL_HAS_COLOR_ATTAKED_BY(BLACK)
cell_h_c_att_by_wr = CELL_HAS_PIECE_ATTAKED_BY(WHITE_TOWER)
cell_h_c_att_by_wk = CELL_HAS_PIECE_ATTAKED_BY(WHITE_KING)
cell_h_c_att_by_bk = CELL_HAS_PIECE_ATTAKED_BY(BLACK_KING)
cell_is_in_top = CELL_IS_IN(TOP)
cell_is_in_right_most = CELL_IS_IN(RIGHT)
cell_is_in_left_most = CELL_IS_IN(LEFT)
cell_is_in_bottom = CELL_IS_IN(BOTTOM)
cell_h_c_bk_ava_q = CELL_IS_IN(BLACK_KING_AVAILABLE_QUADRANT)


Atom = lambda what: f'Atom[{what}]'
Num = lambda what: f'Num[{what}]'
Dist = lambda elem0, sep, elem1: f'Dist[{elem0};{sep};{elem1}]'
Bool = lambda what: f'Bool[{what}]'
Not = lambda what: f'Not({what})'
Exists = lambda sep, elem: f'Exists({sep},{elem})'
Forall = lambda sep, elem: f'Forall({sep},{elem})'
And = lambda elem0, elem1: f'And({elem0},{elem1})'
LessThan = lambda elem0, elem1: 'LessThan{' + elem0 + elem1 + '}'


def debug_features_checkmate_tactic_rook():
    return [
        Atom(CHECK),
        # Atom(CHECKMATE),
        # Atom('player-1'),
        # Atom(STALEMATE),
        # Atom(BLACK_HAS_ACTION),

        # Num(cell_h_c_bk_ava_q),
        # "Num[cell-has-black_attacked]",
        # "Num[cell-has-white_attacked]",
        # "Bool[And(col-has-black_king,col-has-white_king)]",
        # "Bool[And(col-has-black_king,col-has-white_rook)]",
        # "Bool[And(row-has-black_king,row-has-white_king)]",
        # "Bool[And(row-has-black_king,row-has-white_rook)]",

        # "Bool[And(cell-has-black_attacked,cell-has-white_rook)]",

        # Num(And(cell_h_c_att_by_b, cell_h_c_att_by_w)),
        # Bool(f"And({cell_h_c_att_by_w},{cell_h_bk})"),
        # Bool(f"And({cell_is_in_top},{cell_h_bk})"),
        # Bool(f"And({cell_is_in_bottom},{cell_h_bk})"),
        # Bool(f"And({cell_is_in_left_most},{cell_h_bk})"),
        # Bool(f"And({cell_is_in_right_most},{cell_h_bk})"),
        # Bool(f"And({col_h_wk},{col_h_wr})"),
        # Bool(f"And({row_h_wk},{row_h_wr})"),

        # Bool(f"And({cell_h_c_att_by_wr},{cell_is_in_top})"),
        # Bool(f"And({cell_h_c_att_by_wr},{cell_is_in_bottom})"),
        # Bool(f"And({cell_h_c_att_by_wr},{cell_is_in_right_most})"),
        # Bool(f"And({cell_h_c_att_by_wr},{cell_is_in_left_most})"),

        # Bool(And(cell_h_bk, cell_is_in_top)),
        # Bool(And(cell_h_bk, cell_is_in_bottom)),
        # Bool(And(cell_h_bk, cell_is_in_right_most)),
        # Bool(And(cell_h_bk, cell_is_in_left_most)),

        Bool(And(col_h_bk, col_h_wk)),
        Bool(And(col_h_bk, col_h_wr)),

        # "Bool[And(cell-has-white_attacked,cell-has-black_king)]",
        # "Num[And(Not(cell-has-black_attacked),cell-has-white_rook)]",
        # "Num[And(cell-has-white_attacked,cell-has-black_king)]",
        # "Num[And(Not(cell-has-white_attacked),cell-has-black_king)]",
        #
        # "Dist[row-has-black_king;adjacent_row;row-has-white_rook]",
        # "Dist[row-has-black_king;adjacent_row;row-has-white_king]",
        # "Dist[col-has-black_king;adjacent_col;col-has-white_rook]",
        # "Dist[col-has-black_king;adjacent_col;col-has-white_king]",
        # "Dist[cell-has-black_king;adjacent_cell;cell-has-white_rook]",

        # Dist(f"{cell_h_bk};{adj_cell};{cell_is_in_top}"),
        # Dist(f"{cell_h_bk};{adj_cell};{cell_is_in_bottom}"),
        # Dist(f"{cell_h_bk};{adj_cell};{cell_is_in_left_most}"),
        # Dist(f"{cell_h_bk};{adj_cell};{cell_is_in_right_most}"),

        Dist(row_h_bk, adj_row, row_h_wr),
        Dist(row_h_bk, adj_row, row_h_wk),
        # Dist(col_h_bk, adj_col, col_h_wr),
        # Dist(col_h_bk, adj_col, col_h_wk),
        # Dist(col_h_bk, adj_cell, col_h_wr),
        # Dist(col_h_bk, adj_cell, col_h_wk),

        # "Bool[And(col-has-black_king,Exists(distance_2_col,col-has-white_rook))]",
        # "Bool[And(col-has-black_king,Exists(distance_2_col,col-has-white_king))]",
        # "Bool[And(row-has-black_king,Exists(distance_2_row,col-has-white_rook))]",
        # "Bool[And(row-has-black_king,Exists(distance_2_row,row-has-white_king))]",
        # "Bool[And(cell-has-black_king,Exists(distance_2_cell,cell-has-white_king))]",
        # "Bool[And(cell-has-black_king,Exists(distance_2_cell,cell-has-white_rook))]",
        # Bool(And(row_h_bk, Exists(adj_row, row_h_wr))),
        # "Bool[And(row-has-black_king,Exists(adjacent_row,row-has-none))]",
        # "Bool[And(col-has-black_king,Exists(adjacent_col,col-has-white_rook))]",
        # "Bool[And(col-has-black_king,Exists(adjacent_col,col-has-none))]",
        Bool(And(cell_h_bk, Exists(adj_cell, cell_h_wr))),
        Bool(And(cell_h_wk, Exists(adj_cell, cell_h_wr))),
        # Bool(And(cell_h_c_att_by_w, Exists(adj_cell, cell_h_bk))),
        Bool(And(cell_h_bk, Exists(adj_cell, Not(cell_h_c_att_by_w)))),

        # Bool(And(row_h_bk, Exists(adj_row, row_h_wr))),
        # Bool(And(row_h_bk, Exists(adj_row, row_h_wk))),
        # Bool(And(col_h_bk, Exists(adj_col, col_h_wr))),
        # Bool(And(col_h_bk, Exists(adj_row, col_h_wk))),

        # Bool(f"And({cell_h_bk},Exists({adj_cell},{cell_h_wr}))"),

        # "Bool[And(cell-has-white_king,Exists(adjacent_cell,cell-has-white_rook))]",
        # "Bool[And(cell-has-black_attacked,Exists(adjacent_cell,cell-has-white_king))]",
        # "Num[And(cell-has-white_attacked,Exists(adjacent_cell,cell-has-black_king))]",
        #
        # "Num[And(cell-has-black_attacked,Exists(adjacent_cell,cell-has-white_rook))]",
        # "Num[And(Not(cell-has-black_attacked),Exists(adjacent_cell,cell-has-white_rook))]",
        # "Num[And(cell-has-white_attacked,Exists(adjacent_cell,cell-has-black_king))]",
        # "Num[And(Not(cell-has-white_attacked),Exists(adjacent_cell,cell-has-black_king))]",
        #
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