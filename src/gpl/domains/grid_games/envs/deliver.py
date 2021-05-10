import copy
import random
import sys

import numpy as np

EMPTY = 'empty'
AGENT = 'agent'
PACKAGE = 'package'
DESTINY = 'destiny'
AGENT_WITH_PACKAGE = f'{AGENT}_with_{PACKAGE}'
AGENT_IN_DESTINY_WITH_PACKAGE = f'{AGENT}_in_{DESTINY}_with_{PACKAGE}'
AGENT_IN_DESTINY_WITHOUT_PACKAGE = f'{AGENT}_in_{DESTINY}_without_{PACKAGE}'

SIMPLIFIED_OBJECT = {
    EMPTY:' . ',
    PACKAGE:' P ',
    AGENT:' A ',
    DESTINY:' D ',
    AGENT_WITH_PACKAGE:'A_P',
    AGENT_IN_DESTINY_WITH_PACKAGE:'ADP',
    AGENT_IN_DESTINY_WITHOUT_PACKAGE:'A_D'
}

ALL_TOKENS = [EMPTY, PACKAGE, AGENT, DESTINY, AGENT_WITH_PACKAGE, AGENT_IN_DESTINY_WITH_PACKAGE, AGENT_IN_DESTINY_WITHOUT_PACKAGE]

PLAYER_1 = 1
PLAYER_2 = 2

# Actions IDs

UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3
LEFTUP = 4
RIGHTUP = 5
RIGHTDOWN = 6
LEFTDOWN = 7


AGENT_ACTION_SPACE = {
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
    LEFTUP: (-1, -1),
    RIGHTUP: (-1, 1),
    RIGHTDOWN: (1, 1),
    LEFTDOWN: (1, -1),
}

MOVE_ACTION = {
    ACTION_MOVE_DIRECTION[RIGHT]: RIGHT,
    ACTION_MOVE_DIRECTION[LEFT]: LEFT,
    ACTION_MOVE_DIRECTION[UP]: UP,
    ACTION_MOVE_DIRECTION[DOWN]: DOWN,
}

class Env(object):
    @staticmethod
    def act(rep, action_id):
        layout, player, nact = rep
        assert Env.check_game_status(rep) == 0
        valid_actions = Env.available_actions(rep)
        assert action_id in valid_actions
        l = layout_after_agent_action(layout, action_id)
        return (l, PLAYER_1, 0)

    @staticmethod
    def check_game_status(rep):
        layout, player, nact = rep
        if AGENT_IN_DESTINY_WITH_PACKAGE in layout:
            return 1
        elif AGENT_IN_DESTINY_WITHOUT_PACKAGE in layout:
            return -1
        else:
            return 0

    @staticmethod
    def available_actions(rep):
        layout, player, nact = rep
        actions = []
        if AGENT in layout:
            pos = np.argwhere(layout == AGENT)[0]
        elif AGENT_WITH_PACKAGE in layout:
            pos = np.argwhere(layout == AGENT_WITH_PACKAGE)[0]
        actions += agent_valid_actions(pos, layout)
        return actions

    @staticmethod
    def player2_policy(rep):
        raise RuntimeError("There is not player 2 in this environment")

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
        if next_cell in [DESTINY] and AGENT in layout:
            continue
        if next_cell in [PACKAGE]:
            pass
        valid_action.append(action_id)
    return valid_action


def get_attaking_mask(pos, layout):
    attaking_mask = np.full(layout.shape, False, dtype=bool)
    for direction in ACTION_MOVE_DIRECTION.values():
        running_pos = np.array(pos)
        running_pos += direction
        if np.any(running_pos < 0):
            continue
        try:
            next_cell = layout[running_pos[0], running_pos[1]]
        except IndexError:
            continue
        attaking_mask[running_pos[0], running_pos[1]] = True
    return attaking_mask


def layout_after_agent_action(layout, action_id):
    assert action_id in AGENT_ACTION_SPACE
    l = layout.copy()
    if AGENT in layout:
        pos = np.argwhere(layout == AGENT)[0]
        running_pos = np.add(pos, ACTION_MOVE_DIRECTION[action_id])
        old_r, old_c = pos
        new_r, new_c = running_pos
        if layout[new_r, new_c] == PACKAGE:
            l[new_r, new_c] = AGENT_WITH_PACKAGE
        if layout[new_r, new_c] == DESTINY:  # not running into pits!
            l[new_r, new_c] = AGENT_IN_DESTINY_WITHOUT_PACKAGE
        if layout[new_r, new_c] == EMPTY:
            l[new_r, new_c] = AGENT
        l[old_r, old_c] = EMPTY
    elif AGENT_WITH_PACKAGE in layout:
        pos = np.argwhere(layout == AGENT_WITH_PACKAGE)[0]
        running_pos = np.add(pos, ACTION_MOVE_DIRECTION[action_id])
        old_r, old_c = pos
        new_r, new_c = running_pos
        if layout[new_r, new_c] == DESTINY:
            l[new_r, new_c] = AGENT_IN_DESTINY_WITH_PACKAGE
        if layout[new_r, new_c] == EMPTY:
            l[new_r, new_c] = AGENT_WITH_PACKAGE
        l[old_r, old_c] = EMPTY
    return l


### Instances

def generate_gird(key):
    height, width, cell_destiny, cell_package, cell_agent = LAYOUTS[key]
    grid = np.full((height, width), EMPTY, dtype=object)
    grid[cell_destiny] = DESTINY
    grid[cell_package] = PACKAGE
    grid[cell_agent] = AGENT
    return grid

LAYOUTS = {
    0: (7, 7, (1, 0), (4, 4), (0, 0)),
    1: (7, 7, (4, 4), (0, 0), (4, 4)),
    2: (7, 7, (0, 0), (3, 4), (6, 0)),
    3: (8, 8, (5, 5), (3, 6), (4, 4)),
    4: (9, 8, (1, 0), (4, 4), (0, 0)),
    5: (4, 4, (1, 0), (3, 3), (0, 0)),
    6: (6, 6, (5, 4), (0, 0), (5, 5)),
}













