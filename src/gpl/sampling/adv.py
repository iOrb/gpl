import copy
import itertools
import logging
import math
import sys
from collections import defaultdict, OrderedDict, deque

from ..utils import encode_operator

from sltp.returncodes import ExitCode
from sltp.util.command import read_file
from sltp.util.naming import filename_core


class TransitionSampleADV:
    """ """
    def __init__(self):
        self.states = OrderedDict()
        self.states_encoded = dict()
        self.operators = dict()
        self.transitions = defaultdict(lambda: defaultdict(set))
        self.adv_transitions = defaultdict(set)
        self.parents = defaultdict(set)
        self.goals = set()
        self.alive_states = set()
        self.optimal_transitions = defaultdict(set)
        self.roots = set()  # The set of all roots
        self.instance_roots = dict()  # The root of each instance
        self.instance = dict()  # A mapping between states and the problem instances they came from
        self.representative_instances = dict()  # A mappint between repr_instance_name and the first seen representative_instace
        self.deadends = set()
        self.instance_ids = dict()
        self.remapping = dict()
        self.vstar = {}
        self.sid_count = 0
        self.oid_count = 0
        self.instance_id_count = 0
        self.given_action_space = False

    def add_transition(self, tx, task):
        s, op0, sp, spp = tx
        assert None not in [s, op0, sp, spp]
        new_instance_, instance_id = self.check_instance_name(task)
        sids = [self.check_state(s, task, instance_id) for s in [s, sp, spp]]
        oid = op0 if self.given_action_space else self.check_operator(s, op0, task, instance_id)
        self.update_transitions(self.get_tx(sids, oid))
        if new_instance_:
            self.mark_as_root(sids[0], instance_id)
        _ = [self.update_instance(sid, instance_id) for sid in sids]

    def update_transitions(self, tx):
        """ main method """
        s, op, sp, spp = tx # IDs
        # s: {(op0, s'): {s'', ...}}
        self.transitions[s][op].add(sp)
        self.adv_transitions[sp].add(spp)
        # parents transitions
        self.parents[sp].add(s)
        self.parents[spp].add(sp)

    def get_tx(self, sids, oid):
        return (sids[0], oid, sids[1], sids[2])

    def check_state(self, state, task, instance_id):
        sr, s_enc_raw = state
        s_encoded = self.encode_state(instance_id, s_enc_raw)
        if s_encoded not in self.states_encoded:
            self.states_encoded[s_encoded] = self.sid_count
            self.states[self.get_state_id(s_encoded)] = task.state_to_atoms(
                state)  # this should be the representation as atoms
            # print("{}. {}".format(self.sid_count, sr.goal))
            # print(task.get_printable_rep(sr))
            self.sid_count += 1
        id = self.get_state_id(s_encoded)
        if sr.goal:
            self.goals.add(id)
        elif sr.deadend:
            self.deadends.add(id)
        return id

    def get_state_id(self, s_encoded):
        return self.states_encoded[s_encoded]

    def get_instance_id(self, instance_name):
        return self.instance_ids[instance_name]

    def check_operator(self, s, op, task, instance_id):
        o_raw = encode_operator(s, op, task)
        o = self.encode_operator(instance_id, o_raw)
        if o not in self.operators:
            self.operators[o] = self.oid_count
            self.oid_count += 1
        return self.operators[o]

    def set_operators(self, ops):
        self.given_action_space = True
        for o in ops:
            self.operators[o] = o

    def update_instance(self, sid, intance_id):
        self.instance[sid] = intance_id # {state_id: instance_id}

    def check_instance_name(self, task):
        repr_instance_name = task.get_representative_instance_name()
        if repr_instance_name not in self.instance_ids:
            self.instance_ids[repr_instance_name] = self.instance_id_count
            self.representative_instances[repr_instance_name] = task.get_instance_name()
            self.instance_id_count += 1
            return True, self.get_instance_id(repr_instance_name) # the intance is new
        return False, self.get_instance_id(repr_instance_name)

    def encode_state(self, instance_id, s_enc_raw):
        return '_'.join([str(instance_id), str(s_enc_raw)])

    def encode_operator(self, instance_id, op_enc_raw):
        return '_'.join([str(instance_id), str(op_enc_raw)])

    def num_transitions(self):
        return sum(len(x) for x in self.transitions.values())

    def mark_as_optimal(self, optimal):
        for s, targets in optimal.items():
            self.optimal_transitions[s] |= targets

    def mark_as_alive(self, states):
        self.alive_states.update(states)

    def mark_as_root(self, sid, instance_id):
        self.roots.add(sid)
        self.instance_roots[instance_id] = sid # {instance_id: root_state_id}

    def mark_state_as_deadend(self, s, task):
        id = self.check_state(s, task)
        self.deadends.add(id)

    def num_states(self):
        return len(self.states)

    def info(self):
        return f"roots: {len(self.roots)}, states: {len(self.states)}, " \
               f"transitions: {self.num_transitions()} ({self.num_optimal_transitions()} optimal)," \
               f" goals: {len(self.goals)}, alive: {len(self.alive_states)}"

    def num_optimal_transitions(self):
        count = 0
        for s, targets in self.optimal_transitions.items():
            count += len(targets)
        return count

    def __str__(self):
        return "TransitionsSample[{}]".format(self.info())

    def get_sorted_state_ids(self):
        return sorted(self.states.keys())

    def get_sorted_op_ids(self):
        return sorted(self.operators.values())

    def process_successors(self, s, succs, task):
        alive, goals, deadends = list(), list(), list()
        for op, sp, spp in succs:
            sp_r, sp_encoded = sp
            spp_r, spp_encoded = spp
            self.add_transition((s, op, sp, spp), task)
            if spp_r.goal:
                goals.append((op, sp, spp))
            elif spp_r.deadend:
                deadends.append((op, sp, spp))
            else:
                alive.append((op, sp, spp))
        return alive, goals, deadends


