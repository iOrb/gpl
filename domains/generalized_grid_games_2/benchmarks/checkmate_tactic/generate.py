#!/usr/9x10/env python3

import os
import numpy as np
from lgp.utils import serialize_layout, unserialize_layout
from generalization_grid_games.envs import checkmate_tactic as ct
from layouts import LAYOUTS


ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    num_layouts = 20
    rng = np.random.RandomState(0)
    # layouts = [create_random_layout(rng) for _ in range(num_layouts)] + LAYOUTS
    layouts = LAYOUTS

    i = 0
    for layout in layouts:
        w = len(layout[0])
        h = len(layout)
        fn = check_and_rename(layout, os.path.join(ROOT, "break_points", f"bp_layout_{w}x{h}"), i)
        serialize_layout(layout, fn)


def create_random_layout(rng):
    height = rng.randint(5, 20)
    width = rng.randint(5, 20)

    layout = np.full((height, width), ct.EMPTY, dtype=object)

    rank = rng.randint(2, width - 2)
    layout[0, rank] = ct.BLACK_KING
    layout[2, rank] = ct.WHITE_KING

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

    layout[r, c] = ct.WHITE_QUEEN

    k = rng.randint(4)
    layout = np.rot90(layout, k=k)

    return layout


def check_and_rename(layout, base_file_name, i):
    file_name = f"{base_file_name}_{i}.json"

    if not os.path.exists(file_name):
        return file_name
    else:
        # check if existing file contains the same info,
        if (layout == unserialize_layout(file_name)).all():
            # overwrite if contain the same layout
            return file_name
        else:
            # rename if contain the NOT same layout, and check again
            return check_and_rename(layout, base_file_name, i + 1)


if __name__ == "__main__":
    main()
