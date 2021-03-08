import os
import numpy as np
from lgp.utils import serialize_layout, unserialize_layout
from generalization_grid_games.envs import two_pile_nim as tpn
from layouts import LAYOUTS


ROOT = os.path.dirname(os.path.abspath(__file__))


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


def create_random_layout(rng):
    height = rng.randint(2, 20)
    left_column_height = rng.randint(1, height)
    while True:
        right_column_height = rng.randint(1, height)
        if right_column_height != left_column_height:
            break
    layout = np.full((height, 2), tpn.TOKEN, dtype=object)
    layout[:left_column_height, 0] = tpn.EMPTY
    layout[:right_column_height, 1] = tpn.EMPTY
    return layout.tolist()


def main():
    num_layouts = 20
    rng = np.random.RandomState(0)
    layouts = [create_random_layout(rng) for _ in range(num_layouts)] + LAYOUTS

    i = 0
    for layout in layouts:
        w = len(layout[0])
        h = len(layout)
        fn = check_and_rename(layout, os.path.join(ROOT, f"layout_{w}x{h}"), i)
        serialize_layout(layout, fn)


if __name__ == "__main__":
    main()
