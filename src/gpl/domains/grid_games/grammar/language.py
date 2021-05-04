CELL_S = 'cell'
ROW_S = 'row'
COL_S = 'col'

CONST = {
    CELL_S: lambda r, c: f'{CELL_S}{r}-{c}',
    ROW_S: lambda r, c: f'{ROW_S}{r}',
    COL_S: lambda r, c: f'{COL_S}{c}',
}

ALL_GRID_DIRECTIONS = ['up', 'rightup', 'right', 'rightdown', 'down', 'leftdown', 'left', 'leftup']
UP, RIGHTUP, RIGHT, RIGHTDOWN, DOWN, LEFTDOWN, LEFT, LEFTUP = [d for d in ALL_GRID_DIRECTIONS]
ADJACENT = 'adjacent'

GRID_DIRECTIONS = {
    CELL_S: ALL_GRID_DIRECTIONS,
    ROW_S: [UP, DOWN],
    COL_S: [RIGHT, LEFT],
}
