#! /usr/bin/env python3
import copy
import os
from lgp.utils import serialize_layout, unserialize_layout
from generalization_grid_games.envs import chase as ec
from layouts import LAYOUTS
from itertools import permutations
from lgp.utils import get_operators_from_shape
import numpy as np
from tqdm import tqdm


ROOT = os.path.dirname(os.path.abspath(__file__))


def main():

    layouts = create_all_possible_layouts(2, 3)
    # layouts = LAYOUTS

    i=0
    for layout in tqdm(layouts):
        h = len(layout)
        w = len(layout[0])
        # fn = check_and_rename(layout, os.path.join(ROOT, "all_8x9", f"b_layout_{w}x{h}"), i=0
        fn = '{}_{:03d}.json'.format(os.path.join(ROOT, "all_5x5", f"a_layout_{w}x{h}"), i)
        i += 1
        serialize_layout(layout, fn)


def create_all_possible_layouts(nrows, ncols):
    layouts = list()

    maxlen = max(len(s) for s in ec.ALL_TOKENS)

    base_layout = np.empty(shape=(nrows + 3, ncols + 2), dtype=f"<S{maxlen}")
    base_layout[:] = ec.EMPTY
    base_layout[:, [0, -1]] = ec.WALL
    base_layout[[0, -2, -1], :] = ec.WALL
    base_layout[-1, 0] = ec.LEFT_ARROW
    base_layout[-1, 1] = ec.RIGHT_ARROW
    base_layout[-1, 2] = ec.DOWN_ARROW
    base_layout[-1, 3] = ec.UP_ARROW

    operators = get_operators_from_shape(nrows, ncols)

    permutations_agent_target = permutations(operators, 2)

    for (agent_r, agent_c), (target_r, target_c) in permutations_agent_target:

        layout = np.copy(base_layout)
        layout[agent_r + 1, agent_c + 1] = ec.AGENT
        layout[target_r + 1, target_c + 1] = ec.TARGET

        layouts.append(layout.astype(f"U{maxlen}"))

    return layouts


def check_and_rename(layout, base_file_name, i):
    file_name = f"{base_file_name}_{i}.json"

    while os.path.exists(file_name):
        # check if existing file contains the same info,
        if (layout == unserialize_layout(file_name)).all():
            # overwrite if contain the same layout
            return file_name
        else:
            # rename if contain the NOT same layout, and check again
            i += 1
            file_name = f"{base_file_name}_{i}.json"

    return file_name


if __name__ == "__main__":

    main()

