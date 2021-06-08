from .grammar.objects import PLAYER1, PLAYER2
import numpy as np
import json
import os.path

def identify_margin(r, c, nrows, ncols):
    if r < 0 and 0 <= c < ncols:
        return OBJECTS.margin['m0']
    if r == nrows and 0 <= c < ncols:
        return OBJECTS.margin['m1']
    if 0 <= r < nrows and c == ncols:
        return OBJECTS.margin['m2']
    if 0 <= r < nrows and c < 0:
        return OBJECTS.margin['m3']
    if r < 0 and c == ncols:
        return OBJECTS.margin['m4']
    if r == nrows and c == ncols:
        return OBJECTS.margin['m5']
    if r < 0 and c < 0:
        return OBJECTS.margin['m6']
    if r == nrows and c < 0:
        return OBJECTS.margin['m7']


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