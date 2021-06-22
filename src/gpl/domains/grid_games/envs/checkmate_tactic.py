import sys
from gpl.utils import Bunch
from ..grammar.objects import  WHITE_KING, WHITE_QUEEN, BLACK_KING, EMPTY, WHITE_TOWER, OBJECTS_CHECK
from ..utils import identify_next_player

import numpy as np
import copy

WHITE = 1
BLACK = 2

N_MOVE = 'n_move'

SIMPLIFIED_OBJECT = {
    EMPTY:'.',
    BLACK_KING:'k' ,
    WHITE_KING:'K',
    WHITE_QUEEN:'Q' ,
    WHITE_TOWER:'R',
}

ALL_TOKENS = [EMPTY, BLACK_KING, WHITE_KING]

COLOR_TO_PIECES = {
    WHITE: [WHITE_KING, WHITE_TOWER, WHITE_QUEEN,],
    BLACK: [BLACK_KING,],
}

opposite_color = lambda c: BLACK if c == WHITE else WHITE

PIECE_VALID_MOVES = {
    WHITE_KING: lambda pos, layout: king_valid_moves(pos, layout, WHITE),
    WHITE_QUEEN: lambda pos, layout: cool_piece_valid_moves(pos, layout, WHITE, WHITE_QUEEN),
    WHITE_TOWER: lambda pos, layout: cool_piece_valid_moves(pos, layout, WHITE, WHITE_TOWER),
    BLACK_KING: lambda pos, layout: king_valid_moves(pos, layout, BLACK),
}

# Actions IDs

UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3
LEFTUP = 4
RIGHTUP = 5
RIGHTDOWN = 6
LEFTDOWN = 7

ALL_DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
PERPENDICULAR_DIRECTIONS = [(-1, 0), (0, -1), (0, 1), (1, 0)]
DIAGONAL_DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

DIRECTIONS = {
    WHITE_KING: ALL_DIRECTIONS,
    WHITE_QUEEN: ALL_DIRECTIONS,
    WHITE_TOWER: PERPENDICULAR_DIRECTIONS,
    BLACK_KING: ALL_DIRECTIONS,
}

# Unary predicates
CHECK = 'check'
CHECKMATE = 'checkmate'
STALEMATE = 'stalemate'
BLACK_HAS_ACTION = 'black_has_action'
ROOK_ATTACKED_WHITOUT_PROTECTION = 'rook_attaked_without_protection'
QUEEN_ATTACKED_WHITOUT_PROTECTION = 'queen_attaked_without_protection'
BLACK_KING_CLOSED_IN_EDGE_BY_WHITE_QUEEN = 'black_king_closed_in_edge_by_white_queen'
WHITE_QUEEN_AND_BLACK_KING_IN_ADJACENT_EDGE = 'white_queen_and_black_king_in_adjacent_edge'
WHITE_QUEEN_AND_WHITE_KING_IN_ADJACENT_EDGE = 'white_queen_and_white_king_in_adjacent_edge'
WHITE_QUEEN_AND_BLACK_KING_IN_SAME_EDGE = 'white_queen_and_black_king_in_same_edge'
WHITE_QUEEN_AND_WHITE_KING_IN_SAME_EDGE = 'white_queen_and_white_king_in_same_edge'
BLACK_KING_AND_WHITE_KING_IN_SAME_EDGE = 'black_king_and_white_king_in_same_edge'
BLACK_KING_AND_WHITE_KING_IN_SAME_QUEEN_QUADRANT = 'black_king_and_white_king_same_queen_quadrant'
WHITE_QUEEN_IN_EDGE = 'white_queen_in_edge'
WHITE_KING_IN_EDGE = 'white_king_in_edge'
BLACK_KING_IN_CORNER = 'black_king_in_corner'

# Begin Chase =================================

