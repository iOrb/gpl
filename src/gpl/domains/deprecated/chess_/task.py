import chess
from gpl.task import ITask
from gpl.utils import unpack_state
import random
from gpl.domains.deprecated.chess_.grammar.grammar import Grammar
from .instances import INSTANCES
from stockfish import Stockfish
from .utils import stockfish_default_params

# State: (representation, info, state_encoded)

class Task(ITask):
    """
    General Planning task
    """
    def __init__(self, domain_name, instance_name, config):
        super().__init__(domain_name, instance_name)

        self.player2_agent = Stockfish(parameters=stockfish_default_params)
        self.config = config
        self.env = chess.Board()
        # self.env = gym.make('chess-v0')
        self.__init_task(instance_name)

    def __init_task(self, instance_name):
        # brd, mark = self.env.reset()
        fen_rep = INSTANCES[instance_name]
        self.env.set_fen(fen_rep)
        self.player2_agent.set_fen_position(fen_rep)
        info = {'goal': False,
                'deadend': False,
                'prev_repr': 'root'}
        self.grammar = Grammar(self._domain_name,)
        encoded_s = self.encode_state(fen_rep, info)
        self.initial_state = (fen_rep, info, encoded_s)

    def encode_state(self, representation, info):
        return self.grammar.encode_state(representation, info)

    def state_to_atoms(self, state,):
        return self.grammar.state_to_atoms(state,)

    def state_to_atoms_string(self, state,):
        return self.grammar.atom_tuples_to_string(self.state_to_atom_tuples(state,))

    def get_successor_states(self, state0,):  # just 1 s" for each s -> a
        # if hasattr(self.config, 'all_possible_successors'):
        #     if self.config.all_possible_successors:
        #         return self.get_successor_states_all(state0)
        successors = []
        r0 = state0[0]
        self.env.set_fen(r0)
        tmp_succ_encoded = set()
        ava_actions = self.env.legal_moves
        for op in ava_actions:
            state1 = self.transition(state0, op)
            if state1[2] == state0[2]:
                continue
            if state1[2] in tmp_succ_encoded:
                continue
            self.env.set_fen(r0)
            tmp_succ_encoded.add(state1[2])
            successors.append((op, state1))
        return successors

    def transition(self, state0, operator):  # s -> a -> s' -> a -> s"
        r0 = state0[0]
        self.env.set_fen(r0)
        goal, deadend = self.infer_info(r0)
        assert not goal and not deadend
        self.env.push(operator)  # our move
        r1 = self.env.fen()
        goal, deadend = self.infer_info()
        if goal or deadend:
            return self.colapse_state(r1, goal, deadend, r0)
        self.player2_agent.set_fen_position(r1)
        op = self.player2_agent.get_best_move_time(time=5)
        self.env.push_uci(op)  # adversary move
        r2 = self.env.fen()
        goal, deadend = self.infer_info()
        return self.colapse_state(r2, goal, deadend, r0)

    def infer_info(self,):
        goal, deadend = [0] * 2
        if self.env.is_game_over():
            if self.env.is_checkmate() and not self.env.turn:
                goal = True
            else:
                deadend = True
        return goal, deadend

    def colapse_state(self, rep1, goal, deadend, rep0):
        info = {'goal': goal,
                'deadend': deadend,
                'prev_repr': rep0}
        s_encoded = self.encode_state(rep1, info)
        state1 = (rep1, info, s_encoded)
        return state1

    # def get_successor_states_all(self, state0): # all possible s" for each s -> a
    #
    #     def __transition_player(s, op):  # s -> a -> s'
    #         brd0, mark0 = s[0]
    #         goal, deadend = self.infer_info(brd0)
    #         assert not goal and not deadend
    #
    #         brd1, mark1 = after_action_state((brd0, mark0), op)  # player move
    #         goal, deadend = self.infer_info(brd1)
    #         return self.colapse_state((brd1, mark1), goal, deadend, (brd0, mark0))
    #
    #     successors = []
    #     brd0, mark0 = state0[0]
    #     tmp_succ_encoded = set()
    #     ava_actions = available_actions(brd0)
    #
    #     for op0 in ava_actions:
    #         state1 = __transition_player(state0, op0)
    #         if state1[1]['goal'] or state1[1]['deadend']:
    #             if state1[2] == state0[2]:
    #                 continue
    #             if state1[2] in tmp_succ_encoded:
    #                 continue
    #             tmp_succ_encoded.add(state1[2])
    #             successors.append((op0, state1))
    #         else:
    #             ava_actions1 = available_actions(state1[0][0])
    #             for op1 in ava_actions1:
    #                 state2 = __transition_player(state1, op1)
    #                 if state2[2] == state1[2]:
    #                     continue
    #                 if state2[2] in tmp_succ_encoded:
    #                     continue
    #                 tmp_succ_encoded.add(state2[2])
    #                 successors.append((op1, state2))
    #
    #     return successors

    def filter_successors(self, succs,):
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


class BaseAgent(object):
    def __init__(self, mark):
        self.mark = mark

    def act(self, state, ava_actions):
        for action in ava_actions:
            nstate = after_action_state(state, action)
            gstatus = check_game_status(nstate[0])
            if gstatus > 0:
                if tomark(gstatus) == self.mark:
                    return action
        return random.choice(ava_actions)
        # return ava_actions[-1]
