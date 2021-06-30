import copy
import itertools
import math
from sltp.util.misc import update_dict
from gpl.domains.grid_games.domain import Domain
from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import *
from gpl.domains.grid_games.envs.checkmate_tactic import \
    CHECKMATE, STALEMATE, CHECK, BLACK_HAS_ACTION, WHITE_KING, BLACK_KING, \
    WHITE, BLACK, QUEEN_ATTACKED_WHITOUT_PROTECTION, WHITE_QUEEN, \
    BLACK_KING_CLOSED_IN_EDGE_BY_WHITE_QUEEN, \
    WHITE_QUEEN_AND_BLACK_KING_IN_ADJACENT_EDGE, BLACK_KING_IN_CORNER, \
    WHITE_QUEEN_AND_WHITE_KING_IN_ADJACENT_EDGE, \
    WHITE_QUEEN_AND_WHITE_KING_IN_SAME_EDGE, \
    WHITE_QUEEN_AND_BLACK_KING_IN_SAME_EDGE, \
    BLACK_KING_AND_WHITE_KING_IN_SAME_EDGE, \
    WHITE_QUEEN_IN_EDGE, WHITE_KING_IN_EDGE, BLACK_KING_AND_WHITE_KING_IN_SAME_QUEEN_QUADRANT

DEADEND = 'deadend'

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
    'use_adjacency': {CELL_S, ROW_S , COL_S},
    'use_distance_2': {},
    'use_distance_more_than_1': {},
    'use_bidirectional': {CELL_S, ROW_S , COL_S},
    'sorts_to_use': {CELL_S, ROW_S , COL_S},
    'n_moves': 10000,
    'unary_predicates': {CHECKMATE, STALEMATE, CHECK,
                         QUEEN_ATTACKED_WHITOUT_PROTECTION,
                         BLACK_KING_CLOSED_IN_EDGE_BY_WHITE_QUEEN,
                         WHITE_QUEEN_AND_BLACK_KING_IN_ADJACENT_EDGE,
                         WHITE_QUEEN_AND_WHITE_KING_IN_ADJACENT_EDGE,
                         WHITE_QUEEN_AND_BLACK_KING_IN_SAME_EDGE,
                         WHITE_QUEEN_AND_WHITE_KING_IN_SAME_EDGE,
                         BLACK_KING_AND_WHITE_KING_IN_SAME_EDGE,
                         BLACK_HAS_ACTION, BLACK_KING_IN_CORNER,
                         WHITE_QUEEN_IN_EDGE, WHITE_KING_IN_EDGE,
                         BLACK_KING_AND_WHITE_KING_IN_SAME_QUEEN_QUADRANT},
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
        comparison_features=True,
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
        # train_instances_to_expand=[],0
        train_instances_to_expand=list(range(1000)),
        max_states_expanded=math.inf,
        use_state_novelty=True,
    )
    exps = dict()

    # version 1:
    # using queen
    ct_params_v1 = copy.deepcopy(ct_params)
    ct_params_v1.game_version = 0
    exps["1"] = update_dict(
        base,
        domain=Domain(ct_params_v1),
        instances=[0],
        # instances=[70, 150],
        # test_instances=[0],
        allow_bad_states=True,
        test_instances=list(range(0, -1000, -1)),  # using negative keys for test instances
        # test_instances=[-1, -2, -3],
        feature_generator=debug_features_checkmate_tactic_queen(),
        validate_features=debug_validate_features_queen(),
        d2l_policy=debug_policy_queen(),
        # skip_train_steps=[0, 1, 2, 3],
    )

    exps["2"] = update_dict(
        exps["1"],
        validate_features=debug_validate_features_queen(),
    )

    exps["3"] = update_dict(
        exps["1"],
        instances=[1500],
        validate_features=debug_validate_features_queen(),
    )

    exps["4"] = update_dict(
        exps["1"],
        instances=[1500],
        validate_features=debug_validate_features_queen(),
    )

    return exps


# % % % % % % % % %
#    FEATURES
# % % % % % % % % %

