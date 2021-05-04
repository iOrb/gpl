import sys

import numpy as np

WHITE = 1
BLACK = 2

EMPTY = 'empty'
BLACK_KING = 'black_king'
WHITE_KING = 'white_king'

ALL_TOKENS = [EMPTY, BLACK_KING, WHITE_KING]

COLOR_TO_PIECES = {
    WHITE: [WHITE_KING,],
    BLACK: [BLACK_KING,],
}

opposite_color = lambda c: BLACK if c == WHITE else WHITE


PIECE_VALID_ACTIONS = {
    WHITE_KING: lambda pos, layout: king_valid_actions(pos, layout, WHITE),
    BLACK_KING: lambda pos, layout: king_valid_actions(pos, layout, BLACK),
}

# Actions IDs

UP = 0 # 'up'
DOWN = 1 # 'down'
RIGHT = 2 # 'right'
LEFT = 3 # 'left'
LEFTUP = 4 # 'left'
RIGHTUP = 5 # 'left'
RIGHTDOWN = 6 # 'left'
LEFTDOWN = 7 # 'left'
# STAY = 4 # 'left'


ACTION_SPACE = {
    UP,
    DOWN,
    RIGHT,
    LEFT,
    LEFTUP,
    RIGHTUP,
    RIGHTDOWN,
    LEFTDOWN,
    # STAY,
}

ACTION_MOVE_DIRECTION = {
    UP: (-1, 0),
    DOWN: (1, 0),
    RIGHT: (0, 1),
    LEFT: (0, -1),
    LEFTUP: (-1, -1),
    RIGHTUP: (-1, 1),
    RIGHTDOWN: (1, 1),
    LEFTDOWN: (1, -1),
    # STAY: (0, 0),
}

MAX_ACTIONS_BY_TURN = {
    WHITE:2,
    BLACK:1,
}

MOVE_ACTION = {
    ACTION_MOVE_DIRECTION[UP]: {WHITE: UP, BLACK: UP},
    ACTION_MOVE_DIRECTION[DOWN]: {WHITE: DOWN, BLACK: DOWN},
    ACTION_MOVE_DIRECTION[RIGHT]: {WHITE: RIGHT, BLACK: RIGHT},
    ACTION_MOVE_DIRECTION[LEFT]: {WHITE: LEFT, BLACK: LEFT},
    ACTION_MOVE_DIRECTION[LEFTUP]: {WHITE: LEFTUP, BLACK: LEFTUP},
    ACTION_MOVE_DIRECTION[RIGHTUP]: {WHITE: RIGHTUP, BLACK: RIGHTUP},
    ACTION_MOVE_DIRECTION[RIGHTDOWN]: {WHITE: RIGHTDOWN, BLACK: RIGHTDOWN},
    ACTION_MOVE_DIRECTION[LEFTDOWN]: {WHITE: LEFTDOWN, BLACK: LEFTDOWN},
    # (0, 0): {WHITE: STAY, BLACK: STAY},
}

# Begin Chase =================================

