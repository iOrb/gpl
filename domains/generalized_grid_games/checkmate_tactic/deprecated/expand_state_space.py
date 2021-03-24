
from collections import deque
import time

from tqdm import tqdm
from .grammar.grammar import Grammar
from ..utils import unserialize_layout, create_gym_env, get_operators, infer_info_from_state
from .teach_policies import compute_actions_from_policies

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

    initial_state_encoded = grammar.encode_state(initial_state, {'reward': False, 'is_goal': False,
                                                                 'is_dead_end': False})
    visited[initial_state_encoded] = id

    # Assume that initial state is not a goal nor dead_end
    queue.append((initial_state, initial_state_encoded, 0, 0))
    atoms = grammar.state_to_atoms_string(initial_state, {'reward': False, 'is_goal': False,
                                                          'is_dead_end': False})
    f.write(f'(N) {id} 0 0 {atoms}\n')

    while queue:
        expanded, exp_encoded, is_goal, is_dead_end = queue.popleft()
        id_expanded = visited[exp_encoded]

        if is_goal or is_dead_end:
            num_goals += 1
            # We do not expand the goal or dead_end states
            continue

        adjacent = set()

        if teach_policies:
            recommended_actions = compute_actions_from_policies(teach_policies, state=expanded)
            not_recommended_actions = all_possible_actions.difference(recommended_actions)
            queue_not_recommended.append((expanded, exp_encoded, is_goal, is_dead_end, not_recommended_actions))
        else:
            recommended_actions = all_possible_actions

        for action in recommended_actions:
            generated = env.transition(expanded, action)
            is_goal, is_dead_end, reward = infer_info_from_state(env, expanded, action, generated)
            gen_encoded = grammar.encode_state(generated, {'reward': reward, 'is_goal': is_goal,
                                                           'is_dead_end': is_dead_end, 'prev_layout': expanded,
                                                           'clicked': action})

            if gen_encoded == exp_encoded:
                # At the moment we ignore self-loop transitions, i.e. proceed as if the action was not applicable
                continue

            if gen_encoded not in visited:  # The state is a new state
                id += 1
                visited[gen_encoded] = id
                queue.append((generated, gen_encoded, is_goal, is_dead_end))
                atoms = grammar.state_to_atoms_string(generated, {'reward': reward, 'is_goal': is_goal,
                                                                  'is_dead_end': is_dead_end, 'prev_layout': expanded,
                                                                  'clicked': action})
                f.write(f'(N) {str(id)} {str(is_goal)} {str(is_dead_end)} {atoms}\n')
                adjacent.add(id)

            else:  # The state has already been visited, but we still want to record the incoming edge
                adjacent.add(visited[gen_encoded])

        for oid in adjacent:
            f.write(f'(E) {id_expanded} {oid}\n')
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

        adjacent = set()

        for action in not_recommended_actions:
            generated = env.transition(expanded, action)
            is_goal, is_dead_end, reward = infer_info_from_state(env, expanded, action, generated)
            gen_encoded = grammar.encode_state(generated, {'reward': reward, 'is_goal':is_goal,
                                                           'is_dead_end':is_dead_end, 'prev_layout': expanded,
                                                           'clicked': action})

            if gen_encoded == exp_encoded:
                # At the moment we ignore self-loop transitions, i.e. proceed as if the action was not applicable
                continue

            if gen_encoded not in visited:  # The state is a new state
                id += 1
                visited[gen_encoded] = id
                atoms = grammar.state_to_atoms_string(generated, {'reward': reward, 'is_goal':is_goal,
                                                                  'is_dead_end':is_dead_end, 'prev_layout': expanded,
                                                                  'clicked': action})
                f.write(f"(N) {str(id)} {str(is_goal)} {str(is_dead_end)} {atoms}\n")
                adjacent.add(id)

            else:  # The state has already been visited, but we still want to record the incoming edge
                adjacent.add(visited[gen_encoded])

        for oid in adjacent:
            f.write(f'(E) {id_expanded} {oid}\n')
        num_transitions += len(adjacent)

        num_explored += 1
        pbar.update(1)

    total_time = time.time() - start
    pbar.close()
    print(f'State space of instance "{task.get_instance_filename()}" stored in "{f.name}"')
    print(f"[# nodes: {id+1}, # goals: {num_goals}, # edges: {num_transitions}, total time: {round(total_time, 5)} seconds]")
    f.close()

