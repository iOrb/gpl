import copy

import numpy as np

from .language import *
from .objects import OBJECTS
from ..utils import identify_margin, in_top, in_bottom, in_left_most, in_right_most

# General State to atoms
def state_to_atoms(domain_name, state, p):
    rep, _ = state
    brd = rep.grid
    nrows, ncols = brd.shape

    # These are the general atoms for all the domains
    atoms = list()

    for r in range(-1, nrows + 1):
        for c in range(-1, ncols + 1):
            for sort in p.sorts_to_use:
                o = brd[r, c] if (nrows > r >= 0 and ncols > c >= 0) else OBJECTS.none
                if o == OBJECTS.none:
                    if p.use_verbose_margin_as_feature:
                        o = identify_margin(r, c, nrows, ncols)
                    elif p.use_margin_as_feature:
                        pass
                    else:
                        continue
                if o not in {OBJECTS.empty} | p.objects_to_ignore:
                    atoms.append((CELL_HAS(sort, o), CONST[sort](r, c, nrows, ncols)))

    if p.domain_name == 'checkmate_tactic':
        # CHECKMATE TACTIC
        from ..envs.checkmate_tactic import get_attacking_mask_from_piece, get_attacking_mask, \
            WHITE, BLACK, WHITE_KING, WHITE_TOWER, BLACK_KING, CHECKMATE, WHITE_QUEEN
        mask_white = get_attacking_mask(brd, WHITE)
        mask_black = get_attacking_mask(brd, BLACK)
        mask_bk = get_attacking_mask_from_piece(brd, BLACK_KING)
        mask_wk = get_attacking_mask_from_piece(brd, WHITE_KING)
        # mask_wr = get_attacking_mask_from_piece(brd, WHITE_TOWER)
        mask_wq = get_attacking_mask_from_piece(brd, WHITE_QUEEN)
        # mask_quadrant_bk = get_mask_quadrant_black_king(brd)
        for r in range(nrows):
            for c in range(ncols):
                cell = CONST[CELL_S](r, c, nrows, ncols)
                if mask_wk[r, c]:
                    atoms.append((CELL_HAS_PIECE_ATTAKED_BY(WHITE_KING), cell))
                # if mask_wr[r, c]:
                #     atoms.append((CELL_HAS_PIECE_ATTAKED_BY(WHITE_TOWER), cell))
                if mask_bk[r, c]:
                    atoms.append((CELL_HAS_PIECE_ATTAKED_BY(BLACK_KING), cell))
                if mask_wq[r, c]:
                    atoms.append((CELL_HAS_PIECE_ATTAKED_BY(WHITE_QUEEN), cell))
                if mask_white[r, c]:
                    atoms.append((CELL_HAS_COLOR_ATTAKED_BY(WHITE), cell))
                if mask_black[r, c]:
                    atoms.append((CELL_HAS_COLOR_ATTAKED_BY(BLACK), cell))
                # if mask_quadrant_bk[r, c] and not mask_white[r, c] and not getattr(rep, CHECKMATE):
                #     atoms.append((CELL_IS_IN(BLACK_KING_AVAILABLE_QUADRANT), cell))
                if in_top(r, c, nrows, ncols):
                    atoms.append((CELL_IS_IN(TOP), cell))
                if in_bottom(r, c, nrows, ncols):
                    atoms.append((CELL_IS_IN(BOTTOM), cell))
                if in_left_most(r, c, nrows, ncols):
                    atoms.append((CELL_IS_IN(LEFT), cell))
                if in_right_most(r, c, nrows, ncols):
                    atoms.append((CELL_IS_IN(RIGHT), cell))

    # WUMPUS
    # from ..envs.wumpus import AT_WUMPUS, AT_PIT, AGENT, WUMPUS
    # if AGENT not in brd and getattr(rep, AT_WUMPUS):
    #     r, c = np.argwhere(brd==WUMPUS)[0]
    #     sort = CELL_S
    #     o=AGENT
    #     atoms.append((f'{sort}-has-{o}', CONST[sort](r, c, nrows, ncols)))
    # if AGENT not in brd and getattr(rep, AT_PIT) is not None:
    #     r, c = getattr(rep, AT_PIT)
    #     sort = CELL_S
    #     o=AGENT
    #     atoms.append((f'{sort}-has-{o}', CONST[sort](r, c, nrows, ncols)))

    # DELIVERY
    # from ..envs.delivery import AT_DESTINATION, HOLDING_PACKAGE, DESTINY, PACKAGE, AGENT
    # if getattr(rep, AT_DESTINATION):
    #     r, c = np.argwhere(brd==AGENT)[0]
    #     sort = CELL_S
    #     o=DESTINY
    #     atoms.append((f'{sort}-has-{o}', CONST[sort](r, c, nrows, ncols)))
    # if not PACKAGE in rep.grid:
    #     r, c = np.argwhere(brd==AGENT)[0]
    #     sort = CELL_S
    #     o=PACKAGE
    #     atoms.append((f'{sort}-has-{o}', CONST[sort](r, c, nrows, ncols)))

    for u in p.unary_predicates:
        if getattr(rep, u):
            atoms.append((u,))

    if p.use_player_as_feature:
        atoms.append(('player-{}'.format(rep.player),))

    if p.use_next_player_as_feature:
        atoms.append(('next_player-{}'.format(rep.next_player),))

    return atoms


def atom_tuples_to_string(atom_tuples):
    return ' '.join(f"{a[0]}({','.join(str(var) for var in a[1:])})" for a in atom_tuples)
