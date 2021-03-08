from generalization_grid_games.envs import chase as ec


E = ec.EMPTY
T = ec.TARGET
A = ec.AGENT
W = ec.WALL
U = ec.UP_ARROW
D = ec.DOWN_ARROW
L = ec.LEFT_ARROW
R = ec.RIGHT_ARROW


layout0 = [
    [W, W, W, W, W, W, W,],
    [W, E, E, T, E, E, W],
    [W, E, E, E, E, E, W,],
    [W, E, E, E, E, E, W,],
    [W, E, A, E, E, E, W,],
    [W, E, E, E, E, E, W,],
    [W, E, E, E, E, E, W,],
    [W, E, E, E, E, E, W,],
    [W, W, W, W, W, W, W,],
    [W, W, W, R, L, U, D],
]

layout1 = [
    [W, W, W, W, W, W, W, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, T, E, A, E, W],
    [W, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W],
    [W, W, W, W, U, D, L, R],
]

layout2 = [
    [W, W, W, W, W, W, W],
    [W, E, E, E, E, E, W],
    [W, E, E, E, T, E, W],
    [W, E, E, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, E, A, E, E, E, W],
    [W, W, W, W, W, W, W],
    [R, W, L, W, D, W, U],
]

layout3 = [
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, A, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, T, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    [W, W, W, W, W, W, W, W, W, W, W, W, R, L, D, U],
]

layout4 = [
    [W, W, W, W, W, W, W, W, W, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, T, E, E, E, E, E, W],
    [W, E, E, E, A, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W, W, W],
    [W, W, W, W, W, W, U, D, L, R],
]

layout5 = [
    [W, W, W, W, W, W, W],
    [W, E, E, E, T, E, W],
    [W, E, E, E, E, E, W],
    [W, E, A, E, E, E, W],
    [W, W, W, W, W, W, W],
    [W, W, W, D, U, R, L],
]

layout6 = [
    [W, W, W, R, L, D, U, W, W, W, W],
    [W, W, W, W, W, W, W, W, W, W, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, A, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, T, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W, W, W, W],
]

layout7 = [
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, A, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, T, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    [D, W, L, W, W, W, W, W, W, W, W, W, W, W],
    [R, W, U, W, W, W, W, W, W, W, W, W, W, W],
]

layout8 = [
    [W, W, W, W, W],
    [W, E, E, E, W],
    [W, E, E, E, W],
    [W, E, E, E, W],
    [W, E, E, E, W],
    [W, E, E, E, W],
    [W, E, E, E, W],
    [W, E, E, E, W],
    [W, E, E, E, W],
    [W, E, E, E, W],
    [W, E, T, E, W],
    [W, E, A, E, W],
    [W, E, E, E, W],
    [W, E, E, E, W],
    [W, E, E, E, W],
    [W, W, W, W, W],
    [W, U, D, L, R],
]

layout9 = [
    [W, W, W, W, W, W, W, W, W, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, A, E, E, E, E, E, E, W],
    [W, E, E, E, T, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W, W, W],
    [W, W, W, W, W, W, U, D, L, R],
]

layout10 = [
    [W, W, W, W, W, W, W, W,],
    [W, E, E, E, E, E, E, W,],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, A, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, T, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W],
    [W, W, W, W, U, D, L, R],
]

