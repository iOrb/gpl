import numpy as np

from generalization_grid_games.envs import two_pile_nim as tpn
from generalization_grid_games.envs import checkmate_tactic as ct
from generalization_grid_games.envs import stop_the_fall as stf
from generalization_grid_games.envs import chase as ec
from generalization_grid_games.envs import reach_for_the_star as rfts

import random


def compute_actions_from_policies(policies, state):
    actions = set()
    for policy in policies:
        actions = actions | set(policy(state))
    return actions


def expert_nim_policy_original(layout):
    r1 = np.max(np.argwhere(layout == tpn.EMPTY)[:, 0])
    if layout[r1, 0] == tpn.TOKEN:
        c1 = 0
    elif layout[r1, 1] == tpn.TOKEN:
        c1 = 1
    else:
        r1 += 1
        c1 = 0
    return [(r1, c1)]


def expert_nim_policy(layout):
    r1 = np.max(np.argwhere(layout == tpn.EMPTY)[:, 0])
    if layout[r1, 0] == tpn.TOKEN:
        c1 = 0
        return [(r1, c1)]
    elif layout[r1, 1] == tpn.TOKEN:
        c1 = 1
        return [(r1, c1)]
    return []


def expert_checkmate_tactic_policy(layout):
    if np.any(layout == ct.WHITE_QUEEN):
        return [tuple(np.argwhere(layout == ct.WHITE_QUEEN)[0])]

    black_king_pos = np.argwhere(layout == ct.BLACK_KING)[0]
    white_king_pos = np.argwhere(layout == ct.WHITE_KING)[0]

    r, c = ((black_king_pos[0] + white_king_pos[0]) // 2, (black_king_pos[1] + white_king_pos[1]) // 2)
    return [(r, c)]


def expert_stf_policy(layout):
    r, c = np.argwhere(layout == stf.FALLING)[0]
    num_rows, num_cols = layout.shape

    while True:
        if layout[r + 1, c] in [stf.STATIC, stf.DRAWN]:
            break
        r += 1

    if c - 1 >= 0 and layout[r, c - 1] == stf.RED:
        return [(r, c)]

    if c + 1 < num_cols and layout[r, c + 1] == stf.RED:
        return [(r, c)]

    r, c = np.argwhere(layout == stf.ADVANCE)[0]
    return [(r, c)]


def expert_stf_policy_original(layout):
    r, c = np.argwhere(layout == stf.FALLING)[0]

    while True:
        if layout[r + 1, c] in [stf.STATIC, stf.DRAWN]:
            break
        r += 1

    if layout[r, c - 1] == stf.RED or layout[r, c + 1] == stf.RED:
        return [(r, c)]

    r, c = np.argwhere(layout == stf.ADVANCE)[0]
    return [(r, c)]


def general_stf_policy_0(layout):

    fr, fc = np.argwhere(layout == stf.FALLING)[0]

    col_falling = [(r[0], fc) for r in np.argwhere(layout[fr:, fc] == stf.EMPTY)]
    # col_falling = [(r[0], fc) for r in zip(*np.where(layout[fr:, fc] == stf.EMPTY))]

    if not col_falling:
        r, c = np.argwhere(layout == stf.ADVANCE)[0]
        return [(r, c)]
    else:
        return [col_falling[0]]
        # return [col_falling[0], random.choice(col_falling)]


def general_stf_policy_1(layout):

    fr, fc = np.argwhere(layout == stf.FALLING)[0]

    col_falling = [(r[0], fc) for r in np.argwhere(layout[:, fc] == stf.EMPTY)]

    if not col_falling:
        r, c = np.argwhere(layout == stf.ADVANCE)[0]
        return [(r, c)]
    else:
        return [col_falling[0]]
        # return [col_falling[0], random.choice(col_falling)]


def general_stf_policy_fill_all(layout):

    emptys = [(r, c) for r, c in zip(*np.where(layout == stf.EMPTY))]

    if not emptys:
        r, c = np.argwhere(layout == stf.ADVANCE)[0]
        return [(r, c)]
    else:
        return [emptys[0]]


def expert_ec_policy(layout):
    r, c = np.argwhere(layout == ec.TARGET)[0]
    ra, ca = np.argwhere(layout == ec.AGENT)[0]

    left_arrow = tuple(np.argwhere(layout == ec.LEFT_ARROW)[0])
    right_arrow = tuple(np.argwhere(layout == ec.RIGHT_ARROW)[0])
    up_arrow = tuple(np.argwhere(layout == ec.UP_ARROW)[0])
    down_arrow = tuple(np.argwhere(layout == ec.DOWN_ARROW)[0])

    if layout[r + 1, c] == ec.WALL or layout[r + 1, c] == ec.DRAWN:

        if ra < r:

            return [down_arrow]

        if ra > r:

            return [up_arrow]

        if ca < c:

            return [right_arrow]

        if ca > c:

            return [left_arrow]

    else:

        return [(r + 1, c)]


def fill_agent_column_ec_policy(layout):
    r, c = np.argwhere(layout == ec.TARGET)[0]
    ra, ca = np.argwhere(layout == ec.AGENT)[0]

    left_arrow = tuple(np.argwhere(layout == ec.LEFT_ARROW)[0])
    right_arrow = tuple(np.argwhere(layout == ec.RIGHT_ARROW)[0])
    up_arrow = tuple(np.argwhere(layout == ec.UP_ARROW)[0])
    down_arrow = tuple(np.argwhere(layout == ec.DOWN_ARROW)[0])

    if c == ca:
        if ra < r:
            return [down_arrow]

        if ra > r:
            return [up_arrow]

    if np.any(layout[:, ca] == ec.EMPTY):
        col_agent_emptys = [(r[0], ca) for r in np.argwhere(layout[:, ca] == ec.EMPTY)]
        # return col_agent_emptys
        return [col_agent_emptys[0]]

    if ca < c:

        return [right_arrow]

    if ca > c:

        return [left_arrow]



def expert_ec_policy_original(layout):
    r, c = np.argwhere(layout == ec.TARGET)[0]
    ra, ca = np.argwhere(layout == ec.AGENT)[0]

    left_arrow = tuple(np.argwhere(layout == ec.LEFT_ARROW)[0])
    right_arrow = tuple(np.argwhere(layout == ec.RIGHT_ARROW)[0])
    up_arrow = tuple(np.argwhere(layout == ec.UP_ARROW)[0])
    down_arrow = tuple(np.argwhere(layout == ec.DOWN_ARROW)[0])

    # Top left corner
    if layout[r - 1, c] == ec.WALL and layout[r, c - 1] == ec.WALL:

        # Draw on right
        if layout[r, c + 1] == ec.EMPTY:
            return [(r, c + 1)]

        # Move to left
        if layout[ra, ca - 1] == ec.EMPTY:
            return [left_arrow]

        # Move up
        return [up_arrow]

    # Top right corner
    if layout[r - 1, c] == ec.WALL and layout[r, c + 1] == ec.WALL:

        # Draw on left
        if layout[r, c - 1] == ec.EMPTY:
            return [(r, c - 1)]

        # Move to right
        if layout[ra, ca + 1] == ec.EMPTY:
            return [right_arrow]

        # Move up
        return [up_arrow]

    # Bottom left corner
    if layout[r + 1, c] == ec.WALL and layout[r, c - 1] == ec.WALL:

        # Draw on right
        if layout[r, c + 1] == ec.EMPTY:
            return [(r, c + 1)]

        # Move to left
        if layout[ra, ca - 1] == ec.EMPTY:
            return [left_arrow]

        # Move down
        return [down_arrow]

    # Bottom right corner
    if layout[r + 1, c] == ec.WALL and layout[r, c + 1] == ec.WALL:

        # Draw on left
        if layout[r, c - 1] == ec.EMPTY:
            return [(r, c - 1)]

        # Move to right
        if layout[ra, ca + 1] == ec.EMPTY:
            return [right_arrow]

        # Move down
        return [down_arrow]

    # Wait
    return [(0, 0)]

    # # do any movement into an empty cell
    # any_move_into_empty = list()
    # # Move to right
    # if layout[ra, ca + 1] == ec.EMPTY:
    #     any_move_into_empty.append(right_arrow)
    # # Move to left
    # if layout[ra, ca - 1] == ec.EMPTY:
    #     any_move_into_empty.append(left_arrow)
    # # Move to up
    # if layout[ra - 1, ca] == ec.EMPTY:
    #     any_move_into_empty.append(up_arrow)
    # # Move to down
    # if layout[ra + 1, ca] == ec.EMPTY:
    #     any_move_into_empty.append(down_arrow)
    # return any_move_into_empty


def expert_rfts_policy(layout):
    agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
    star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
    right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
    left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])
    num_rows, num_cols = layout.shape

    height_to_star = agent_r - star_r

    # there is place to build stairs to climb from left
    space_left_available = star_c >= height_to_star

    # there is place to build stairs to climb from right
    space_right_available = num_cols - star_c - 1 >= height_to_star

    # gonna climb up from the left
    if agent_c <= star_c:

        if space_left_available:

            # move to the left more
            if abs(agent_c - star_c) < height_to_star:
                return [left_arrow]

            # stairs do not exist
            sr, sc = star_r + 1, star_c
            while sc > agent_c:
                if sr >= layout.shape[0] - 2:
                    break
                if layout[sr, sc] != rfts.DRAWN:
                    return [(sr, sc)]
                sr += 1
                sc -= 1

            # move to the right
            return [right_arrow]

        else:
            return [right_arrow]

    # gonna climb up from the right
    if agent_c > star_c:

        if space_right_available:
            # move to the right more
            if abs(agent_c - star_c) < height_to_star:
                return [right_arrow]

            # stairs do not exist
            sr, sc = star_r + 1, star_c
            while sc < agent_c:
                if sr >= layout.shape[0] - 2:
                    break
                if layout[sr, sc] != rfts.DRAWN:
                    return [(sr, sc)]
                sr += 1
                sc += 1

            # move to the left
            return [left_arrow]

        else:
            return [left_arrow]



