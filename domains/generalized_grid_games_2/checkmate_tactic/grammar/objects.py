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
    'general': {BLACK_KING,
                WHITE_KING,
                WHITE_QUEEN},
    'empty': EMPTY,
    'player': Bunch({'w': "white",
                     'b': "black"}),
    'margin':   {'m0': "top-margin",
                 'm1': "bottom-margin",
                 'm2': "right-margin",
                 'm3': "left-margin",
                 'm4': "rightup-corner",
                 'm5': "rightdown-corner",
                 'm6': "leftup-corner",
                 'm7': "leftdown-corner",}
})

