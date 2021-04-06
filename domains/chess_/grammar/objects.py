from domains.utils import split_all_chars
from gpl.utils import Bunch
import numpy as np

OBJECTS = Bunch({
    'general': set(split_all_chars("PNBRQKpnbrqk")),
    'player_marks': {"w": "white",
                     "b": "black"},
    'empty': "empty",
    'none': "none",
})

def array_from_fen(rep):
    """
    input: String from chess.Board.board_fen().  Ex.: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

    :return: 8x8 numpy array.
    """
    state = np.empty((8, 8), dtype=object)
    state[:] = OBJECTS.empty

    split_board = rep.split(" ")[0].split("/")
    row = 0
    for rank in split_board:
        col = 0
        for file in rank:
            if file.isdigit():
                col += int(file)
            else:
                state[row][col] = file
                col += 1
        row += 1
    return state
