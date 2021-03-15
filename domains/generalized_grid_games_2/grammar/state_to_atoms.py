import numpy as np
from generalization_grid_games.envs import reach_for_the_star as rfts
from generalization_grid_games.envs import stop_the_fall as stf
from generalization_grid_games.envs import chase as ec
from generalization_grid_games.envs import checkmate_tactic as ct
from generalization_grid_games.envs import two_pile_nim as tpn
import copy

GRID_DIRECTIONS = up, rightup, right, rightdown, down, leftdown, left, leftup =\
    ['up', 'rightup', 'right', 'rightdown', 'down', 'leftdown', 'left', 'leftup']


def state_to_atoms(domain_name, state, info):
    return {

        'ReachForTheStar': state_to_atoms_rfts,
        'StopTheFall': state_to_atoms_stf,
        'Chase': state_to_atoms_ec,
        'CheckmateTactic': state_to_atoms_ct,
        'TwoPileNim': state_to_atoms_tpn,

    }.get(domain_name)(state, info)


# Reach for the star
def state_to_atoms_rfts(state, info):
    layout = copy.deepcopy(state)
    layout = np.delete(layout, [-1], axis=0)
    atoms = state_to_atoms_general(layout, info)
    return atoms


# Stop the fall
def state_to_atoms_stf(state, info):
    atoms = state_to_atoms_general(state, info)
    return atoms


# Checkmate tactic
def state_to_atoms_ct(state, info):
    atoms = state_to_atoms_general(state, info)
    return atoms


# Two pile nim
def state_to_atoms_tpn(layout, info):
    atoms = state_to_atoms_general(layout, info)
    if not info['is_dead_end']:
        atoms.append(('player0',))
    return atoms


# Chase
def state_to_atoms_ec(state, info):
    layout = copy.deepcopy(state)
    try:
        la, _ = np.argwhere(layout == ec.LEFT_ARROW)[0]
    except:
        print('h')
    ra, _ = np.argwhere(layout == ec.RIGHT_ARROW)[0]
    da, _ = np.argwhere(layout == ec.DOWN_ARROW)[0]
    ua, _ = np.argwhere(layout == ec.UP_ARROW)[0]
    layout = np.delete(layout, [la, ra, da, ua], axis=0)
    nrows, ncols = layout.shape
    layout = layout.flatten()
    layout = np.delete(layout, np.argwhere(layout==ec.WALL)).reshape(nrows - 2, ncols - 2)
    atoms = list()
    nrows, ncols = layout.shape

    for r in range(-1, nrows + 1):

        for c in range(-1, ncols + 1):

            if r < nrows and r >= 0 and c < ncols and c >= 0:
                val = layout[r, c]
            else:
                # Add the None value for cells outside the world
                val = 'none'

            atoms.append((f'cell-hv-{val}', f'c{r}-{c}'))
            atoms.append((f'row-hv-{val}', f'row-{r}'))
            atoms.append((f'col-hv-{val}', f'col-{c}'))

    return atoms


# General State to atoms
def state_to_atoms_general(layout, info):
    # These are the general atoms for all the domains
    atoms = list()

    nrows, ncols = layout.shape

    for r in range(-1, nrows + 1):

        for c in range(-1, ncols + 1):

            if r < nrows and r >= 0 and c < ncols and c >= 0:
                val = layout[r, c]
            else:
                # Add the None value for cells outside the world
                val = 'none'

            atoms.append((f'cell-hv-{val}', f'c{r}-{c}'))

    return atoms



def add_bool_atom(atoms, predicate, condition):
    if condition:
        atoms.append((predicate,))


def atom_tuples_to_string(atom_tuples):
    return ' '.join(f"{a[0]}({','.join(str(var) for var in a[1:])})" for a in atom_tuples)
