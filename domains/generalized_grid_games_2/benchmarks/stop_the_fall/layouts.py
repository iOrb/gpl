from generalization_grid_games.envs import stop_the_fall as stf


E = stf.EMPTY
R = stf.RED
F = stf.FALLING
S = stf.STATIC
A = stf.ADVANCE
D = stf.DRAWN


layout0 = [
    [E, E, E, E, E, F, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, R, R, E, E],
    [E, E, E, R, R, E, E, R, R, E, E],
    [E, E, E, R, R, E, E, R, R, E, E],
    [S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, A, S, S]
]

layout1 = [
    [E, E, E, F, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [R, R, R, E, R, R, R, R, R, R, R, R],
    [R, R, R, E, R, R, R, R, R, R, R, R],
    [R, R, R, E, R, R, R, R, R, R, R, R],
    [R, R, R, E, R, R, R, R, R, R, R, R],
    [R, R, R, E, R, R, R, R, R, R, R, R],
    [R, R, R, E, R, R, R, R, R, R, R, R],
    [S, S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S, A]
]

layout2 = [
    [E, E, E, E, E, E, E, E, F, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, R, R, E, E, E, E],
    [E, E, E, E, E, E, R, R, E, E, E, E],
    [E, E, E, E, E, E, R, R, E, E, E, E],
    [E, E, E, E, E, E, R, R, E, E, E, E],
    [E, E, E, E, E, E, R, R, E, E, E, E],
    [E, E, E, E, E, E, R, R, E, E, E, E],
    [S, S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S, A]
]

layout3 = [
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, F, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, R, R, R, R, R, R],
    [E, E, E, E, E, E, R, R, R, R, R, R],
    [E, E, E, E, E, E, R, R, R, R, R, R],
    [E, E, E, E, E, E, R, R, R, R, R, R],
    [E, E, S, S, S, S, S, S, S, S, S, S],
    [E, E, S, S, S, S, S, S, S, S, S, S],
    [E, E, S, S, S, S, S, S, S, S, S, S],
    [E, E, S, S, S, S, S, S, S, S, S, S],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [S, S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S, A]
]

layout4 = [
    [E, E, E, E, E, E, F, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [R, R, R, R, R, R, E, R, R, R, R, R, R, R, R, R, R],
    [S, S, S, S, S, S, S, S, S, S, S, S, S, S, S, S, A]
]

layout5 = [
    [E, E, E, E, E, E, E, F, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [R, R, E, E, R, E, R, E, R, E, E, R],
    [R, R, E, R, R, R, R, E, R, R, R, R],
    [S, S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S, A]
]

layout6 = [
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, F, E, E],
    [E, E, E, E, E],
    [E, R, E, R, E],
    [E, R, E, R, E],
    [E, R, E, R, E],
    [E, R, E, R, E],
    [E, R, E, R, E],
    [E, R, E, R, E],
    [E, R, E, R, E],
    [S, S, S, S, S],
    [A, S, S, S, S],
]

layout7 = [
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, S, S, S],
    [E, R, R, E, E, F, E, E, E, E, E, E],
    [E, S, S, E, R, E, R, E, E, E, E, E],
    [E, E, E, E, S, S, S, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, S, E, S, S, E, S, S, S],
    [E, E, S, S, S, S, S, S, S, S, S, S],
    [R, R, S, S, S, S, S, S, S, S, S, S],
    [R, R, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S, A]
]

layout8 = [
    [E, E, E, E, E, A, E, E, E, E, E, E, E, E, E, E],
    [S, S, S, S, S, S, S, S, S, S, S, S, S, S, S, S],
    [E, E, E, E, E, E, E, E, F, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, R, R, R, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, R, R, R, E, E, E, E, E, E, E, E],
    [S, S, S, S, S, S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S, S, S, S, S, S],
]

layout9 = [
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, F, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, R, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, R, E, R, E, E, E, E],
    [E, E, E, E, E, E, E, R, E, R, E, E, E, E],
    [S, S, S, S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S, A, S, S]
]

