import random
import sys

import numpy as np
from gpl.utils import Bunch
import copy

from ..grammar.objects import AGENT, EMPTY, PIT, PACKAGE, DESTINY, PLAYER1, PLAYER2
from ..utils import identify_next_player


SIMPLIFIED_OBJECT = {
    EMPTY:'.',
    AGENT:'A',
    PACKAGE:'p',
    DESTINY:'D',
    PIT:'*',
}

opposite_player = lambda c: PLAYER2 if c == PLAYER1 else PLAYER1


PLAYER_VALID_ACTIONS = {
    PLAYER1: lambda pos, layout, params: agent_valid_actions(pos, layout, params),
    PLAYER2: lambda layout, params: wumpus_valid_actions(layout, params),
}

ALL_DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# Actions IDs

UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3
LEFTUP = 4
RIGHTUP = 5
RIGHTDOWN = 6
LEFTDOWN = 7

DROP_UP = 8
DROP_DOWN = 9
DROP_RIGHT = 10
DROP_LEFT = 11
DROP_LEFTUP = 12
DROP_RIGHTUP = 13
DROP_RIGHTDOWN = 14
DROP_LEFTDOWN = 15

PICK = 16
DROP = 17

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

ACTION_DROP_DIRECTION = {
    DROP_UP: ACTION_MOVE_DIRECTION[UP],
    DROP_DOWN: ACTION_MOVE_DIRECTION[DOWN],
    DROP_RIGHT: ACTION_MOVE_DIRECTION[RIGHT],
    DROP_LEFT: ACTION_MOVE_DIRECTION[LEFT],
    DROP_LEFTUP: ACTION_MOVE_DIRECTION[LEFTUP],
    DROP_RIGHTUP: ACTION_MOVE_DIRECTION[RIGHTUP],
    DROP_RIGHTDOWN: ACTION_MOVE_DIRECTION[RIGHTDOWN],
    DROP_LEFTDOWN: ACTION_MOVE_DIRECTION[LEFTDOWN],
}

PACKAGES_QUEUE = 'packages_queue'
# unary predicates
HOLDING_PACKAGE = 'holding_pet'
AT_DESTINATION = 'at_destination'
ALL_PETS_DELIVERED = 'all_pets_delivered'


# Begin Wumpus =================================

class Env(object):
    def __init__(self, params):
        self.params = params

    def act(self, rep, action):
        layout = rep.grid
        assert rep.nact < self.params.max_actions[rep.player] + 1
        valid_actions = self.available_actions(rep)
        # assert action in valid_actions
        l = layout.copy()
        if rep.player == PLAYER1:
            l, holding, at_dest = layout_after_agent_action(rep, action, self.params)
        else:
            l, holding, at_dest = layout_after_wumpus_action(rep, action, self.params)
        new_rep = copy.deepcopy(rep)
        new_rep.grid = l
        if rep.nact < self.params.max_actions[rep.player]:
            new_rep.nact += 1
        else:
            new_rep.nact = 1
            new_rep.player = opposite_player(rep.player)
        if self.params.use_next_player_as_feature:
            new_rep.next_player = identify_next_player(new_rep, self.params)
        setattr(new_rep, HOLDING_PACKAGE, holding)
        setattr(new_rep, AT_DESTINATION, at_dest)
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
        if terminated(rep, self.params):
            return 1
        else:
            return 0

    def available_actions(self, rep):
        layout = rep.grid
        actions = []
        if rep.player == PLAYER1:
            c0 = np.argwhere(layout == AGENT)[0]
            actions += PLAYER_VALID_ACTIONS[PLAYER1](c0, rep, self.params)
        elif rep.player == PLAYER2:
            actions += PLAYER_VALID_ACTIONS[PLAYER2](rep, self.params)
        return actions

    def player2_policy(self, rep):
        ava_actions = self.available_actions(rep)
        if not ava_actions:
            return None
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
        layout = generate_gird(key)
        rep['grid'] = layout
        rep['nact'] = 1
        rep['player'] = PLAYER1
        rep['goal'] = False
        rep['nmoves'] = 0
        rep['deadend'] = False
        assert PACKAGE in rep['grid']
        rep[HOLDING_PACKAGE] = False
        rep[AT_DESTINATION] = False
        rep['next_player'] = identify_next_player(Bunch(rep), self.params)
        return Bunch(rep)


# Helper mehtods =================================


def terminated(rep, params):
    if not holding_package(rep) and not any_pet(rep.grid):
        return True
    else:
        return False


def any_pet(layout):
    return len(pets(layout)) > 0


def pets(layout):
    return np.argwhere(layout==PACKAGE)


def at_destination(rep):
    return getattr(rep, AT_DESTINATION)


def holding_package(rep):
    return getattr(rep, HOLDING_PACKAGE)


def agent_valid_actions(pos, rep, params):
    layout = rep.grid
    valid_actions = set()
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
        if next_cell in {PIT, PACKAGE}:
            continue
        if not holding_package(rep) and next_cell in DESTINY:
            continue
        valid_actions.add(action_id)
    if not holding_package(rep):
        assert PACKAGE in layout
        amask = get_mask(np.argwhere(layout == AGENT)[0], layout)
        for pp in pets(rep.grid):
            if amask[pp[0], pp[1]]:
                valid_actions.add(PICK)
                break
    if holding_package(rep) and at_destination(rep):
        valid_actions.add(DROP)
    return list(valid_actions)


