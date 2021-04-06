
from gpl.task import ITask
from .grammar.grammar import Grammar
from ..utils import unserialize_layout, create_gym_env, get_operators
from  gpl.utils import unpack_state

from generalization_grid_games.envs import CheckmateTactic

import numpy as np
import random

from .expand_state_space import expand_state_space

# State: (representation, info, state_encoded)

class Task(ITask):
    """
    General Planning task
    """
    def __init__(self, domain_name, objects, instance_file_name=None, initial_state=None,):
        super().__init__(domain_name, objects,)

        self._objects = objects
        self.__init_task(instance_file_name, initial_state)
        self.env = create_gym_env(CheckmateTactic, self.initial_state[0])

    def __init_task(self, instance_file_name, initial_state):

        assert (initial_state and not instance_file_name) or (not initial_state and instance_file_name)

        def __init_from_state():
            self.actions = get_operators(initial_state[0])
            self.grammar = Grammar(self._domain_name, self._objects, self.actions)
            self.initial_state = initial_state

        def __init_from_file():
            r = unserialize_layout(instance_file_name)
            info = {'goal': 0, 'deadend': 0, 'reward': 0,}
            self.actions = get_operators(r)
            self.grammar = Grammar(self._domain_name, self._objects, self.actions)
            self.initial_state = (r, info, self.grammar.encode_state(r, info))

        if initial_state is not None:
            __init_from_state()
        else:
            __init_from_file()

    def encode_state(self, representation, info):
        return self.grammar.encode_state(representation, info)

    def state_to_atoms(self, state,):
        return self.grammar.state_to_atoms(state,)

    def state_to_atoms_string(self, state,):
        return self.grammar.atom_tuples_to_string(self.state_to_atom_tuples(state,))

    def get_successor_states(self, state0):
        successors = []
        tmp_succ_encoded = set()
        for op in self.actions:
            state1 = self.transition(state0, op)
            if state0 == state1:
                continue
            if state1[2] in tmp_succ_encoded:
                continue
            tmp_succ_encoded.add(state1[2])
            successors.append((op, state1))
        return successors

    def transition(self, state0, operator):
        rep0, _, _ = state0
        rep1 = self.env.transition(rep0, operator)
        is_goal, is_dead_end, reward = self.infer_info_from_transition(rep0, operator, rep1)
        info1 = {'reward': reward,
                 'goal': is_goal,
                 'deadend': is_dead_end,
                 'prev_repr': rep0}
        state1_encoded = self.encode_state(rep1, info1)
        state1 = (rep1, info1, state1_encoded)
        return state1

    def dfs_transition(self, state0, rng, visited=None):
        actions = self.actions
        al = list(actions)
        random.Random(rng).shuffle(al)
        for op in al:
            state1 = self.transition(state0, op)
            if self.same(state0, state1):
                continue
            if visited:
                if self.visited(state1, visited):
                    continue
            return state1, op
        return None, None

    def visited(self, s, visited):
        if s[2] in visited:
            return True
        else:
            return False

    def infer_info_from_transition(self, state0, operator, state1):
        is_goal, is_dead_end, reward = infer_info_from_transition(self.env, state0, operator, state1)
        return is_goal, is_dead_end, reward

    def get_all_possible_operators(self, state=None):
        return get_operators(state)

    def filter_successors(self, s, succs, instance_name, task):
        alive, goals, deadends = list(), list(), list()
        for op, sprime in succs:
            s_r, goal, deadend, s_encoded, info = unpack_state(sprime)
            if goal:
                goals.append((op, sprime))
            elif deadend:
                deadends.append((op, sprime))
            else:
                alive.append((op, sprime))
        return alive, goals, deadends

    def expand_state_space(self, teach_policies, output):
        expand_state_space(self, teach_policies, output)



def infer_info_from_transition(env, r0, action, r1):
    """
    Infer some relevant info from the current state, based on the simulator
    """
    reward = env.compute_reward(r0, action, r1)
    is_done = env.compute_done(r1)

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
