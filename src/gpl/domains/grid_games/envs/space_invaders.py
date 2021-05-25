import copy
import random
import sys

import numpy as np
from gpl.utils import Bunch
from ..grammar.objects import TARGET_MARTIAN, MARTIAN, AGENT, EMPTY

WHITE = 1
BLACK = 2


SIMPLIFIED_OBJECT = {
    EMPTY:'.',
    MARTIAN:'m',
    TARGET_MARTIAN:'M',
    AGENT:'A',
}

ALL_TOKENS = [EMPTY, MARTIAN, TARGET_MARTIAN, AGENT]

COLOR_TO_PIECES = {
    WHITE: [AGENT,],
    BLACK: [MARTIAN, TARGET_MARTIAN],
}

opposite_color = lambda c: BLACK if c == WHITE else WHITE

# Actions IDs

SHOOT = 0
LEFT = 1
RIGHT = 2
DOWN = 3
UP = 4

AGENT_ACTION_SPACE = {
    SHOOT,
    RIGHT,
    LEFT,
}

MARTIANS_ACTION_SPACE = {
    RIGHT,
    LEFT,
    DOWN,
    UP,
}

ACTION_MOVE_DIRECTION = {
    RIGHT: (0, 1),
    LEFT: (0, -1),
    DOWN: (1, 0),
    UP: (-1, 0),
}

MOVE_ACTION = {
    ACTION_MOVE_DIRECTION[RIGHT]: RIGHT,
    ACTION_MOVE_DIRECTION[LEFT]: LEFT,
}

PIECE_VALID_ACTIONS = {
    AGENT: lambda pos, layout, params: agent_valid_actions(pos, layout, params),
    MARTIAN: lambda layout, params: martians_valid_actions(layout, params),
}

class Env(object):
    def __init__(self, params):
        self.params = params

    def act(self, rep, action_id):
        layout = rep.grid
        assert rep.nact < self.params.max_actions[rep.player] + 1
        assert not terminated(rep)
        if rep.player == WHITE:
            l = layout_after_agent_action(layout, action_id, self.params)
        elif rep.player == BLACK:
            l = layout_after_env_action(layout, action_id) if action_id else layout
        new_rep = copy.deepcopy(rep)
        new_rep.grid = l
        if rep.nact < self.params.max_actions[rep.player]:
            new_rep.nact += 1
        else:
            new_rep.nact = 1
            new_rep.player = opposite_color(rep.player)
        return self.__update_rep(new_rep)

    def __update_rep(self, rep):
        updated_rep = rep.to_dict()
        if Env.check_game_status(rep) == 1:
            updated_rep['goal'] = True
        if Env.check_game_status(rep) == -1:
            updated_rep['deadend'] = True
        updated_rep['nmoves'] += 1
        return Bunch(updated_rep)

    @staticmethod
    def check_game_status(rep):
        layout = rep.grid
        if not MARTIAN in layout and not TARGET_MARTIAN in layout:
            return 1
        elif not AGENT in layout:
            return -1
        else:
            return 0

    def available_actions(self, rep):
        layout = rep.grid
        actions = []
        if rep.player == WHITE:
            pos = np.argwhere(layout == AGENT)[0]
            actions += PIECE_VALID_ACTIONS[AGENT](pos, layout, self.params)
        elif rep.player == BLACK:
            actions += PIECE_VALID_ACTIONS[MARTIAN](layout, self.params)
        if not actions:
            actions.append(None)
        return actions

    def player2_policy(self, rep):
        valid_actions = self.available_actions(rep)
        if not valid_actions:
            return None
        return random.choice(valid_actions)
        # return DOWN

    @staticmethod
    def get_action_space():
        return AGENT_ACTION_SPACE

    @staticmethod
    def get_grid(key):
        return generate_gird(key)

    @staticmethod
    def get_simplified_objects():
        return SIMPLIFIED_OBJECT

    @staticmethod
    def encode_op(rep, op):
        return op

    def init_instance(self, key):
        rep = {u: False for u in self.params.unary_predicates}
        rep['grid'] = generate_gird(key)
        rep['nact'] = 1
        rep['player'] = WHITE
        rep['goal'] = False
        rep['deadend'] = False
        rep['nmoves'] = 0
        return Bunch(rep)

