

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

GRID_DIRECTIONS = {
    CELL_S: ALL_GRID_DIRECTIONS,
    ROW_S: [UP, DOWN],
    COL_S: [RIGHT, LEFT],
    D1_S: [RIGHT, LEFT],
    D2_S: [RIGHT, LEFT],
}
