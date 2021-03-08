from generalization_grid_games.envs import checkmate_tactic as ct


E = ct.EMPTY
BK = ct.BLACK_KING
WK = ct.WHITE_KING
WQ = ct.WHITE_QUEEN
HWQ = ct.HIGHLIGHTED_WHITE_QUEEN
HWK = ct.HIGHLIGHTED_WHITE_KING
HBK = ct.HIGHLIGHTED_BLACK_KING


layout0 = [
    [WQ, WK, E],
    [E, E, E],
    [E, BK, E],
]


layout1 = [
    [WQ, WK, E, E],
    [E, E, E, E],
    [E, E, E, BK],
    [E, E, E, E],
]

layout2 = [
    [WQ, WK],
    [E, E],
    [E, BK]
]

# 4x4
l3 = [
    [WQ, E, E, E],
    [E, E, E, E],
    [E, WK, E, BK],
    [E, E, E, E],
]
l4 = [
    [E, E, WQ, E],
    [E, E, E, E],
    [E, WK, E, BK],
    [E, E, E, E],
]
l5 = [
    [E, E, E, E],
    [E, E, E, E],
    [E, WK, E, BK],
    [E, WQ, E, E],
]
l6 = [
    [E, WQ, E, E],
    [E, E, E, E],
    [BK, E, WK, E],
    [E, E, E, E],
]
l7 = [
    [E, E, E, WQ],
    [E, E, E, E],
    [BK, E, WK, E],
    [E, E, E, E],
]
l8 = [
    [E, E, E, E],
    [E, E, E, E],
    [BK, E, WK, E],
    [E, E, WQ, E],
]
l9 = [
    [E, WK, E, BK],
    [E, E, E, E],
    [E, E, E, E],
    [E, E, WQ, E],
]
l10 = [
    [E, WK, E, BK],
    [E, E, E, E],
    [WQ, E, E, E],
    [E, E, E, E],
]
l11 = [
    [E, WK, E, BK],
    [E, E, E, E],
    [E, E, WQ, E],
    [E, E, E, E],
]
l12 = [
    [BK, E, WK, E],
    [E, E, E, E],
    [E, E, E, WQ],
    [E, E, E, E],
]

five_five_instances = {
    0: [
        [E, E, E, E, E],
        [E, E, E, E, E],
        [E, E, WK, E, E],
        [WQ, E, E, E, E],
        [E, E, E, E, BK],
    ],
    1: [
        [E, E, E, WQ, E],
        [E, E, E, E, E],
        [E, E, WK, E, E],
        [E, E, E, E, E],
        [E, E, E, E, BK],
    ],
    2: [
        [E, WQ, E, E, E],
        [E, E, E, E, E],
        [E, E, WK, E, E],
        [E, E, E, E, E],
        [BK, E, E, E, E],
    ],
    3: [
        [E, E, E, E, E],
        [E, E, E, E, E],
        [E, E, WK, E, E],
        [E, E, E, E, WQ],
        [BK, E, E, E, E],
    ],
    4: [
        [BK, E, E, E, E],
        [E, E, E, E, E],
        [E, E, WK, E, E],
        [E, E, E, E, E],
        [E, WQ, E, E, E],
    ],
    5: [
        [BK, E, E, E, E],
        [E, E, E, E, WQ],
        [E, E, WK, E, E],
        [E, E, E, E, E],
        [E, E, E, E, E],
    ],
    6: [
        [E, E, E, E, BK],
        [WQ, E, E, E, E],
        [E, E, WK, E, E],
        [E, E, E, E, E],
        [E, E, E, E, E],
    ],
    7: [
        [E, E, E, E, BK],
        [E, E, E, E, E],
        [E, E, WK, E, E],
        [E, E, E, E, E],
        [E, E, E, WQ, E],
    ],

}


LAYOUTS = list(five_five_instances.values())