def process_sample(config, sample, rng):
    num_tx_entries = sum(len(tx) for tx in sample.transitions.values())
    num_tx = sum(len(t) for tx in sample.transitions.values() for t in tx.values())
    logging.info('%s: #states=%d, #transition-entries=%d, #transitions=%d' %
                 ('sample', len(sample.states), num_tx_entries, num_tx))
    reorder_states_not_reachable_by_agent(config, sample)
    mark_optimal_transitions(config, sample)
    logging.info(f"Entire sample: {sample.info()}")
    return sample


def reorder_states_not_reachable_by_agent(config, sample):
    not_reachable_states = set()
    for s in sample.get_sorted_state_ids():
        if s not in sample.adv_transitions or s in sample.transitions:
            continue
        s_reachable = False
        for s_, edge in sample.transitions.items():
            for op, sps in edge.items():
                if s in sps:
                    s_reachable = True
        if not s_reachable:
            not_reachable_states.add(s)
    for s in not_reachable_states:
        logging.warning("State {} is no reachable by the agent".format(s))



def mark_optimal_transitions(config, sample):
    """
    Marks which transitions are optimal in a transition system according to some selection criterion
    such as marking *all* optimal transitions.
    """
    optimal, alive, sample.vstar = mark_all_optimal(sample)
    # We also mark which states are alive.
    sample.mark_as_alive(alive)
    # Mark all transitions that are optimal from some alive state
    sample.mark_as_optimal(optimal)


def mark_all_optimal(sample):
    goals, parents = sample.goals, sample.parents
    """ Collect all transitions that lie on at least one optimal plan starting from some alive state (i.e. solvable,
     reachable, and not a goal). """
    vstar, minactions = {}, {}
    for g in goals:
        run_backwards_brfs(g, parents, vstar, minactions, sample)

    # minactions contains a map between state IDs and a list with those successors that represent an optimal transition
    # from that state
    optimal_txs = defaultdict(set)
    for s, targets in minactions.items():
        _ = [optimal_txs[s].add(t) for t in targets]

    # Incidentally, the set of alive states will contain all states with a mincost > 0 and which have been reached on
    # the backwards brfs (i.e. for which mincost[s] is actually defined). Note that the "reachable" part of a state
    # being alive is already guaranteed by the fact that the state is on the sample, as we sample states with a simple
    # breadth first search.
    alive = {s for s, cost in vstar.items() if cost > 0}

    return optimal_txs, alive, vstar


