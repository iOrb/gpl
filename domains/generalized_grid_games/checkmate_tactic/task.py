
from gpl.task import ITask
from .grammar.grammar import Grammar
from ..utils import unserialize_layout, create_gym_env, get_operators, infer_info_from_state
from collections import defaultdict

from generalization_grid_games.envs import CheckmateTactic

import numpy as np

from .expand_state_space import expand_state_space


class Task(ITask):
    """
    General Grid planning task
    """
    def __init__(self, domain_name, instance_file_name, objects):
        super().__init__(domain_name, instance_file_name)
        self.initial_state = unserialize_layout(self._instance_file_name)
        self.env = create_gym_env(CheckmateTactic, self.initial_state)
        self.actions = get_operators(self.initial_state)
        self.grammar = Grammar(self._domain_name, objects, self.actions)

    def encode_state(self, state, info):
        return self.grammar.encode_state(state, info)

    def state_to_atoms(self, state, info):
        return self.grammar.state_to_atoms(state, info)

    def state_to_atoms_string(self, state, info):
        return self.grammar.atom_tuples_to_string(self.state_to_atom_tuples(state, info))

    def get_successor_states(self, state0):
        successors = defaultdict(list)
        tmp_succ_encoded = defaultdict(set)
        for action in self.actions:
            states1 = self.env.possible_transitions(state0, action)
            for state1 in states1:
                is_goal, is_dead_end, reward = infer_info_from_state(self.env, state0, action, state1)
                info = {'reward': reward,
                        'is_goal': is_goal,
                        'is_dead_end': is_dead_end,
                        'prev_layout': state0,
                        'clicked': action}
                state1_encoded = self.encode_state(state1, info)
                if state0.shape == state1.shape:
                    if np.array_equal(state0, state1):
                        continue
                if state1_encoded in tmp_succ_encoded[action]:
                    continue
                tmp_succ_encoded[action].add(state1_encoded)
                successors[action].append((action, (state1, info)))
        return successors

    def transition(self, state0, action):
        state1 = self.env.transition(state0, action)
        is_goal, is_dead_end, reward = infer_info_from_state(self.env, state0, action, state1)
        info = {'reward': reward,
                'is_goal': is_goal,
                'is_dead_end': is_dead_end,
                'prev_layout': state0,
                'clicked': action}
        return (state1, info)

    def infer_info_from_state(self, state0, operator, state1):
        is_goal, is_dead_end, reward = infer_info_from_state(self.env, state0, operator, state1)
        return is_goal, is_dead_end, reward

    def get_all_possible_operators(self, state=None):
        return get_operators(state)

    def expand_state_space(self, teach_policies, output):
        expand_state_space(self, teach_policies, output)