# Helper mehtods =================================

def terminated(rep):
    layout = rep.grid
    assert AGENT in layout or MARTIAN in layout or TARGET_MARTIAN in layout
    if AGENT not in layout or (MARTIAN not in layout and TARGET_MARTIAN not in layout):
        return True
    else:
        return False


def martians_valid_actions(layout, params):
    nrows, ncols = layout.shape
    martians = np.where((layout == MARTIAN) | (layout == TARGET_MARTIAN))
    valid_actions = set(MARTIANS_ACTION_SPACE)
    for r, c in zip(martians[0], martians[1]):
        if DOWN in valid_actions and not params.adv_can_move_down:
            valid_actions.remove(DOWN)
        if DOWN in valid_actions and r == nrows - 2:
            valid_actions.remove(DOWN)
        if DOWN in valid_actions and not params.adv_can_kill_agent and r == nrows - 3:
            valid_actions.remove(DOWN)
        if UP in valid_actions and not params.adv_can_move_up:
            valid_actions.remove(UP)
        if UP in valid_actions and r == 0:
            valid_actions.remove(UP)
        if LEFT in valid_actions and c <= 0:
            valid_actions.remove(LEFT)
        if RIGHT in valid_actions and c >= ncols - 1:
            valid_actions.remove(RIGHT)
    return valid_actions


def layout_after_env_action(layout, action_id):
    assert TARGET_MARTIAN in layout
    assert action_id in MARTIANS_ACTION_SPACE
    martians_pos = np.argwhere(layout == MARTIAN)
    target_martian_pos = np.argwhere(layout == TARGET_MARTIAN)[0]
    martians_new_pos = []
    for pos in martians_pos:
        running_pos = np.add(pos, ACTION_MOVE_DIRECTION[action_id])
        martians_new_pos.append((running_pos[0], running_pos[1]))
    new_target_martian_pos = np.add(target_martian_pos, ACTION_MOVE_DIRECTION[action_id])
    nrows, ncols = layout.shape
    l = copy.deepcopy(layout)
    l = np.where(l == MARTIAN, EMPTY, l)
    l = np.where(l == TARGET_MARTIAN, EMPTY, l)
    for pos in martians_new_pos:
        l[pos] = MARTIAN
        if pos[0] == nrows-2:
            l = np.where(l == AGENT, EMPTY, l)
    l[new_target_martian_pos[0], new_target_martian_pos[1]] = TARGET_MARTIAN
    if new_target_martian_pos[0] == nrows-2:
        l = np.where(l == AGENT, EMPTY, l)
    return l


def agent_valid_actions(pos, layout, params):
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
        if next_cell in MARTIAN or next_cell in TARGET_MARTIAN:
            continue
        valid_action.append(action_id)
    if params.agent_has_to_shoot:
        if SHOOT in AGENT_ACTION_SPACE:
            num_martias = len(np.argwhere((layout == MARTIAN) | (layout == TARGET_MARTIAN)))
            layout_after_shoot = layout_after_agent_shoot(pos, layout)
            num_martias_after_shoot = len(np.argwhere((layout_after_shoot == MARTIAN) | (layout_after_shoot == TARGET_MARTIAN)))
            if num_martias != num_martias_after_shoot:
                valid_action.append(SHOOT)
    return valid_action