def expert_rfts_policy_original(layout):
    agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
    star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
    right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
    left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])

    height_to_star = agent_r - star_r

    # gonna climb up from the left
    if agent_c <= star_c:

        # move to the left more
        if abs(agent_c - star_c) < height_to_star:
            return [left_arrow]

        # stairs do not exist
        sr, sc = star_r + 1, star_c
        while sc > agent_c:
            if sr >= layout.shape[0] - 2:
                break
            if layout[sr, sc] != rfts.DRAWN:
                return [(sr, sc)]
            sr += 1
            sc -= 1

        # move to the right
        return [right_arrow]

    # gonna climb up from the right
    else:
        # move to the right more
        if abs(agent_c - star_c) < height_to_star:
            return [right_arrow]

        # stairs do not exist
        sr, sc = star_r + 1, star_c
        while sc < agent_c:
            if sr >= layout.shape[0] - 2:
                break
            if layout[sr, sc] != rfts.DRAWN:
                return [(sr, sc)]
            sr += 1
            sc += 1

        # move to the left
        return [left_arrow]


def expert_rfts_policy_two_stairs_bunch(layout):
    agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
    star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
    right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
    left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])

    height_to_star = agent_r - star_r

    nrows = len(layout)
    ncols = len(layout[0])

    cells_under_star_diagonals = set()
    for row in range(nrows):
        for col in range(ncols):
            diff_cols = abs(star_c - col)
            diff_rows = abs(star_r - row)
            if row > star_r:
                if diff_cols < diff_rows:
                    if layout[(row, col)] == rfts.EMPTY:
                        cells_under_star_diagonals.add((row, col))

    # gonna climb up from the left
    if agent_c <= star_c:

        if cells_under_star_diagonals != set():
            return cells_under_star_diagonals
        else:
            # move to the right
            return [right_arrow]

    # gonna climb up from the right
    else:

        if cells_under_star_diagonals != set():
            return cells_under_star_diagonals
        else:
            # move to the right
            return [left_arrow]