def layout_after_agent_action(rep, action, params):
    layout = rep.grid
    assert AGENT in layout
    assert action in params.ava_actions[PLAYER1]
    # layout = rep.grid
    l = layout.copy()
    holding = holding_package(rep)
    at_dest = at_destination(rep)
    if action == PICK:
        assert PACKAGE in layout
        amask = get_mask(np.argwhere(layout==AGENT)[0], layout)
        for pp in pets(layout):
            if amask[pp[0], pp[1]]:
                l[pp[0], pp[1]] = EMPTY
                holding=True
                break
    elif action == DROP:
        holding = False
    else:
        agent_pos = np.argwhere(layout == AGENT)[0]
        running_pos = np.add(agent_pos, ACTION_MOVE_DIRECTION[action])
        assert not np.any(running_pos < 0)
        try:
            next_cell = l[running_pos[0], running_pos[1]]
        except:
            raise IndexError
        if at_dest:
            l[agent_pos[0], agent_pos[1]] = DESTINY
            at_dest=False
        else:
            l[agent_pos[0], agent_pos[1]] = EMPTY
        if next_cell not in {PIT}:
            l[running_pos[0], running_pos[1]] = AGENT
            if next_cell in DESTINY:
                at_dest = True
    return l, holding, at_dest


def wumpus_valid_actions(rep, params):
    holding = holding_package(rep)
    at_dest = at_destination(rep)
    layout = rep.grid
    if not holding:
        return [None]
    valid_actions = []
    if holding:
        pet_pos = pr, pc = np.argwhere(layout == AGENT)[0]
    else:
        pet_pos = pets(layout)[0]
    if at_dest:
        dr, dc = np.argwhere(layout == AGENT)[0]
    else:
        dr, dc = np.argwhere(layout == DESTINY)[0]
    distance = lambda x, xp: abs(x - xp)
    action_space = params.ava_actions[PLAYER2]
    for action_id, direction in ACTION_DROP_DIRECTION.items():
        if not action_id in action_space:
            continue
        running_pos = rpr, rpc = np.add(pet_pos, direction)
        if np.any(running_pos < 0):
            continue
        try:
            next_cell = layout[rpr, rpc]
        except IndexError:
            continue
        if next_cell in {DESTINY, PIT, AGENT}:
            continue
        if distance(rpr, dr) < distance(pr, dr) or distance(rpc, dc) < distance(pc, dc):
            continue
        valid_actions.append(action_id)
    return valid_actions


def layout_after_wumpus_action(rep, action, params):
    # assert action in params.ava_actions[PLAYER2]
    holding = holding_package(rep)
    at_dest = at_destination(rep)
    layout = rep.grid
    if action is None:
        assert not holding or at_dest
        l = layout.copy()
    else:
        if holding:
            pet_pos = np.argwhere(layout == AGENT)[0]
        else:
            pet_pos = pets(layout)[0]
        l = layout.copy()
        next_pet_pos = np.add(pet_pos, ACTION_DROP_DIRECTION[action])
        assert not np.any(next_pet_pos < 0)
        try:
            next_cell = l[next_pet_pos[0], next_pet_pos[1]]
        except:
            raise IndexError
        assert next_cell not in {DESTINY, PIT, AGENT}
        l[next_pet_pos[0], next_pet_pos[1]] = PACKAGE
        if not holding:
            l[pet_pos[0], pet_pos[1]] = EMPTY
        holding=False
    return l, holding, at_dest


def package_pos(layout):
    return np.argwhere((layout==PACKAGE))[0]


def get_mask(pos, layout):
    mask = np.zeros(layout.shape, dtype=bool)
    for direction in ALL_DIRECTIONS:
        running_pos = np.array(pos)
        running_pos += direction
        if np.any(running_pos < 0):
            continue
        try:
            next_cell = layout[running_pos[0], running_pos[1]]
        except IndexError:
            continue
        mask[running_pos[0], running_pos[1]] = True
    return mask


### Instances

def generate_gird(key):
    height, width, cell_agent, cells_pet, cell_destiny =\
        LAYOUTS[key]
    grid = np.full((height, width), EMPTY, dtype=object)
    grid[cell_agent] = AGENT
    grid[cell_destiny] = DESTINY
    PACKAGES_QUEUE = list()
    for c in cells_pet:
        PACKAGES_QUEUE.append(c)
    grid[PACKAGES_QUEUE.pop()] = PACKAGE
    return grid


LAYOUTS = {
    0: (4, 4, (0, 0), {(3, 3)}, (0, 3)),
    1: (6, 6, (0, 5), {(5, 5)}, (0, 0)),
    2: (5, 5, (4, 0), {(0, 0)}, (4, 4)),
    3: (3, 3, (2, 0), {(1, 0), (0, 1)}, (2, 2)),
    4: (4, 4, (0, 0), {(3, 3), (1, 0)}, (0, 3)),
    5: (4, 3, (0, 0), {(3, 2), (1, 0)}, (0, 2)),
}


