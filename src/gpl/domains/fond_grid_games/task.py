import copy

from gpl.task import ITask
from gpl.utils import unpack_state
import random
from .grammar.grammar import Grammar

from .grammar.objects import OBJECTS

# State: (representation, info, state_encoded)

class Task(ITask):
    """
    General Planning task
    """
    def __init__(self, domain_name, instance_name, env, params):
        super().__init__(domain_name, instance_name)

        self.params = params
        self.env = env
        self.__init_task(instance_name)

    def __init_task(self, instance_name):
        brd = self.env.get_grid(instance_name)
        self.__representative_instance_name = "{}x{}".format(*brd.shape)
        num_actions_executed = 0
        r = (brd, OBJECTS.player.w, num_actions_executed)
        info = {'goal': 0, 'deadend': 0}
        self.grammar = Grammar(self.get_domain_name(),)
        encoded_s = self.grammar.encode_state(r, info)
        self.initial_state = (r, info, encoded_s)

    def encode_state(self, rep, info):
        return self.grammar.encode_state(rep, info)

    def state_to_atoms(self, state):
        return self.grammar.state_to_atoms(state, self.params)

    def state_to_atoms_string(self, state,):
        return self.grammar.atom_tuples_to_string(self.state_to_atom_tuples(state,))

    def transition(self, state0, operator):  # s -> a -> s'
        r0 = state0[0]
        goal, deadend = self.infer_info(r0)
        assert not goal and not deadend
        r1 = self.env.act(r0, operator)  # our move
        goal, deadend = self.infer_info(r1)
        if goal or deadend or r1[1] == OBJECTS.player.w:
            return self.colapse_state(r1, goal, deadend)
        op = self.env.player2_policy(r1)
        r2 = self.env.act(r1, op)  # adversary move
        goal, deadend = self.infer_info(r2)
        return self.colapse_state(r2, goal, deadend)

    def infer_info(self, r):
        goal, deadend = [0] * 2
        gstatus = self.env.check_game_status(r)
        if gstatus == 1:
            goal = True
        elif gstatus == -1:
            deadend = True
        return goal, deadend

    def colapse_state(self, rep1, goal, deadend):
        info = {'goal': goal,
                'deadend': deadend}
        s_encoded = self.encode_state(rep1, info)
        state1 = (rep1, info, s_encoded)
        return state1

    def get_successor_states(self, state0):
        def __transition_player(state, op):  # s -> a -> s'
            r = state[0]
            goal, deadend = self.infer_info(r)
            try:
                assert not goal and not deadend
            except:
                pass
            r1 = self.env.act(r, op)  # player move
            goal, deadend = self.infer_info(r1)
            return self.colapse_state(r1, goal, deadend)
        r0 = state0[0]
        succs_sp = []
        ava_actions = self.env.available_actions(r0)
        for op0 in ava_actions:
            state1 = __transition_player(state0, op0)
            if state1[1]['goal'] or state1[1]['deadend'] or state1[0][1] == OBJECTS.player.w:
                if state1[2] == state0[2]:
                    continue
                succs_sp.append((op0, state1))
            else:
                succs_spp = []
                ava_actions1 = self.env.available_actions(state1[0])
                for op1 in ava_actions1:
                    state2 = __transition_player(state1, op1)
                    if state2[2] == state1[2]:
                        continue
                    succs_spp.append((op0, state2))
                if succs_spp:
                    succs_sp += succs_spp
        return succs_sp

    def get_representative_instance_name(self):
        return self.__representative_instance_name

    def encode_sa_pair(self, sa):
        s, op = sa
        sa_enc = '_'.join([str(s[2]), str(op)])
        return sa_enc