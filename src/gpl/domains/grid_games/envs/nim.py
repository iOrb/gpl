import random
import sys
from gpl.utils import Bunch
from ..grammar.objects import TOKEN, EMPTY, TOP_TOKEN, BOTTOM_TOKEN

import numpy as np
import copy

PLAYER_1 = 1
PLAYER_2 = 2

SIMPLIFIED_OBJECT = {
    EMPTY:' . ',
    TOKEN:' t ',
    TOP_TOKEN:' T ',
    BOTTOM_TOKEN:' B ',
}

ALL_TOKENS = [EMPTY, TOKEN]

opposite_player = lambda c: PLAYER_2 if c == PLAYER_1 else PLAYER_1

# Unary predicates
ONLY_ONE_LEFT = 'only_one_token_left'

# Begin Chase =================================

class Env(object):
    def __init__(self, params):
        self.params = params

    def act(self, rep, action):
        assert not terminated(rep)
        layout = rep.grid
        try:
            next_cell = layout[action[0], action[1]]
        except:
            raise IndexError
        new_rep = copy.deepcopy(rep)
        l = layout_after_action(layout, action)
        new_rep.grid = l
        new_rep.nact = 0
        new_rep.player = opposite_player(rep.player)
        return self.__update_rep(new_rep)

    def __update_rep(self, rep):
        updated_rep = rep.to_dict()
        if self.check_game_status(rep) == 1:
            updated_rep['goal'] = True
        elif self.check_game_status(rep) == -1:
            updated_rep['deadend'] = True
        if ONLY_ONE_LEFT in self.params.unary_predicates:
            ntokens = np.count_nonzero(rep.grid == TOKEN)
            updated_rep[ONLY_ONE_LEFT] = True if ntokens == 1 else False
        updated_rep['nmoves'] += 1
        return Bunch(updated_rep)

    def check_game_status(self, rep):
        if self.params.last_player_win:
            if not grid_have_tokens(rep.grid):
                if rep.player == PLAYER_2:
                    return 1
                else:
                    return -1
            else:
                return 0
        else:
            if not grid_have_tokens(rep.grid):
                if rep.player == PLAYER_2:
                    return -1
                else:
                    return 1
            else:
                return 0

    @staticmethod
    def available_actions(rep):
        layout = rep.grid
        actions = []
        tokens = np.argwhere((layout == TOKEN) | (layout == TOP_TOKEN) | (layout == BOTTOM_TOKEN))
        for pos in tokens:
            actions.append((pos[0], pos[1]))
        return actions

    @staticmethod
    def player2_policy(rep):
        valid_actions = Env.available_actions(rep)
        return random.choice(valid_actions)

    @staticmethod
    def get_action_space():
        return None

    @staticmethod
    def get_simplified_objects():
        return SIMPLIFIED_OBJECT

    @staticmethod
    def encode_op(rep, op):
        piece = rep.grid[op[0], op[1]]
        assert piece not in EMPTY
        o = copy.deepcopy(op)
        return "{}.{}".format(o[0], o[1])

    def init_instance(self, key):
        rep = {u: False for u in self.params.unary_predicates}
        rep['grid'] = generate_gird(key)
        rep['player'] = PLAYER_1
        rep['goal'] = False
        rep['deadend'] = False
        rep['nmoves'] = 0
        return Bunch(rep)


# Helper mehtods =================================

def terminated(rep):
    return True if not grid_have_tokens(rep.grid) else False

def grid_have_tokens(grid):
    if (TOP_TOKEN in grid) or (TOKEN in grid) or (BOTTOM_TOKEN in grid):
        return True
    else:
        return False

def layout_after_action(layout, action):
    new_layout = layout.copy()
    new_layout[:action[0] + 1, action[1]] = EMPTY
    if TOKEN in new_layout[:, action[1]]:
        new_layout[action[0] + 1, action[1]] = TOP_TOKEN
    return new_layout

### Instances
def generate_gird(key):
    height, width, piles = \
        LAYOUTS_TWO_PILE_NIM[key]
    assert len(piles) == width
    grid = np.full((height, width), EMPTY, dtype=object)
    for i, size_p in enumerate(piles):
        grid[height - size_p, i] = TOP_TOKEN
        grid[(height - size_p + 1):height, i] = TOKEN
        grid[height - 1, i] = BOTTOM_TOKEN
    return grid


LAYOUTS_TWO_PILE_NIM = {
    0: (3, 2, (2, 1)),
    1: (20, 2, (10, 15)),
    2: (20, 2, (15, 10)),
    3: (15, 2, (10, 11)),
    4: (5, 2, (4, 1)),
    5: (40, 2, (10, 15)),
    6: (25, 2, (10, 15)),
    7: (5, 2, (3, 2)),
    8: (6, 2, (4, 5)),
    9: (8, 2, (7, 5)),
    10: (50, 2, (48, 47)),
    11: (6, 2, (5, 4)),
}

LAYOUTS_THREE_PILE_NIM = {
    0: (3, 3, (2, 2, 3)),
    1: (20, 3, (10, 10, 12)),
    2: (20, 3, (12, 12, 15)),
    3: (20, 3, (3, 3, 5)),
    4: (20, 3, (4, 4, 5)),
    5: (6, 3, (5, 4, 4)),
}

LAYOUTS_FOUR_PILE_NIM = {
    0: (3, 4, (2, 4, 4, 2)),
    1: (20, 4, (10, 15, 15, 10)),
    2: (20, 4, (14, 15, 15, 14)),
    3: (20, 4, (9, 10, 10, 9)),
    4: (20, 4, (13, 14, 14, 13)),
    5: (6, 4, (4, 5, 5, 4)),
}

PIRAMIDS_FOUR_PILE_NIM = {
    0: (4, 5, (1, 2, 3, 2, 1)),
    1: (5, 7, (1, 2, 3, 4, 3, 2, 1)),
    2: (6, 9, (1, 2, 3, 4, 5, 4, 3, 2, 1)),
}

PILES_ORDERED = {
    0: (5, 3, (1, 3, 5)),
    1: (7, 4, (1, 3, 5, 7)),
    2: (9, 5, (1, 3, 5, 7, 9)),
    3: (11, 6, (1, 3, 5, 7, 9, 11)),
    4: (13, 7, (1, 3, 5, 7, 9, 11, 13)),
    5: (15, 8, (1, 3, 5, 7, 9, 11, 13, 15)),
}