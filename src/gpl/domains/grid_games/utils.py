from .grammar.objects import PLAYER1, PLAYER2
import numpy as np
import json
import os.path
from .grammar.objects import MARGINS

def identify_margin(r, c, nrows, ncols):
    if r < 0 and 0 <= c < ncols:
        return MARGINS['m0']
    if r == nrows and 0 <= c < ncols:
        return MARGINS['m1']
    if 0 <= r < nrows and c == ncols:
        return MARGINS['m2']
    if 0 <= r < nrows and c < 0:
        return MARGINS['m3']
    if r < 0 and c == ncols:
        return MARGINS['m4']
    if r == nrows and c == ncols:
        return MARGINS['m5']
    if r < 0 and c < 0:
        return MARGINS['m6']
    if r == nrows and c < 0:
        return MARGINS['m7']


def in_top(r, c, nrows, ncols):
    return r == 0


def in_bottom(r, c, nrows, ncols):
    return r == nrows - 1


def in_right_most(r, c, nrows, ncols):
    return c == ncols - 1


def in_left_most(r, c, nrows, ncols):
    return c == 0


def identify_next_player(rep, params):
    opposite_player = lambda c: PLAYER2 if c == PLAYER1 else PLAYER1
    if rep.nact < params.max_actions[rep.player]:
        return rep.player
    else:
        return opposite_player(rep.player)

def in_grid(r, c, nrows, ncols, use_margins=False):
    if (nrows > r >= 0 and ncols > c >= 0):
        return True
    elif use_margins and (nrows >= r >= -1 and ncols >= c >= -1):
        return True
    else:
        return False


