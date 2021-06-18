import os
import copy
import logging
from pathlib import Path

from sltp.features import InstanceInformation
from sltp.models import FeatureModel, DLModelFactory
from sltp.returncodes import ExitCode
from sltp.separation import generate_user_provided_policy, TransitionClassificationPolicy
from sltp.tester import PolicySearchException
from sltp.util.misc import compute_universe_from_pddl_model, state_as_atoms, types_as_atoms
from tarski.dl import compute_dl_vocabulary

from .utils import Bunch

"""
rollout:
    process:
        for _ in n-rollouts:
            for _ in rollout-depth:
                if d2l-policy exists:
                    if d2l-policy applies:
                        select action from d2l-policy
                else:
                    select action from DFS
    
    params:
        n-rollouts
        rollout-depth
"""

def rollout(config, data, get_policy, rng):

    for i, task in enumerate(data.tasks):
        try:
            """ Run a search on the train instances that follows the given policy or DFS """
            lang, static_predicates = config.domain.generate_language()
            vocabulary = compute_dl_vocabulary(lang)

            # Get the instance name
            instance_name = task.get_instance_name()

            # We interpret as DL nominals all constants that are defined on the entire domain, i.e. instance-independent
            nominals = lang.constants()
            static_predicates |= {s.name for s in lang.sorts}  # Add unary predicates coming from types!

            # We clone the language so that objects from different instances don't get registered all in the same language;
            # if that happened, we'd be unable to properly compute the universe of each instance.
            pl = copy.deepcopy(lang)
            problem = config.domain.generate_problem(pl, instance_name)

            # Compute the universe of each instance: a set with all objects in the universe
            universe = compute_universe_from_pddl_model(problem.language)

            # Compute the set of all sstatic atoms in the instance, including those stemming from types
            static_atoms = {atom for atom in state_as_atoms(problem.init) if atom[0] in static_predicates} | \
                           {atom for atom in types_as_atoms(problem.language)}

            info = InstanceInformation(universe, static_atoms, static_predicates, {}, {})

            # Parse the domain & instance and create a model generator
            model_factory = DLModelFactory(vocabulary, nominals, info)

            # Compute an actual policy object that returns the next action to be applied
            search_policy = get_policy(model_factory, static_atoms, data)

            # And now we inject our desired search and heuristic functions
            if i in config.train_instances_to_expand:
                bfs(config, data, search_policy, task, instance_name, rng)
            else:
                # pass
                run_rollout(config, data, search_policy, task, instance_name, rng)

        except PolicySearchException as e:
            logging.warning(f"Rollout of policy failed with code: {e.code}")
            return e.code

    return ExitCode.Success


def run_rollout(config, data, search_policy, task, instance_name, rng):

    logging.info(f'Appying rollout in train instance "{instance_name}"')

    root_state = task.initial_state

    for _ in range(config.num_rollouts):

        end_node_reached = False
        rollout_depth = 0
        state = copy.deepcopy(root_state)
        succcessors = task.get_successor_states(state)
        alive, _, _ = data.sample.process_successors(state, succcessors, task)
        if not alive:
            break

        while rollout_depth < config.rollout_depth and not end_node_reached:
            rollout_depth += 1
            succcessors = task.get_successor_states(state)

            alive, _, _ = data.sample.process_successors(state, succcessors, task)

            if not alive:
                end_node_reached = True;
                continue
                # raise RuntimeError("No successors for expanded state: \n{}".format(state[1],))
            else:
                rnd_op, rnd_sp = alive[0]

                if search_policy is not None:
                    exitcode, good_succs = run_policy_based_search(config, search_policy, task, state, alive)
                    if exitcode != ExitCode.Success:
                        op, sp = rnd_op, rnd_sp
                    else:
                        op, sp = good_succs[0]
                else:
                    op, sp = rnd_op, rnd_sp

            state = sp


def run_policy_based_search(config, search_policy, task, state, successors):

    # Show the successors to our D2L-type policy to let it pick one
    exitcode, good_succs = search_policy(task, state, successors)

    return exitcode, good_succs


def bfs(config, data, search_policy, task, instance_name, rng):

    logging.info(f'Expanding train instance: {task.get_domain_name()} - {instance_name}')

    if config.verbosity > 0:
        print(task.get_printable_rep(task.initial_state[0]))

    visited = set()
    istate = task.initial_state
    queue = [istate]

    while queue:
        s = queue.pop(0)
        sr, s_encoded = s
        succcessors = task.get_successor_states(s)
        alive, _, _ = data.sample.process_successors(s, succcessors, task)
        for op, sp, spp in alive:
            if spp[1] not in visited:
                visited.add(spp[1])
                queue.append(spp)
        if data.sample.num_states() > config.max_states_expanded:
            break


def translate_state(task, state, static_atoms):
    """ Translate a pyperplan-like state into a list with the format required by SLTP's concept denotation processor """
    translated_state = task.state_to_atoms(state) + list(static_atoms)
    return translated_stateidentify_margin


def generate_model_from_state(task, model_factory, state, static_atoms):
    translated = translate_state(task, state, static_atoms)
    return FeatureModel(model_factory.create_model(translated))


def create_action_selection_function_from_transition_policy(config, model_factory, static_atoms, policy):
    # assert isinstance(policy, TransitionClassificationPolicy)

    def _policy(task, state, successors):
        m0 = generate_model_from_state(task, model_factory, state, static_atoms)

        good_succs = list()

        for op, sp in successors:
            m1 = generate_model_from_state(task, model_factory, sp, static_atoms)
            if policy.transition_is_good(m0, m1):
                # return ExitCode.Success, op, sp
                good_succs.append((op, sp))
        if not good_succs:
            return ExitCode.AbstractPolicyNotCompleteOnTestInstances, None
        else:
            return ExitCode.Success, good_succs

    return _policy


def run(config, data, rng):
    def get_policy(model_factory, static_atoms, data):
        if data.d2l_policy is not None:
            policy = create_action_selection_function_from_transition_policy(config, model_factory, static_atoms, data.d2l_policy)
        else:
            policy = None
        return policy

    # Test that the policy reaches a goal when applied on all test instances
    res = rollout(config, data, get_policy, rng)
    return res, dict()
