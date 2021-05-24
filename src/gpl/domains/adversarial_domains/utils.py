from .grammar.objects import OBJECTS, BLACK_KING, WHITE_KING
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