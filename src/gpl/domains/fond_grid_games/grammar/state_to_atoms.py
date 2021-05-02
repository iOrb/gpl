import copy

from .objects import OBJECTS
from .language import *
from gpl.domains.fond_grid_games import configd


# General State to atoms
def state_to_atoms(domain_name, state):
    brd = copy.deepcopy(state[0][0])
    nrows, ncols = brd.shape

    # These are the general atoms for all the domains
    atoms = list()

    for r in range(-1, nrows + 1):
        for c in range(-1, ncols + 1):
            for sort in configd.sorts_to_use:
                if nrows > r >= 0 and ncols > c >= 0:
                    o = brd[r, c]
                else:
                    # Add value for cells outside the grid
                    o = OBJECTS.none
                if o not in {OBJECTS.empty, OBJECTS.none}:
                    atoms.append((f'{sort}-hv-{o}', CONST[sort](r, c)))

    if configd.use_player_as_feature:
        atoms.append(('player-{}'.format(state[0][1]),))

    return atoms


def atom_tuples_to_string(atom_tuples):
    return ' '.join(f"{a[0]}({','.join(str(var) for var in a[1:])})" for a in atom_tuples)