layout10 = [
    [E, E, E, F, E, E, E],
    [E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E],
    [S, E, E, E, E, E, S],
    [R, S, E, E, E, S, R],
    [S, R, S, E, S, R, S],
    [R, S, R, E, R, S, R],
    [R, R, S, E, S, R, R],
    [R, R, R, E, R, R, R],
    [S, S, S, S, S, S, S],
    [S, S, S, S, S, S, A]
]

layout11 = [
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, F, E, E, E, E, E, E, E, E, E],
    [E, S, E, S, E, E, E, E, E, E, E, E],
    [E, S, E, S, E, E, E, E, E, E, E, E],
    [E, S, E, S, E, E, E, E, E, E, E, E],
    [E, S, E, S, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E],
    [E, R, E, R, E, E, E, E, E, E, E, E],
    [E, R, E, R, E, E, E, E, E, E, E, E],
    [S, S, S, S, S, S, S, S, S, S, S, S],
    [S, S, A, S, S, S, S, S, S, S, S, S],
]

layout12 = [
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, S, S, S, E, E, E, E, E],
    [E, E, E, E, E, E, E, S, A, S, E, E, E, E, E],
    [E, E, E, E, E, E, E, S, S, S, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, F, E, E, E, E, E, E, E, E, E],
    [R, R, R, R, R, E, E, E, E, E, E, E, E, E, E],
    [R, R, R, R, R, E, E, E, E, E, E, E, E, E, E],
    [S, S, S, S, S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S, S, S, S, S],
]

layout13 = [
    [E, E, E, E, E, E, E, R, R, R, R],
    [E, E, E, E, E, F, E, R, R, R, R],
    [E, E, E, E, E, E, E, R, R, R, R],
    [E, E, E, E, E, E, E, R, R, R, R],
    [E, E, E, E, E, E, E, R, R, R, R],
    [R, R, R, R, E, E, E, E, E, E, E],
    [R, R, R, R, E, E, E, E, E, E, E],
    [R, R, R, R, E, E, E, E, E, E, E],
    [R, R, R, R, E, E, E, E, E, E, E],
    [R, R, R, R, R, E, R, R, R, R, R],
    [R, R, R, R, R, E, R, R, R, R, R],
    [S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, A, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S],
]

layout14 = [
    [E, E, E, E, F, E, E, E, E, E, S, A],
    [E, E, E, E, E, E, E, E, E, E, S, S],
    [S, S, S, S, E, E, E, E, E, E, E, E],
    [R, R, R, R, E, E, E, E, E, E, E, E],
    [S, S, S, S, E, E, E, E, E, E, E, E],
    [R, R, R, R, E, E, E, E, E, E, E, E],
    [S, S, S, S, E, E, E, E, E, E, E, E],
    [R, R, R, R, E, E, E, E, E, E, E, E],
    [S, S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S, S, S],
]

layout15 = [
    [E, E, E, E, E, E, E, F, E, E],
    [E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, R, E, R, E],
    [E, E, E, E, E, E, S, E, S, E],
    [E, E, E, E, E, E, R, E, R, E],
    [E, E, E, E, E, E, S, E, S, E],
    [E, E, E, E, E, E, R, E, R, E],
    [S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, S, S, S, S, S],
    [S, S, A, S, S, S, S, S, S, S],
]

layout16 = [
    [E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, F, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, R, E, R, E, R, E, R, E, E, E],
    [E, E, E, R, E, R, E, R, E, R, E, E, E],
    [E, E, E, R, E, R, E, R, E, R, E, E, E],
    [S, S, S, S, S, S, S, S, S, S, S, S, S],
    [S, S, S, S, S, A, S, S, S, S, S, S, S],
    [E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E, E, E, E],
]

