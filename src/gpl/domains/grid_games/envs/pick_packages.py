import copy
import random
import sys

import numpy as np

EMPTY = 'empty'
AGENT = 'agent'
PACKAGE = 'package'
PIT = 'pit'

ALL_TOKENS = [EMPTY, PACKAGE, AGENT, PIT]

PLAYER_1 = 1
PLAYER_2 = 2

# Actions IDs

LEFT = 1
RIGHT = 2
DOWN = 3
UP = 4

AGENT_ACTION_SPACE = {
    RIGHT,
    LEFT,
    UP,
    DOWN,
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
    ACTION_MOVE_DIRECTION[UP]: UP,
    ACTION_MOVE_DIRECTION[DOWN]: DOWN,
}

PIECE_VALID_ACTIONS = {
    AGENT: lambda pos, layout: agent_valid_actions(pos, layout),
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
        if not PACKAGE in layout:
            return 1
        elif not AGENT in layout:
            return -1
        else:
            return 0

    @staticmethod
    def available_actions(rep):
        layout, player, nact = rep
        actions = []
        if player == PLAYER_1:
            pos = np.argwhere(layout == AGENT)[0]
            actions += PIECE_VALID_ACTIONS[AGENT](pos, layout)
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
        if next_cell in [PACKAGE]:
            pass
        if next_cell in [PIT]:
            pass
        valid_action.append(action_id)
    return valid_action


def layout_after_agent_action(layout, action_id):
    assert action_id in AGENT_ACTION_SPACE
    l = layout.copy()
    assert AGENT in layout
    pos = np.argwhere(layout == AGENT)[0]
    running_pos = np.add(pos, ACTION_MOVE_DIRECTION[action_id])
    old_r, old_c = pos
    new_r, new_c = running_pos
    piece = l[old_r, old_c]
    if layout[new_r, new_c] != PIT:  # not running into pits!
        l[new_r, new_c] = piece
    # rand = np.random.randint(0, 100)
    # if rand > 70:
    #     l[old_r, old_c] = PIT
    # else:
    #     l[old_r, old_c] = EMPTY
    l[old_r, old_c] = EMPTY
    return l


### Instances


def generate_gird(key):
    height, width, cell_agent, num_packages = LAYOUTS[key]
    grid = np.full((height, width), EMPTY, dtype=object)
    grid.flat[np.random.choice(height*width, 3, replace=False)] = PIT
    grid.flat[np.random.choice(height*width, num_packages, replace=False)] = PACKAGE
    grid[cell_agent] = AGENT
    return grid

LAYOUTS = {
    0: (4, 4, (1, 0), 3),
    1: (4, 4, (2, 2), 3),
    2: (4, 4, (3, 2), 3),
    3: (4, 4, (1, 2), 3),
    4: (10, 4, (2, 2), 5),
    5: (10, 10, (5, 5), 10),
    6: (5, 5, (0, 0), 4),
}













