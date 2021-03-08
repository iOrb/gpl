import os
import numpy as np
from lgp.utils import serialize_layout, unserialize_layout
from generalization_grid_games.envs import reach_for_the_star as rfts
from layouts import LAYOUTS


ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    num_layouts = 20
    rng = np.random.RandomState(0)
    # layouts = [create_random_layout(rng) for _ in range(num_layouts)] + LAYOUTS
    layouts = LAYOUTS

    dir = 'climb_from_left'

    i = 0
    for layout in layouts:
        w = len(layout[0])
        h = len(layout)
        fn = check_and_rename(layout, os.path.join(ROOT, dir, f"layout_{w}x{h}"), i)
        serialize_layout(layout, fn)


def create_random_layout(rng):
    reduce = 4
    stairs_height = rng.randint(2, 11 - reduce)
    stairs_dist_from_right = rng.randint(0, 5-reduce)
    stairs_dist_from_top = rng.randint(0, 5-reduce)
    agent_dist_from_stairs = rng.randint(0, 5-reduce)
    agent_dist_from_left = rng.randint(0, 5-reduce)

    height = 2 + stairs_height + stairs_dist_from_top
    width = stairs_dist_from_right + 2*stairs_height + agent_dist_from_stairs + agent_dist_from_left
    layout = np.full((height, width), rfts.EMPTY, dtype=object)

    star_r = stairs_dist_from_top
    star_c = agent_dist_from_left + agent_dist_from_stairs + stairs_height
    agent_r = height - 3
    agent_c = agent_dist_from_left

    layout[star_r, star_c] = rfts.STAR
    layout[agent_r, agent_c] = rfts.AGENT

    if rng.uniform() > 0.5:
        layout = np.fliplr(layout)

    layout[-2:, :] = rfts.DRAWN
    layout[-1, -1] = rfts.RIGHT_ARROW
    layout[-1, -2] = rfts.LEFT_ARROW

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