def expert_rfts_policy_two_stairs_deterministic(layout):
    agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
    star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
    right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
    left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])

    height_to_star = agent_r - star_r

    nrows = len(layout)
    ncols = len(layout[0])

    cells_under_star_diagonals = set()
    for row in range(nrows):
        for col in range(ncols):
            diff_cols = abs(star_c - col)
            diff_rows = abs(star_r - row)
            if row > star_r:
                if diff_cols < diff_rows:
                    if layout[(row, col)] == rfts.EMPTY:
                        cells_under_star_diagonals.add((row, col))

    # gonna climb up from the left
    if agent_c <= star_c:

        if cells_under_star_diagonals != set():
            return [cells_under_star_diagonals.pop()]
        else:
            # move to the right
            return [right_arrow]

    # gonna climb up from the right
    else:

        if cells_under_star_diagonals != set():
            return [cells_under_star_diagonals.pop()]
        else:
            # move to the right
            return [left_arrow]


def build_and_advance_rfts_policy(layout):
    agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
    star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
    right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
    left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])

    height_to_star = agent_r - star_r

    # Walk in the direction of the star
    if height_to_star == 0:

        if agent_c < star_c:

            if layout[agent_r + 1, agent_c + 1] == rfts.DRAWN:
                return [right_arrow]
            else:
                return [(agent_r + 1, agent_c + 1)]

        if agent_c > star_c:

            if layout[agent_r + 1, agent_c - 1] == rfts.DRAWN:
                return [left_arrow]
            else:
                return [(agent_r + 1, agent_c - 1)]

    # gonna climb up from the left
    if agent_c < star_c:

        if layout[agent_r, agent_c + 1] == rfts.DRAWN:
            return [right_arrow]
        else:
            return [(agent_r, agent_c + 1)]

    # gonna climb up from the right
    if agent_c > star_c:

        if layout[agent_r, agent_c - 1] == rfts.DRAWN:
            return [left_arrow]
        else:
            return [(agent_r, agent_c - 1)]

    # gonna climb up from down
    if agent_c == star_c:
        return [right_arrow, left_arrow]



