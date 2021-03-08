#!/usr/bin/env python3
import sys
from collections import deque
import time

from lgp.domains import get_domain_data
from tqdm import tqdm
from lgp.grammar.grammar import Grammar
from lgp.utils import unserialize_layout, create_gym_env, get_operators, infer_info_from_state
from lgp.teach_policies import compute_actions_from_policies


"""
Possible domain names:
'stop_the_fall'
'chase'
'reach_for_the_star'
'two_pile_nim'
'checkmate_tactic'
"""


def expand_state_space(domain_name, instance_filename, policies, output):

    domain = get_domain_data(domain_name)
    initial_state = unserialize_layout(instance_filename)
    grammar = Grammar(domain, initial_state)
    env = create_gym_env(domain.base_class, initial_state)
    all_possible_actions = get_operators(initial_state)

    visited = dict()  # {state_encoded: id}

    queue = deque()
    queue_not_recommended = deque()

    f = open(output, "w")
    pbar = tqdm()
    start = time.time()
    id, num_explored, num_transitions, num_goals = [0]*4

    initial_state_encoded = grammar.encode_state(initial_state, {'reward': False,
                                                                 'is_goal': False,
                                                                 'is_dead_end': False})
    visited[initial_state_encoded] = id

    # Assume that initial state is not a goal nor dead_end
    queue.append((initial_state, initial_state_encoded, 0, 0))
    atoms = grammar.state_to_atoms_string(initial_state, {'reward': False,
                                                          'is_goal': False,
                                                          'is_dead_end': False})
    f.write(f'(N) {id} 0 0 {atoms}\n')

    while queue:
        expanded, exp_encoded, is_goal, is_dead_end = queue.popleft()
        id_expanded = visited[exp_encoded]

        if is_goal or is_dead_end:
            num_goals += 1
            # We do not expand the goal or dead_end states
            continue

        adjacent = dict()

        if policies:
            recommended_actions = compute_actions_from_policies(policies, state=expanded)
            not_recommended_actions = all_possible_actions.difference(recommended_actions)
            queue_not_recommended.append((expanded, exp_encoded, is_goal, is_dead_end, not_recommended_actions))
        else:
            recommended_actions = all_possible_actions

        for action in recommended_actions:
            generateds = env.possible_transitions(expanded, action)

            for generated in generateds:
                is_goal, is_dead_end, reward = infer_info_from_state(env, expanded, action, generated)
                info = {'reward': reward,
                        'is_goal': is_goal,
                        'is_dead_end': is_dead_end,
                        'prev_layout': expanded,
                        'clicked': action}
                gen_encoded = grammar.encode_state(generated, info)

                if gen_encoded == exp_encoded:
                    # At the moment we ignore self-loop transitions, i.e. proceed as if the action was not applicable
                    continue

                if action not in adjacent:
                    adjacent[action] = set()

                if gen_encoded not in visited:  # The state is a new state
                    id += 1
                    visited[gen_encoded] = id
                    queue.append((generated, gen_encoded, is_goal, is_dead_end))
                    atoms = grammar.state_to_atoms_string(generated, info)
                    f.write(f'(N) {str(id)} {str(is_goal)} {str(is_dead_end)} {atoms}\n')
                    adjacent[action].add(str(id),)
                    # adjacent.add(id)

                else:  # The state has already been visited, but we still want to record the incoming edge
                    adjacent[action].add(str(visited[gen_encoded]),)

        for _, oids in adjacent.items():
            f.write(f'(E) {id_expanded} {" ".join(sorted(oids))}\n')
        num_transitions += len(adjacent)

        num_explored += 1
        pbar.update(1)

    while queue_not_recommended:
        expanded, exp_encoded, is_goal, is_dead_end, not_recommended_actions = queue_not_recommended.popleft()
        id_expanded = visited[exp_encoded]

        if is_goal or is_dead_end:
            num_goals += 1
            # We do not expand the goal or dead_end states
            continue

        adjacent = dict()

        for action in not_recommended_actions:
            generateds = env.possible_transitions(expanded, action)

            for generated in generateds:
                is_goal, is_dead_end, reward = infer_info_from_state(env, expanded, action, generated)
                info = {'reward': reward,
                        'is_goal':is_goal,
                        'is_dead_end':is_dead_end,
                        'prev_layout': expanded,
                        'clicked': action}
                gen_encoded = grammar.encode_state(generated, info)

                if gen_encoded == exp_encoded:
                    # At the moment we ignore self-loop transitions, i.e. proceed as if the action was not applicable
                    continue

                if action not in adjacent:
                    adjacent[action] = set()

                if gen_encoded not in visited:  # The state is a new state
                    id += 1
                    visited[gen_encoded] = id
                    atoms = grammar.state_to_atoms_string(generated, info)
                    f.write(f'(N) {str(id)} {str(is_goal)} {str(is_dead_end)} {atoms}\n')
                    adjacent[action].add(str(id),)

                else:  # The state has already been visited, but we still want to record the incoming edge
                    adjacent[action].add(str(visited[gen_encoded]),)

        for _, oids in adjacent.items():
            f.write(f'(E) {id_expanded} {" ".join(sorted(oids))}\n')
        num_transitions += len(adjacent)
        num_explored += 1
        pbar.update(1)

    total_time = time.time() - start
    pbar.close()
    print(f'State space of instance "{instance_filename}" stored in "{f.name}"')
    print(f"[# nodes: {id+1}, # goals: {num_goals}, # edges: {num_transitions}, total time: {round(total_time, 5)} seconds]")
    f.close()


if __name__ == "__main__":
    expand_state_space(domain_name=sys.argv[1],
                       instance_filename=sys.argv[2],
                       policies=None,
                       output=sys.argv[3])
