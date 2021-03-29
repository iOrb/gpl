from collections import deque
import time

from tqdm import tqdm
from .teach_policies import compute_actions_from_policies
from gpl.utils import unpack_state

"""
Possible domain names:
'stop_the_fall'
'chase'
'reach_for_the_star'
'two_pile_nim'
'checkmate_tactic'
"""

def expand_state_space(task, teach_policies, output):

    initial_state = task.initial_state
    env = task.env
    grammar = task.grammar
    all_possible_actions = task.actions

    visited = dict()  # {state_encoded: id}

    queue = deque()
    queue_not_recommended = deque()

    f = open(output, "w")
    pbar = tqdm()
    start = time.time()
    id, num_explored, num_transitions, num_goals = [0]*4

    visited[initial_state[2]] = id

    # Assume that initial state is not a goal nor dead_end
    queue.append((initial_state))
    atoms = grammar.state_to_atoms_string(initial_state,)
    f.write(f'(N) {id} 0 0 {atoms}\n')

    while queue:
        expanded = queue.popleft()
        exp_rep, goal, deadend, exp_encode, info = unpack_state(expanded)
        id_expanded = visited[exp_encode]

        if goal or deadend:
            num_goals += 1
            # We do not expand the goal or dead_end states
            continue

        adjacent = dict()

        if teach_policies:
            recommended_actions = compute_actions_from_policies(teach_policies, state=exp_rep)
            not_recommended_actions = all_possible_actions.difference(recommended_actions)
            queue_not_recommended.append((exp_rep, goal, deadend, exp_encode, not_recommended_actions))
        else:
            recommended_actions = all_possible_actions

        for action in recommended_actions:
            generated = task.transition(expanded, action)
            gen_rep, goal, deadend, gen_encode, info = unpack_state(generated)

            if gen_encode == exp_encode:
                # At the moment we ignore self-loop transitions, i.e. proceed as if the action was not applicable
                continue

            if action not in adjacent:
                adjacent[action] = set()

            if gen_encode not in visited:  # The state is a new state
                id += 1
                visited[gen_encode] = id
                queue.append(generated)
                atoms = grammar.state_to_atoms_string(generated,)
                f.write(f'(N) {str(id)} {str(goal)} {str(deadend)} {atoms}\n')
                adjacent[action].add(str(id),)
                # adjacent.add(id)

            else:  # The state has already been visited, but we still want to record the incoming edge
                adjacent[action].add(str(visited[gen_encode]),)

        for _, oids in adjacent.items():
            f.write(f'(E) {id_expanded} {" ".join(sorted(oids))}\n')
        num_transitions += len(adjacent)

        num_explored += 1
        pbar.update(1)

    while queue_not_recommended:
        exp_rep, goal, deadend, exp_encode, not_recommended_actions = queue_not_recommended.popleft()
        id_expanded = visited[exp_encode]

        if goal or deadend:
            num_goals += 1
            # We do not expand the goal or dead_end states
            continue

        adjacent = dict()

        for action in not_recommended_actions:
            generated = env.transition(expanded, action)
            gen_rep, goal, deadend, gen_encode, info = unpack_state(generated)

            if gen_encode == exp_encode:
                # At the moment we ignore self-loop transitions, i.e. proceed as if the action was not applicable
                continue

            if action not in adjacent:
                adjacent[action] = set()

            if gen_encode not in visited:  # The state is a new state
                id += 1
                visited[gen_encode] = id
                atoms = grammar.state_to_atoms_string(generated)
                f.write(f'(N) {str(id)} {str(goal)} {str(deadend)} {atoms}\n')
                adjacent[action].add(str(id),)

            else:  # The state has already been visited, but we still want to record the incoming edge
                adjacent[action].add(str(visited[gen_encode]),)

        for _, oids in adjacent.items():
            f.write(f'(E) {id_expanded} {" ".join(sorted(oids))}\n')
        num_transitions += len(adjacent)
        num_explored += 1
        pbar.update(1)

    total_time = time.time() - start
    pbar.close()
    print(f'State space of instance "{task.get_instance_filename()}" stored in "{f.name}"')
    print(
        f"[# nodes: {id + 1}, # goals: {num_goals}, # edges: {num_transitions}, total time: {round(total_time, 5)} seconds]")
    f.close()

