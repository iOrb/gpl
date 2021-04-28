import numpy as np

EMPTY = 'empty'
BLACK_KING = 'black_king'
WHITE_KING = 'white_king'
WHITE_QUEEN = 'white_queen'
WHITE_TOWER = 'white_tower'

ALL_TOKENS = [EMPTY, BLACK_KING, WHITE_KING, WHITE_QUEEN, WHITE_TOWER]

COLOR_TO_PIECES = {
    'white': [WHITE_KING, WHITE_QUEEN, WHITE_TOWER],
    'black': [BLACK_KING],
}
opposite_color = lambda c: 'black' if c == 'white' else 'white'

PIECE_VALID_MOVES = {
    BLACK_KING: lambda pos, layout: king_valid_moves(pos, layout, 'black'),
    WHITE_KING: lambda pos, layout: king_valid_moves(pos, layout, 'white'),
    WHITE_QUEEN: lambda pos, layout: queen_valid_moves(pos, layout, 'white'),
    WHITE_TOWER: lambda pos, layout: tower_valid_moves(pos, layout, 'white'),
}

# Begin Checkmate =================================

def act(rep, action):
    r0 = rep[0].copy()
    # valid_actions = available_actions(rep)
    # assert action in valid_actions

    old_r, old_c = action[0]
    new_r, new_c = action[1]

    piece = r0[old_r, old_c]

    r0[new_r, new_c] = piece
    r0[old_r, old_c] = EMPTY

    return (r0, opposite_color(rep[1]))


def available_actions(rep):
    layout, player = rep
    moves = []
    if player == 'white':
        if WHITE_QUEEN in layout:
            c0 = np.argwhere(layout == WHITE_QUEEN)[0]
            moves += [(c0, c1) for c1 in PIECE_VALID_MOVES[WHITE_QUEEN](c0, layout)]
        elif WHITE_TOWER in layout:
            c0 = np.argwhere(layout == WHITE_TOWER)[0]
            moves += [(c0, c1) for c1 in PIECE_VALID_MOVES[WHITE_TOWER](c0, layout)]
        elif WHITE_KING in layout:
            c0 = np.argwhere(layout == WHITE_KING)[0]
            moves += [(c0, c1) for c1 in PIECE_VALID_MOVES[WHITE_KING](c0, layout)]
    elif player == 'black':
        c0 = np.argwhere(layout == BLACK_KING)[0]
        moves += [(c0, c1) for c1 in PIECE_VALID_MOVES[BLACK_KING](c0, layout)]
    return moves


def check_game_status(rep):
    if checkmate(rep):
        return 1
    if stale_mate(rep):
        return 0
    else:
        return -1


def checkmate(rep):
    layout, player = rep
    assert (BLACK_KING in layout)

    if player == 'black':
        valid_moves = available_actions(rep)
        if len(valid_moves) == 0:
            king_pos = np.argwhere(layout == BLACK_KING)[0]
            attacking_mask = get_attacking_mask(layout, opposite_color(player))
            if attacking_mask[king_pos[0], king_pos[1]]:
                return True
        return False
    return False


def stale_mate(rep):
    layout, player = rep
    # assert not checkmate(rep)

    if player == 'black' and not available_actions(rep):
        return True
    elif player == 'white' and not WHITE_QUEEN in layout and not WHITE_TOWER in layout:
        return True
    else:
        return False


def player2_policy(rep):
    layout, color = rep
    king_pos = np.argwhere(rep[0] == BLACK_KING)[0]
    valid_actions = available_actions(rep)
    if WHITE_QUEEN in layout:
        no_king_piece_pos = np.argwhere(rep[0] == WHITE_QUEEN)[0]
    elif WHITE_TOWER in layout:
        no_king_piece_pos = np.argwhere(rep[0] == WHITE_TOWER)[0]
    if abs(no_king_piece_pos[0] - king_pos[0]) == 1 and abs(no_king_piece_pos[1] - king_pos[1]) == 1:
        king_valid_moves = PIECE_VALID_MOVES[BLACK_KING](king_pos, rep[0])
        if any((no_king_piece_pos == pos).all() for pos in king_valid_moves):
            return [king_pos, no_king_piece_pos]
    return valid_actions[0]


# End Checkmate =================================


