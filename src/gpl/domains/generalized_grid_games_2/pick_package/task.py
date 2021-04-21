import copy

from gpl.task import ITask
from gpl.utils import unpack_state
import random
from .grammar.grammar import Grammar
from .instances import INSTANCES
from .utils import stockfish_default_params

from ..utils import unserialize_layout, get_operators
from .grammar.objects import OBJECTS
# from generalization_grid_games_2.envs.checkmate_tactic import available_actions, check_game_status, act, player2_policy
from generalization_grid_games_2.envs.pick_package import available_actions, check_game_status, act

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

    def transition(self, state0, operator):  # s -> a -> s'
        r0 = state0[0]
        goal, deadend = self.infer_info(r0)
        assert not goal and not deadend

        r1 = act(r0, operator)  # our move
        goal, deadend = self.infer_info(r1)
        return self.colapse_state(r1, goal, deadend, r0)

    def infer_info(self, r):
        goal, deadend = [0] * 2
        gstatus = check_game_status(r)
        if gstatus == 1:
            goal = True
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
        r0 = state0[0]
        succs_sp = []
        visited_tx = set()
        ava_actions = available_actions(r0)

        for op0 in ava_actions:
            state1 = self.transition(state0, op0)
            if state1[2] == state0[2]:
                continue
            tx_enc = self.encode_tx((state0[2], op0, state1[2]))
            if tx_enc in visited_tx:
                continue
            visited_tx.add(tx_enc)
            succs_sp.append((op0, state1, None))

        return succs_sp

    def encode_tx(self, tx):
        s_enc, op, sp_enc = tx
        op_enc = self.encode_op(op)
        tx_enc = '_'.join([str(s_enc), op_enc, str(sp_enc)])
        return tx_enc

    def encode_op(self, op):
        o = copy.deepcopy(op)
        return "{}.{}_{}.{}".format(o[0][0], o[0][1], o[1][0], o[1][1])