class Env(object):
    def __init__(self, params):
        self.params = params

    def act(self, rep, action):
        layout = rep.grid
        new_rep = copy.deepcopy(rep)
        l = new_rep.grid
        pos = action[0]
        running_pos = action[1]
        try:
            next_cell = l[running_pos[0], running_pos[1]]
        except IndexError:
            print("Index error")
            sys.exit(1)
        assert not (getattr(rep, CHECK) and rep.player == WHITE)
        try:
            assert 'king' not in next_cell
        except:
            raise
        assert next_cell not in COLOR_TO_PIECES[rep.player]
        piece = l[pos[0], pos[1]]
        l[running_pos[0], running_pos[1]] = piece
        l[pos[0], pos[1]] = EMPTY
        new_rep.grid = l
        if rep.player == WHITE:
            new_rep.nmoves += 1
        new_rep.player = opposite_color(rep.player)
        new_rep.next_player = rep.player
        return self.__update_rep(new_rep)

    def __update_rep(self, rep):
        updated_rep = rep.to_dict()
        if CHECKMATE in self.params.unary_predicates:
            updated_rep[CHECKMATE] = checkmate(rep)
        if STALEMATE in self.params.unary_predicates:
            updated_rep[STALEMATE] = stale_mate(rep)
        if CHECK in self.params.unary_predicates:
            updated_rep[CHECK] = check(rep)
        if ROOK_ATTACKED_WHITOUT_PROTECTION in self.params.unary_predicates:
            updated_rep[ROOK_ATTACKED_WHITOUT_PROTECTION] = deadend_extension(rep)
        if QUEEN_ATTACKED_WHITOUT_PROTECTION in self.params.unary_predicates:
            updated_rep[QUEEN_ATTACKED_WHITOUT_PROTECTION] = deadend_extension(rep)
        if BLACK_KING_CLOSED_IN_EDGE_BY_WHITE_QUEEN in self.params.unary_predicates:
            updated_rep[BLACK_KING_CLOSED_IN_EDGE_BY_WHITE_QUEEN] = black_king_closed_in_edge_by_white_queen(rep)
        if WHITE_QUEEN_AND_BLACK_KING_IN_ADJACENT_EDGE in self.params.unary_predicates:
            updated_rep[WHITE_QUEEN_AND_BLACK_KING_IN_ADJACENT_EDGE] = white_queen_and_black_king_adjacent_edge(rep)
        if WHITE_QUEEN_AND_WHITE_KING_IN_ADJACENT_EDGE in self.params.unary_predicates:
            updated_rep[WHITE_QUEEN_AND_WHITE_KING_IN_ADJACENT_EDGE] = white_queen_and_white_king_adjacent_edge(rep)
        if WHITE_QUEEN_AND_BLACK_KING_IN_SAME_EDGE in self.params.unary_predicates:
            updated_rep[WHITE_QUEEN_AND_BLACK_KING_IN_SAME_EDGE] = white_queen_and_black_king_same_edge(rep)
        if WHITE_QUEEN_AND_WHITE_KING_IN_SAME_EDGE in self.params.unary_predicates:
            updated_rep[WHITE_QUEEN_AND_WHITE_KING_IN_SAME_EDGE] = white_queen_and_white_king_same_edge(rep)
        if BLACK_KING_AND_WHITE_KING_IN_SAME_EDGE in self.params.unary_predicates:
            updated_rep[BLACK_KING_AND_WHITE_KING_IN_SAME_EDGE] = black_king_and_white_king_same_edge(rep)
        if BLACK_KING_AND_WHITE_KING_IN_SAME_QUEEN_QUADRANT in self.params.unary_predicates:
            updated_rep[BLACK_KING_AND_WHITE_KING_IN_SAME_QUEEN_QUADRANT] = black_king_and_white_king_same_queen_quadrant(rep)
        if WHITE_QUEEN_IN_EDGE in self.params.unary_predicates:
            updated_rep[WHITE_QUEEN_IN_EDGE] = white_queen_in_edge(rep)
        if WHITE_KING_IN_EDGE in self.params.unary_predicates:
            updated_rep[WHITE_KING_IN_EDGE] = white_king_in_edge(rep)
        if BLACK_HAS_ACTION in self.params.unary_predicates:
            new_rep = copy.deepcopy(rep)
            new_rep.player = BLACK
            updated_rep[BLACK_HAS_ACTION] = len(Env.available_actions(new_rep)) > 0
        if BLACK_KING_IN_CORNER in self.params.unary_predicates:
            updated_rep[BLACK_KING_IN_CORNER] = black_king_in_corner(rep)
            # if rep.player == BLACK:
            #     updated_rep[BLACK_HAS_ACTION] = len(Env.available_actions(rep)) > 0
            # else:
            #     updated_rep[BLACK_HAS_ACTION] = False
        updated_rep[f"{N_MOVE}_{rep.nmoves}"] = True
        gstatus = Env.check_game_status(rep)
        if gstatus == 1:
            updated_rep['goal'] = True
        elif gstatus == -1:
            updated_rep['deadend'] = True
        if rep.nmoves >= self.params.n_moves and gstatus != 1:
            updated_rep['deadend'] = True
        return Bunch(updated_rep)

    @staticmethod
    def check_game_status(rep):
        if checkmate(rep):
            return 1
        if stale_mate(rep):
            return -1
        if rep.player==BLACK and deadend_extension(rep):
            return -1
        else:
            return 0

    @staticmethod
    def available_actions(rep):
        layout = rep.grid
        assert not rep.goal and not rep.deadend
        actions = []
        if rep.player == WHITE:
            if WHITE_QUEEN in layout:
                c0 = np.argwhere(layout == WHITE_QUEEN)[0]
                actions += [(c0, c1) for c1 in PIECE_VALID_MOVES[WHITE_QUEEN](c0, layout)]
            if WHITE_TOWER in layout:
                c0 = np.argwhere(layout == WHITE_TOWER)[0]
                actions += [(c0, c1) for c1 in PIECE_VALID_MOVES[WHITE_TOWER](c0, layout)]
            if WHITE_KING in layout:
                c0 = np.argwhere(layout == WHITE_KING)[0]
                actions += [(c0, c1) for c1 in PIECE_VALID_MOVES[WHITE_KING](c0, layout)]
        elif rep.player == BLACK:
            c0 = np.argwhere(layout == BLACK_KING)[0]
            actions += [(c0, c1) for c1 in PIECE_VALID_MOVES[BLACK_KING](c0, layout)]
        return actions

    def player2_policy(self, rep):
        layout = rep.grid
        king_pos = np.argwhere(layout == BLACK_KING)[0]
        valid_actions = Env.available_actions(rep)
        if WHITE_QUEEN in layout:
            no_king_piece_pos = np.argwhere(layout == WHITE_QUEEN)[0]
        elif WHITE_TOWER in layout:
            no_king_piece_pos = np.argwhere(layout == WHITE_TOWER)[0]
        if abs(no_king_piece_pos[0] - king_pos[0]) == 1 and abs(no_king_piece_pos[1] - king_pos[1]) == 1:
            king_valid_moves = PIECE_VALID_MOVES[BLACK_KING](king_pos, rep.grid)
            if any((no_king_piece_pos == pos).all() for pos in king_valid_moves):
                return [king_pos, no_king_piece_pos]
        return valid_actions[0]

    @staticmethod
    def get_action_space():
        return None

    @staticmethod
    def get_simplified_objects():
        return SIMPLIFIED_OBJECT

    @staticmethod
    def encode_op(rep, op):
        try:
            piece = rep.grid[op[0][0], op[0][1]]
        except:
            raise
        assert piece not in EMPTY
        o = copy.deepcopy(op)
        return "{}_{}.{}_{}.{}".format(piece, o[0][0], o[0][1], o[1][0], o[1][1])

    def init_instance(self, key):
        rep = {u: False for u in self.params.unary_predicates}
        rep['nmoves'] = 0
        rep[f"{N_MOVE}_0"] = True
        rep['grid'] = generate_gird(key, self.params)
        rep['player'] = WHITE
        rep['next_player'] = BLACK
        rep['goal'] = False
        rep['deadend'] = False
        return self.__update_rep(Bunch(rep))


