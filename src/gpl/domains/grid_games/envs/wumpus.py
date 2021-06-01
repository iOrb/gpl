import random
import sys

import numpy as np
from gpl.utils import Bunch
import copy

from ..grammar.objects import WUMPUS, GOLD, AGENT, EMPTY, PIT, PLAYER1, PLAYER2
from ..utils import identify_next_player


SIMPLIFIED_OBJECT = {
    EMPTY:' . ',
    WUMPUS:' W ',
    AGENT:' A ',
    GOLD:' g ',
    PIT:' * ',
}

TURN_TO_PIECES = {
    PLAYER1: [AGENT,],
    PLAYER2: [WUMPUS,],
}

opposite_player = lambda c: PLAYER2 if c == PLAYER1 else PLAYER1


PIECE_VALID_ACTIONS = {
    AGENT: lambda pos, rep, params: agent_valid_actions(pos, rep, params),
    WUMPUS: lambda pos, rep, params: wumpus_valid_actions(pos, rep, params),
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
    ACTION_MOVE_DIRECTION[UP]: UP,
    ACTION_MOVE_DIRECTION[DOWN]: DOWN,
    ACTION_MOVE_DIRECTION[RIGHT]: RIGHT,
    ACTION_MOVE_DIRECTION[LEFT]: LEFT,
    ACTION_MOVE_DIRECTION[LEFTUP]: LEFTUP,
    ACTION_MOVE_DIRECTION[RIGHTUP]: RIGHTUP,
    ACTION_MOVE_DIRECTION[RIGHTDOWN]: RIGHTDOWN,
    ACTION_MOVE_DIRECTION[LEFTDOWN]: LEFTDOWN,
}

# unary predicates
AT_WUMPUS = 'at_wumpus'
AT_PIT = 'at_pit'


# Begin Wumpus =================================

class Env(object):
    def __init__(self, params):
        self.params = params

    def act(self, rep, action):
        layout = rep.grid
        assert rep.nact < self.params.max_actions[rep.player] + 1
        assert not terminated(rep)
        valid_actions = self.available_actions(rep)
        assert action in valid_actions
        l = layout.copy()
        if rep.player == PLAYER1:
            l, at_wumpus_, at_pit_ = layout_after_agent_action(rep, action, self.params)
        else:
            l, at_wumpus_, at_pit_ = layout_after_wumpus_action(rep, action, self.params)
        new_rep = copy.deepcopy(rep)
        new_rep.grid = l
        if rep.nact < self.params.max_actions[rep.player]:
            new_rep.nact += 1
        else:
            new_rep.nact = 1
            new_rep.player = opposite_player(rep.player)
        if self.params.use_next_player_as_feature:
            new_rep.next_player = identify_next_player(new_rep, self.params)
        setattr(new_rep, AT_WUMPUS, at_wumpus_)
        setattr(new_rep, AT_PIT, at_pit_)
        return self.__update_rep(new_rep)

    def __update_rep(self, rep):
        updated_rep = rep.to_dict()
        gstatus = self.check_game_status(rep)
        if gstatus == 1:
            updated_rep['goal'] = True
        elif gstatus == -1:
            updated_rep['deadend'] = True
        updated_rep['nmoves'] += 1
        return Bunch(updated_rep)

    @staticmethod
    def get_simplified_objects():
        return SIMPLIFIED_OBJECT

    def check_game_status(self, rep):
        if len(gold_positions(rep.grid)) == 0:
            return 1
        elif not agent_alive(rep):
            return -1
        else:
            return 0

    def available_actions(self, rep):
        layout = rep.grid
        actions = []
        if rep.player == PLAYER1:
            try:
                c0 = np.argwhere(layout == AGENT)[0]
            except:
                print('H')
            actions += PIECE_VALID_ACTIONS[AGENT](c0, rep, self.params)
        elif rep.player == PLAYER2:
            c0 = np.argwhere(layout == WUMPUS)[0]
            actions += PIECE_VALID_ACTIONS[WUMPUS](c0, rep, self.params)
        return actions

    def player2_policy(self, rep):
        ava_actions = self.available_actions(rep)
        return np.random.choice(ava_actions)

    def get_action_space(self):
        if not self.params.can_build_walls:
            return self.params.ava_actions[PLAYER1]
        else:
            return None

    @staticmethod
    def encode_op(rep, op):
        if not isinstance(op, tuple):
            return op
        else:
            return "{}_{}.{}".format(WALL, op[0], op[1])

    def init_instance(self, key):
        rep = {u: False for u in self.params.unary_predicates}
        rep['grid'] = generate_gird(key)
        rep['nact'] = 1
        rep['player'] = PLAYER1
        rep['goal'] = False
        rep['nmoves'] = 0
        rep['deadend'] = False
        assert AGENT in rep['grid'] and GOLD in rep['grid']
        rep[AT_WUMPUS] = False
        rep[AT_PIT] = None
        rep['next_player'] = identify_next_player(Bunch(rep), self.params)
        return Bunch(rep)

