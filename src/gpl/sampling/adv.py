import copy
import itertools
import logging
import math
from collections import defaultdict, OrderedDict, deque

from ..utils import unpack_state, encode_operator

from sltp.returncodes import ExitCode
from sltp.util.command import read_file
from sltp.util.naming import filename_core


class TransitionSampleADV:
    """ """
    def __init__(self):
        self.states = OrderedDict()
        self.states_s_spp = set()
        self.states_encoded = dict()
        self.operators = dict()
        self.transitions = defaultdict(lambda: defaultdict(set))
        self.parents = defaultdict(set)
        self.goals = set()
        self.alive_states = set()
        self.optimal_transitions = set()
        self.roots = set()  # The set of all roots
        self.instance_roots = dict()  # The root of each instance
        self.deadends = set()
        self.instance = dict()  # A mapping between states and the problem instances they came from
        self.instance_ids = dict()
        self.remapping = dict()
        self.vstar = {}
        self.sid_count = 0
        self.oid_count = 0
        self.instance_id_count = 0

    def add_transition(self, tx, task):
        s, op0, sp, _, spp = tx # for now ignore op1
        assert None not in [s, op0, sp]
        new_instance_, instance_id = self.check_instance_name(task.get_instance_name())
        spp = spp if spp is not None else copy.deepcopy(sp) # if sp is goal or deadend just extende it to spp
        sids = [self.check_state(s, task, instance_id) for s in [s, sp, spp]]
        self.states_s_spp |= {sids[0], sids[2]}
        oid = self.check_operator(op0, task, instance_id)
        self.update_transitions(self.get_tx(sids, oid))
        if new_instance_:
            self.mark_as_root(sids[0], instance_id)
        _ = [self.update_instance(sid, instance_id) for sid in sids]

    def update_transitions(self, tx):
        """ main method """
        s, op0, sp, spp = tx # IDs
        # s {(op0, s'): {s'', ...}}
        self.transitions[s][(op0, sp)].add(spp)
        # for simplicity we just take into account the adversary transitions as FOND
        self.parents[spp].add(s)

    def get_tx(self, sids, oid):
        return (sids[0], oid, sids[1], sids[2])

    def check_state(self, state, task, instance_id):
        s_r, goal, deadend, s_enc_raw, info = unpack_state(state)
        s_encoded = self.encode_state(instance_id, s_enc_raw)
        if s_encoded not in self.states_encoded:
            self.states_encoded[s_encoded] = self.sid_count
            self.states[self.get_state_id(s_encoded)] = task.state_to_atoms(
                state)  # this should be the representation as atoms
            self.sid_count += 1
        id = self.get_state_id(s_encoded)
        if goal:
            self.goals.add(id)
        elif deadend:
            self.deadends.add(id)
        return id

    def get_state_id(self, s_encoded):
        return self.states_encoded[s_encoded]

    def get_instance_id(self, instance_name):
        return self.instance_ids[instance_name]

    def check_operator(self, op, task, intance_id):
        o_raw = encode_operator(op, task)
        o = self.encode_operator(intance_id, o_raw)
        if o not in self.operators:
            self.operators[o] = self.oid_count
            self.oid_count += 1
        return self.operators[o]

    def update_instance(self, sid, intance_id):
        self.instance[sid] = intance_id # {state_id: instance_id}

    def check_instance_name(self, instance_name):
        if instance_name not in self.instance_ids:
            self.instance_ids[instance_name] = self.instance_id_count
            self.instance_id_count += 1
            return True, self.get_instance_id(instance_name) # the intance is new
        return False, self.get_instance_id(instance_name)

    def encode_state(self, instance_id, s_enc_raw):
        return '_'.join([str(instance_id), str(s_enc_raw)])

    def encode_operator(self, instance_id, op_enc_raw):
        return '_'.join([str(instance_id), str(op_enc_raw)])

    def num_transitions(self):
        return sum(len(x) for x in self.transitions.values())

    def mark_as_optimal(self, optimal):
        self.optimal_transitions.update(optimal)

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
               f"transitions: {self.num_transitions()} ({len(self.optimal_transitions)} optimal)," \
               f" goals: {len(self.goals)}, alive: {len(self.alive_states)}"

    def __str__(self):
        return "TransitionsSample[{}]".format(self.info())

    def get_sorted_state_ids(self):
        return sorted(self.states.keys())

    def get_sorted_state_s_spp_ids(self):
        return sorted(self.states_s_spp)

    def process_successors(self, s, succs, task):
        alive, goals, deadends = list(), list(), list()
        for op0, sp, spps in succs:
            s_r, goal, deadend, s_encoded, info = unpack_state(sp)
            if goal:
                assert not spps, "One state with successor is marked as Goal"
                goals.append((op0, sp))
                self.add_transition((s, op0, sp, None, None), task)
            elif deadend:
                assert not spps, "One state with successor is marked as Dead"
                deadends.append((op0, sp))
                self.add_transition((s, op0, sp, None, None), task)
            else:
                assert spps, "One state with not any successor is marked as Alive"
                alive.append((op0, sp, spps))
                for op1, spp in spps:
                    self.add_transition((s, op0, sp, op1, spp), task)
        return alive, goals, deadends


