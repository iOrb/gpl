import copy

from gpl.task import ITask
from gpl.utils import unpack_state
import random
from .grammar.grammar import Grammar
from .utils import stockfish_default_params

from ..utils import unserialize_layout, get_operators
from .grammar.objects import OBJECTS
from generalization_grid_games_2.envs.checkmate_tactic import available_actions, check_game_status, act, player2_policy

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
        self.grammar = Grammar(self.get_domain_name(),)
        encoded_s = self.grammar.encode_state(r, info)
        self.initial_state = (r, info, encoded_s)
        self.queue = [self.initial_state]

    def get_state_from_queue(self):
        if self.queue:
            return self.queue.pop(0)
        else:
            return None

    def add_state_to_queue(self, state):
        self.queue.append(state)

    def encode_state(self, rep, info):
        return self.grammar.encode_state(rep, info)

    def state_to_atoms(self, state,):
        return self.grammar.state_to_atoms(state,)

    def state_to_atoms_string(self, state,):
        return self.grammar.atom_tuples_to_string(self.state_to_atom_tuples(state,))

    def transition_adversary(self, sp):  # (FOND Adversary) s' -> a -> s"
        r0 = sp[0]
        goal, deadend = self.infer_info(r0)
        assert not goal and not deadend

        op = player2_policy(r0)
        r1 = act(r0, op)  # adversary move
        goal, deadend = self.infer_info(r1)
        assert not goal and not deadend
        return self.colapse_state(r1, goal, deadend, r0)

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

    def get_successor_states(self, state0):
        # all possible s' for each s, and all possible s" for each alive s

        def __transition_player(state, op):  # s -> a -> s'
            r = state[0]
            goal, deadend = self.infer_info(r)
            assert not goal and not deadend

            r1 = act(r, op)  # player move
            goal, deadend = self.infer_info(r1)
            return self.colapse_state(r1, goal, deadend, r)

        r0 = state0[0]
        succs_sp = []
        visited_tx = set()
        ava_actions = available_actions(r0)

        for op0 in ava_actions:
            state1 = __transition_player(state0, op0)
            if state1[1]['goal'] or state1[1]['deadend']:
                if state1[2] == state0[2]:
                    continue
                tx_enc = self.encode_tx((state0, op0, state1))
                if tx_enc in visited_tx:
                    continue
                visited_tx.add(tx_enc)
                succs_sp.append((op0, state1, None))
            else:
                succs_spp = []
                ava_actions1 = available_actions(state1[0])
                # deadend = False
                for op1 in ava_actions1:
                    state2 = __transition_player(state1, op1)
                    if state2[2] == state1[2]:
                        continue
                    tx_enc = self.encode_tx((state0, op0, state2))
                    if tx_enc in visited_tx:
                        continue
                    visited_tx.add(state2[2])
                    # assert not state2[1]['goal']
                    # if state2[1]['deadend']:
                    #     deadend = True
                    succs_spp.append((op1, state2))
                    # succs_sp.append((op0, state2, None))
                # if deadend:
                # #     If any succ(s') is dead-end, then s' is dead-end
                #     succs_sp.append((op0, self.__change_to_deadend(state1), succs_spp))
                # else:
                # #     If not-any succ(s') is dead-end, then s' is alive
                #     succs_sp.append((op0, state1, succs_spp))
                succs_sp.append((op0, state1, succs_spp))

        return succs_sp

    def __change_to_deadend(self, s):
        new_info = copy.deepcopy(s[1])
        new_info['deadend'] = True
        return (s[0], new_info, s[2])

    def encode_tx(self, tx):
        s, op, sp = tx
        op_enc = self.encode_op(s, op)
        tx_enc = '_'.join([str(s[2]), op_enc, str(sp[2])])
        return tx_enc

    def encode_op(self, s, op):
        piece = s[0][0][op[0][0], op[0][1]]
        assert piece not in "empty"
        o = copy.deepcopy(op)
        return "{}_{}.{}_{}.{}".format(piece, o[0][0], o[0][1], o[1][0], o[1][1])