class Env(object):
    @staticmethod
    def act(rep, action):
        layout, color, nact = rep
        assert nact < MAX_ACTIONS_BY_TURN[color]
        assert not terminated(rep)
        valid_actions = Env.available_actions(rep)
        assert action in valid_actions
        l = layout.copy()
        pos = runnable_position(rep)
        running_pos = np.add(pos, ACTION_MOVE_DIRECTION[action])
        assert not np.any(running_pos < 0)
        try:
            next_cell = l[running_pos[0], running_pos[1]]
        except IndexError:
            print("Index error")
            sys.exit(1)
        old_r, old_c = pos
        new_r, new_c = running_pos
        piece = l[old_r, old_c]
        # if l[new_r, new_c] != WHITE_KING:  # chaser can not be catched!
        #     l[new_r, new_c] = piece
        l[new_r, new_c] = piece
        l[old_r, old_c] = EMPTY
        if nact + 1 < MAX_ACTIONS_BY_TURN[color]:
            return (l, color, nact + 1)
        else:
            return (l, opposite_color(color), 0)

    @staticmethod
    def check_game_status(rep):
        if catched(rep):
            return 1
        else:
            return 0

    @staticmethod
    def available_actions(rep):
        layout, player, nact = rep
        actions = []
        if player == WHITE:
            c0 = np.argwhere(layout == WHITE_KING)[0]
            actions += PIECE_VALID_ACTIONS[WHITE_KING](c0, layout)
        elif player == BLACK:
            c0 = np.argwhere(layout == BLACK_KING)[0]
            actions += PIECE_VALID_ACTIONS[BLACK_KING](c0, layout)
        return actions

    @staticmethod
    def player2_policy(rep):
        assert (BLACK_KING in rep[0])
        assert (rep[1] == BLACK)
        bk = np.argwhere(rep[0] == BLACK_KING)[0]
        wk = np.argwhere(rep[0] == WHITE_KING)[0]
        valid_actions = Env.available_actions(rep)
        assert valid_actions
        return valid_actions[0]

    @staticmethod
    def get_action_space():
        return ACTION_SPACE

    @staticmethod
    def get_grid(key):
        return generate_gird(key)

# Helper mehtods =================================

def terminated(rep):
    if catched(rep):
        return 1
    else:
        return 0

def get_action_from_move(move, color):
    return MOVE_ACTION[move][color]


def runnable_position(rep):
    layout, player, nact = rep
    if player == WHITE:
        return np.argwhere(layout == WHITE_KING)[0]
    elif player == BLACK:
        return np.argwhere(layout == BLACK_KING)[0]


def catched(rep):
    attakig_mask = get_attaking_mask((rep[0], WHITE, 0))
    opposite_pos = runnable_position((rep[0], BLACK, 0))
    if any((opposite_pos == att).all() for att in attakig_mask):
        return True
    else:
        return False


def king_valid_actions(pos, layout, color):
    valid_action = []
    # for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
    for direction in ACTION_MOVE_DIRECTION.values():
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
            pass
        valid_action.append(get_action_from_move(direction, color))
    return valid_action


def get_attaking_mask(rep):
    layout, color, _ = rep
    attaking_mask = []
    assert color==WHITE

    pos = runnable_position(rep)
    for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
    # for direction in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
        running_pos = np.array(pos)
        running_pos += direction
        if np.any(running_pos < 0):
            continue
        try:
            next_cell = layout[running_pos[0], running_pos[1]]
        except IndexError:
            continue

        if next_cell in COLOR_TO_PIECES[color]:
            continue
        elif next_cell == EMPTY or 'king' in next_cell:
            attaking_mask.append(running_pos.copy())
        else:
            assert next_cell in COLOR_TO_PIECES[opposite_color(color)]
            attaking_mask.append(running_pos.copy())
            continue

    return attaking_mask

### Instances
def generate_gird(key):
    height, width, cell_agent, cell_target = LAYOUTS[key]
    grid = np.full((height, width), EMPTY, dtype=object)
    grid[cell_agent] = WHITE_KING
    grid[cell_target] = BLACK_KING
    return grid

LAYOUTS = {
    0: (4, 6, (0, 0), (3, 5)),
    1: (4, 6, (3, 5), (0, 0)),
    2: (6, 4, (5, 3), (0, 0)),
    3: (6, 6, (0, 5), (5, 0)),
    4: (8, 4, (6, 3), (0, 0)),
    5: (7, 7, (0, 0), (5, 5)),
    6: (10, 10, (3, 3), (0, 0)),
    7: (11, 4, (3, 3), (0, 0)),
    8: (8, 9, (3, 3), (0, 0)),
    9: (4, 4, (3, 3), (0, 0)),
    10: (4, 4, (0, 0), (3, 3)),
}
