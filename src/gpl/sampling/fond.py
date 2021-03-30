import itertools
import logging
import math
from collections import defaultdict, OrderedDict, deque

from ..utils import unpack_state

from sltp.returncodes import ExitCode
from sltp.util.command import read_file
from sltp.util.naming import filename_core


class TransitionSampleMDP:
    """ """
    def __init__(self):
        self.states = OrderedDict()
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

    def add_transition(self, state0, state1, operator, instance_name, task):
        # state0_encoded, state0 = state0
        # state1_encoded, state1 = state1

        sids = self.check_states([state0, state1], task)
        oid = self.check_operator(operator)
        self.update_transitions(sids, oid)
        _ = [self.update_instances(i, instance_name) for i in sids]

    def check_states(self, states_pair, task):
        states_pair_ids = [0]*2
        for i, state in enumerate(states_pair):
            states_pair_ids[i] = self.check_state(state, task)
        return states_pair_ids

    def check_state(self, state, task):
        state_id = 0
        s_r, goal, deadend, s_encoded, info = unpack_state(state)
        if s_encoded not in self.states_encoded:
            self.states_encoded[s_encoded] = self.sid_count
            self.states[self.get_state_id(s_encoded)] = task.state_to_atoms(
                state)  # this should be the representation as atoms
            self.sid_count += 1
        id = self.get_state_id(s_encoded)
        state_id = id
        if goal:
            self.goals.add(id)
        elif deadend:
            self.deadends.add(id)
        return state_id

    def get_state_id(self, s_encoded):
        return self.states_encoded[s_encoded]

    def check_operator(self, op):
        if op not in self.operators:
            self.operators[op] = self.oid_count
            self.oid_count += 1
        return self.operators[op]

    def update_transitions(self, states_pair_ids, operator_id):
        # TODO Here is some space for update the montecarlo value or any representative number for the node
        self.transitions[states_pair_ids[0]][operator_id].add(states_pair_ids[1])
        self.parents[states_pair_ids[1]].add(states_pair_ids[0])

    def update_instances(self, sid, instance_name):
        if instance_name not in self.instance_ids:
            self.instance_ids[instance_name] = self.instance_id_count
            self.mark_as_root(sid, self.instance_id_count)
            self.instance_id_count += 1
        self.instance[sid] = self.instance_ids[instance_name] # {state_id: instance_id}

    def num_transitions(self):
        return sum(len(x) for x in self.transitions.values())

    def mark_as_optimal(self, optimal):
        self.optimal_transitions.update(optimal)

    def mark_as_alive(self, states):
        self.alive_states.update(states)

    def mark_as_root(self, sid, instance_id):
        self.roots.add(sid)
        self.instance_roots[instance_id] = sid # {instance_id: root_state_id}

    def mark_as_goals(self, goal):
        self.goals.add(goal)

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

    def filter_successors(self, s, succs, instance_name, task):
        alive, goals, deadends = list(), list(), list()
        for op, sprime in succs:
            s_r, goal, deadend, s_encoded, info = unpack_state(sprime)
            if goal:
                goals.append((op, sprime))
                self.add_transition(s, sprime, op, instance_name, task)
            elif deadend:
                deadends.append((op, sprime))
                self.add_transition(s, sprime, op, instance_name, task)
            else:
                alive.append((op, sprime))
                self.add_transition(s, sprime, op, instance_name, task)
            """
            self.add_transition(s, sprime, op, instance_name, task)
            if goal or deadend:
                pass
            else:   
                alive.append((op, sprime))
            """
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
    transitions = sample.transitions
    num_transitions = sum(len(t) for tx in sample.transitions.values() for t in tx.values())
    # num_transitions = 0
    # for targets in transitions.values():
    #     num_transitions += sum(len(x) for x in targets)
    # optimal_transitions = sample.optimal_transitions
    # num_optimal_transitions = len(optimal_transitions)
    logging.info(f"Printing SAT transition matrix with {len(state_ids)} states,"
                 f" {len(transitions.keys())} states with some outgoing transition"
                 f" and {num_transitions} transitions to '{transitions_filename}'")

    # State Ids should start at 0 and be contiguous
    assert state_ids == list(range(0, len(state_ids)))

    with open(transitions_filename, 'w') as f:
        # first line: <#states> <#transitions> <#marked-transitions>
        # print(f"{num_states} {num_transitions} {num_optimal_transitions}", file=f)
        print(f"{len(state_ids)} {num_transitions}", file=f)

        # second line: all marked transitions, in format: <src0> <dst0> <src1> <dst1> ...
        # print(" ".join(map(str, itertools.chain(*optimal_transitions))), file=f)

        # Print one line for each source state, representing all non-det transitions that start in that state,
        # with format:
        #     source_id, num_successors, <a1, succ11>, <a1, succ12>, <a2, succ21>, ...
        for s in state_ids:
            pairs = []
            for op, succs in transitions.get(s, {}).items():
                pairs += [(op, sprime) for sprime in sorted(succs)]
            nondet_successors = ' '.join(f'{i} {sprime}' for i, sprime in pairs)
            print(f"{s} {len(pairs)} {nondet_successors}", file=f)

        # Next: A space-separated list of V^*(s) values, one per each state s, where -1 denotes infinity
        print(' '.join(str(sample.vstar.get(s, -1)) for s in state_ids), file=f)


def run(config, data, rng):
    sample = process_sample(config, data.sample, rng)
    print_transition_matrix(sample, config.transitions_info_filename)
    return ExitCode.Success, dict(sample = sample)