# Helper mehtods =================================

def terminated(rep):
    if checkmate(rep) or stalemate(rep) or deadend_extension(rep):
        return True
    else:
        return False


def checkmate(rep):
    layout = rep.grid
    assert BLACK_KING in layout
    if rep.player == BLACK:
        king_pos = np.argwhere(layout == BLACK_KING)[0]
        valid_moves = PIECE_VALID_MOVES[BLACK_KING](king_pos, layout)
        if len(valid_moves) == 0:
            attacking_mask = get_attacking_mask(layout, opposite_color(rep.player))
            if attacking_mask[king_pos[0], king_pos[1]]:
                return True
        return False
    return False


def deadend_extension(rep):
    layout = rep.grid
    if rep.player == WHITE:
        return False
    bk_mask = get_attacking_mask(layout, BLACK)
    wk_mask = get_king_attacking_spaces(np.argwhere(layout==WHITE_KING)[0], layout, get_mask=True)
    if WHITE_QUEEN in layout:
        piece_pos = np.argwhere(layout == WHITE_QUEEN)[0]
    elif WHITE_TOWER in layout:
        piece_pos = np.argwhere(layout == WHITE_TOWER)[0]
    if bk_mask[piece_pos[0], piece_pos[1]] and not wk_mask[piece_pos[0], piece_pos[1]]:
        return True
    else:
        return False


