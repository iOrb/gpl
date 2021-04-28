from .grammar.objects import OBJECTS
import numpy as np
from .config import no_king_piece
from .grammar.objects import WHITE_TOWER, WHITE_QUEEN
import json

def unserialize_layout(filename):
    with open(filename, 'r') as f:
        l = np.array(json.loads(f.read()), dtype=object)
    l = np.where(l == WHITE_QUEEN, no_king_piece, l)
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