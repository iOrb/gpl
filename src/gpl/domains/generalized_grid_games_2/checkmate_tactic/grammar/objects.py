from gpl.utils import Bunch

# from generalization_grid_games_2.envs import checkmate_tactic as ct

EMPTY = 'empty'
BLACK_KING = 'black_king'
WHITE_KING = 'white_king'
WHITE_QUEEN = 'white_queen'
WHITE_TOWER = 'white_tower'

OBJECTS = Bunch({
    'general': {BLACK_KING,
                WHITE_KING,
                WHITE_QUEEN,
                WHITE_TOWER},
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