layout17 = [
   [S, E, S, E, E, F, S, E, S, E],
   [E, S, E, S, E, E, E, S, E, S],
   [S, E, S, E, E, E, S, E, S, E],
   [E, S, E, S, E, E, E, S, E, S],
   [S, E, S, E, E, E, S, E, S, E],
   [E, S, E, S, E, E, E, S, E, S],
   [S, E, S, E, R, E, S, E, S, E],
   [E, S, E, S, R, E, E, S, E, S],
   [S, E, S, R, R, E, S, E, S, E],
   [S, S, S, S, S, S, S, S, S, S],
   [S, S, A, S, S, S, S, S, S, S],
]

layout18 = [
   [R, R, E, E, R, R, E, F, E, E, E, E],
   [R, R, E, E, R, R, E, E, E, E, E, E],
   [E, E, R, R, E, E, E, E, E, E, E, E],
   [E, E, R, R, E, E, E, E, R, E, E, E],
   [R, R, E, E, R, R, E, E, R, R, E, E],
   [R, R, E, E, R, R, E, E, R, R, R, E],
   [E, E, R, R, E, E, E, E, R, R, R, R],
   [E, E, R, R, E, E, E, E, R, R, R, R],
   [S, S, S, S, S, S, S, S, S, S, S, S],
   [S, S, A, S, S, S, S, S, S, S, S, S],
   [S, S, S, S, S, S, S, S, S, S, S, S],
]

layout19 = [
    [E, E, E, E, E, E, E],
    [E, E, F, E, E, E, E],
    [E, E, E, E, E, E, E],
    [R, R, E, E, E, E, E],
    [R, R, E, E, E, E, E],
    [S, S, S, E, S, S, S],
    [E, E, E, E, S, A, S],
    [E, E, E, E, S, S, S],
]

layout20 = [
    [E, F],
    [E, E],
    [R, E],
    [S, S],
    [S, A]
]

layout21 = [
    [E, F],
    [R, E],
    [S, A]
]

layout22 = [
    [E, E, F, E, E],
    [E, E, E, E, E],
    [R, R, E, E, E],
    [R, R, E, A, S],
    [R, R, S, S, S],
]

layout_5x5 = {
    0: [[E, E, F, E, E],
        [E, E, E, E, E],
        [R, R, E, E, E],
        [R, R, S, A, S],
        [R, R, S, S, S],],
    1: [[E, E, F, E, E],
        [E, E, E, E, E],
        [R, R, E, R, R],
        [R, R, E, A, S],
        [R, R, S, S, S],],
    2: [[E, E, F, E, E],
        [R, R, E, R, R],
        [R, R, E, R, R],
        [R, R, E, S, S],
        [R, R, E, S, A],],
    3: [[E, E, F, E, E],
        [E, E, E, E, E],
        [R, R, E, E, E],
        [R, R, E, A, S],
        [R, R, E, S, S],],
    4: [[E, E, F, E, E],
        [E, E, E, E, E],
        [R, R, E, E, E],
        [R, R, E, A, S],
        [R, R, E, S, S],],
    5: [[E, E, F, E, E],
        [E, E, E, E, E],
        [R, R, E, E, E],
        [R, R, E, A, S],
        [R, R, E, S, S],],
    6: [[E, E, F, E, E],
        [E, E, E, E, E],
        [R, R, E, E, E],
        [R, R, E, A, S],
        [R, R, E, S, S],],
    7: [[E, E, F, E, E],
        [E, E, E, E, E],
        [R, R, E, E, E],
        [R, R, E, A, S],
        [R, R, E, S, S],],
    8: [[E, E, F, E, E],
        [E, E, E, E, E],
        [R, R, E, E, E],
        [R, R, E, A, S],
        [R, R, E, S, S],],
    9: [[E, E, F, E, E],
        [E, E, E, E, E],
        [R, R, E, E, E],
        [R, R, E, A, S],
        [R, R, E, S, S], ],
    10: [[E, E, F, E, E],
        [E, E, E, E, E],
        [R, R, E, E, E],
        [R, R, E, A, S],
        [R, R, E, S, S], ],
}

LAYOUTS = [layout_5x5.values()]
