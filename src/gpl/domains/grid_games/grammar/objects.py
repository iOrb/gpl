from gpl.utils import Bunch
from ..envs.pick_packages import AGENT, PACKAGE, PIT

EMPTY = 'empty'
BLACK_KING = 'black_king'
WHITE_KING = 'white_king'
NONE = 'none'
PLAYER1 = 1
PLAYER2 = 2

OBJECTS = Bunch({
    'general': {BLACK_KING,
                WHITE_KING},
    'empty': EMPTY,
    'player1': PLAYER1,
    'player2': PLAYER2,
    'none': NONE,
})

OBJECTS_PICK = Bunch({
    'general': {AGENT,
                PACKAGE,
                PIT},
    'empty': EMPTY,
    'player1': PLAYER1,
    'player2': PLAYER2,
    'none': NONE,
})

def get_domain_objects(domain_name):
    return {
        'chase': OBJECTS,
        'shoot': OBJECTS,
        'space_invaders': OBJECTS,
        'pick_packages': OBJECTS_PICK,
    }[domain_name]