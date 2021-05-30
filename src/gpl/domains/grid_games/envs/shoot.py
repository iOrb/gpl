import random
import sys

from ..grammar.objects import EMPTY, WHITE_KING, BLACK_KING, PLAYER1, PLAYER2
from ..grammar.language import D1_S, D2_S, COL_S, ROW_S

import numpy as np
from gpl.utils import Bunch
import copy
from ..utils import identify_next_player


WHITE = 1 # player 1
BLACK = 2 # player 2

SIMPLIFIED_OBJECT = {
    EMPTY:'.',
    BLACK_KING:'T',
    WHITE_KING:'A',
}

ALL_TOKENS = [EMPTY, BLACK_KING, WHITE_KING]

PLAYER_TO_PIECES = {
    WHITE: WHITE_KING,
    BLACK: BLACK_KING,
}


opposite_color = lambda c: BLACK if c == WHITE else WHITE

PIECE_VALID_ACTIONS = {
    WHITE_KING: lambda pos, layout, params: king_valid_actions(pos, layout, WHITE, params),
    BLACK_KING: lambda pos, layout, params: king_valid_actions(pos, layout, BLACK, params),
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
SHOOT = 8

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

# Begin Shoot =================================

# check_game_status, act, available_actions

class Env(object):
    def __init__(self, params):
        self.params = params

    def act(self, rep, action):
        layout = rep.grid
        l = layout.copy()
        valid_actions = self.available_actions(rep)
        try:
            assert action in valid_actions
        except:
            raise
        if action == SHOOT and rep.player in self.params.player_can_shoot:
            l = layout_after_shoot(l, rep.player, self.params)
        else:
            pos = runnable_position(rep.grid, rep.player)
            running_pos = np.add(pos, ACTION_MOVE_DIRECTION[action])
            assert not np.any(running_pos < 0)
            try:
                next_cell = l[running_pos[0], running_pos[1]]
            except:
                raise IndexError
            old_r, old_c = pos
            new_r, new_c = running_pos
            piece = l[old_r, old_c]
            l[new_r, new_c] = piece
            l[old_r, old_c] = EMPTY
        new_rep = copy.deepcopy(rep)
        new_rep.grid = l
        if rep.nact + 1 < self.params.max_actions[rep.player]:
            new_rep.nact += 1
        else:
            new_rep.nact = 0
            new_rep.player = opposite_color(rep.player)
        new_rep.next_player = identify_next_player(new_rep, self.params)
        return self.__update_rep(new_rep, rep.player)

    def __update_rep(self, rep, prev_in_act):
        updated_rep = rep.to_dict()
        if self.check_game_status(rep) == 1:
            updated_rep['goal'] = True
        elif self.check_game_status(rep) == -1:
            updated_rep['deadend'] = True
        updated_rep['nmoves'] += 1
        updated_rep['prev_in_act'] = prev_in_act
        return Bunch(updated_rep)

    def available_actions(self, rep):
        layout = rep.grid
        actions = []
        if rep.player == WHITE:
            c0 = np.argwhere(layout == WHITE_KING)[0]
            actions += [a for a in PIECE_VALID_ACTIONS[WHITE_KING](c0, layout, self.params)]
        elif rep.player == BLACK:
            c0 = np.argwhere(layout == BLACK_KING)[0]
            actions += [a for a in PIECE_VALID_ACTIONS[BLACK_KING](c0, layout, self.params)]
        return actions

    def check_game_status(self, rep):
        l = rep.grid.copy()
        if len(self.params.player_can_shoot) > 0:
            if BLACK_KING not in rep.grid:
                return 1
            if WHITE_KING not in rep.grid:
                return -1
            else:
                return 0
        elif check(rep, self.params):
            if BLACK in self.params.player_can_check and rep.prev_in_act == BLACK:
                return -1
            else:
                return 1
        else:
            return 0

    def player2_policy(self, rep):
        layout=rep.grid
        assert BLACK_KING in layout
        valid_actions = self.available_actions(rep)
        r_wk, c_wk = runnable_position(rep.grid, WHITE)
        r_bk, c_bk = runnable_position(rep.grid, BLACK)
        if r_wk - r_bk == 1:
            if UP in valid_actions:
                return UP
        if r_wk - r_bk == -1:
            if DOWN in valid_actions:
                return DOWN
        if c_wk - c_bk == -1:
            if RIGHT in valid_actions:
                return RIGHT
        if c_wk - c_bk == 1:
            if LEFT in valid_actions:
                return LEFT
        if r_wk == r_bk:
            if DOWN in valid_actions:
                return DOWN
            if UP in valid_actions:
                return UP
        if c_wk == c_bk:
            if LEFT in valid_actions:
                return LEFT
            if RIGHT in valid_actions:
                return RIGHT
        return random.choice(valid_actions)

    @staticmethod
    def get_grid(key):
        return generate_gird(key)

    def get_action_space(self):
        return self.params.ava_actions[PLAYER1]

    @staticmethod
    def get_simplified_objects():
        return SIMPLIFIED_OBJECT

    @staticmethod
    def encode_op(rep, op):
        return op

    def init_instance(self, key):
        rep = {u: False for u in self.params.unary_predicates}
        rep['grid'] = generate_gird(key)
        rep['nact'] = 0
        rep['player'] = WHITE
        rep['goal'] = False
        rep['deadend'] = False
        rep['nmoves'] = 0
        rep['prev_in_act'] = WHITE
        rep['next_player'] = identify_next_player(Bunch(rep), self.params)
        return Bunch(rep)


def runnable_position(layout, player):
    if player == WHITE:
        return np.argwhere(layout == WHITE_KING)[0]
    elif player == BLACK:
        return np.argwhere(layout == BLACK_KING)[0]


def layout_after_shoot(layout, player_shooting, params):
    assert WHITE_KING in layout and BLACK_KING in layout
    new_l = layout.copy()
    attakig_mask = get_attaking_mask(new_l, WHITE, params)
    bk_pos = runnable_position(new_l, BLACK)
    if attakig_mask[bk_pos[0], bk_pos[1]]:
        return np.where(new_l == PLAYER_TO_PIECES[opposite_color(player_shooting)], EMPTY, new_l)
    return new_l


def king_valid_actions(pos, layout, player, params):
    valid_action = []
    action_space = params.ava_actions[player]
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
        if next_cell in {WHITE_KING, BLACK_KING}:
            continue
        valid_action.append(MOVE_ACTION[direction])
    if player in params.player_can_shoot:
        l_after = layout_after_shoot(layout, player, params)
        other_player_piece = PLAYER_TO_PIECES[opposite_color(player)]
        if other_player_piece not in l_after:
            valid_action.append(SHOOT)
    return valid_action


def get_attaking_mask(layout, player, params):
    attaking_mask = attaking_mask = np.full(layout.shape, False, dtype=bool)
    assert player == WHITE
    pos = runnable_position(layout, player)
    for action_id, direction in ACTION_MOVE_DIRECTION.items():
        if not action_id in params.attaking_mask:
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
            attaking_mask[running_pos[0], running_pos[1]] = True
    return attaking_mask


def check(rep, params):
    if len(params.player_can_shoot) > 0:
        if WHITE_KING not in rep.grid or BLACK_KING not in rep.grid:
            return True
        else:
            return False
    else:
        attakig_mask = get_attaking_mask(rep.grid, WHITE, params)
        bk_pos = runnable_position(rep.grid, BLACK)
        if attakig_mask[bk_pos[0], bk_pos[1]]:
            return True
        else:
            return False


### Instances

def generate_gird(key):
    height, width, cell_agent, cell_target = LAYOUTS[key]
    grid = np.full((height, width), EMPTY, dtype=object)
    grid[cell_agent] = WHITE_KING
    grid[cell_target] = BLACK_KING
    return grid


LAYOUTS = {
    0: (4, 8, (0, 0), (3, 5)),
    1: (8, 6, (7, 5), (2, 1)),
    2: (7, 7, (0, 0), (5, 5)),
    3: (10, 10, (3, 2), (0, 0)),
    4: (11, 4, (4, 3), (0, 0)),
    5: (8, 9, (6, 3), (0, 0)),
    6: (4, 4, (2, 3), (0, 0)),
    7: (4, 4, (0, 0), (2, 3)),
    8: (20, 20, (0, 0), (16, 19)),
    9: (4, 4, (0, 0), (3, 3)),
    10: (4, 4, (3, 3), (1, 1)),
    11: (5, 5, (4, 4), (1, 1)),
}