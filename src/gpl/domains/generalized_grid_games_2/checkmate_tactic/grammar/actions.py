import copy

from .objects import OBJECTS

from generalization_grid_games_2.envs.checkmate_tactic import available_actions, \
    check_game_status, act, WHITE_KING, WHITE_QUEEN, PIECE_VALID_MOVES

import numpy as np

def create_representative_transitions(nrows, ncols):

    ACTION_TX_REPR = dict()

    layout_ = np.full((nrows, ncols), OBJECTS.empty, dtype=object)

    pieces = [WHITE_KING, WHITE_QUEEN]
    color = OBJECTS.player.w

    for piece in pieces:
        for r in range(nrows):
            for c in range(ncols):
                layout = copy.deepcopy(layout_)
                layout[r, c] = piece
                c0 = np.argwhere(layout == piece)[0]
                moves = [(c0, c1) for c1 in PIECE_VALID_MOVES[piece](c0, layout)]
                for op in moves:
                    op_enc = encode_op(piece, op)
                    rep = (layout, color)
                    ACTION_TX_REPR[op_enc] = (rep, act(rep, op))

    return ACTION_TX_REPR



def encode_op(piece, o):
    return "{}_{}.{}_{}.{}".format(piece, o[0][0], o[0][1], o[1][0], o[1][1])