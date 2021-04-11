import copy

import chess
from gpl.task import ITask
from gpl.utils import unpack_state
import random
from .grammar.grammar import Grammar
from .instances import INSTANCES
from .utils import stockfish_default_params

from ..utils import unserialize_layout, get_operators
from .grammar.objects import OBJECTS
from generalization_grid_games_2.envs.checkmate_tactic import available_actions, check_game_status, act, player2_policy
# from generalization_grid_games_2.envs.checkmate_tactic import check_game_status, after_action_state, tomark, available_actions

# State: (representation, info, state_encoded)

class Task(ITask):
    """
    General Planning task
    """
    def __init__(self, domain_name, instance_name, config):
        super().__init__(domain_name, instance_name)

        self.config = config
        self.__init_task(instance_name)

    def __init_task(self, instance_name):
        brd = unserialize_layout(instance_name)
        r = (brd, OBJECTS.player.w)
        info = {'goal': 0, 'deadend': 0, 'reward': 0,}
        self.grammar = Grammar(self._domain_name,)
        encoded_s = self.grammar.encode_state(r, info)
        self.initial_state = (r, info, encoded_s)

    def encode_state(self, rep, info):
        return self.grammar.encode_state(rep, info)

    def state_to_atoms(self, state,):
        return self.grammar.state_to_atoms(state,)

    def state_to_atoms_string(self, state,):
        return self.grammar.atom_tuples_to_string(self.state_to_atom_tuples(state,))

    def get_successor_states(self, state0,):  # just 1 s" for each s -> a
        if hasattr(self.config, 'all_possible_successors'):
            if self.config.all_possible_successors:
                return self.get_successor_states_all(state0)
        successors = []
        r0 = state0[0]
        tmp_succ_encoded = set()
        ava_actions = available_actions(r0)
        for op in ava_actions:
            state1 = self.transition(state0, op)
            if state1[2] == state0[2]:
                continue
            if state1[2] in tmp_succ_encoded:
                continue
            tmp_succ_encoded.add(state1[2])
            successors.append((op, state1))
        return successors

    def transition(self, state0, operator):  # s -> a -> s' -> a -> s"
        r0 = state0[0]
        goal, deadend = self.infer_info(r0)
        assert not goal and not deadend

        r1 = act(r0, operator)  # our move
        goal, deadend = self.infer_info(r1)
        if goal or deadend:
            return self.colapse_state(r1, goal, deadend, r0)

        op = player2_policy(r1)
        r2 = act(r1, op)  # adversary move
        goal, deadend = self.infer_info(r2)
        return self.colapse_state(r2, goal, deadend, r1)

    def infer_info(self, r):
        goal, deadend = [0] * 2
        gstatus = check_game_status(r)
        if gstatus == 1:
            goal = True
        if gstatus == 0:
            deadend = True
        return goal, deadend

    def colapse_state(self, rep1, goal, deadend, rep0):
        info = {'goal': goal,
                'deadend': deadend,
                'prev_repr': rep0}
        s_encoded = self.encode_state(rep1, info)
        state1 = (rep1, info, s_encoded)
        return state1

    def get_successor_states_all(self, state0): # all possible s" for each s -> a

        def __transition_player(state, op, root=None):  # s -> a -> s'
            r = state[0]
            goal, deadend = self.infer_info(r)
            assert not goal and not deadend

            r1 = act(r, op)  # player move
            goal, deadend = self.infer_info(r1)
            return self.colapse_state(r1, goal, deadend, root if root else r)

        r0 = state0[0]
        successors = []
        tmp_succ_encoded = set()
        ava_actions = available_actions(r0)

        for op0 in ava_actions:
            state1 = __transition_player(state0, op0)
            if state1[1]['goal'] or state1[1]['deadend']:
                if state1[2] == state0[2]:
                    continue
                if state1[2] in tmp_succ_encoded:
                    continue
                tmp_succ_encoded.add(state1[2])
                successors.append((op0, state1))
            else:
                ava_actions1 = available_actions(state1[0])
                for op1 in ava_actions1:
                    state2 = __transition_player(state1, op1, r0)
                    if state2[2] == state1[2]:
                        continue
                    if state2[2] in tmp_succ_encoded:
                        continue
                    tmp_succ_encoded.add(state2[2])
                    successors.append((op0, state2))

        return successors

    def encode_op(self, op):
        o = copy.deepcopy(op)
        return "{}.{}_{}.{}".format(o[0][0], o[0][1], o[1][0], o[1][1])

    def filter_successors(self, succs, ):
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