def check(rep):
    layout = rep.grid
    assert BLACK_KING in layout
    if rep.player == BLACK:
        bk_pos = np.argwhere(layout == BLACK_KING)[0]
        attacking_mask = get_attacking_mask(layout, WHITE)
        if attacking_mask[bk_pos[0], bk_pos[1]]:
            return True
        return False
    return False


def stale_mate(rep):
    layout = rep.grid
    if checkmate(rep):
        return False
    assert BLACK_KING in layout
    if rep.player == BLACK:
        bk_valid_moves = PIECE_VALID_MOVES[BLACK_KING](np.argwhere(layout == BLACK_KING)[0], layout)
        if not bk_valid_moves:
            return True
    elif not WHITE_QUEEN in layout and not WHITE_TOWER in layout:
        return True
    else:
        return False


def black_king_closed_in_edge_by_white_queen(rep):
    """ El rey negro está "encerrado" por la reina en un edge del tablero, file or rank, no importa. """
    layout = rep.grid
    assert BLACK_KING in layout and WHITE_QUEEN in layout
    nrows, ncols = layout.shape
    r_bk, c_bk = np.argwhere(layout == BLACK_KING)[0]
    r_wq, c_wq = np.argwhere(layout == WHITE_QUEEN)[0]
    if (r_bk == 0 or r_bk == nrows - 1) and abs(r_bk - r_wq) ==  1:
        if abs(c_bk - c_wq) == 3 and black_king_in_corner(rep):
            return True
        if abs(c_bk - c_wq) == 2 and (c_bk == 1 or c_bk == ncols - 2):
            return True
    elif (c_bk == 0 or c_bk == ncols - 1) and abs(c_bk - c_wq) ==  1:
        if abs(r_bk - r_wq) == 3 and black_king_in_corner(rep):
            return True
        if abs(r_bk - r_wq) == 2 and (r_bk == 1 or r_bk == ncols - 2):
            return True
    return False


def white_queen_and_black_king_adjacent_edge(rep):
    layout = rep.grid
    assert BLACK_KING in layout and WHITE_QUEEN in layout
    nrows, ncols = layout.shape
    r_bk, c_bk = np.argwhere(layout == BLACK_KING)[0]
    r_wq, c_wq = np.argwhere(layout == WHITE_QUEEN)[0]
    if abs(r_bk - r_wq) == 1 or abs(c_bk - c_wq) == 1:
        return True
    else:
        return False

def white_queen_and_white_king_adjacent_edge(rep):
    layout = rep.grid
    assert WHITE_KING in layout and WHITE_QUEEN in layout
    nrows, ncols = layout.shape
    r_bk, c_bk = np.argwhere(layout == WHITE_KING)[0]
    r_wq, c_wq = np.argwhere(layout == WHITE_QUEEN)[0]
    if abs(r_bk - r_wq) == 1 or abs(c_bk - c_wq) == 1:
        return True
    else:
        return False

def white_queen_and_black_king_same_edge(rep):
    layout = rep.grid
    assert BLACK_KING in layout and WHITE_QUEEN in layout
    nrows, ncols = layout.shape
    r_bk, c_bk = np.argwhere(layout == BLACK_KING)[0]
    r_wq, c_wq = np.argwhere(layout == WHITE_QUEEN)[0]
    if r_bk == r_wq or c_bk - c_wq:
        return True
    else:
        return False

