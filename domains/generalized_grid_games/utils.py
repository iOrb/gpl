import json
import numpy as np

from generalization_grid_games.envs.generalization_grid_game import GymEnvFactory


def serialize_layout(layout, filename):
    if not isinstance(layout, list):
        layout = layout.tolist()

    with open(filename, 'w') as f:
        json.dump(layout, f)


def unserialize_layout(filename):
    with open(filename, 'r') as f:
        return np.array(json.loads(f.read()), dtype=object)


def create_gym_env(base_class, layout):
    return GymEnvFactory(base_class, 0, layout)


def in_state(cell, state):
    r, c = cell
    if 0 <= r < len(state) and 0 <= c < len(state[0]):
        return True
    else:
        return False


def get_operators(state):
    positions = set()
    for row in range(len(state)):
        for col in range(len(state[0])):
            positions.add((row, col))
    return positions


def get_operators_from_shape(height, width):
    positions = set()
    for row in range(height):
        for col in range(width):
            positions.add((row, col))
    return positions


def infer_info_from_state(env, state0, action, state1):
    """
    Infer some relevant info from the current state, based on the simulator
    """
    reward = env.compute_reward(state0, action, state1)
    try:
        is_done = env.compute_done(state1)
    except:
        print('h')

    if is_done:

        if reward == 1.:

            reward = 1
            is_goal = 1
            is_dead_end = 0

        else:

            reward = 0  # rewards different than 1. or 0 are not registered at the moment
            is_goal = 0
            is_dead_end = 1

    else:

        reward = 0
        is_goal = 0
        is_dead_end = 0

    return is_goal, is_dead_end, reward
