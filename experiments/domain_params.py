from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import CELL_S, COL_S, ROW_S

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
    'domain_name': 'space_invaders',
    'use_player_as_feature': False,
    'map_cells': False,
    'use_diagonals_for_map_cells': True,
    'use_adjacency_for_map_cells': False,
    'sorts_to_use': {COL_S}
})

pick_package_params = Bunch({
    'domain_name': 'pick_packages',
    'use_player_as_feature': False,
    'map_cells': True,
    'use_diagonals_for_map_cells': False,
    'use_adjacency_for_map_cells': False,
    'sorts_to_use': {CELL_S},
})

deliver_params = Bunch({
    'domain_name': 'deliver',
    'use_player_as_feature': False,
    'map_cells': True,
    'use_diagonals_for_map_cells': False,
    'use_adjacency_for_map_cells': False,
    'sorts_to_use': {ROW_S, COL_S, CELL_S},
})