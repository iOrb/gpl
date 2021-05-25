import sys
from gpl.utils import Bunch
from ..grammar.objects import  WHITE_KING, WHITE_QUEEN, BLACK_KING, EMPTY, WHITE_TOWER, OBJECTS_CHECK

import numpy as np
import copy

WHITE = 1
BLACK = 2

N_MOVE = 'n_move'

SIMPLIFIED_OBJECT = {
    EMPTY:' . ',
    BLACK_KING:' k ',
    WHITE_KING:' K ',
    WHITE_QUEEN:' Q ',
    WHITE_TOWER:' R ',
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

# Begin Chase =================================

class Env(object):
    def __init__(self, params):
        self.params = params

    def act(self, rep, action):
        layout = rep.grid
        # assert not terminated(rep)
        # valid_actions = Env.available_actions(rep)
        # assert action in valid_actions
        new_rep = copy.deepcopy(rep)
        l = new_rep.grid
        pos = action[0]
        running_pos = action[1]
        try:
            next_cell = l[running_pos[0], running_pos[1]]
        except IndexError:
            print("Index error")
            sys.exit(1)
        assert 'king' not in next_cell
        assert next_cell not in COLOR_TO_PIECES[rep.player]
        piece = l[pos[0], pos[1]]
        l[running_pos[0], running_pos[1]] = piece
        l[pos[0], pos[1]] = EMPTY
        new_rep.grid = l
        if rep.player == WHITE:
            new_rep.nmoves += 1
        new_rep.player = opposite_color(rep.player)
        return self.__update_rep(new_rep)

    def __update_rep(self, rep):
        updated_rep = rep.to_dict()
        if CHECKMATE in self.params.unary_predicates:
            updated_rep[CHECKMATE] = checkmate(rep)
        if STALEMATE in self.params.unary_predicates:
            updated_rep[STALEMATE] = stale_mate(rep)
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
        else:
            return 0

    @staticmethod
    def available_actions(rep):
        layout = rep.grid
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

    @staticmethod
    def player2_policy(rep):
        layout = rep.grid
        king_pos = np.argwhere(layout == BLACK_KING)[0]
        valid_actions = Env.available_actions(rep)
        if WHITE_QUEEN in layout:
            no_king_piece_pos = np.argwhere(layout == WHITE_QUEEN)[0]
        elif WHITE_TOWER in layout:
            no_king_piece_pos = np.argwhere(layout == WHITE_TOWER)[0]
        if abs(no_king_piece_pos[0] - king_pos[0]) == 1 and abs(no_king_piece_pos[1] - king_pos[1]) == 1:
            king_valid_moves = PIECE_VALID_MOVES[BLACK_KING](king_pos, rep[0])
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
        piece = rep.grid[op[0][0], op[0][1]]
        assert piece not in EMPTY
        o = copy.deepcopy(op)
        return "{}_{}.{}_{}.{}".format(piece, o[0][0], o[0][1], o[1][0], o[1][1])

    def init_instance(self, key):
        rep = {u: False for u in self.params.unary_predicates}
        rep['nmoves'] = 0
        rep[f"{N_MOVE}_0"] = True
        rep['grid'] = generate_gird(key, self.params)
        rep['player'] = WHITE
        rep['goal'] = False
        rep['deadend'] = False
        return Bunch(rep)


# Helper mehtods =================================

def terminated(rep):
    if checkmate(rep) or stalemate(rep):
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

def check(rep):
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

# def generate_gird(key):
#     height, width, cell_white_king, cell_black_king, cell_white_queen, cell_white_tower = \
#         LAYOUTS_QUEEN[key]
#     grid = np.full((height, width), EMPTY, dtype=object)
#     grid[cell_white_king] = WHITE_KING
#     grid[cell_black_king] = BLACK_KING
#     if cell_white_queen:
#         grid[cell_white_queen] = WHITE_QUEEN
#     if cell_white_tower:
#         grid[cell_white_tower] = WHITE_TOWER
#     return grid


def generate_gird(key, params):
    return LAYOUTS[params.game_version][key]


def generate_check_in_one(shapes, piece):
    grids = list()
    for height, width in shapes:
        grids_tmp = list()
        grid_blank = np.full((height, width), EMPTY, dtype=object)
        # checkmate in one grids
        for i in range(width + 1):
            grid_tmp = grid_blank.copy()
            if i == width:
                if piece == WHITE_TOWER:
                    continue
                bk_pos = (0, i - 1)
                wk_pos = (2, i - 3)
            else:
                bk_pos = (0, i)
                wk_pos = (2, i)
            grid_tmp[wk_pos[0], wk_pos[1]] = WHITE_KING
            grid_tmp[bk_pos[0], bk_pos[1]] = BLACK_KING
            if piece == WHITE_TOWER:
                checkmate_positions = [(0, j) for j in range(width) if 0 < j < width and abs(i - j) > 1]
            elif piece == WHITE_QUEEN:
                checkmate_positions = [(0, j) for j in range(width) if 0 < j < width and abs(i - j) > 1] + [(1, i)] if i != width else [(1, i - 2)]
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


LAYOUTS_QUEEN = {
    0: (4, 4, (1, 1), (1, 3), (1, 0), None),
    1: (4, 3, (1, 1), (3, 1), (1, 2), None),
    2: (3, 3, (0, 0), (1, 2), (2, 0), None),
    3: (3, 2, (0, 1), (2, 1), (0, 0), None),
}

LAYOUTS_TOWER = {
    0: (4, 4, (1, 1), (1, 3), None, (3, 2)),
    1: (4, 3, (2, 0), (0, 0), None, (3, 2)),
    2: (3, 3, (0, 0), (2, 0), None, (1, 2)),
    3: (5, 5, (4, 0), (0, 4), None, (4, 2)),
}

LAYOUTS_CHECK_IN_ONE_QUEEN = generate_check_in_one([(4, 4), (5, 5), (6, 6)], WHITE_QUEEN)
LAYOUTS_CHECK_IN_ONE_TOWER = generate_check_in_one([(4, 4), (5, 5), (6, 6)], WHITE_TOWER)

LAYOUTS = {
    0: LAYOUTS_CHECK_IN_ONE_QUEEN,
    1: LAYOUTS_CHECK_IN_ONE_TOWER,
}