def white_queen_and_white_king_same_edge(rep):
    layout = rep.grid
    assert WHITE_KING in layout and WHITE_QUEEN in layout
    nrows, ncols = layout.shape
    r_bk, c_bk = np.argwhere(layout == WHITE_KING)[0]
    r_wq, c_wq = np.argwhere(layout == WHITE_QUEEN)[0]
    if r_bk == r_wq or c_bk == c_wq:
        return True
    else:
        return False


def black_king_and_white_king_same_edge(rep):
    layout = rep.grid
    assert WHITE_KING in layout and BLACK_KING in layout
    nrows, ncols = layout.shape
    r_bk, c_bk = np.argwhere(layout == BLACK_KING)[0]
    r_wq, c_wq = np.argwhere(layout == WHITE_KING)[0]
    if r_bk == r_wq or c_bk == c_wq:
        return True
    else:
        return False

def black_king_and_white_king_same_queen_quadrant(rep):
    layout = rep.grid
    assert WHITE_KING in layout and BLACK_KING in layout
    nrows, ncols = layout.shape
    r_bk, c_bk = np.argwhere(layout == BLACK_KING)[0]
    r_wk, c_wk = np.argwhere(layout == WHITE_KING)[0]
    r_wq, c_wq = np.argwhere(layout == WHITE_QUEEN)[0]

    if (r_wk <= r_wq and r_bk <= r_wq):
        if (c_wk <= c_wq and c_bk <= c_wq):
            # q1
            return True
        if (c_wk >= c_wq and c_bk >= c_wq):
            # q2
            return True
    if r_wk >= r_wq and r_bk >= r_wq:
        if c_wk <= c_wq and c_bk <= c_wq:
            # q3
            return True
        if c_wk >= c_wq and c_bk >= c_wq:
            # q4
            return True

    return False

def white_queen_in_edge(rep):
    layout = rep.grid
    assert WHITE_QUEEN in layout
    nrows, ncols = layout.shape
    r, c = np.argwhere(layout == WHITE_QUEEN)[0]
    if (r == 0 or r == nrows - 1 or c == 0 or c == ncols - 1):
        return True
    else:
        return False

def white_king_in_edge(rep):
    layout = rep.grid
    assert WHITE_KING in layout
    nrows, ncols = layout.shape
    r, c = np.argwhere(layout == WHITE_KING)[0]
    if (r == 0 or r == nrows - 1 or c == 0 or c == ncols - 1):
        return True
    else:
        return False


def black_king_in_corner(rep):
    layout = rep.grid
    r_bk, c_bk = np.argwhere(layout == BLACK_KING)[0]
    nrows, ncols = layout.shape
    if (r_bk == 0 or r_bk == nrows - 1) and (c_bk == 0 or c_bk == ncols -1):
        return True
    else:
        return False


def king_valid_moves(pos, layout, color):
    valid_moves = []
    attacking_mask = get_attacking_mask(layout, opposite_color(color))
    for direction in ALL_DIRECTIONS:
        running_pos = np.add(pos, direction)
        if np.any(running_pos < 0):
            continue
        try:
            next_cell = layout[running_pos[0], running_pos[1]]
        except IndexError:
            continue
        if next_cell in COLOR_TO_PIECES[color]:
            continue
        if next_cell in COLOR_TO_PIECES[opposite_color(color)]:
            excluded_layout = layout.copy()
            excluded_layout[running_pos[0], running_pos[1]] = EMPTY
            excluded_attacking_mask = get_attacking_mask(excluded_layout, opposite_color(color))
            if not excluded_attacking_mask[running_pos[0], running_pos[1]]:
                valid_moves.append(running_pos)
            continue
        if not attacking_mask[running_pos[0], running_pos[1]]:
            valid_moves.append(running_pos)
    return valid_moves


def get_attacking_mask(layout, color):
    attacking_mask = np.zeros(layout.shape, dtype=bool)
    for piece in COLOR_TO_PIECES[color]:
        if not piece in layout:
            continue
        pos = np.argwhere(layout == piece)[0]
        if 'king' in piece:
            attacked_spaces = get_king_attacking_spaces(pos, layout)
        else:
            attacked_spaces = PIECE_VALID_MOVES[piece](pos, layout)
        for space in attacked_spaces + [pos]:
            attacking_mask[space[0], space[1]] = True
    return attacking_mask


