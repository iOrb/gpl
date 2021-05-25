import copy

from .language import *
from .objects import OBJECTS

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
                    continue
                if o not in {OBJECTS.empty, OBJECTS.none}:
                    atoms.append((f'{sort}-has-{o}', CONST[sort](r, c, nrows, ncols)))

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