col_h_wk = 'col-has-white_king'
col_h_wq = 'col-has-white_queen'
col_h_bk = 'col-has-black_king'
row_h_wk = 'row-has-white_king'
row_h_wq = 'row-has-white_queen'
row_h_bk = 'row-has-black_king'
cell_h_wk = 'cell-has-white_king'
cell_h_wq = 'cell-has-white_queen'
cell_h_bk = 'cell-has-black_king'
cell_in_bottom = CELL_IS_IN(BOTTOM)
cell_in_top = CELL_IS_IN(TOP)
cell_in_left = CELL_IS_IN(LEFT)
cell_in_right = CELL_IS_IN(RIGHT)
adj_col = 'adjacent_col'
adj_row = 'adjacent_row'
adj_cell = 'adjacent_cell'
left_cell = 'left_cell'
right_cell = 'right_cell'
up_cell = 'up_cell'
down_cell = 'down_cell'
cell_h_c_att_by_w = CELL_HAS_COLOR_ATTAKED_BY(WHITE)
cell_h_c_att_by_b = CELL_HAS_COLOR_ATTAKED_BY(BLACK)
cell_h_c_att_by_wq = CELL_HAS_PIECE_ATTAKED_BY(WHITE_QUEEN)
cell_h_c_att_by_wk = CELL_HAS_PIECE_ATTAKED_BY(WHITE_KING)
cell_h_c_att_by_bk = CELL_HAS_PIECE_ATTAKED_BY(BLACK_KING)
cell_is_in_top = CELL_IS_IN(TOP)
cell_is_in_right_most = CELL_IS_IN(RIGHT)
cell_is_in_left_most = CELL_IS_IN(LEFT)
cell_is_in_bottom = CELL_IS_IN(BOTTOM)

Atom = lambda what: f'Atom[{what}]'
Num = lambda what: f'Num[{what}]'
Dist = lambda elem0, sep, elem1: f'Dist[{elem0};{sep};{elem1}]'
Bool = lambda what: f'Bool[{what}]'
Not = lambda what: f'Not({what})'
Exists = lambda sep, elem: f'Exists({sep},{elem})'
Forall = lambda sep, elem: f'Forall({sep},{elem})'
And = lambda elem0, elem1: f'And({elem0},{elem1})'
LessThan = lambda elem0, elem1: 'LessThan{' + elem0 + '}{' + elem1 + '}'
Star = lambda what: f'Star({what})'
Inverse = lambda what: f'Inverse({what})'

"""
Las features serían:
(A) Número de celdas que son reachable desde la posición del rey negro sin cruzar ninguna línea de jaque de la reina blanca.
(CM) La posición es un jaque mate
(C) La posición es un jaque 
(P1) White turn
(WQABK) = Atom(WHITE_QUEEN_AND_BLACK_KING_IN_ADJACENT_EDGE)
(KE) El rey negro está "encerrado" por la reina en un edge del tablero, file or rank, no importa.
(QA) = Atom(QUEEN_ATTACKED_WHITOUT_PROTECTION)
(KD) manhattan distance entre los dos reyes.
(SM) La posición es un stalemate   [esta la usaremos solo implícitamente en las reglas, para indicar que nunca se pone a cierto]
(BM) La posición es un jaque de negra-a-blanca. También la usaremos solo implícitamente para indicar que eso nunca ocurre.

Las reglas:
R1.  not KE, A>0  --> A dec | A dec, KE
R2. KE, KD>0  --> KD dec
R3. True --> CM 
"""

