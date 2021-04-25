from .grammar.objects import OBJECTS, BLACK_KING, WHITE_KING
import numpy as np
import json
import os.path


def unserialize_layout(filename):
    with open(filename, 'r') as f:
        l = np.array(json.loads(f.read()), dtype=object)
    l = np.where(l == WHITE_KING, OBJECTS.empty, l)
    l = np.where(l == 'white_queen', WHITE_KING, l)
    return l


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