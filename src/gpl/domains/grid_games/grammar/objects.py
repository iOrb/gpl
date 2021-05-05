from gpl.utils import Bunch
from ..envs.pick_packages import AGENT, PACKAGE, PIT
from ..envs.deliver import DESTINY, PACKAGE, AGENT, AGENT_WITH_PACKAGE, AGENT_IN_DESTINY_WITH_PACKAGE, AGENT_IN_DESTINY_WITHOUT_PACKAGE

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

OBJECTS_DELIVER = Bunch({
    'general': {DESTINY,
                PACKAGE,
                AGENT,
                AGENT_WITH_PACKAGE,
                AGENT_IN_DESTINY_WITH_PACKAGE,
                AGENT_IN_DESTINY_WITHOUT_PACKAGE},
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
        'deliver': OBJECTS_DELIVER,
    }[domain_name]