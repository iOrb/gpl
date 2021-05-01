from gpl.utils import Bunch

EMPTY = 'empty'
BLACK_KING = 'black_king'
WHITE_KING = 'white_king'
NONE = 'none'

OBJECTS = Bunch({
    'general': {BLACK_KING,
                WHITE_KING},
    'empty': EMPTY,
    'player': Bunch({'w': "white",
                     'b': "black"}),
    'none': NONE,
    'margin':   {'m0': "top-margin",
                 'm1': "bottom-margin",
                 'm2': "right-margin",
                 'm3': "left-margin",
                 'm4': "rightup-corner",
                 'm5': "rightdown-corner",
                 'm6': "leftup-corner",
                 'm7': "leftdown-corner",}
})