def get_attacking_mask_from_piece(layout, piece):
    if 'king' in piece:
        color  = WHITE if piece in WHITE_KING else BLACK
        mask = get_king_attacking_mask(layout, color)
    else:
        mask = no_king_piece_attaking_mask(layout, piece)
    return mask


def get_king_attacking_mask(layout, color):
    attacking_mask = np.zeros(layout.shape, dtype=bool)
    piece = WHITE_KING if color == WHITE else BLACK_KING
    pos = np.argwhere(layout == piece)[0]
    attacking_mask = get_king_attacking_spaces(pos, layout, get_mask=True)
    return attacking_mask


def no_king_piece_attaking_mask(layout, piece):
    mask = np.zeros(layout.shape, dtype=bool)
    pos = np.argwhere(layout == piece)[0]
    for direction in DIRECTIONS[piece]:
        running_pos = np.array(pos)
        while True:
            running_pos += direction
            if np.any(running_pos < 0):
                break
            try:
                next_cell = layout[running_pos[0], running_pos[1]]
            except IndexError:
                break
            if WHITE_KING in next_cell:
                break
            if next_cell in EMPTY or BLACK_KING in next_cell:
                mask[running_pos[0], running_pos[1]] = True
    mask[pos[0], pos[1]] = True
    return mask


def get_king_attacking_spaces(pos, layout, get_mask=False):
    attacking_spaces = list()
    attacking_mask = np.zeros(layout.shape, dtype=bool)
    for direction in ALL_DIRECTIONS:
        running_pos = np.array(pos)
        running_pos += direction
        if np.any(running_pos < 0):
            continue
        try:
            next_cell = layout[running_pos[0], running_pos[1]]
        except IndexError:
            continue
        attacking_spaces.append(running_pos)
        attacking_mask[running_pos[0], running_pos[1]] = True
    attacking_mask[pos[0], pos[1]] = True
    return attacking_mask if get_mask else attacking_spaces


def cool_piece_valid_moves(pos, layout, color, piece):
    valid_moves = []
    for direction in DIRECTIONS[piece]:
        running_pos = np.array(pos)
        while True:
            running_pos += direction
            if np.any(running_pos < 0):
                break
            try:
                next_cell = layout[running_pos[0], running_pos[1]]
            except IndexError:
                break
            if next_cell in COLOR_TO_PIECES[color]:
                break
            elif next_cell in EMPTY or 'king' in next_cell:
                valid_moves.append(running_pos.copy())
            else:
                assert next_cell in COLOR_TO_PIECES[opposite_color(color)]
                valid_moves.append(running_pos.copy())
                break
    return valid_moves


### Instances

def generate_gird(key, params):
    return LAYOUTS[params.game_version][key]


def generate_check_in_one(shapes, piece):
    grids = list()
    for height, width in shapes:
        grids_tmp = list()
        grid_blank = np.full((height, width), EMPTY, dtype=object)
        # checkmate in one grids
        for i in range(width + 1):
            for j in range(-1, 2):
                grid_tmp = grid_blank.copy()
                if i == width:
                    if piece == WHITE_TOWER:
                        continue
                    bk_pos = (0, i - 1)
                    if j == -1:
                        wk_pos = (1, i - 3)
                    elif j == 0:
                        wk_pos = (2, i - 3)
                    elif j == 1:
                        wk_pos = (2, i - 2)
                else:
                    bk_pos = (0, i)
                    wk_pos = (2, i + j)
                if np.any(np.array(wk_pos) < 0) or np.any(np.array(wk_pos) > width - 1):
                    continue
                grid_tmp[wk_pos[0], wk_pos[1]] = WHITE_KING
                grid_tmp[bk_pos[0], bk_pos[1]] = BLACK_KING
                if piece == WHITE_TOWER:
                    checkmate_positions = [(0, j) for j in range(width) if 0 < j < width and abs(i - j) > 1]
                elif piece == WHITE_QUEEN:
                    if i != width:
                        checkmate_positions = [(1, i)]
                        if j==0:
                            checkmate_positions += [(0, j) for j in range(width) if 0 < j < width and abs(i - j) > 1]
                    else:
                        checkmate_positions = [(1, i - 2)]
                        if j == -1:
                            checkmate_positions += [(0, i - 2)]
                        elif j == 1:
                            checkmate_positions += [(1, i - 1)]
                for pos in checkmate_positions:
                    checkmate_positions_from = cool_piece_valid_moves(pos, grid_tmp, WHITE, piece)
                    for r, c in checkmate_positions_from:
                        grid = grid_tmp.copy()
                        cell_value = grid[r, c]
                        if cell_value != EMPTY:
                            continue
                        grid[r, c] = piece
                        if get_attacking_mask(grid, WHITE)[bk_pos[0], bk_pos[1]]:
                            continue
                        grids_tmp.append(grid)
                        grids.append(grid)

        for grid_tmp in grids_tmp:
            grids.append(np.rot90(grid_tmp, 1))
            grids.append(np.rot90(grid_tmp, 2))
            grids.append(np.rot90(grid_tmp, 3))

    return {i: g for i, g in enumerate(grids)}