# P1 = Atom("player-1")
# BKHA = Atom(BLACK_HAS_ACTION)
A = Num(And(cell_h_c_att_by_bk, Not(cell_h_c_att_by_wq)))
AWK = Num(And(cell_h_c_att_by_bk, Not(cell_h_c_att_by_wk)))
AW = Num(And(cell_h_c_att_by_bk, Not(cell_h_c_att_by_w)))
WQAdjBK = Atom(WHITE_QUEEN_AND_BLACK_KING_IN_ADJACENT_EDGE)
WQAdjWK = Atom(WHITE_QUEEN_AND_WHITE_KING_IN_ADJACENT_EDGE)
CM = Atom(CHECKMATE)
KE = Atom(BLACK_KING_CLOSED_IN_EDGE_BY_WHITE_QUEEN)
QA = Bool(And(And(cell_h_wq,Not(Exists(adj_cell, cell_h_wk))),And(cell_h_wk,Exists(adj_cell, cell_h_bk))))
# QA = Atom(QUEEN_ATTACKED_WHITOUT_PROTECTION)
SAME_QUADRANT = Atom(BLACK_KING_AND_WHITE_KING_IN_SAME_QUEEN_QUADRANT)
#
KRD = Dist(row_h_wk, adj_row, row_h_bk)
KCD = Dist(col_h_wk, adj_col, col_h_bk)
KD = Dist(cell_h_wk, adj_cell, cell_h_bk)
#
KQRD = Dist(row_h_wq, adj_row, row_h_bk)
KQCD = Dist(col_h_wq, adj_col, col_h_bk)
WKD = Dist(cell_h_wq, adj_cell, cell_h_bk)
SM = Atom(STALEMATE)
C = Atom(CHECK)
#
# BKinC = Atom(BLACK_KING_IN_CORNER)

BK_WK_same_row = Bool(And(row_h_bk, row_h_wk))
BK_WK_same_col = Bool(And(col_h_bk, col_h_wk))
BK_WQ_same_row = Bool(And(row_h_bk, row_h_wq))
BK_WQ_same_col = Bool(And(col_h_bk, col_h_wq))
WK_WQ_same_row = Bool(And(row_h_wk, row_h_wq))
WK_WQ_same_col = Bool(And(col_h_wk, col_h_wq))

BK_WK_same_edge = Atom(BLACK_KING_AND_WHITE_KING_IN_SAME_EDGE)
WQ_WK_same_edge = Atom(WHITE_QUEEN_AND_WHITE_KING_IN_SAME_EDGE)
WQ_BK_same_edge = Atom(WHITE_QUEEN_AND_BLACK_KING_IN_SAME_EDGE)
#
WQ_in_edge = Atom(WHITE_QUEEN_IN_EDGE)
WK_in_edge = Atom(WHITE_KING_IN_EDGE)

dist_WK_left = Num(Exists(Inverse(Star(left_cell)),cell_h_wk))
dist_WK_right = Num(Exists(Inverse(Star(right_cell)),cell_h_wk))
dist_WK_up = Num(Exists(Inverse(Star(up_cell)),cell_h_wk))
dist_WK_down = Num(Exists(Inverse(Star(down_cell)),cell_h_wk))

dist_WQ_left = Num(Exists(Inverse(Star(left_cell)),cell_h_wq))
dist_WQ_right = Num(Exists(Inverse(Star(right_cell)),cell_h_wq))
dist_WQ_up = Num(Exists(Inverse(Star(up_cell)),cell_h_wq))
dist_WQ_down = Num(Exists(Inverse(Star(down_cell)),cell_h_wq))

dist_BK_left = Num(Exists(Inverse(Star(left_cell)),cell_h_bk))
dist_BK_right = Num(Exists(Inverse(Star(right_cell)),cell_h_bk))
dist_BK_up = Num(Exists(Inverse(Star(up_cell)),cell_h_bk))
dist_BK_down = Num(Exists(Inverse(Star(down_cell)),cell_h_bk))


LTs = list()
for wk_, wq_, bk_ in zip([dist_WK_left, dist_WK_down, dist_WK_right, dist_WK_up,],
                         [dist_WQ_left, dist_WQ_down, dist_WQ_right, dist_WQ_up,],
                         [dist_BK_left, dist_BK_down, dist_BK_right, dist_BK_up,]):
    LTs.append(LessThan(wk_, wq_))
    LTs.append(LessThan(wk_, bk_))
    LTs.append(LessThan(wq_, bk_))

OTHER_FEATURES = [
    WQ_BK_same_edge, BK_WK_same_row, BK_WK_same_row, BK_WK_same_col,
    BK_WQ_same_row, BK_WQ_same_col, WK_WQ_same_row, WK_WQ_same_col,
    KD, BK_WK_same_edge, KQRD,KQCD, WKD, AWK, AW, WQAdjBK, WQAdjWK,
    # dist_WK_left, dist_WK_down, dist_WK_right, dist_WK_up,
    # dist_WQ_left, dist_WQ_down, dist_WQ_right, dist_WQ_up,
    # dist_BK_left, dist_BK_down, dist_BK_right, dist_BK_up,
]

