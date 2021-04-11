from domains.utils import split_all_chars
from gpl.utils import Bunch
import numpy as np
# from generalization_grid_games_2.envs import checkmate_tactic as ct

EMPTY = 'empty'
BLACK_KING = 'black_king'
WHITE_KING = 'white_king'
WHITE_QUEEN = 'white_queen'
HIGHLIGHTED_WHITE_QUEEN = 'highlighted_white_queen'
HIGHLIGHTED_WHITE_KING = 'highlighted_white_king'
HIGHLIGHTED_BLACK_KING = 'highlighted_black_king'

OBJECTS = Bunch({
    'general': {EMPTY,
                HIGHLIGHTED_WHITE_QUEEN,
                BLACK_KING,
                HIGHLIGHTED_WHITE_KING,
                HIGHLIGHTED_BLACK_KING,
                WHITE_KING,
                WHITE_QUEEN},
    'player': Bunch({'w': "white",
                           'b': "black"}),
    'empty': "empty",
    'none': "none",
})