def generate_test_gird(key):
    height, width, cell_white_king, cell_black_king, cell_white_queen, cell_white_tower = \
        TEST_LAYOUTS_QUEEN[key]
    grid = np.full((height, width), EMPTY, dtype=object)
    grid[cell_white_king] = WHITE_KING
    grid[cell_black_king] = BLACK_KING
    if cell_white_queen is not None:
        grid[cell_white_queen] = WHITE_QUEEN
    if cell_white_tower is not None:
        grid[cell_white_tower] = WHITE_TOWER
    return grid


TEST_LAYOUTS_TOWER = {
    -1: (4, 4, (3, 2), (0, 2), None, (3, 1)),
    -2: (3, 4, (1, 1), (1, 3), None, (1, 0)),
    -3: (5, 5, (0, 0), (4, 4), None, (1, 2)),
    -4: (6, 6, (0, 0), (3, 3), None, (5, 1)),
    -5: (7, 7, (1, 1), (1, 3), None, (1, 0)),
    -6: (8, 8, (1, 1), (1, 3), None, (1, 0)),
    -7: (9, 9, (1, 1), (1, 3), None, (1, 0)),
    -8: (10, 10, (1, 1), (1, 3), None, (1, 0)),
}

TEST_LAYOUTS_QUEEN = {
    -1: (4, 4, (3, 2), (0, 2), (3, 1), None),
    -2: (4, 4, (1, 1), (1, 3), (1, 0), None),
    -3: (5, 5, (0, 0), (4, 4), (1, 2), None),
    -4: (6, 6, (0, 0), (3, 3), (5, 2), None),
    -5: (7, 7, (1, 1), (1, 3), (1, 0), None),
    -6: (8, 8, (1, 1), (1, 3), (1, 0), None),
    -7: (9, 9, (1, 1), (1, 3), (1, 0), None),
    -8: (10, 10, (1, 1), (1, 3), (1, 0), None),
    -9: (7, 7, (0, 3), (1, 6), (0, 4), None),
    -10: (15, 15, (6, 6), (9, 9), (0, 0), None),
}

LAYOUTS_CHECK_IN_ONE_QUEEN = generate_check_in_one([(3, 3), (4, 3), (4, 4), (5, 5), (6, 6)], WHITE_QUEEN)
LAYOUTS_CHECK_IN_ONE_TOWER = generate_check_in_one([(3, 3), (4, 3), (3, 4), (4, 4), (4, 5), (5, 4), (5, 5), (6, 6)], WHITE_TOWER)

for k in TEST_LAYOUTS_TOWER.keys():
    LAYOUTS_CHECK_IN_ONE_TOWER[k] = generate_test_gird(k)

for k in TEST_LAYOUTS_QUEEN.keys():
    LAYOUTS_CHECK_IN_ONE_QUEEN[k] = generate_test_gird(k)

LAYOUTS = {
    0: LAYOUTS_CHECK_IN_ONE_QUEEN,
    1: LAYOUTS_CHECK_IN_ONE_TOWER,
}