RIGHT_FEATURES = [
        C, CM, SM, KE, WK_in_edge,
        WQ_WK_same_edge, WQ_in_edge, SAME_QUADRANT, KRD, KCD, QA,
    ]

def debug_features_checkmate_tactic_queen():
    return RIGHT_FEATURES


def debug_validate_features_queen():
    return list(range(len(debug_features_checkmate_tactic_queen())))


# % % % % % % % % %
#    POLICY
# % % % % % % % % %

NIL = 'NIL'
INC= 'INC'
DEC = 'DEC'
e0 = '=0'
mt0 = '>0'

def debug_policy_queen():

    rules = [
        [(CM, e0), (CM, INC)],
        # [(KE, e0), (A, DEC)],
        [(KE, e0), (KE, INC)],
        [(KE, e0), (A, DEC), (SAME_QUADRANT, e0), (SAME_QUADRANT, NIL), (WQ_in_edge, mt0), (WQ_in_edge, DEC), (C, NIL)],
        [(KE, e0), (A, NIL), (SAME_QUADRANT, e0), (SAME_QUADRANT, NIL), (WQ_in_edge, mt0), (WQ_in_edge, DEC), (C, NIL)],
        [(KE, e0), (A, DEC), (SAME_QUADRANT, e0), (SAME_QUADRANT, NIL), (WQ_in_edge, e0), (WQ_in_edge, NIL), (C, NIL)],
        [(KE, e0), (A, NIL), (SAME_QUADRANT, e0), (SAME_QUADRANT, NIL), (WQ_in_edge, e0), (WQ_in_edge, NIL), (C, NIL)],
        [(KE, e0), (SAME_QUADRANT, mt0), (SAME_QUADRANT, DEC)],

        # [(KE, e0), (A, INC)],
        # [(WQ_in_edge, mt0), (KE, e0), (WQ_in_edge, DEC), (A, DEC)],
        # [(WQ_in_edge, e0), (KE, e0), (WQ_in_edge, NIL), (A, DEC)],
        # [(KE, mt0), (A, DEC), (KE, NIL)],
        # [(KE, e0), (WQAdjBK, e0), (WQAdjBK, INC), (A, NIL),],
        # [(KE, e0), (WQAdjBK, mt0), (WQAdjBK, NIL), (A, NIL),],
        # [(KE, e0), (WQAdjBK, e0), (WQAdjBK, INC), (A, DEC)],
        # [(KE, e0), (WQAdjBK, mt0), (WQAdjBK, NIL), (A, DEC)],
        # [(KE, e0), (KE, INC)],
        # [(KE, e0), (AWK, mt0), (AWK, INC),],
        # [(KE, e0), (AWK, mt0), (AWK, NIL),],
        # [(BKHA, e0), (KE, mt0), (KE, NIL), (A, INC)],
        # [(A, e0), (A, INC), (C, INC)],
        # [(KE, e0), (AWK, DEC)],
        # [(KE, e0), (WQAdjBK, mt0), (WQAdjBK, NIL), (A, DEC)],
        # [(KE, e0), (WQAdjBK, mt0), (WQAdjBK, NIL), (A, NIL), (KD, DEC)],

        # [(KE, mt0), (BK_WK_same_edge, mt0), (WQ_WK_same_edge, mt0), (WQ_WK_same_edge, DEC), (WQ_BK_same_edge, INC)],
        # [(KE, mt0), (BK_WK_same_edge, mt0), (WQ_WK_same_edge, e0), (WQ_WK_same_edge, NIL), (WQ_BK_same_edge, INC)],

        # [(WQAdjBK, mt0), (WQAdjBK, NIL), (A, DEC)],
        # [(WQAdjBK, e0), (WQAdjBK, INC), (A, DEC)],
        # [(WQAdjBK, mt0), (WQAdjWK, mt0), (KE, mt0)],
        # [(WQAdjBK, mt0), (WQAdjWK, mt0), (KE, mt0), (WQAdjBK, NIL)],
        # [(WQAdjBK, mt0), (WQAdjWK, mt0), (BKinC, mt0), (KE, mt0), (KE, NIL), (WQAdjWK, DEC)],
        # [(WQABK, more_than_0),  (A, equal_0), (A, INC), (WQABK, NIL)],
        # [(WQABK, more_than_0),  (A, more_than_0), (A, NIL), (WQABK, NIL)],
        # [(KE, equal_0), (BKHA, equal_0), (BKHA, INC), (A, DEC)],
        # [(KE, equal_0), (BKHA, equal_0), (BKHA, INC), (A, DEC), (KE, NIL)],
        # [(KE, equal_0), (BKHA, equal_0), (BKHA, INC), (KE, INC)],
        # [(BKHA, equal_0), ],
        # [(KE, equal_0), (KE, NIL)],
        # [(KE, equal_0), (WQABK, more_than_0), (KCD, DEC)],
        # [(KE, equal_0), (WQABK, more_than_0), (KRD, DEC)],
        # [(EWQ, more_than_0), (C, INC)],
        # [(A, equal_0), (A, INC)],
        # [(A, equal_0), (A, INC), (KE, NIL)],
        # [(A, equal_0), (A, INC), (KE, INC)],
        # [(KE, equal_0), (A, NIL)],
        # [(KE, equal_0), (A, NIL)],
        # [(KE, more_than_0), (KE, NIL)],
        # [(KE, equal_0), (A, NIL)],
        # [(KE, equal_0), (KD, DEC)],
        # [(KE, equal_0), (A, DEC), (KE, NIL)],
        # [(KE, equal_0), (A, NIL)],

        # [(KE, more_than_0), (KCD, DEC), (KRD, NIL), (KE, NIL), (A, NIL)],
        # [(KE, more_than_0), (KCD, NIL), (KRD, DEC), (KE, NIL), (A, NIL)],
        # [(KE, more_than_0), (KE, NIL), (KCD, DEC), (KRD, DEC), (A, NIL)],
        # [(KE, equal_0), (WQABK, more_than_0), (WQABK, NIL), (KE, NIL), (KCD, NIL), (KRD, NIL), (A, NIL)],

        # [(KE, mt0), (KD, DEC)],
        # [(WQAdjBK, mt0), (KD, DEC)]
        # [(KE, equal_0), (WQABK, more_than_0), (WQABK, NIL), (KD, DEC)],

        [(KE, mt0), (KE, NIL), (WQ_WK_same_edge, mt0)],
        # [(KE, mt0), (KE, NIL), (WQ_WK_same_edge, mt0), (WK_in_edge, mt0), (BK_WK_same_edge, mt0), (BK_WK_same_edge, DEC)],
        # [(KE, mt0), (KE, NIL), (WQ_WK_same_edge, mt0), (WQ_WK_same_edge, DEC)],
        # [(KE, mt0), (KE, NIL), (WK_in_edge, mt0), (BK_WK_same_edge, mt0), (BK_WK_same_edge, DEC)],

        [(KE, mt0), (WQ_WK_same_edge, e0), (KE, NIL), (KCD, DEC), (KRD, NIL)],
        [(KE, mt0), (WQ_WK_same_edge, e0), (KE, NIL), (KCD, NIL), (KRD, DEC)],
        [(KE, mt0), (WQ_WK_same_edge, e0), (KE, NIL), (KCD, DEC), (KRD, DEC)],

        # [(WQAdjBK, mt0), (KE, INC)],
        # [(KE, mt0), (KCD, DEC), (KRD, DEC)],

        # [(KE, more_than_0), (KD, more_than_0), (C, INC)],
    ]

    rules_1 = [
        [(SM, e0), (SM, NIL), (QA, e0), (QA, NIL)],
        [(SM, e0), (SM, NIL), (QA, mt0), (QA, DEC)],
    ]

    return combined_rules(rules, rules_1)


def combined_rules(rules_0, rules_1):
    rules = list()
    for r0 in rules_0:
        for r1 in rules_1:
            rules.append(r0 + r1)
    return rules