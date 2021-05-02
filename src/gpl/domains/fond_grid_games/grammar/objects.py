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
})

