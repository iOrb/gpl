

CELL_S = 'cell'
ROW_S = 'row'
COL_S = 'col'
D1_S = 'd1'
D2_S = 'd2'

CONST = {
    CELL_S: lambda r, c, nrows, ncols: f'{CELL_S}{r}-{c}',
    ROW_S: lambda r, c, nrows, ncols: f'{ROW_S}{r}',
    COL_S: lambda r, c, nrows, ncols: f'{COL_S}{c}',
    D1_S: lambda r, c, nrows, ncols: f'{D1_S}_{c - r + nrows -1}',
    D2_S: lambda r, c, nrows, ncols: f'{D2_S}_{(ncols - 1 - c) - r + nrows -1}',
}

ALL_GRID_DIRECTIONS = ['up', 'rightup', 'right', 'rightdown', 'down', 'leftdown', 'left', 'leftup']
UP, RIGHTUP, RIGHT, RIGHTDOWN, DOWN, LEFTDOWN, LEFT, LEFTUP = [d for d in ALL_GRID_DIRECTIONS]
ADJACENT = 'adjacent'
DISTANCE_2 ='distance_2'
DISTANCE_MORE_THAN_1 ='distance_more_than_1'
CELL_HAS = lambda sort, object: f'{sort}-has-{object}'
CELL_HAS_PIECE_ATTAKED_BY = lambda piece: f'cell-attaked-by-{piece}'
CELL_HAS_COLOR_ATTAKED_BY = lambda color: f'cell-attaked-by-{color}'
CELL_IS_IN = lambda where: f'cell-is-in-{where}'

GRID_DIRECTIONS = {
    CELL_S: ALL_GRID_DIRECTIONS,
    ROW_S: [UP, DOWN],
    COL_S: [RIGHT, LEFT],
    D1_S: [RIGHT, LEFT],
    D2_S: [RIGHT, LEFT],
}

# TEMPORAL, TODO: remove them:
BLACK_KING_AVAILABLE_QUADRANT = 'black_king_available_quadrant'
TOP = 'top'
BOTTOM = 'bottom'