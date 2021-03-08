from generalization_grid_games.envs import reach_for_the_star as rfts


E = rfts.EMPTY
A = rfts.AGENT
S = rfts.STAR
D = rfts.DRAWN
L = rfts.LEFT_ARROW
R = rfts.RIGHT_ARROW


layout0 = [[S, E, E, E],
           [E, E, E, E],
           [E, E, E, A],
           [D, D, D, D],
           [D, D, L, R],]
layout1 = [[S, E, E, E, E],
           [E, E, E, E, E],
           [E, E, E, A, E],
           [D, D, D, D, D],
           [D, D, L, R, D],]
layout2 = [[E, S, E, E, E],
           [E, E, E, E, E],
           [E, E, E, A, E],
           [D, D, D, D, D],
           [D, D, L, R, D],]
layout3 = [[E, E, E, E, S],
           [E, E, E, E, E],
           [E, E, E, A, E],
           [D, D, D, D, D],
           [D, D, L, R, D],]
layout4 = [[E, E, E, E, S],
           [E, E, E, E, E],
           [E, A, E, E, E],
           [D, D, D, D, D],
           [D, D, L, R, D],]
layout5 = [[E, E, E, S, E],
           [E, E, E, E, E],
           [E, A, E, E, E],
           [D, D, D, D, D],
           [D, D, L, R, D],]
layout6 = [[S, E, E, E, E],
           [E, E, E, E, E],
           [E, A, E, E, E],
           [D, D, D, D, D],
           [D, D, L, R, D],]
layout7 = [[S, E, E, E, E, E],
           [E, E, E, E, E, E],
           [E, E, E, E, E, E],
           [E, E, E, E, E, E],
           [E, A, E, E, E, E],
           [D, D, D, D, D, D],
           [D, D, L, R, D, D],]
layout8 = [[E, E, E, E, E, S],
           [E, E, E, E, E, E],
           [E, E, E, E, E, E],
           [E, E, E, E, E, E],
           [E, A, E, E, E, E],
           [D, D, D, D, D, D],
           [D, D, L, R, D, D],]
layout9 = [[E, E, E, E, E, E],
           [E, E, E, E, S, E],
           [E, E, E, E, E, E],
           [E, E, E, E, E, E],
           [E, A, E, E, E, E],
           [D, D, D, D, D, D],
           [D, D, L, R, D, D],]
layout10 = [[E, E, E, E, E, E],
           [E, S, E, E, E, E],
           [E, E, E, E, E, E],
           [E, E, E, E, E, E],
           [E, E, E, E, A, E],
           [D, D, D, D, D, D],
           [D, D, L, R, D, D],]