def layout_after_agent_action(layout, action_id, params):
    assert action_id in AGENT_ACTION_SPACE
    if action_id == SHOOT:
        pos = np.argwhere(layout == AGENT)[0]
        return layout_after_agent_shoot(pos, layout)
    else:
        l = copy.deepcopy(layout)
        assert AGENT in layout
        pos = np.argwhere(layout == AGENT)[0]
        running_pos = np.add(pos, ACTION_MOVE_DIRECTION[action_id])
        old_r, old_c = pos
        new_r, new_c = running_pos
        piece = l[old_r, old_c]
        if layout[new_r, new_c] not in {MARTIAN, TARGET_MARTIAN}:  # not running into martians!
            l[new_r, new_c] = piece
        l[old_r, old_c] = EMPTY
        if not params.agent_has_to_shoot:
            return layout_after_agent_shoot(running_pos, l)
        else:
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
            if next_cell in MARTIAN:
                # new_layout[running_pos[0], running_pos[1]] = EMPTY
                # break
                continue # The Agent can not shoot normal martians
            if next_cell in TARGET_MARTIAN:
                new_layout[running_pos[0], running_pos[1]] = EMPTY
                break
    if MARTIAN in new_layout and TARGET_MARTIAN not in new_layout:
        new_layout = set_one_random_target_martian(new_layout)
    return new_layout


def set_one_random_target_martian(layout):
    assert TARGET_MARTIAN not in layout
    if MARTIAN not in layout:
        return layout
    valid_martians = list()
    nrows, ncols = layout.shape
    for c in range(ncols):
        running_pos = np.array((0, c))
        direction = ACTION_MOVE_DIRECTION[DOWN] # down direction (1, 0)
        last_martian_seen = None
        while True:
            try:
                next_cell = layout[running_pos[0], running_pos[1]]
            except IndexError:
                break
            if next_cell in MARTIAN:
                last_martian_seen = running_pos.copy()
            running_pos += direction
        if last_martian_seen is not None:
            valid_martians.append(last_martian_seen)
    # selected_martian_pos = valid_martians[0]
    selected_martian_pos = random.choice(valid_martians)
    l = layout.copy()
    l[selected_martian_pos[0], selected_martian_pos[1]] = TARGET_MARTIAN
    return l


### Instances
def generate_gird(key):
    height, width, col_agent, martian_rows, target_martian_column, martian_columns = LAYOUTS[key]
    grid = np.full((height, width), EMPTY, dtype=object)
    grid[height - 1, col_agent] = AGENT
    for c in martian_columns:
        grid[martian_rows, c] = MARTIAN
    grid = set_one_random_target_martian(grid)
    return grid

LAYOUTS = {
    0: (6, 4, 2, [0], 0, [0, 2, 3]),
    # 1: (6, 4, 2, [0], 2, [0, 2, 3]),
    2: (6, 4, 2, [0], 3, [0, 2, 3]),
    1: (10, 4, 1, [0], 2, [0, 2, 3]),
    2: (10, 10, 1, [0], 3, [0, 2, 3]),
    3: (7, 5, 2, [0], 0, [0, 2, 3]),
    4: (9, 5, 0, [0, 1], 0, [0, 3]),
    5: (20, 8, 4, list(range(6)), 0, [0, 2, 3]),
    6: (20, 10, 0, [0], 2, [0, 2, 3]),
    7: (20, 20, 4, [0], 0, [0, 19]),
    8: (9, 6, 4, [0, 1], 0, [0, 2, 4]),
    9: (6, 10, 5, [0], 5, [5]),
    10: (6, 10, 5, [0], 9, [1, 9]),
    11: (11, 10, 5, [0], 1, [1]),
    12: (6, 10, 5, [0], 9, [9]),
    13: (6, 4, 1, [0], 3, [3]),
    14: (3, 3, 2, [0], 0, [0, 2]),
    15: (5, 5, 2, [0], 4, [0, 4]),
    16: (4, 5, 2, [0, 1], 4, [0, 4]),
    17: (5, 4, 2, [0, 1], 0, [0, 3]),
    18: (4, 5, 3, [0, 1], 0, [0, 4]),
}