import numpy as np
import copy

from ..utils import identify_margin
from .objects import OBJECTS
from ..config import use_player_as_feature, use_margin_as_feature, \
    sorts_to_use

SORT = {
    'cell': lambda r, c: f'c{r}-{c}',
    'row': lambda r, c: f'row-{r}',
    'col': lambda r, c: f'col-{c}',
}

# General State to atoms
def state_to_atoms(domain_name, state):
    rep = copy.deepcopy(state[0][0])
    nrows, ncols = rep.shape

    # These are the general atoms for all the domains
    atoms = list()

    for r in range(-1, nrows + 1):
        for c in range(-1, ncols + 1):
            for sort in sorts_to_use:
                if nrows > r >= 0 and ncols > c >= 0:
                    o = rep[r, c]
                    if o == OBJECTS.empty:
                        continue
                else:
                    # Add value for cells outside the grid
                    o = f'{identify_margin(r, c, nrows, ncols)}' if use_margin_as_feature else f'{OBJECTS.none}'

                atoms.append((f'{sort}-hv-{o}', SORT[sort](r, c)))

    if use_player_as_feature:
        atoms.append(('player-{}'.format(state[0][1]),))

    return atoms


def atom_tuples_to_string(atom_tuples):
    return ' '.join(f"{a[0]}({','.join(str(var) for var in a[1:])})" for a in atom_tuples)