layout11 = [
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    [W, T, E, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, A, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    [W, W, W, W, U, D, L, R, W, W, W, W, W, W, W, W, W],
]

layout12 = [
    [W, W, W, W, W, W, W, W, W, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, T, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, E, E, A, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W, W, W],
    [W, D, U, W, W, W, W, L, R, W],
]

layout13 = [
    [W, W, W, W, W, W, W,],
    [W, E, E, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, T, E, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, E, E, E, A, E, W],
    [W, E, E, E, E, E, W],
    [W, W, W, W, W, W, W],
    [W, W, W, U, D, L, R],
]

layout14 = [
    [W, W, W, W, U, L, D, R, W, W, W],
    [W, W, W, W, W, W, W, W, W, W, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, A, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, E, T, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W, W, W, W],
]

layout15 = [
    [W, W, W, W, W, W, W, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, T, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, A, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W],
    [W, W, D, U, L, R, W, W],
]


layout16 = [
    [W, W, W, W, W, W, W],
    [W, E, E, E, E, E, W],
    [W, E, E, A, E, E, W],
    [W, E, E, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, E, T, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, W, W, W, W, W, W],
    [W, W, U, D, L, R, W],
]

layout17 = [
    [W, W, L, R, U, D, W],
    [W, W, W, W, W, W, W],
    [W, E, E, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, E, E, E, E, E, W],
    [W, E, E, A, E, E, W],
    [W, E, E, E, T, E, W],
    [W, E, E, E, E, E, W],
    [W, W, W, W, W, W, W],
]

layout18 = [
    [W, W, W, W, W, W, W, W, W, W, W, W],
    [W, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, A, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, T, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W, W, W, W, W],
    [W, W, D, U, L, R, W, W, W, W, W, W],
]

layout19 = [
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, A, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, T, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, E, E, E, E, E, E, E, E, E, E, E, E, E, W],
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    [W, W, W, D, U, L, R, W, W, W, W, W, W, W, W],
]

layout20 = [
    [W, W, W, W],
    [W, A, E, W],
    [W, E, T, W],
    [W, W, W, W],
    [D, U, L, R],
]

layout21 = [
    [W, W, W, W, W],
    [W, A, E, E, W],
    [W, E, E, E, W],
    [W, E, E, T, W],
    [W, W, W, W, W],
    [W, D, U, L, R],
]

layout22 = [
    [W, W, W, W, W],
    [W, A, E, E, W],
    [W, E, E, T, W],
    [W, W, W, W, W],
    [W, D, U, L, R],
]

