from gpl.utils import Bunch

NONE = 'none'
PLAYER1 = 1
PLAYER2 = 2

# WHITE_KING = 'AGENT'
WHITE_KING = 'white_king'
# BLACK_KING = 'TARGET'
BLACK_KING = 'black_king'
WHITE_QUEEN = 'white_queen'
WHITE_TOWER = 'white_rook'
MARTIAN = 'martian'
# TARGET_MARTIAN = 'martian'
TARGET_MARTIAN = 'target_martian'
PACKAGE = 'pet'
DESTINY = 'destiny'
PIT = 'pit'
AGENT = 'agent'
EMPTY = 'empty'
WALL = 'wall'
TOKEN = 'token'
TOP_TOKEN = 'top_token'
BOTTOM_TOKEN = 'bottom_token'
WUMPUS = 'wumpus'
GOLD = 'gold'
TARGET_GOLD = 'target_gold'
WHITE_ATTACKED = 'white_attacked'
BLACK_ATTACKED = 'black_attacked'


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
                WHITE_TOWER,
                WHITE_ATTACKED,
                BLACK_ATTACKED},
    'empty': EMPTY,
    'player1': PLAYER1,
    'player2': PLAYER2,
    'none': NONE,
})

OBJECTS_WUMPUS = Bunch({
    'general': {AGENT,
                WUMPUS,
                GOLD,
                TARGET_GOLD,
                PIT},
    'empty': EMPTY,
    'player1': PLAYER1,
    'player2': PLAYER2,
    'none': NONE,
})

OBJECTS_NIM = Bunch({
    'general': {
        TOKEN,
        f'{TOKEN}-0',
        f'{TOKEN}-1',
        f'{TOKEN}-2',
        TOP_TOKEN,
        f'{TOP_TOKEN}-0',
        f'{TOP_TOKEN}-1',
        f'{TOP_TOKEN}-2',
        BOTTOM_TOKEN,
        f'{BOTTOM_TOKEN}-0',
        f'{BOTTOM_TOKEN}-1',
        f'{BOTTOM_TOKEN}-2',
    },
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


OBJECTS_DELIVERY = Bunch({
    'general': {AGENT,
                PACKAGE,
                DESTINY,
                PIT},
    'empty': EMPTY,
    'player1': PLAYER1,
    'player2': PLAYER2,
    'none': NONE,
})

MARGINS = {
    'm0': 'margin_0',
    'm1': 'margin_1',
    'm2': 'margin_2',
    'm3': 'margin_3',
    'm4': 'margin_4',
    'm5': 'margin_5',
    'm6': 'margin_6',
    'm7': 'margin_7',
}

def get_domain_objects(domain_name):
    return {
        'chase': OBJECTS_CHASE,
        'nim': OBJECTS_NIM,
        'shoot': OBJECTS,
        'space_invaders': OBJECTS_SPACE,
        'checkmate_tactic': OBJECTS_CHECK,
        'wumpus': OBJECTS_WUMPUS,
        'delivery': OBJECTS_DELIVERY,
    }[domain_name]