# def climb_from_down_policy_random(layout):
#     agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
#     star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
#     right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
#     left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])
#     _, ncols = layout.shape
#
#     # there is place to build stairs to climb from left
#     space_left_available_for_agent = agent_c > 0
#
#     # there is place to build stairs to climb from right
#     space_right_available_for_agent = agent_c < ncols - 1
#
#     # Agent is not under the star
#     if star_c != agent_c:
#
#         # Put a block under the star and in the agent row
#         if layout[agent_r, star_c] != rfts.DRAWN:
#
#             return [(agent_r, star_c)]
#
#         # Climb the pilar!
#         else:
#             # agent left to star
#             if agent_c < star_c:
#
#                 return [right_arrow]
#
#             # agent right to star
#             if agent_c > star_c:
#
#                 return [left_arrow]
#
#     # Put the agent between two blocks
#     if space_left_available_for_agent and layout[agent_r, agent_c - 1] != rfts.DRAWN and \
#             space_right_available_for_agent and layout[agent_r, agent_c + 1] != rfts.DRAWN:
#         return [(agent_r, agent_c - 1), (agent_r, agent_c + 1)]
#
#     if space_left_available_for_agent and layout[agent_r, agent_c - 1] != rfts.DRAWN:
#         return [(agent_r, agent_c - 1)]
#
#     if space_right_available_for_agent and layout[agent_r, agent_c + 1] != rfts.DRAWN:
#         return [(agent_r, agent_c + 1)]
#
#     # go away from star column for build the pilar
#     if space_left_available_for_agent and layout[agent_r, agent_c - 1] == rfts.DRAWN and \
#         space_right_available_for_agent and layout[agent_r, agent_c + 1] == rfts.DRAWN:
#         return [right_arrow, left_arrow]
#
#     if space_left_available_for_agent and layout[agent_r, agent_c - 1] == rfts.DRAWN:
#         return [left_arrow]
#
#     if space_right_available_for_agent and layout[agent_r, agent_c + 1] == rfts.DRAWN:
#         return [right_arrow]


