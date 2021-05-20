from gpl.utils import Bunch
from ..envs.pick_packages import AGENT, PACKAGE, PIT, EMPTY
from ..envs.deliver import DESTINY, PACKAGE, AGENT, AGENT_WITH_PACKAGE, AGENT_IN_DESTINY_WITH_PACKAGE, AGENT_IN_DESTINY_WITHOUT_PACKAGE

NONE = 'none'
PLAYER1 = 1
PLAYER2 = 2

WHITE_KING = 'white_king'
BLACK_KING = 'black_king'
WHITE_QUEEN = 'white_queen'
WHITE_TOWER = 'white_tower'

MARTIAN = 'martian'
TARGET_MARTIAN = 'target_martian'

PACKAGE = 'package'
DESTINY = 'destiny'
PIT = 'pit'
AGENT = 'agent'
EMPTY = 'empty'
WALL = 'wall'

TOKEN = 'token'
TOP_TOKEN = 'top_token'
BOTTOM_TOKEN = 'bottom_token'


OBJECTS = Bunch({
    'general': {BLACK_KING,
                WHITE_KING},
    'empty': EMPTY,
    'player1': PLAYER1,
    'player2': PLAYER2,
    'none': NONE,
})

OBJECTS_SPACE = Bunch({
    'general': {MARTIAN,
                TARGET_MARTIAN,
                AGENT},
    'empty': EMPTY,
    'player1': PLAYER1,
    'player2': PLAYER2,
    'none': NONE,
})

OBJECTS_CHECK = Bunch({
    'general': {BLACK_KING,
                WHITE_KING,
                WHITE_QUEEN,
                WHITE_TOWER,},
    'empty': EMPTY,
    'player1': PLAYER1,
    'player2': PLAYER2,
    'none': NONE,
})

OBJECTS_NIM = Bunch({
    'general': {TOKEN, TOP_TOKEN, BOTTOM_TOKEN},
    'empty': EMPTY,
    'player1': PLAYER1,
    'player2': PLAYER2,
    'none': NONE,
})

OBJECTS_CHASE = Bunch({
    'general': {BLACK_KING,
                WHITE_KING,
                WALL,},
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
        'chase': OBJECTS_CHASE,
        'nim': OBJECTS_NIM,
        'shoot': OBJECTS,
        'space_invaders': OBJECTS_SPACE,
        'pick_packages': OBJECTS_PICK,
        'deliver': OBJECTS_DELIVER,
        'checkmate_tactic': OBJECTS_CHECK,
    }[domain_name]