def king_valid_moves(pos, layout, color):
    valid_moves = []

    attacking_mask = get_attacking_mask(layout, opposite_color(color))

    for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        running_pos = np.add(pos, direction)
        if np.any(running_pos < 0):
            continue
        try:
            next_cell = layout[running_pos[0], running_pos[1]]
        except IndexError:
            continue

        if next_cell in COLOR_TO_PIECES[color]:
            continue

        if next_cell in COLOR_TO_PIECES[opposite_color(color)]:
            excluded_layout = layout.copy()
            excluded_layout[running_pos[0], running_pos[1]] = EMPTY
            excluded_attacking_mask = get_attacking_mask(excluded_layout, opposite_color(color))
            if not excluded_attacking_mask[running_pos[0], running_pos[1]]:
                valid_moves.append(running_pos)
            continue

        if not attacking_mask[running_pos[0], running_pos[1]]:
            valid_moves.append(running_pos)

    return valid_moves


def get_king_attacking_spaces(pos, layout):
    attacking_spaces = []
    for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        running_pos = np.add(pos, direction)
        if np.any(running_pos < 0):
            continue
        try:
            next_cell = layout[running_pos[0], running_pos[1]]
        except IndexError:
            continue
        attacking_spaces.append(running_pos)
    return attacking_spaces


def queen_valid_moves(pos, layout, color):
    valid_moves = []

    for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        running_pos = np.array(pos)
        while True:
            running_pos += direction
            if np.any(running_pos < 0):
                break
            try:
                next_cell = layout[running_pos[0], running_pos[1]]
            except IndexError:
                break

            if next_cell in COLOR_TO_PIECES[color]:
                break
            elif next_cell == EMPTY or 'king' in next_cell:
                valid_moves.append(running_pos.copy())
            else:
                assert next_cell in COLOR_TO_PIECES[opposite_color(color)]
                valid_moves.append(running_pos.copy())
                break

    return valid_moves

def tower_valid_moves(pos, layout, color):
    valid_moves = []

    for direction in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
        running_pos = np.array(pos)
        while True:
            running_pos += direction
            if np.any(running_pos < 0):
                break
            try:
                next_cell = layout[running_pos[0], running_pos[1]]
            except IndexError:
                break

            if next_cell in COLOR_TO_PIECES[color]:
                break
            elif next_cell == EMPTY or 'king' in next_cell:
                valid_moves.append(running_pos.copy())
            else:
                assert next_cell in COLOR_TO_PIECES[opposite_color(color)]
                valid_moves.append(running_pos.copy())
                break

    return valid_moves


def get_attacking_mask(layout, color):
    attacking_mask = np.zeros(layout.shape, dtype=bool)

    for r in range(layout.shape[0]):
        for c in range(layout.shape[1]):
            piece = layout[r, c]
            if piece not in COLOR_TO_PIECES[color]:
                continue

            if 'king' in piece:
                attacked_spaces = get_king_attacking_spaces((r, c), layout)
            else:
                attacked_spaces = PIECE_VALID_MOVES[piece]((r, c), layout)

            for space in attacked_spaces + [(r, c)]:
                attacking_mask[space[0], space[1]] = True

    return attacking_mask


### Specific environments
rng = np.random.RandomState(0)
num_layouts = 20


def create_random_layout():
    height = rng.randint(5, 20)
    width = rng.randint(5, 20)

    layout = np.full((height, width), EMPTY, dtype=object)

    rank = rng.randint(2, width - 2)
    layout[0, rank] = BLACK_KING
    layout[2, rank] = WHITE_KING

    attack_direction = rng.randint(4)

    if attack_direction == 0:
        r = 1
        c = rng.randint(rank + 2, width)
    elif attack_direction == 1:
        r = 1
        c = rng.randint(0, rank - 1)
    elif attack_direction == 2:
        r = 1
        c = rank
        delta = rng.randint(2, min(height, width - rank))
        r += delta
        c += delta
    elif attack_direction == 3:
        r = 1
        c = rank
        delta = rng.randint(2, min(height, rank + 1))
        r += delta
        c -= delta

    layout[r, c] = WHITE_QUEEN

    k = rng.randint(4)
    layout = np.rot90(layout, k=k)

    return layout


layouts = [create_random_layout() for _ in range(num_layouts)]
