
from lgp.grammar.grammar import Grammar
from .domains import get_domain_data
from lgp.utils import unserialize_layout, create_gym_env, get_operators, infer_info_from_state
from collections import defaultdict

import numpy as np


class Task:
    """
    General Grid planning task
    """
    def __init__(self, domain_name, instance_file_name):
        self.domain = get_domain_data(domain_name)
        self.initial_state = unserialize_layout(instance_file_name)
        self.grammar = Grammar(self.domain, self.initial_state)
        self.env = create_gym_env(self.domain.base_class, self.initial_state)
        self.actions = get_operators(self.initial_state)

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