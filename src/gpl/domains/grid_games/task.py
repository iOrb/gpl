import copy

from gpl.task import ITask
from gpl.utils import Bunch
import random
from .grammar.grammar import Grammar
from .grammar.objects import get_domain_objects
from collections import defaultdict

# State: (representation, state_encoded)

i =0
class Task(ITask):
    """
    General Planning task
    """
    def __init__(self, domain_name, instance_name, env):
        super().__init__(domain_name, instance_name)
        self.params = env.params
        self.env = env
        self.objects = get_domain_objects(domain_name)
        self.__init_task(instance_name)

    def __init_task(self, instance_name):
        rep = self.env.init_instance(instance_name)
        self.grammar = Grammar(self.get_domain_name(), self.params)
        encoded_s = self.grammar.encode_state(rep)
        self.initial_state = (rep, encoded_s)

    def encode_state(self, rep):
        return self.grammar.encode_state(rep)

    def state_to_atoms(self, state):
        return self.grammar.state_to_atoms(state)

    def state_to_atoms_string(self, state,):
        return self.grammar.atom_tuples_to_string(self.state_to_atom_tuples(state,))

    def transition_env(self, state1):  # s' -> a -> s"
        r1=state1[0]
        if r1.goal or r1.deadend or r1.player == self.objects.player1:
            return self.colapse_state(r1)
        op = self.env.player2_policy(r1)
        r2 = self.env.act(r1, op)  # adversary move
        s2 = self.colapse_state(r2)
        if r2.player != self.objects.player1:
            return self.transition_env(s2)
        else:
            return s2

    def colapse_state(self, rep):
        s_encoded = self.encode_state(rep)
        state1 = (rep, s_encoded)
        return state1

    def get_successor_states(self, s0, just_sp=False):
        def __transition_player(state, op):  # s -> a -> s'
            r = state[0]
            assert not r.goal and not r.deadend
            r1 = self.env.act(r, op)  # player move
            return self.colapse_state(r1)
        r0 = s0[0]
        succs_sp = list()
        succs = list()
        succs_reps = list()
        assert r0.player == self.objects.player1
        avaactions = self.env.available_actions(r0)
        for op0 in avaactions:
            s1 = __transition_player(s0, op0)
            succs_sp.append((op0, s1))
            if s1[0].goal or s1[0].deadend or s1[0].player == self.objects.player1:
                # if s1[1] == s0[1]:
                #     continue
                succs.append((op0, s1, s1))
            else:
                assert s1[0].player == self.objects.player2
                s2 = copy.deepcopy(s1)
                queue = [s2]
                vistited_s2={s2[1]}
                while queue:
                    s2_ = queue.pop()
                    ava_actions_1 = self.env.available_actions(s2_[0])
                    for op1 in ava_actions_1:
                        s2 = __transition_player(s2_, op1)
                        if s2[0].player == self.objects.player1:
                            succs.append((op0, s1, s2))
                        else:
                            if s2[1] not in vistited_s2:
                                queue.append(s2)

        # succs_reps.append(r0)
        # for _, sp, spp in succs:
        #     succs_reps.append(sp[0])
        #     if sp[1] != spp[1]:
        #         succs_reps.append(spp[0])
        # self.print_path(succs_reps)

        # succs_reps.append(r0)
        # for _, sp in succs_sp:
        #     succs_reps.append(sp[0])
        # self.print_path(succs_reps)

        if just_sp:
            return succs_sp
        else:
            return succs

    def get_representative_instance_name(self):
        return self.get_instance_name()
        # return self.__representative_instance_name

    def encode_sa_pair(self, sa):
        s, op = sa
        sa_enc = '_'.join([str(s[1]), str(op)])
        return sa_enc

    def print_state(self, s):
        layout = s[0].grid
        nrows, ncols = layout.shape
        for r in range(0, nrows):
            tmp_str = ""
            for c in range(0, ncols):
                tmp_str += SIMPLIFIED_OBJECT[layout[r, c]]
            print(tmp_str)
        print("#" * ncols)

    def print_path(self, reps):
        simplified_objects = self.env.get_simplified_objects()
        nrows, ncols = reps[0].grid.shape
        total_path_rep = ""
        for row in range(nrows):
            tmp_full_row = ""
            for rep in reps:
                layout = rep.grid
                tmp_row = ""
                for o in layout[row, :]:
                    tmp_row += simplified_objects[o]
                tmp_full_row += "{} # ".format(tmp_row)
            total_path_rep += "{}\n".format(tmp_full_row)

        single_rep_row = ""
        for o in layout[0, :]:
            single_rep_row += simplified_objects[o]
        size_single_row = len("{} # ".format(single_rep_row))

        info_to_print = ["player", "nmoves", "last_turn", "next_player", "holding_pet", "goal"]
        for info in info_to_print:
            try:
                tmp_full_row = ""
                for rep in reps:
                    att = getattr(rep, info)
                    tmp_full_row += "{} ({})".format(int(att), info[:2]).ljust(size_single_row)
                total_path_rep += "{}\n".format(tmp_full_row)
            except:
                pass

        print(total_path_rep)

    def get_printable_rep(self, rep):
        simplified_objects = self.env.get_simplified_objects()
        layout = rep.grid
        nrows, ncols = layout.shape
        total_rep = ""
        for row in range(nrows):
            tmp_row = ""
            for o in layout[row, :]:
                tmp_row += simplified_objects[o]
            total_rep += "#{}#\n".format(tmp_row)
        return total_rep

    def encode_op(self, s, op):
        return self.env.encode_op(s[0], op)