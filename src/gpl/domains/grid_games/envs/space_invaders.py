import copy
import random
import sys

import numpy as np

WHITE = 1
BLACK = 2

EMPTY = 'empty'
BLACK_KING = 'black_king'
WHITE_KING = 'white_king'

SIMPLIFIED_OBJECT = {
    EMPTY:'.',
    BLACK_KING:'M',
    WHITE_KING:'A',
}

ALL_TOKENS = [EMPTY, BLACK_KING, WHITE_KING]

COLOR_TO_PIECES = {
    WHITE: [WHITE_KING,],
    BLACK: [BLACK_KING,],
}

opposite_color = lambda c: BLACK if c == WHITE else WHITE

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
    WHITE:3,
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
        if color == WHITE:
            l = layout_after_agent_action(layout, action_id)
        elif color == BLACK:
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
        if player == WHITE:
            pos = np.argwhere(layout == WHITE_KING)[0]
            actions += PIECE_VALID_ACTIONS[WHITE_KING](pos, layout)
        elif player == BLACK:
            actions += PIECE_VALID_ACTIONS[BLACK_KING](layout)
        return actions

    @staticmethod
    def player2_policy(rep):
        valid_actions = Env.available_actions(rep)
        assert valid_actions
        return random.choice(valid_actions)

    @staticmethod
    def get_action_space():
        return AGENT_ACTION_SPACE

    @staticmethod
    def get_grid(key):
        return generate_gird(key)

    @staticmethod
    def get_simplified_objects():
        return SIMPLIFIED_OBJECT

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
    nrows, ncols = layout.shape
    for pos in martians_new_pos:
        l[pos] = BLACK_KING
        if pos[0] == nrows-2:
            l = np.where(l == WHITE_KING, EMPTY, l)
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
    if SHOOT in AGENT_ACTION_SPACE:
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
        return layout_after_agent_shoot(running_pos, l)
        # return l


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
    height, width, col_agent, martian_rows, martian_columns = LAYOUTS[key]
    grid = np.full((height, width), EMPTY, dtype=object)
    grid[height - 1, col_agent] = WHITE_KING
    for c in martian_columns:
        grid[martian_rows, c] = BLACK_KING
    return grid

LAYOUTS_ = {
    0: (6, 4, 2, [0], [0]),
    1: (10, 4, 1, [0], [3]),
    2: (10, 10, 1, [0],[9]),
    3: (7, 5, 2, [0], [4]),
    4: (9, 5, 4, [0], [2]),
    5: (20, 8, 6, [0], [1]),
    6: (20, 10, 0, [0], [8]),
    7: (20, 20, 15, [0], [0]),
    8: (9, 6, 0, [0], [5]),
}


LAYOUTS = {
    0: (6, 4, 2, [0], [0, 2, 3]),
    1: (10, 4, 1, [0], [0, 2, 3]),
    2: (10, 10, 1, [0],[0, 2, 3]),
    3: (7, 5, 2, [0], [0, 2, 3]),
    4: (9, 5, 4, [0, 1], [0, 2, 3]),
    5: (20, 8, 4, list(range(6)), [0, 2, 3]),
    6: (20, 10, 0, [0], [0, 2, 3]),
    7: (20, 20, 4, [0], [0, 19]),
    8: (9, 6, 4, [0, 1], [0, 2, 4]),
}