# def climb_from_down_policy_deterministic(layout):
#     agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
#     star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
#     right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
#     left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])
#     _, ncols = layout.shape
#
#     # there is place to build stairs to climb from left
#     space_left_available_for_agent = agent_c > 0
#
#     # there is place to build stairs to climb from right
#     space_right_available_for_agent = agent_c < ncols - 1
#
#     # gonna climb form left
#     if agent_c <= star_c and space_left_available_for_agent:
#
#         # Agent is not under the star
#         if star_c != agent_c:
#
#             # Put a block under the star and in the agent row
#             if layout[agent_r, star_c] != rfts.DRAWN:
#
#                 return [(agent_r, star_c)]
#
#             # Climb the pilar!
#             else:
#                 # agent left to star
#                 if agent_c < star_c:
#                     return [right_arrow]
#
#                 # agent right to star
#                 if agent_c > star_c:
#                     return [left_arrow]
#
#     # gonna climb from right
#     elif agent_c > star_c:
#         pass
#
#     # Put the agent between two blocks
#     if space_left_available_for_agent and layout[agent_r, agent_c - 1] != rfts.DRAWN and \
#             space_right_available_for_agent and layout[agent_r, agent_c + 1] != rfts.DRAWN:
#         return [(agent_r, agent_c - 1), (agent_r, agent_c + 1)]
#
#     if space_left_available_for_agent and layout[agent_r, agent_c - 1] != rfts.DRAWN:
#         return [(agent_r, agent_c - 1)]
#
#     if space_right_available_for_agent and layout[agent_r, agent_c + 1] != rfts.DRAWN:
#         return [(agent_r, agent_c + 1)]
#
#     # go away from star column for build the pilar
#     if space_left_available_for_agent and layout[agent_r, agent_c - 1] == rfts.DRAWN and \
#             space_right_available_for_agent and layout[agent_r, agent_c + 1] == rfts.DRAWN:
#         return [right_arrow, left_arrow]
#
#     if space_left_available_for_agent and layout[agent_r, agent_c - 1] == rfts.DRAWN:
#         return [right_arrow]
#
#     if space_right_available_for_agent and layout[agent_r, agent_c + 1] == rfts.DRAWN:
#         return [left_arrow]


def climb_the_pilar_rfts_policy_deterministic_0(layout):
    agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
    star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
    right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
    left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])
    _, ncols = layout.shape

    # there is place to build stairs to climb from left
    space_left_available_for_agent = agent_c > 0

    # there is place to build stairs to climb from right
    space_right_available_for_agent = agent_c < ncols - 1

    # Agent is not under the star
    if star_c != agent_c:

        # Put a block under the star and in the agent row
        if layout[agent_r, star_c] != rfts.DRAWN:

            return [(agent_r, star_c)]

        # Climb the pilar!
        else:
            # agent left to star
            if agent_c < star_c:

                return [right_arrow]

            # agent right to star
            if agent_c > star_c:

                return [left_arrow]

    # go away from star column for build the pilar, going to the left
    if space_left_available_for_agent and layout[agent_r + 1, agent_c - 1] == rfts.DRAWN:
        return [left_arrow]

    # go away from star column for build the pilar, going to the right
    if space_right_available_for_agent and layout[agent_r + 1, agent_c + 1] == rfts.DRAWN:
        return [right_arrow]

    # Put a block to the right of the agent
    if space_right_available_for_agent and layout[agent_r + 1, agent_c + 1] != rfts.DRAWN:
        return [(agent_r + 1, agent_c + 1)]

    # Put a block to the left of the agent
    if space_left_available_for_agent and layout[agent_r + 1, agent_c - 1] != rfts.DRAWN:
        return [(agent_r + 1, agent_c - 1)]


