import copy
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

# Actions IDs

SHOOT = 0
LEFT = 1
RIGHT = 2
DOWN = 3

AGENT_ACTION_SPACE = {
    SHOOT,
    RIGHT,
    LEFT,
}

MARTIANS_ACTION_SPACE = {
    RIGHT,
    LEFT,
    DOWN,
}

ACTION_MOVE_DIRECTION = {
    RIGHT: (0, 1),
    LEFT: (0, -1),
    DOWN: (1, 0),
}

MAX_ACTIONS_BY_TURN = {
    WHITE:5,
    BLACK:1,
}

MOVE_ACTION = {
    ACTION_MOVE_DIRECTION[RIGHT]: RIGHT,
    ACTION_MOVE_DIRECTION[LEFT]: LEFT,
}

PIECE_VALID_ACTIONS = {
    WHITE_KING: lambda pos, layout: agent_valid_actions(pos, layout),
    BLACK_KING: lambda layout: martians_valid_actions(layout),
}


class Env(object):
    @staticmethod
    def act(rep, action_id):
        layout, color, nact = rep
        assert nact < MAX_ACTIONS_BY_TURN[color]
        assert not terminated(rep)
        valid_actions = Env.available_actions(rep)
        assert action_id in valid_actions
        if color in WHITE:
            l = layout_after_agent_action(layout, action_id)
        elif color in BLACK:
            l = layout_after_env_action(layout, action_id)
        if nact + 1 < MAX_ACTIONS_BY_TURN[color]:
            return (l, color, nact + 1)
        else:
            return (l, opposite_color(color), 0)

    @staticmethod
    def check_game_status(rep):
        layout, player, nact = rep
        assert WHITE_KING in layout or BLACK_KING in layout
        if not BLACK_KING in layout:
            return 1
        elif not WHITE_KING in layout:
            return -1
        else:
            return 0

    @staticmethod
    def available_actions(rep):
        layout, player, nact = rep
        actions = []
        if player == 'white':
            pos = np.argwhere(layout == WHITE_KING)[0]
            actions += PIECE_VALID_ACTIONS[WHITE_KING](pos, layout)
        elif player == 'black':
            actions += PIECE_VALID_ACTIONS[BLACK_KING](layout)
        return actions

    @staticmethod
    def player2_policy(rep):
        assert (BLACK_KING in rep[0])
        assert (rep[1] in BLACK)
        bk = np.argwhere(rep[0] == BLACK_KING)[0]
        wk = np.argwhere(rep[0] == WHITE_KING)[0]
        valid_actions = Env.available_actions(rep)
        assert valid_actions
        return valid_actions[0]

    @staticmethod
    def get_action_space():
        return AGENT_ACTION_SPACE

    @staticmethod
    def get_grid(key):
        return generate_gird(key)

# Helper mehtods =================================

def terminated(rep):
    layout, player, nact = rep
    assert WHITE_KING in layout or BLACK_KING in layout
    if WHITE_KING not in layout or BLACK_KING not in layout:
        return True
    else:
        return False


def martians_valid_actions(layout):
    nrows, ncols = layout.shape
    martians = np.where(layout == BLACK_KING)
    valid_actions = set(MARTIANS_ACTION_SPACE)
    for r, c in zip(martians[0], martians[1]):
        if DOWN in valid_actions and r >= nrows - 1:
            valid_actions.remove(DOWN)
        if LEFT in valid_actions and c <= 0:
            valid_actions.remove(LEFT)
        if RIGHT in valid_actions and c >= ncols - 1:
            valid_actions.remove(RIGHT)
    return valid_actions


def layout_after_env_action(layout, action_id):
    assert BLACK_KING in layout
    assert action_id in MARTIANS_ACTION_SPACE
    l = copy.deepcopy(layout)
    l = np.where(l == BLACK_KING, EMPTY, l)
    martians_pos = np.where(layout == BLACK_KING)
    martians_new_pos = []
    for pos in zip(martians_pos[0], martians_pos[1]):
        running_pos = np.add(pos, ACTION_MOVE_DIRECTION[action_id])
        martians_new_pos.append((running_pos[0], running_pos[1]))
    for pos in martians_new_pos:
        l[pos] = BLACK_KING
    return l


def agent_valid_actions(pos, layout):
    valid_action = []
    for action_id, direction in ACTION_MOVE_DIRECTION.items():
        if not action_id in AGENT_ACTION_SPACE:
            continue
        running_pos = np.add(pos, direction)
        if np.any(running_pos < 0):
            continue
        try:
            next_cell = layout[running_pos[0], running_pos[1]]
        except IndexError:
            continue
        if next_cell in [BLACK_KING]:
            continue
        valid_action.append(action_id)
    valid_action.append(SHOOT)
    return valid_action


def layout_after_agent_action(layout, action_id):
    assert action_id in AGENT_ACTION_SPACE
    if action_id == SHOOT:
        pos = np.argwhere(layout == WHITE_KING)[0]
        return layout_after_agent_shoot(pos, layout)
    else:
        l = copy.deepcopy(layout)
        assert WHITE_KING in layout
        pos = np.argwhere(layout == WHITE_KING)[0]
        running_pos = np.add(pos, ACTION_MOVE_DIRECTION[action_id])
        old_r, old_c = pos
        new_r, new_c = running_pos
        piece = l[old_r, old_c]
        if layout[new_r, new_c] != BLACK_KING:  # not running into martians!
            l[new_r, new_c] = piece
        l[old_r, old_c] = EMPTY
        return l


def layout_after_agent_shoot(pos, layout):
    new_layout = layout.copy()

    for direction in [(-1, 0)]: # always shoot up
        running_pos = np.array(pos)
        while True:
            running_pos += direction
            try:
                next_cell = layout[running_pos[0], running_pos[1]]
            except IndexError:
                break
            if next_cell in BLACK_KING:
                new_layout[running_pos[0], running_pos[1]] = EMPTY
                break

    return new_layout


### Instances
def generate_gird(key):
    height, width, col_agent, martian_rows = LAYOUTS[key]
    grid = np.full((height, width), EMPTY, dtype=object)
    grid[height - 1, col_agent] = WHITE_KING
    grid[martian_rows, :-1] = BLACK_KING
    return grid

LAYOUTS = {
    0: (6, 4, 2, [0]),
    1: (10, 4, 1, [0]),
}













