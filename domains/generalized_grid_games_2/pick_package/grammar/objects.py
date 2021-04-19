from domains.utils import split_all_chars
from gpl.utils import Bunch
import numpy as np
# from generalization_grid_games_2.envs import checkmate_tactic as ct

EMPTY = 'empty'
AGENT = 'agent'
PACKAGE = 'package'
OBSTACLE = 'obstacle'
ALL_TOKENS = [EMPTY, AGENT, PACKAGE, OBSTACLE]


OBJECTS = Bunch({
    'general': {AGENT,
                PACKAGE,
                OBSTACLE},
    'empty': EMPTY,
    'margin':   {'m0': "top-margin",
                 'm1': "bottom-margin",
                 'm2': "right-margin",
                 'm3': "left-margin",
                 'm4': "rightup-corner",
                 'm5': "rightdown-corner",
                 'm6': "leftup-corner",
                 'm7': "leftdown-corner",}
})

