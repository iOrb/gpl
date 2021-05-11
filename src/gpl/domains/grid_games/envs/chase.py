import sys

import numpy as np
from gpl.utils import Bunch
import copy

WHITE = 1
BLACK = 2

EMPTY = 'empty'
BLACK_KING = 'black_king'
WHITE_KING = 'white_king'
WALL = 'wall'

SIMPLIFIED_OBJECT = {
    EMPTY:'.',
    BLACK_KING:'T',
    WHITE_KING:'A',
    WALL:'W',
}

ALL_TOKENS = [EMPTY, BLACK_KING, WHITE_KING, WALL]

COLOR_TO_PIECES = {
    WHITE: [WHITE_KING,],
    BLACK: [BLACK_KING,],
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


AGENT_ACTION_SPACE = {
    # UP,
    # DOWN,
    # RIGHT,
    # LEFT,
    LEFTUP,
    RIGHTUP,
    RIGHTDOWN,
    LEFTDOWN,
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

MAX_ACTIONS_BY_TURN = {
    WHITE:1,
    BLACK:1,
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

# Begin Chase =================================

class Env(object):
    def __init__(self, params):
        self.params = params

    def act(self, rep, action):
        layout = rep.grid
        assert rep.nact < MAX_ACTIONS_BY_TURN[rep.player]
        assert not terminated(rep)
        valid_actions = self.available_actions(rep)
        assert action in valid_actions
        if not isinstance(action, tuple):
            return self.__rep_after_move(rep, action)
        else:
            # the agent is putting a WALL
            new_rep = copy.deepcopy(rep)
            l = new_rep.grid
            assert l[action] == EMPTY
            l[action] = WALL
            if rep.nact + 1 < MAX_ACTIONS_BY_TURN[rep.player]:
                new_rep.grid = l
                new_rep.nact += 1
                return self.__update_rep(new_rep)
            else:
                new_rep.grid = l
                new_rep.nact = 0
                new_rep.player = opposite_color(rep.player)
                return self.__update_rep(new_rep)

    def __rep_after_move(self, rep, action):
        new_rep = copy.deepcopy(rep)
        l = new_rep.grid
        pos = runnable_position(rep.grid, rep.player)
        running_pos = np.add(pos, ACTION_MOVE_DIRECTION[action])
        assert not np.any(running_pos < 0)
        try:
            next_cell = l[running_pos[0], running_pos[1]]
        except IndexError:
            print("Index error")
            sys.exit(1)
        old_r, old_c = pos
        new_r, new_c = running_pos
        piece = l[old_r, old_c]
        # if l[new_r, new_c] != WHITE_KING:  # chaser can not be catched!
        #     l[new_r, new_c] = piece
        l[new_r, new_c] = piece
        l[old_r, old_c] = EMPTY
        if rep.nact + 1 < MAX_ACTIONS_BY_TURN[rep.player]:
            new_rep.grid = l
            new_rep.nact += 1
            return self.__update_rep(new_rep)
        else:
            new_rep.grid = l
            new_rep.nact = 0
            new_rep.player = opposite_color(rep.player)
            return self.__update_rep(new_rep)

    def __update_rep(self, rep):
        updated_rep = rep.to_dict()
        if Env.check_game_status(rep) == 1:
            updated_rep['goal'] = True
        if self.params.can_build_walls and WALL in rep.grid:
            updated_rep['wall_one'] = False
        return Bunch(updated_rep)

    @staticmethod
    def get_simplified_objects():
        return SIMPLIFIED_OBJECT

    @staticmethod
    def check_game_status(rep):
        if catched(rep):
            return 1
        else:
            return 0

    def available_actions(self, rep):
        layout = rep.grid
        actions = []
        if rep.player == WHITE:
            c0 = np.argwhere(layout == WHITE_KING)[0]
            actions += PIECE_VALID_ACTIONS[WHITE_KING](c0, layout, self.params)
        elif rep.player == BLACK:
            c0 = np.argwhere(layout == BLACK_KING)[0]
            actions += PIECE_VALID_ACTIONS[BLACK_KING](c0, layout, self.params)
        return actions

    def player2_policy(self, rep):
        assert (BLACK_KING in rep.grid)
        assert (rep.player == BLACK)
        wk_r, wk_c = np.argwhere(rep.grid == WHITE_KING)[0]
        bk_r, bk_c = np.argwhere(rep.grid == BLACK_KING)[0]
        valid_actions = self.available_actions(rep)
        assert valid_actions
        if wk_r < bk_r:
            if DOWN in valid_actions:
                return DOWN
        else:
            if UP in valid_actions:
                return UP
        if wk_c < bk_c:
            if RIGHT in valid_actions:
                return RIGHT
        else:
            if LEFT in valid_actions:
                return LEFT
        return np.random.choice(valid_actions)

    def get_action_space(self):
        if not self.params.can_build_walls:
            return AGENT_ACTION_SPACE
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
        rep['nact'] = 0
        rep['player'] = WHITE
        rep['goal'] = False
        rep['deadend'] = False
        return Bunch(rep)


# Helper mehtods =================================

def terminated(rep):
    if catched(rep):
        return 1
    else:
        return 0

def runnable_position(layout, player):
    if player == WHITE:
        return np.argwhere(layout == WHITE_KING)[0]
    elif player == BLACK:
        return np.argwhere(layout == BLACK_KING)[0]

def catched(rep):
    attakig_mask = get_white_king_attaking_mask(rep)
    bk_pos = runnable_position(rep.grid, BLACK)
    if attakig_mask[bk_pos[0], bk_pos[1]]:
        return True
    else:
        return False

def king_valid_actions(pos, layout, color, params):
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
        if next_cell in WALL:
            continue
        if next_cell in COLOR_TO_PIECES[color]:
            continue
        if next_cell in COLOR_TO_PIECES[opposite_color(color)]:
            continue
        valid_action.append(action_id)
    if params.can_build_walls:
        # if color == WHITE:
        if color == WHITE and not WALL in layout:
            emptys = np.argwhere(layout == EMPTY)
            for r, c in emptys:
                valid_action.append((r, c))
    return valid_action

def get_white_king_attaking_mask(rep):
    layout = rep.grid
    attaking_mask = attaking_mask = np.full(rep.grid.shape, False, dtype=bool)
    pos = runnable_position(rep.grid, WHITE)
    for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        running_pos = np.array(pos)
        running_pos += direction
        if np.any(running_pos < 0):
            continue
        try:
            next_cell = layout[running_pos[0], running_pos[1]]
        except IndexError:
            continue
        if next_cell in COLOR_TO_PIECES[WHITE]:
            continue
        if next_cell in WALL:
            continue
        elif next_cell == EMPTY or 'king' in next_cell:
            attaking_mask[running_pos[0],running_pos[1]] = True
        else:
            assert next_cell in COLOR_TO_PIECES[opposite_color(rep.player)]
            attaking_mask[running_pos[0],running_pos[1]] = True
            continue
    return attaking_mask

### Instances
def generate_gird(key):
    height, width, cell_agent, cell_target = LAYOUTS[key]
    grid = np.full((height, width), EMPTY, dtype=object)
    grid[cell_agent] = WHITE_KING
    grid[cell_target] = BLACK_KING
    return grid

LAYOUTS = {
    0: (4, 6, (0, 0), (3, 5)),
    1: (4, 6, (3, 5), (0, 0)),
    2: (6, 4, (5, 3), (0, 0)),
    3: (6, 6, (0, 5), (5, 0)),
    4: (8, 4, (6, 3), (0, 0)),
    5: (7, 7, (0, 0), (5, 5)),
    6: (10, 10, (3, 3), (0, 0)),
    7: (11, 4, (3, 3), (0, 0)),
    8: (8, 9, (3, 3), (0, 0)),
    9: (4, 4, (3, 3), (0, 0)),
    10: (20, 21, (0, 0), (3, 3)),
    11: (20, 20, (0, 1), (3, 3)),
    12: (40, 40, (0, 1), (30, 30)),
    13: (40, 40, (30, 30), (0, 1)),
    14: (3, 3, (0, 0), (2, 2)),
    15: (4, 6, (3, 5), (1, 1)),
    16: (7, 7, (6, 3), (3, 4)),
}
