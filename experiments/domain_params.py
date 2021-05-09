from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import CELL_S, COL_S, ROW_S


shoot_params = Bunch({
    'domain_name': 'shoot',
    'use_player_as_feature': False,
    'map_cells': True,
    'use_diagonals_for_map_cells': True,
    'use_adjacency': True,
    'sorts_to_use': {COL_S, ROW_S, CELL_S}
})

space_invaders_params = Bunch({
    'domain_name': 'space_invaders',
    'use_player_as_feature': False,
    'map_cells': False,
    'use_diagonals_for_map_cells': False,
    'use_adjacency': False,
    'sorts_to_use': {COL_S, ROW_S},
})



