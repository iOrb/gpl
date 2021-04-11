import numpy as np
import copy

from .objects import OBJECTS

# General State to atoms
def state_to_atoms(domain_name, state):
    rep = copy.deepcopy(state[0][0])
    nrows, ncols = rep.shape

    # These are the general atoms for all the domains
    atoms = list()

    for r in range(-1, nrows + 1):

        for c in range(-1, ncols + 1):

            if nrows > r >= 0 and ncols > c >= 0:
                val = rep[r, c]
            else:
                # Add the None value for cells outside the world
                val = OBJECTS.none

            atoms.append((f'cell-hv-{val}', f'c{r}-{c}'))

    # atoms.append(('player-{}'.format(mrk),))
    return atoms


def atom_tuples_to_string(atom_tuples):
    return ' '.join(f"{a[0]}({','.join(str(var) for var in a[1:])})" for a in atom_tuples)
