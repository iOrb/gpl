import numpy as np
import copy

# General State to atoms
def state_to_atoms(domain_name, state):
    rep, mrk = copy.deepcopy(state[0])
    # These are the general atoms for all the domains
    atoms = list()

    nrows, ncols = 3, 3

    rep = np.array(rep).reshape(nrows, ncols)

    for r in range(-1, nrows + 1):

        for c in range(-1, ncols + 1):

            if r < nrows and r >= 0 and c < ncols and c >= 0:
                val = rep[r, c]
            else:
                # Add the None value for cells outside the world
                val = 'none'

            atoms.append((f'cell-hv-{val}', f'c{r}-{c}'))

    # atoms.append(('player-{}'.format(mrk),))
    return atoms


def atom_tuples_to_string(atom_tuples):
    return ' '.join(f"{a[0]}({','.join(str(var) for var in a[1:])})" for a in atom_tuples)