# Helper mehtods =================================

def terminated(rep):
    if not agent_alive(rep) or len(gold_positions(rep.grid)) == 0:
        return 1
    else:
        return 0


def agent_alive(rep):
    if at_pit(rep) is not None:
        return False
    elif at_wumpus(rep):
        return False
    else:
        return True


def at_wumpus(rep):
    return getattr(rep, AT_WUMPUS)


def at_pit(rep):
    return getattr(rep, AT_PIT)


def agent_valid_actions(pos, rep, params):
    layout = rep.grid
    valid_action = []
    action_space = params.ava_actions[PLAYER1]
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
        if next_cell in {PIT, WUMPUS}:
            continue
        else:
            valid_action.append(action_id)
    return valid_action


def layout_after_agent_action(rep, action, params):
    layout = rep.grid
    assert AGENT in layout
    assert action in params.ava_actions[PLAYER1]
    at_wumpus_ = at_wumpus(rep)
    at_pit_ = at_pit(rep)
    l = layout.copy()
    agent_pos = np.argwhere(layout == AGENT)[0]
    running_pos = np.add(agent_pos, ACTION_MOVE_DIRECTION[action])
    assert not np.any(running_pos < 0)
    try:
        next_cell = l[running_pos[0], running_pos[1]]
    except:
        raise IndexError
    l[agent_pos[0], agent_pos[1]] = EMPTY
    if next_cell not in {PIT, WUMPUS}:
        l[running_pos[0], running_pos[1]] = AGENT
    elif next_cell in WUMPUS:
        at_wumpus_ = True
    elif next_cell in PIT:
        at_pit_ = (running_pos[0], running_pos[1])
    return l, at_wumpus_, at_pit_


def wumpus_valid_actions(pos, rep, params):
    layout = rep.grid
    valid_action = []
    action_space = params.ava_actions[PLAYER2]
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
        if next_cell in {GOLD, PIT}:
            continue
        else:
            valid_action.append(action_id)
    return valid_action


def layout_after_wumpus_action(rep, action, params):
    layout = rep.grid
    assert WUMPUS in layout
    assert action in params.ava_actions[PLAYER2]
    at_wumpus_ = at_wumpus(rep)
    at_pit_ = at_pit(rep)
    l = layout.copy()
    pos = np.argwhere(layout == WUMPUS)[0]
    running_pos = np.add(pos, ACTION_MOVE_DIRECTION[action])
    assert not np.any(running_pos < 0)
    try:
        next_cell = l[running_pos[0], running_pos[1]]
    except:
        raise IndexError
    assert next_cell not in {GOLD, PIT}
    l[pos[0], pos[1]] = EMPTY
    if next_cell in AGENT:
        at_wumpus_ = True
    l[running_pos[0], running_pos[1]] = WUMPUS
    return l, at_wumpus_, at_pit_


def gold_positions(layout):
    return np.argwhere(layout==GOLD)


### Instances

def generate_gird(key):
    height, width, cell_agent, cell_wumpus, pits, golds =\
        LAYOUTS[key]
    grid = np.full((height, width), EMPTY, dtype=object)
    grid[cell_agent] = AGENT
    grid[cell_wumpus] = WUMPUS
    for p_pos in pits:
        grid[p_pos] = PIT
    for g_pos in golds:
        grid[g_pos] = GOLD
    return grid


LAYOUTS = {
    0: (4, 4, (0, 0), (3, 3), {(1, 3), (1, 0), (2, 2), (3, 0), (0, 3)}, {(2, 3)}),
    1: (3, 3, (0, 0), (2, 0), {(1, 2), (1, 0), (2, 2)}, {(1, 2)}),
    2: (6, 6, (4, 5), (4, 0), {(3, 0), (4, 4), (2, 2)}, {(1, 2), (0, 0)}),
    3: (8, 8, (1, 1), (5, 5), {}, {(3, 4), (2, 2), (5, 0)}),
    4: (5, 5, (1, 1), (4, 4), {(0, 1)}, {(4, 0)}),
    5: (4, 4, (0, 0), (3, 3), {}, {(3, 0)}),
    6: (3, 3, (2, 0), (0, 0), {}, {(1, 2)}),
    7: (5, 5, (0, 0), (4, 1), {(2 ,0), (2 ,1), (2 ,2), (0, 4)}, {(2, 4)}),
    8: (4, 4, (2, 3), (3, 0), {(2, 1)}, {(0, 1)}),
    9: (4, 3, (0, 2), (3, 0), {(2, 1), (1, 1)}, {(3, 2), (0, 1)}),
    9: (4, 3, (0, 2), (3, 0), {(2, 1), (1, 1)}, {(3, 2), (0, 1)}),
}



