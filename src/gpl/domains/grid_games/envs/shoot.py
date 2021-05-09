import sys

import numpy as np


WHITE = 1 # player 1
BLACK = 2 # player 2

EMPTY = 'empty'
BLACK_KING = 'black_king'
WHITE_KING = 'white_king'

SIMPLIFIED_OBJECT = {
    EMPTY:'.',
    BLACK_KING:'T',
    WHITE_KING:'A',
}

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

UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

AGENT_ACTION_SPACE = {
    UP,
    DOWN,
    RIGHT,
    LEFT,
}

ENV_ACTION_SPACE = {
    UP,
    DOWN,
    RIGHT,
    LEFT,
}

ACTION_MOVE_DIRECTION = {
    UP: (-1, 0),
    DOWN: (1, 0),
    RIGHT: (0, 1),
    LEFT: (0, -1),
}

MOVE_ACTION = {
    (-1, 0): {WHITE: UP, BLACK: UP},
    (1, 0): {WHITE: DOWN, BLACK: DOWN},
    (0, 1): {WHITE: RIGHT, BLACK: RIGHT},
    (0, -1): {WHITE: LEFT, BLACK: LEFT},
}

# Begin Shoot =================================

# check_game_status, act, available_actions

class Env(object):
    @staticmethod
    def act(rep, action):
        layout, color, _ = rep
        l = layout.copy()
        valid_actions = Env.available_actions(rep)
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
        if not l[new_r, new_c] == WHITE_KING:
            l[new_r, new_c] = piece
        l[old_r, old_c] = EMPTY
        # if BLACK_KING in l: # just the white king can shoot
        #     attakig_mask = get_attaking_mask((l, WHITE, 0))
        #     opposite_pos = runnable_position((l, BLACK, 0))
            # if any((opposite_pos == att).all() for att in attakig_mask):
            #     l[opposite_pos[0], opposite_pos[1]] = EMPTY
        return (l, opposite_color(color), 0)

    @staticmethod
    def available_actions(rep):
        layout, player, _ = rep
        actions = []
        if player == WHITE:
            c0 = np.argwhere(layout == WHITE_KING)[0]
            actions += [a for a in PIECE_VALID_ACTIONS[WHITE_KING](c0, layout)]
        elif player == BLACK:
            c0 = np.argwhere(layout == BLACK_KING)[0]
            actions += [a for a in PIECE_VALID_ACTIONS[BLACK_KING](c0, layout)]
        return actions

    @staticmethod
    def check_game_status(rep):
        if checkmate(rep):
            return 1
        else:
            return 0

    @staticmethod
    def player2_policy(rep):
        assert (BLACK_KING in rep[0])
        bk = np.argwhere(rep[0] == BLACK_KING)[0]
        wk = np.argwhere(rep[0] == WHITE_KING)[0]
        valid_actions = Env.available_actions(rep)
        if not valid_actions:
            return bk
        else:
            return valid_actions[0]

    @staticmethod
    def get_grid(key):
        return generate_gird(key)

    @staticmethod
    def get_action_space():
        return AGENT_ACTION_SPACE

    @staticmethod
    def get_simplified_objects():
        return SIMPLIFIED_OBJECT


def runnable_position(rep):
    layout, player, _ = rep
    if player == WHITE:
        return np.argwhere(layout == WHITE_KING)[0]
    elif player == BLACK:
        try:
            return np.argwhere(layout == BLACK_KING)[0]
        except:
            raise


def king_valid_actions(pos, layout, color):
    valid_action = []
    if color == WHITE:
        action_space = AGENT_ACTION_SPACE
    else:
        action_space = ENV_ACTION_SPACE
    for action_id, direction in ACTION_MOVE_DIRECTION.items():
        if not action_id in action_space:
            continue
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
            continue
        valid_action.append(get_action_from_move(direction, color))
    return valid_action


def get_action_from_move(move, color):
    return MOVE_ACTION[move][color]


def get_attaking_mask(rep):
    layout, color, _ = rep
    attaking_mask = []
    assert color==WHITE
    pos = runnable_position(rep)
    for action_id, direction in ACTION_MOVE_DIRECTION.items():
        if not action_id in AGENT_ACTION_SPACE:
            continue
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
            attaking_mask.append(running_pos.copy())
    return attaking_mask


def checkmate(rep):
    attakig_mask = get_attaking_mask((rep[0], WHITE, 0))
    opposite_pos = runnable_position((rep[0], BLACK, 0))
    if any((opposite_pos == att).all() for att in attakig_mask):
        return True
    else:
        return False
    # layout, color, _ = rep
    # if BLACK_KING not in layout:
    #     return True
    # else:
    #     return False


### Instances
def generate_gird(key):
    height, width, cell_agent, cell_target = LAYOUTS[key]
    grid = np.full((height, width), EMPTY, dtype=object)
    grid[cell_agent] = WHITE_KING
    grid[cell_target] = BLACK_KING
    return grid

LAYOUTS = {
    0: (4, 8, (0, 0), (3, 5)),
    1: (8, 4, (3, 3), (0, 0)),
    2: (7, 7, (0, 0), (5, 5)),
    3: (10, 10, (3, 3), (0, 0)),
    4: (11, 4, (3, 3), (0, 0)),
    5: (8, 9, (3, 3), (0, 0)),
    6: (4, 4, (3, 3), (0, 0)),
    7: (4, 4, (0, 0), (3, 3)),
}