def process_sample(config, sample, rng):

    # if not config.create_goal_features_automatically and not config.sample.goals:
    #     raise logging.warning("No goal found in the sample - increase number of expanded states!")

    # # Make sure all edge IDs have actually been declared as a state
    # for src in config.sample.transitions:
    #     assert src in state_atoms and all(dst in state_atoms for dsts in transitions[src] for dst in dsts)

    num_tx_entries = sum(len(tx) for tx in sample.transitions.values())
    num_tx = sum(len(t) for tx in sample.transitions.values() for t in tx.values())
    logging.info('%s: #states=%d, #transition-entries=%d, #transitions=%d' %
                 ('sample', len(sample.states), num_tx_entries, num_tx))

    mark_optimal_transitions(config, sample) # check if this sample is being updated
    logging.info(f"Entire sample: {sample.info()}")

    # if config.num_sampled_states is not None:
    #     # Resample the full sample and extract only a few specified states
    #     selected = sample_first_x_states(sample.instance_roots, config.num_sampled_states)
    #     states_in_some_optimal_transition = sample.compute_optimal_states(include_goals=True)
    #     selected.update(states_in_some_optimal_transition)
    #     sample = sample.resample(set(selected))
    #     logging.info(f"Sample after resampling: {sample.info()}")
    return sample

def mark_optimal_transitions(config, sample):
    """ Marks which transitions are optimal in a transition system according to some selection criterion
    such as marking *all* optimal transitions.
     """
    # Mark all transitions that are optimal from some alive state
    # We also mark which states are alive.
    optimal, alive, sample.vstar = mark_all_optimal(sample.goals, sample.parents)
    sample.mark_as_alive(alive)
    sample.mark_as_optimal(optimal)


def mark_all_optimal(goals, parents):
    """ Collect all transitions that lie on at least one optimal plan starting from some alive state (i.e. solvable,
     reachable, and not a goal). """
    vstar, minactions = {}, {}
    for g in goals:
        run_backwards_brfs(g, parents, vstar, minactions)

    # minactions contains a map between state IDs and a list with those successors that represent an optimal transition
    # from that state
    optimal_txs = set()
    for s, targets in minactions.items():
        _ = [optimal_txs.add((s, t)) for t in targets]

    # Incidentally, the set of alive states will contain all states with a mincost > 0 and which have been reached on
    # the backwards brfs (i.e. for which mincost[s] is actually defined). Note that the "reachable" part of a state
    # being alive is already guaranteed by the fact that the state is on the sample, as we sample states with a simple
    # breadth first search.
    alive = {s for s, cost in vstar.items() if cost > 0}

    return optimal_txs, alive, vstar


def run_backwards_brfs(g, parents, mincosts, minactions):
    queue = deque([g])
    mincosts[g] = 0
    minactions[g] = []

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
    state_s_spp = sample.get_sorted_state_s_spp_ids()
    transitions = sample.transitions
    num_agent_transitions = sum(len(tx) for tx in transitions.values())
    num_nondet_transitions = sum(len(t) for tx in transitions.values() for t in tx.values())
    num_s_with_outgoind_edge = len(transitions.keys()) - len(sample.goals) - len(sample.deadends)
    logging.info(f"Printing SAT transition matrix with {len(state_ids)} states,"
                 f" {num_s_with_outgoind_edge} states with some outgoing transition,"
                 f" {num_nondet_transitions} (non-det) transitions,"
                 f" and {num_agent_transitions} (agent) transitions to '{transitions_filename}'")

    # State Ids should start at 0 and be contiguous
    # assert state_ids == list(range(0, len(state_ids)))

    with open(transitions_filename, 'w') as f:
        # first line: <#states> <#states_s_spp> <#transitions(non-det)> <#marked-transitions(agent)>
        print(f"{len(state_ids)} {len(state_s_spp)} {num_nondet_transitions} {num_agent_transitions}", file=f)

        # Print one line for each source state, representing all non-det transitions that start in that state,
        # with format:
        #     source_id, vstar_src, num_sps, num_spps, <a1, sp1 spp11>, <a1, sp1, spp>, <a2, sp2, spp21>, ...
        for s in state_s_spp:
            o_edges = []
            num_ops = 0
            for (op, sp), spps in transitions.get(s, {}).items():
                o_edges += [(op, sp, spp) for spp in sorted(spps)]
                num_ops += 1
            nondet_successors = ' '.join(f'{o} {sp} {spp}' for o, sp, spp in o_edges)
            # Next: A space-separated list of V^*(s) values, one per each state s, where -1 denotes infinity
            vstar = sample.vstar.get(s, -1)
            print(f"{s} {vstar} {num_ops} {len(o_edges)} {nondet_successors}", file=f)


def run(config, data, rng):
    sample = process_sample(config, data.sample, rng)
    print_transition_matrix(sample, config.transitions_info_filename)
    return ExitCode.Success, dict(sample = sample)