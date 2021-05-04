from gpl.utils import Bunch
from gpl.domains.fond_grid_games.grammar.language import CELL_S, COL_S, ROW_S

chase_params = Bunch({
    'domain_name': 'chase',
    'use_player_as_feature': False,
    'map_cells': False,
    'sorts_to_use': {COL_S, ROW_S}
})

shoot_params = Bunch({
    'domain_name': 'shoot',
    'use_player_as_feature': False,
    'map_cells': False,
    'sorts_to_use': {COL_S, ROW_S}
})

space_invaders_params = Bunch({
    'domain_name': 'shoot',
    'use_player_as_feature': False,
    'map_cells': False,
    'sorts_to_use': {COL_S, ROW_S}
})