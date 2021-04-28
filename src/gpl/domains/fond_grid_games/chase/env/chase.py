import sys

import numpy as np

EMPTY = 'empty'
BLACK_KING = 'black_king'
WHITE_KING = 'white_king'

ALL_TOKENS = [EMPTY, BLACK_KING, WHITE_KING]

COLOR_TO_PIECES = {
    'white': [WHITE_KING,],
    'black': [BLACK_KING,],
}

WHITE = 'white'
BLACK = 'black'

opposite_color = lambda c: 'black' if c == 'white' else 'white'


PIECE_VALID_ACTIONS = {
    WHITE_KING: lambda pos, layout: king_valid_actions(pos, layout, 'white'),
    BLACK_KING: lambda pos, layout: king_valid_actions(pos, layout, 'black'),
}

# Actions IDs

UP = 0 # 'up'
DOWN = 1 # 'down'
RIGHT = 2 # 'right'
LEFT = 3 # 'left'
# STAY = 4 # 'left'


ACTION_SPACE = {
    UP,
    DOWN,
    RIGHT,
    LEFT,
    # STAY,
}


ACTION_MOVE_DIRECTION = {
    UP: (-1, 0),
    DOWN: (1, 0),
    RIGHT: (0, 1),
    LEFT: (0, -1),
    # STAY: (0, 0),
}

MAX_ACTIONS_BY_TURN = {
    WHITE:2,
    BLACK:1
}

MOVE_ACTION = {
    (-1, 0): {WHITE: UP, BLACK: UP},
    (1, 0): {WHITE: DOWN, BLACK: DOWN},
    (0, 1): {WHITE: RIGHT, BLACK: RIGHT},
    (0, -1): {WHITE: LEFT, BLACK: LEFT},
    # (0, 0): {WHITE: STAY, BLACK: STAY},
}

# Begin Chase =================================

def act(rep, action):
    layout, color, nact = rep
    assert nact < MAX_ACTIONS_BY_TURN[color]
    assert not terminated(rep)
    valid_actions = available_actions(rep)
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
    if l[new_r, new_c] != WHITE_KING:  # chaser can not be catched!
        l[new_r, new_c] = piece
    l[old_r, old_c] = EMPTY
    if nact + 1 < MAX_ACTIONS_BY_TURN[color]:
        return (l, color, nact + 1)
    else:
        return (l, opposite_color(color), 0)


def check_game_status(rep):
    if catched(rep):
        return 1
    else:
        return -1

def terminated(rep):
    if catched(rep):
        return 1
    else:
        return 0

def available_actions(rep):
    layout, player, nact = rep
    actions = []
    if player == 'white':
        c0 = np.argwhere(layout == WHITE_KING)[0]
        actions += PIECE_VALID_ACTIONS[WHITE_KING](c0, layout)
    elif player == 'black':
        c0 = np.argwhere(layout == BLACK_KING)[0]
        actions += PIECE_VALID_ACTIONS[BLACK_KING](c0, layout)
    return actions


# Helper mehtods =================================


def get_action_from_move(move, color):
    return MOVE_ACTION[move][color]


def runnable_position(rep):
    layout, player, nact = rep
    if player == 'white':
        return np.argwhere(layout == WHITE_KING)[0]
    elif player == 'black':
        return np.argwhere(layout == BLACK_KING)[0]


def catched(rep):
    layout, player, nact = rep
    if BLACK_KING not in layout:
        return True
    else:
        return False


def player2_policy(rep):
    assert (BLACK_KING in rep[0])
    assert (rep[1] in 'black')
    bk = np.argwhere(rep[0] == BLACK_KING)[0]
    wk = np.argwhere(rep[0] == WHITE_KING)[0]
    valid_actions = available_actions(rep)
    assert valid_actions
    return valid_actions[0]


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