# 6 x 7
l23 = [
    [W, W, W, W, W, W],
    [W, A, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, T, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l24 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, T, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l25 = [
    [W, W, W, W, W, W],
    [W, A, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, T, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l26 = [
    [W, W, W, W, W, W],
    [W, A, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, T, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l27 = [
    [W, W, W, W, W, W],
    [W, A, E, E, E, W],
    [W, E, E, E, T, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l28 = [
    [W, W, W, W, W, W],
    [W, A, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, T, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l29 = [
    [W, W, W, W, W, W],
    [W, A, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, T, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l30 = [
    [W, W, W, W, W, W],
    [W, A, E, E, E, W],
    [W, E, E, E, E, W],
    [W, T, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l31 = [
    [W, W, W, W, W, W],
    [W, A, E, T, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l32 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, A, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, T, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l23 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, T, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l33 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, A, E, E, E, W],
    [W, E, E, T, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l34 = [
    [W, W, W, W, W, W],
    [W, A, E, E, E, W],
    [W, E, T, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l35 = [
    [W, W, W, W, W, W],
    [W, A, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, T, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l36 = [
    [W, W, W, W, W, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, T, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l37 = [
    [W, W, W, W, W, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, T, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l38 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, T, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l39 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, A, E, T, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l40 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, E, T, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l41 = [
    [W, W, W, W, W, W],
    [W, E, E, T, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l42 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, A, E, E, W],
    [W, T, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l43 = [
    [W, W, W, W, W, W],
    [W, E, E, E, A, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, T, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l44 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, A, E, W],
    [W, E, E, E, E, W],
    [W, T, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l45 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, A, E, W],
    [W, E, E, E, T, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l46 = [
    [W, W, W, W, W, W],
    [W, E, T, E, E, W],
    [W, E, E, A, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l47 = [
    [W, W, W, W, W, W],
    [W, E, E, E, A, W],
    [W, E, E, E, E, W],
    [W, E, T, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l48 = [
    [W, W, W, W, W, W],
    [W, E, E, E, A, W],
    [W, E, E, E, E, W],
    [W, T, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l49 = [
    [W, W, W, W, W, W],
    [W, E, E, E, A, W],
    [W, T, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l50 = [
    [W, W, W, W, W, W],
    [W, E, E, E, A, W],
    [W, E, T, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l51 = [
    [W, W, W, W, W, W],
    [W, E, E, E, A, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, T, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l52 = [
    [W, W, W, W, W, W],
    [W, E, E, E, A, W],
    [W, E, E, E, E, W],
    [W, E, E, E, T, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l53 = [
    [W, W, W, W, W, W],
    [W, E, E, E, A, W],
    [W, E, E, E, E, W],
    [W, E, E, T, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l54 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, A, W],
    [W, E, E, E, E, W],
    [W, T, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l55 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, A, E, W],
    [W, T, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l56 = [
    [W, W, W, W, W, W],
    [W, E, E, E, A, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, T, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l57 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, A, E, W],
    [W, E, E, E, E, W],
    [W, E, T, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l58 = [
    [W, W, W, W, W, W],
    [W, T, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, A, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l59 = [
    [W, W, W, W, W, W],
    [W, T, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, A, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l60 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, T, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, A, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l61 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, T, E, E, E, W],
    [W, E, E, A, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l62 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, T, E, E, W],
    [W, E, E, A, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l63 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, T, W],
    [W, E, E, A, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l64 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, A, E, W],
    [W, E, T, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l65 = [
    [W, W, W, W, W, W],
    [W, E, T, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, A, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l66 = [
    [W, W, W, W, W, W],
    [W, E, T, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, A, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l67 = [
    [W, W, W, W, W, W],
    [W, E, E, T, E, W],
    [W, E, E, E, E, W],
    [W, E, E, A, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l68 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, T, E, A, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l69 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, T, E, A, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l70 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, T, E, E, W],
    [W, E, E, A, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l71 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, T, E, W],
    [W, E, E, E, A, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l72 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, T, E, A, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l72 = [
    [W, W, W, W, W, W],
    [W, E, E, E, T, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, A, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l73 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, T, W],
    [W, E, E, E, E, W],
    [W, A, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l74 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, T, W],
    [W, A, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l75 = [
    [W, W, W, W, W, W],
    [W, E, T, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, A, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l76 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, T, E, E, W],
    [W, E, E, E, E, W],
    [W, A, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l77 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, T, E, W],
    [W, A, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l78 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, T, E, E, W],
    [W, A, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l79 = [
    [W, W, W, W, W, W],
    [W, E, E, E, T, W],
    [W, E, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l80 = [
    [W, W, W, W, W, W],
    [W, E, T, E, E, W],
    [W, E, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l81 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, A, E, T, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l82 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, T, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l83 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, T, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l84 = [
    [W, W, W, W, W, W],
    [W, E, E, T, E, W],
    [W, E, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l85 = [
    [W, W, W, W, W, W],
    [W, E, E, T, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l86 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, T, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l87 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, T, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l88 = [
    [W, W, W, W, W, W],
    [W, E, T, E, E, W],
    [W, E, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l89 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, T, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l90 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, T, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l91 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, E, A, E, T, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l92 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, T, W],
    [W, E, E, E, E, W],
    [W, A, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l93 = [
    [W, W, W, W, W, W],
    [W, E, E, E, E, W],
    [W, E, E, E, T, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l94 = [
    [W, W, W, W, W, W],
    [W, E, E, T, E, W],
    [W, E, E, E, E, W],
    [W, E, E, E, E, W],
    [W, A, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]
l95 = [
    [W, W, W, W, W, W],
    [W, E, E, T, E, W],
    [W, E, E, E, E, W],
    [W, E, A, E, E, W],
    [W, E, E, E, E, W],
    [W, W, W, W, W, W],
    [W, W, D, U, L, R],
]


# LAYOUTS = [l23, l24, l25, l26, l27, l28, l29, l30, l31, l32, l33, l34, l35, l36, l37, l38, l39, l40, l41, l42,
#            l43, l44, l45, l46, l47, l48, l49, l50, l51, l52, l53, l54, l55, l56, l57, l58, l59, l60, l61, l62,
#            l62, l64, l65, l66, l67, l68, l69, l70, l71, l72, l73, l74, l75, l76, l77, l78, l79, l80, l81, l89,
#            l90, l91, l92, l93, l94, l95]

LAYOUTS = [layout0, layout1, layout2, layout3, layout4, layout5, layout6, layout7, layout8, layout9, layout10,
           layout11, layout12, layout13, layout14, layout15, layout16, layout17, layout18, layout19, layout20,
           layout21, layout22]