def climb_the_pilar_rfts_policy_deterministic_1(layout):
    agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
    star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
    right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
    left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])
    _, ncols = layout.shape

    # there is place to build stairs to climb from left
    space_left_available_for_agent = agent_c > 0

    # there is place to build stairs to climb from right
    space_right_available_for_agent = agent_c < ncols - 1

    # Agent is not under the star
    if star_c != agent_c:

        # Put a block under the star and in the agent row
        if layout[agent_r, star_c] != rfts.DRAWN:

            return [(agent_r, star_c)]

        # Climb the pilar!
        else:
            # agent left to star
            if agent_c < star_c:

                return [right_arrow]

            # agent right to star
            if agent_c > star_c:

                return [left_arrow]

    # go away from star column for build the pilar, going to the left
    if space_left_available_for_agent and layout[agent_r + 1, agent_c - 1] == rfts.DRAWN:
        return [left_arrow]

    # go away from star column for build the pilar, going to the right
    if space_right_available_for_agent and layout[agent_r + 1, agent_c + 1] == rfts.DRAWN:
        return [right_arrow]

    # Put a block to the left of the agent
    if space_left_available_for_agent and layout[agent_r + 1, agent_c - 1] != rfts.DRAWN:
        return [(agent_r + 1, agent_c - 1)]

    # Put a block to the right of the agent
    if space_right_available_for_agent and layout[agent_r + 1, agent_c + 1] != rfts.DRAWN:
        return [(agent_r + 1, agent_c + 1)]


def climb_the_pilar_rfts_policy_random_0(layout):
    agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
    star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
    right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
    left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])
    _, ncols = layout.shape

    # there is place to build stairs to climb from left
    space_left_available_for_agent = agent_c > 0

    # there is place to build stairs to climb from right
    space_right_available_for_agent = agent_c < ncols - 1

    # Agent is not under the star
    if star_c != agent_c:

        # Put a block under the star and in the agent row
        if layout[agent_r, star_c] != rfts.DRAWN:

            return [(agent_r, star_c)]

        # Climb the pilar!
        else:
            # agent left to star
            if agent_c < star_c:

                return [right_arrow]

            # agent right to star
            if agent_c > star_c:

                return [left_arrow]

    # go away from star column for build the pilar
    if space_left_available_for_agent and layout[agent_r + 1, agent_c - 1] == rfts.DRAWN:
        return [left_arrow]

    if space_right_available_for_agent and layout[agent_r + 1, agent_c + 1] == rfts.DRAWN:
        return [right_arrow]

    # Put the agent between two blocks
    if space_left_available_for_agent and layout[agent_r + 1, agent_c - 1] != rfts.DRAWN and \
            space_right_available_for_agent and layout[agent_r + 1, agent_c + 1] != rfts.DRAWN:
        return [(agent_r + 1, agent_c - 1), (agent_r + 1, agent_c + 1)]

    if space_left_available_for_agent and layout[agent_r + 1, agent_c - 1] != rfts.DRAWN:
        return [(agent_r + 1, agent_c - 1)]

    if space_right_available_for_agent and layout[agent_r + 1, agent_c + 1] != rfts.DRAWN:
        return [(agent_r + 1, agent_c + 1)]



def climb_the_pilar_rfts_policy_random_1(layout):
    agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
    star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
    right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
    left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])
    _, ncols = layout.shape

    # there is place to build stairs to climb from left
    space_left_available_for_agent = agent_c > 0

    # there is place to build stairs to climb from right
    space_right_available_for_agent = agent_c < ncols - 1

    # Agent is not under the star
    if star_c != agent_c:

        # Put a block under the star and in the agent row
        if layout[agent_r, star_c] != rfts.DRAWN:

            return [(agent_r, star_c)]

        # Climb the pilar!
        else:
            # agent left to star
            if agent_c < star_c:

                return [right_arrow]

            # agent right to star
            if agent_c > star_c:

                return [left_arrow]

    # Put the agent between two blocks
    if space_left_available_for_agent and layout[agent_r + 1, agent_c - 1] != rfts.DRAWN and \
            space_right_available_for_agent and layout[agent_r + 1, agent_c + 1] != rfts.DRAWN:

        return [(agent_r + 1, agent_c - 1), (agent_r + 1, agent_c + 1)]

    if space_left_available_for_agent and layout[agent_r + 1, agent_c - 1] != rfts.DRAWN:

        return [(agent_r + 1, agent_c - 1)]

    if space_right_available_for_agent and layout[agent_r + 1, agent_c + 1] != rfts.DRAWN:

        return [(agent_r + 1, agent_c + 1)]

    # go away from star column for build the pilar
    if space_left_available_for_agent and layout[agent_r + 1, agent_c - 1] == rfts.DRAWN and \
            space_right_available_for_agent and layout[agent_r + 1, agent_c + 1] == rfts.DRAWN:
        return [right_arrow, left_arrow]

    if space_left_available_for_agent and layout[agent_r + 1, agent_c - 1] == rfts.DRAWN:
        return [left_arrow]

    if space_right_available_for_agent and layout[agent_r + 1, agent_c + 1] == rfts.DRAWN:
        return [right_arrow]


