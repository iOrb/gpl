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

PIECE_VALID_MOVES = {
    WHITE_KING: lambda pos, layout: king_valid_moves(pos, layout, 'white'),
    BLACK_KING: lambda pos, layout: king_valid_moves(pos, layout, 'black'),
}

PIECE_VALID_ACTIONS = {
    WHITE_KING: lambda pos, layout: king_valid_actions(pos, layout, 'white'),
    BLACK_KING: lambda pos, layout: king_valid_actions(pos, layout, 'black'),
}

# Actions IDs

UP_S = 0 # 'move_up_and_shoot'
DOWN_S = 1 # 'move_down_and_shoot'
RIGHT_S = 2 # 'move_right_and_shoot'
LEFT_S = 3 # 'move_left_and_shoot'
UP = 4 # 'up'
DOWN = 5 # 'down'
RIGHT = 6 # 'right'
LEFT = 7 # 'left'

# ACTION_SPACE = {SHOOT, UP, DOWN, RIGHT, LEFT}
ACTION_SPACE = {UP_S, DOWN_S, RIGHT_S, LEFT_S, UP, DOWN, RIGHT, LEFT}

# ACTION_ID  = {
#     UP_S:1,
#     DOWN_S:2,
#     RIGHT_S:3,
#     LEFT_S:4,
#     UP:5,
#     DOWN:6,
#     RIGHT:7,
#     LEFT:8,
# }

# ID_ACTION  = {ACTION_ID[k]:k for k in ACTION_ID.keys()}

ACTION_MOVE_DIRECTION = {
    UP_S: (-1, 0),
    DOWN_S: (1, 0),
    RIGHT_S: (0, 1),
    LEFT_S: (0, -1),
    UP: (-1, 0),
    DOWN: (1, 0),
    RIGHT: (0, 1),
    LEFT: (0, -1),
}

MOVE_ACTION = {
    (-1, 0): {WHITE: UP_S, BLACK: UP},
    (1, 0): {WHITE: DOWN_S, BLACK: DOWN},
    (0, 1): {WHITE: RIGHT_S, BLACK: RIGHT},
    (0, -1): {WHITE: LEFT_S, BLACK: LEFT},
}

# Begin Shoot =================================

# check_game_status, act, available_actions

def act(rep, action):
    layout, color = rep
    l = layout.copy()
    valid_actions = available_actions(rep)
    assert action in valid_actions

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
    l[new_r, new_c] = piece
    l[old_r, old_c] = EMPTY
    if color == WHITE and BLACK_KING in l: # just the white king can shot
        attakig_mask = get_attaking_mask((l, color))
        opposite_pos = runnable_position((l, opposite_color(color)))
        if any((opposite_pos == att).all() for att in attakig_mask):
            l[opposite_pos[0], opposite_pos[1]] = EMPTY
    return (l, opposite_color(color))


def get_action_from_move(move, color):
    return MOVE_ACTION[move][color]


def runnable_position(rep):
    layout, player = rep
    if player == 'white':
        return np.argwhere(layout == WHITE_KING)[0]
    elif player == 'black':
        return np.argwhere(layout == BLACK_KING)[0]


def available_actions(rep):
    layout, player = rep
    actions = []
    if player == 'white':
        c0 = np.argwhere(layout == WHITE_KING)[0]
        actions += [a for a in PIECE_VALID_ACTIONS[WHITE_KING](c0, layout)]
    elif player == 'black':
        c0 = np.argwhere(layout == BLACK_KING)[0]
        actions += [a for a in PIECE_VALID_ACTIONS[BLACK_KING](c0, layout)]
    return actions


def check_game_status(rep):
    if checkmate(rep):
        return 1
    else:
        return -1


def checkmate(rep):
    layout, player = rep
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
    if not valid_actions:
        return bk
    else:
        return valid_actions[0]


# End Checkmate =================================


def king_valid_moves(pos, layout, color):
    attacking_spaces = []
    # for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
    for direction in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
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
        attacking_spaces.append(running_pos)
    return attacking_spaces


def king_valid_actions(pos, layout, color):
    valid_action = []
    # for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
    for direction in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
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
    layout, color = rep
    attaking_mask = []
    assert color=='white'

    pos = runnable_position(rep)
    # for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
    for direction in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
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
            elif next_cell == EMPTY or 'king' in next_cell:
                attaking_mask.append(running_pos.copy())
            else:
                assert next_cell in COLOR_TO_PIECES[opposite_color(color)]
                attaking_mask.append(running_pos.copy())
                break

    return attaking_mask

