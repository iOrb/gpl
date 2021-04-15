from .grammar.objects import OBJECTS
import numpy as np

stockfish_default_params = {
    "Write Debug Log": "false",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 1,
    "Ponder": "false",
    "Hash": 16,
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 30,
    "Minimum Thinking Time": 20,
    "Slow Mover": 80,
    "UCI_Chess960": "false",
}

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