# 6x6
layout11 = [[E, E, E, E, E, S],
            [E, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, A, E, E, E, E],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout12 = [[E, E, E, E, E, E],
            [E, E, E, E, S, E],
            [E, E, E, E, E, E],
            [E, A, E, E, E, E],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout13 = [[E, E, E, E, E, S],
            [E, E, E, E, E, E],
            [E, E, E, E, E, E],
            [A, E, E, E, E, E],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout14 = [[E, E, E, E, E, S],
            [E, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, A, E, E, E],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout15 = [[E, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, E, S, E, E],
            [A, E, E, E, E, E],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout16 = [[E, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, E, E, S, E],
            [E, A, E, E, E, E],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout17 = [[E, E, E, E, E, E],
            [E, E, S, E, E, E],
            [E, E, E, E, E, E],
            [E, E, E, E, A, E],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout18 = [[E, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, S, E, E, E, E],
            [E, E, E, E, A, E],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout19 = [[E, S, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, E, E, A, E],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout20 = [[S, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, E, E, A, E],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout21 = [[E, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, S, E, E, E],
            [E, E, E, E, E, A],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout22 = [[E, E, E, E, E, E],
            [E, E, S, E, E, E],
            [E, E, E, E, E, E],
            [E, E, E, E, E, A],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout23 = [[E, E, E, E, E, E],
            [E, E, E, S, E, E],
            [E, E, E, E, E, E],
            [E, E, E, E, E, A],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout24 = [[E, E, E, E, E, E],
            [E, E, E, E, S, E],
            [E, E, E, E, E, E],
            [E, E, E, E, E, A],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout25 = [[S, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, E, E, E, A],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout26 = [[E, E, E, E, E, E],
            [E, S, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, E, E, E, A],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout27 = [[E, E, E, E, E, E],
            [E, S, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, A, E, E, E],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]
layout28 = [[S, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, E, E, E, E],
            [E, E, A, E, E, E],
            [D, D, D, D, D, D],
            [D, D, L, R, D, D],]

# 5x5
layout29 = [[E, E, E, E, S],
            [E, E, E, E, E],
            [E, A, E, E, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout30 = [[E, E, E, E, S],
            [E, E, E, E, E],
            [E, E, A, E, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout31 = [[E, E, E, E, S],
            [E, E, E, E, E],
            [A, E, E, E, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout32 = [[E, E, E, E, E],
            [E, E, E, S, E],
            [E, A, E, E, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout33 = [[E, E, E, E, E],
            [E, E, E, S, E],
            [E, E, A, E, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout34 = [[E, E, E, E, E],
            [E, E, E, S, E],
            [A, E, E, E, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout35 = [[E, E, E, S, E],
            [E, E, E, E, E],
            [E, A, E, E, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout36 = [[E, E, E, S, E],
            [E, E, E, E, E],
            [E, E, A, E, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout37 = [[E, E, E, S, E],
            [E, E, E, E, E],
            [A, E, E, E, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout38 = [[S, E, E, E, E],
            [E, E, E, E, E],
            [E, E, A, E, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout39 = [[S, E, E, E, E],
            [E, E, E, E, E],
            [E, E, E, A, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout40 = [[S, E, E, E, E],
            [E, E, E, E, E],
            [E, E, E, E, A],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout41 = [[E, S, E, E, E],
            [E, E, E, E, E],
            [E, E, A, E, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout42 = [[E, S, E, E, E],
            [E, E, E, E, E],
            [E, E, E, A, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout43 = [[E, S, E, E, E],
            [E, E, E, E, E],
            [E, E, E, E, A],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout34 = [[E, E, E, E, E],
            [E, S, E, E, E],
            [E, E, A, E, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout44 = [[E, E, E, E, E],
            [E, S, E, E, E],
            [E, E, E, A, E],
            [D, D, D, D, D],
            [D, D, L, R, D],]
layout45 = [[E, E, E, E, E],
            [E, S, E, E, E],
            [E, E, E, E, A],
            [D, D, D, D, D],
            [D, D, L, R, D],]

# 4x5
four_five_layouts = {
    0 : [[E, E, E, S],
         [E, E, E, E],
         [E, A, E, E],
         [D, D, D, D],
         [D, D, L, R],],
    1 : [[E, E, E, S],
         [E, E, E, E],
         [A, E, E, E],
         [D, D, D, D],
         [D, L, R, D],],
    2 : [[E, E, S, E],
         [E, E, E, E],
         [A, E, E, E],
         [D, D, D, D],
         [D, L, R, D],],
    3 : [[E, E, S, E],
         [E, E, E, E],
         [E, A, E, E],
         [D, D, D, D],
         [D, L, R, D],],
    4 : [[E, E, E, S],
         [E, E, E, E],
         [E, E, A, E],
         [D, D, D, D],
         [D, L, R, D],],
    5 : [[E, E, E, S],
         [E, E, E, E],
         [E, E, E, A],
         [D, D, D, D],
         [D, L, R, D],],
    6 : [[E, E, S, E],
         [E, E, E, E],
         [E, E, A, E],
         [D, D, D, D],
         [D, L, R, D],],
    7 : [[E, S, E, E],
         [E, E, E, E],
         [E, A, E, E],
         [D, D, D, D],
         [D, L, R, D],],
    8 : [[S, E, E, E],
         [E, E, E, E],
         [A, E, E, E],
         [D, D, D, D],
         [D, L, R, D],],
    9 : [[S, E, E, E],
         [E, E, E, E],
         [E, E, A, E],
         [D, D, D, D],
         [D, D, L, R],],
    10 : [[S, E, E, E],
         [E, E, E, E],
         [E, E, E, A],
         [D, D, D, D],
         [D, D, L, R],],
    11 : [[E, S, E, E],
         [E, E, E, E],
         [E, E, A, E],
         [D, D, D, D],
         [D, D, L, R],],
    12 : [[E, S, E, E],
         [E, E, E, E],
         [E, E, E, A],
         [D, D, D, D],
         [D, D, L, R],],
    13 : [[E, E, S, E],
         [E, E, E, E],
         [E, E, E, A],
         [D, D, D, D],
         [D, D, L, R],],
    14 : [[S, E, E, E],
         [E, E, E, E],
         [E, A, E, E],
         [D, D, D, D],
         [D, D, L, R],],
}



# 3x4
layout58 = [[E, E, S],
            [A, E, E],
            [D, D, D],
            [D, L, R],]
layout59 = [[S, E, E],
            [E, E, A],
            [D, D, D],
            [D, L, R],]
layout60 = [[E, S, E],
            [E, E, A],
            [D, D, D],
            [D, L, R],]
layout61 = [[E, S, E],
            [A, E, E],
            [D, D, D],
            [D, L, R],]
layout62 = [[S, E, E],
            [E, A, E],
            [D, D, D],
            [D, L, R],]
layout63 = [[E, E, S],
            [E, A, E],
            [D, D, D],
            [D, L, R],]

#
l64 = [[E, E, E, E, E, S, E, E, E,],
       [E, E, E, E, E, E, E, E, E,],
       [E, E, A, E, E, E, E, E, E,],
       [D, D, D, D, D, D, D, D, D,],
       [D, D, D, D, D, D, L, R, D],]

l65 = [[E, E, E, E, S],
       [E, E, E, E, E],
       [E, E, E, E, E],
       [A, E, E, E, E],
       [D, D, D, D, D],
       [D, D, L, R, D],]

LAYOUTS = [layout4, layout5, layout8, layout9, layout11, layout13, layout14, layout29, layout31, layout43,
           four_five_layouts[0], four_five_layouts[1], four_five_layouts[2], layout58, layout63, l64, l65]