def general_policy_rfts(layout, mode):
    """
    High level language:
        If agent in the star row advances to star
        Click on all the empty boxes in the agent's row
        right or left arrow
    """

    agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
    star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
    right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
    left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])
    _, num_cols = layout.shape

    height_to_star = agent_r - star_r

    agent_row_has_empty = np.any(layout[agent_r] == rfts.EMPTY)

    # Walk in the direction of the star
    if height_to_star == 0:

        if agent_c < star_c:
            return [right_arrow]

        if agent_c > star_c:
            return [left_arrow]

    # Walk in the direction of the star
    if not agent_row_has_empty:

        # there is place to build stairs to climb from left
        space_left_available_for_agent = agent_c > 0

        # there is place to build stairs to climb from right
        space_right_available_for_agent = agent_c + 1 < num_cols

        if agent_c < star_c:

            if space_right_available_for_agent:
                return [right_arrow]
            else:
                return [left_arrow]

        if agent_c > star_c:

            if space_left_available_for_agent:
                return [left_arrow]
            else:
                return [right_arrow]

        if agent_c == star_c:

            return [right_arrow, left_arrow]

    # Fill the row of the agent with drawns
    agent_row_emptys = [(agent_r, ec[0]) for ec in np.argwhere(layout[agent_r] == rfts.EMPTY)]
    if mode == 'bunch':
        return agent_row_emptys
    elif mode == 'single_deterministic':
        return [agent_row_emptys[0]]
    else:
        return [random.choice(agent_row_emptys)]


def general_policy_rfts_cell_bunch(layout):
    return general_policy_rfts(layout, 'bunch')


def general_policy_rfts_single_cell_deterministic(layout):
    return general_policy_rfts(layout, 'single_deterministic')


def general_policy_rfts_single_cell_random(layout):
    return general_policy_rfts(layout, 'single_random')


def general_policy_rfts_old(layout, mode):
    """
    High level language:
        If agent in the star row advances to star
        Click on all the empty boxes in the agent's row
        right or left arrow
    """

    agent_r, agent_c = np.argwhere(layout == rfts.AGENT)[0]
    star_r, star_c = np.argwhere(layout == rfts.STAR)[0]
    right_arrow = tuple(np.argwhere(layout == rfts.RIGHT_ARROW)[0])
    left_arrow = tuple(np.argwhere(layout == rfts.LEFT_ARROW)[0])
    _, num_cols = layout.shape

    height_to_star = agent_r - star_r

    agent_row_has_empty = np.any(layout[agent_r] == rfts.EMPTY)

    # there is place to build stairs to climb from left
    space_left_available_for_agent = agent_c > 0

    # there is place to build stairs to climb from right
    space_right_available_for_agent = agent_c + 1 < num_cols

    # Walk in the direction of the star
    if height_to_star == 0:

        if agent_c < star_c:
            return [right_arrow]

        if agent_c > star_c:
            return [left_arrow]

    # Walk in the direction of the star
    if not agent_row_has_empty:

        if space_right_available_for_agent:

            if agent_c <= star_c:
                return [right_arrow]
            else:
                return [left_arrow]

        if space_left_available_for_agent:

            if agent_c >= star_c:
                return [left_arrow]
            else:
                return [right_arrow]

    # Fill the row of the agent with drawns
    agent_row_emptys = [(agent_r, ec[0]) for ec in np.argwhere(layout[agent_r] == rfts.EMPTY)]
    if mode == 'bunch':
        return agent_row_emptys
    elif mode == 'single_deterministic':
        return [agent_row_emptys[0]]
    else:
        return [random.choice(agent_row_emptys)]