def run_backwards_brfs(g, parents, mincosts, minactions, sample):
    queue = deque([g])
    mincosts[g] = 0
    minactions[g] = []

    prev_parcost = dict()

    # Run a breadth-first search backwards from the given goal state g
    while queue:
        cur = queue.popleft()
        curcost = mincosts[cur]

        if cur not in parents:
            # A root of the (original) breadth-first search could have no parents
            continue

        for par in parents[cur]:
            parcost = mincosts.get(par, math.inf)
            if parcost > curcost + 1:
                queue.append(par)
                mincosts[par] = curcost + 1
                minactions[par] = [cur]
            elif parcost == curcost + 1:
                minactions[par].append(cur)


def print_transition_matrix(sample, transitions_filename):
    state_ids = sample.get_sorted_state_ids()
    transitions = sample.transitions
    adv_transitions = sample.adv_transitions
    num_nondet_transitions = sum(len(t) for tx in transitions.values() for t in tx.values())
    num_adv_transitions = sum(len(tx) for tx in adv_transitions.values())
    operator_ids = sample.get_sorted_op_ids()
    num_s_with_outgoind_edge = len(transitions.keys()) - len(sample.goals) - len(sample.deadends)
    logging.info(f"Printing SAT transition matrix with {len(state_ids)} states,"
                 f" {num_s_with_outgoind_edge} states with some outgoing transition,"
                 f" {len(operator_ids)} operators,"
                 f" {num_nondet_transitions} (non-det) transitions,"
                 f" and {num_adv_transitions} (adv) transitions,")

    # State Ids should start at 0 and be contiguous
    # assert state_ids == list(range(0, len(state_ids)))

    with open(transitions_filename, 'w') as f:
        # first line: <#states> <#transitions(non-det)>
        print(f"{len(state_ids)} {num_nondet_transitions} {num_adv_transitions}", file=f)

        # Print one line for each source state, representing all non-det transitions that start in that state,
        # with format:
        #     source_id, vstar_src, num_ops, num_spps, <a1, sp1>, <a1, sp1>, <a2, sp2>, ...
        for s in state_ids:
            o_edges = []
            num_ops = 0
            for op, sps in transitions.get(s, {}).items():
                o_edges += [(op, sp) for sp in sorted(sps)]
                num_ops += 1
            nondet_successors = ' '.join(f'{o} {sp}' for o, sp in o_edges)
            # Next: A space-separated list of V^*(s) values, one per each state s, where -1 denotes infinity
            vstar = sample.vstar.get(s, -1)
            print(f"{s} {vstar} {num_ops} {len(o_edges)} {nondet_successors}", file=f)
        # Print dversary transitions for each state
        # with format:
        #   s, num_succs, s1, s2, ...
        for s in state_ids:
            succs = adv_transitions.get(s, {})
            adv_successors = ' '.join(f'{sp}' for sp in succs)
            print(f"{s} {len(succs)} {adv_successors}", file=f)


def print_states(sample, states_filename):
    state_ids = sample.get_sorted_state_ids()
    with open(states_filename, 'w') as f:
        for id in state_ids:
            if id in sample.goals:
                print("{}^ {}".format(id, sample.states[id]), file=f)
            elif id in sample.deadends:
                print("{}* {}".format(id, sample.states[id]), file=f)
            else:
                print("{}º {}".format(id, sample.states[id]), file=f)


def run(config, data, rng):
    sample = process_sample(config, data.sample, rng)
    print_transition_matrix(sample, config.transitions_info_filename)
    print_states(sample, config.states_filename)
    return ExitCode.Success, dict(sample = sample)