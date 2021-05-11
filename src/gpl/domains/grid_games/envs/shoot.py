import random
import sys

import numpy as np
from gpl.utils import Bunch
import copy

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

ENV_ACTION_SPACE = {
    UP,
    DOWN,
    RIGHT,
    LEFT,
    # LEFTUP,
    # RIGHTUP,
    # RIGHTDOWN,
    # LEFTDOWN,
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
        assert action in valid_actions
        pos = runnable_position(rep.grid, rep.player)
        running_pos = np.add(pos, ACTION_MOVE_DIRECTION[action])
        assert not np.any(running_pos < 0)
        try:
            next_cell = l[running_pos[0], running_pos[1]]
        except IndexError:
            print("Index error")
            sys.exit(1)
        new_rep = copy.deepcopy(rep)
        old_r, old_c = pos
        new_r, new_c = running_pos
        piece = l[old_r, old_c]
        l[new_r, new_c] = piece
        l[old_r, old_c] = EMPTY
        new_rep.grid = l
        new_rep.player = opposite_color(rep.player)
        return self.__update_rep(new_rep)

    def __update_rep(self, rep):
        updated_rep = rep.to_dict()
        if Env.check_game_status(rep):
            if self.params.adv_can_shoot:
                if rep.player==BLACK:
                    updated_rep['goal'] = True
                else:
                    updated_rep['deadend'] = True
            else:
                updated_rep['goal'] = True
        return Bunch(updated_rep)

    def available_actions(self, rep):
        layout = rep.grid
        actions = []
        if rep.player == WHITE:
            c0 = np.argwhere(layout == WHITE_KING)[0]
            actions += [a for a in PIECE_VALID_ACTIONS[WHITE_KING](c0, layout)]
        elif rep.player == BLACK:
            c0 = np.argwhere(layout == BLACK_KING)[0]
            actions += [a for a in PIECE_VALID_ACTIONS[BLACK_KING](c0, layout)]
        return actions

    @staticmethod
    def check_game_status(rep):
        if checkmate(rep):
            return 1
        if not WHITE_KING in rep.grid:
            return -1
        else:
            return 0

    def player2_policy(self, rep):
        layout=rep.grid
        assert BLACK_KING in layout
        valid_actions = self.available_actions(rep)
        r_wk, c_wk = runnable_position(rep.grid, WHITE)
        r_bk, c_bk = runnable_position(rep.grid, BLACK)
        if r_wk - r_bk == -1:
            if UP in valid_actions:
                return UP
        if r_wk - r_bk == 1:
            if DOWN in valid_actions:
                return DOWN
        if c_wk - c_bk == 1:
            if RIGHT in valid_actions:
                return RIGHT
        if c_wk - c_bk == -1:
            if LEFT in valid_actions:
                return LEFT
        if r_wk - r_bk == -2:
            if DOWN in valid_actions:
                return DOWN
        if r_wk - r_bk == 2:
            if UP in valid_actions:
                return UP
        if c_wk - c_bk == 2:
            if LEF in valid_actions:
                return LEFT
        if c_wk - c_bk == -2:
            if RIGHT in valid_actions:
                return RIGHT
        return random.choice(valid_actions)

    @staticmethod
    def get_grid(key):
        return generate_gird(key)

    @staticmethod
    def get_action_space():
        return AGENT_ACTION_SPACE

    @staticmethod
    def get_simplified_objects():
        return SIMPLIFIED_OBJECT

    @staticmethod
    def encode_op(rep, op):
        if op in AGENT_ACTION_SPACE:
            return op
        else:
            return "wall"
        return "{}_{}.{}".format(WALL, op[0], op[1])

    def init_instance(self, key):
        rep = {u: False for u in self.params.unary_predicates}
        rep['grid'] = generate_gird(key)
        rep['nact'] = 0
        rep['player'] = WHITE
        rep['goal'] = False
        rep['deadend'] = False
        return Bunch(rep)

def runnable_position(layout, player):
    if player == WHITE:
        return np.argwhere(layout == WHITE_KING)[0]
    elif player == BLACK:
        return np.argwhere(layout == BLACK_KING)[0]


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
        valid_action.append(MOVE_ACTION[direction])
    return valid_action



def get_attaking_mask(layout, player):
    attaking_mask = []
    # assert player==WHITE
    pos = runnable_position(layout, player)
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
            if next_cell in COLOR_TO_PIECES[player]:
                break
            attaking_mask.append(running_pos.copy())
    return attaking_mask


def checkmate(rep):
    wk_attakig_mask = get_attaking_mask(rep.grid, WHITE)
    bk_attakig_mask = get_attaking_mask(rep.grid, BLACK)
    bk_pos = runnable_position(rep.grid, BLACK)
    wk_pos = runnable_position(rep.grid, WHITE)
    if any((bk_pos == att).all() for att in wk_attakig_mask):
        return True
    # if any((wk_pos == att).all() for att in bk_attakig_mask):
    #     return True
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
    8: (20, 20, (0, 0), (19, 19)),
}