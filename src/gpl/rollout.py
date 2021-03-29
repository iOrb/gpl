import os
import copy
import logging
import random
from pathlib import Path

from sltp.features import InstanceInformation
from sltp.models import FeatureModel, DLModelFactory
from sltp.returncodes import ExitCode
from sltp.separation import generate_user_provided_policy, TransitionClassificationPolicy
from sltp.tester import PolicySearchException
from sltp.util.misc import compute_universe_from_pddl_model, state_as_atoms, types_as_atoms
from tarski.dl import compute_dl_vocabulary

from .utils import Bunch, unpack_state

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

    for instance_name in config.instances:
        logging.info(f'Appying rollout in train instance "{instance_name}"')

        try:
            """ Run a search on the train instances that follows the given policy or DFS """
            lang, static_predicates = config.domain.generate_language()
            # lang, static_predicates = generate_language(config.domain)
            vocabulary = compute_dl_vocabulary(lang)

            # We interpret as DL nominals all constants that are defined on the entire domain, i.e. instance-independent
            nominals = lang.constants()
            static_predicates |= {s.name for s in lang.sorts}  # Add unary predicates coming from types!

            # instance_name = Path(instance).stem

            # We clone the language so that objects from different instances don't get registered all in the same language;
            # if that happened, we'd be unable to properly compute the universe of each instance.
            pl = copy.deepcopy(lang)
            problem = config.domain.generate_problem(pl, instance_name)

            # Compute the universe of each instance: a set with all objects in the universe
            universe = compute_universe_from_pddl_model(problem.language)

            # Compute the set of all static atoms in the instance, including those stemming from types
            static_atoms = {atom for atom in state_as_atoms(problem.init) if atom[0] in static_predicates} |\
                           {atom for atom in types_as_atoms(problem.language)}

            info = InstanceInformation(universe, static_atoms, static_predicates, {}, {})

            # Parse the domain & instance and create a model generator
            model_factory = DLModelFactory(vocabulary, nominals, info)

            # Compute an actual policy object that returns the next action to be applied
            search_policy = get_policy(model_factory, static_atoms, data)

            # define the Task
            task = config.domain.generate_task(instance_filename=instance_name)

            # And now we inject our desired search and heuristic functions
            run_rollout(config, search_policy, task, instance_name, rng)

        except PolicySearchException as e:
            logging.warning(f"Rollout of policy failed with code: {e.code}")
            return e.code
    return ExitCode.Success


def run_rollout(config, search_policy, task, instance_name, rng):

    for _ in range(config.num_rollouts):
        state = task.initial_state

        for _ in range(config.rollout_depth):

            succcessors = task.get_successor_states(state)

            if not succcessors:
                config.sample.mark_state_as_deadend(state, task)
                state = task.initial_state
                # raise RuntimeError("No successor")
                continue

            alive, _, _ = config.sample.filter_successors(state, succcessors, instance_name, task)

            rnd_op, rnd_succ = random.Random(rng).choice(alive)
            # rnd_succ, rnd_op = alive[0]

            if search_policy is not None:
                exitcode, good_succs = run_policy_based_search(config, search_policy, task, state, alive)
                if exitcode != 0:
                    op, succ = rnd_op, rnd_succ
                    # succ, op = run_dfs(config, task, state, rng)
                else:
                    op, succ = random.Random(rng).choice(good_succs)
            else:
                op, succ = rnd_op, rnd_succ
                # succ, op = run_dfs(config, task, state, rng)

            # config.visited.add(succ[2])
            config.sample.add_transition(state, succ, op, instance_name, task)
            state = succ


def run_dfs(config, task, state):
    state, action = task.dfs_transition(state, rng, config.visited)
    return state, action


def run_policy_based_search(config, search_policy, task, state, successors):
    # # Compute all possible successors:
    # successors = task.get_successor_states(state)

    # Show the successors to our D2L-type policy to let it pick one
    exitcode, good_succs = search_policy(task, state, successors)

    return exitcode, good_succs


def translate_state(task, state, static_atoms):
    """ Translate a pyperplan-like state into a list with the format required by SLTP's concept denotation processor """
    translated_state = task.state_to_atoms(state) + list(static_atoms)
    return translated_state


def generate_model_from_state(task, model_factory, state, static_atoms):
    translated = translate_state(task, state, static_atoms)
    return FeatureModel(model_factory.create_model(translated))


def create_action_selection_function_from_transition_policy(config, model_factory, static_atoms, policy):
    assert isinstance(policy, TransitionClassificationPolicy)

    def _policy(task, state, successors):
        m0 = generate_model_from_state(task, model_factory, state, static_atoms)

        good_succs = list()

        for op, succ in successors:
            m1 = generate_model_from_state(task, model_factory, succ, static_atoms)
            if policy.transition_is_good(m0, m1):
                # return ExitCode.Success, op, succ
                good_succs.append((op, succ))
        if not good_succs:
            return ExitCode.AbstractPolicyNotCompleteOnTestInstances, None
        else:
            return ExitCode.Success, good_succs

    return _policy


def run(config, data, rng):
    if not config.instances:
        logging.info("No train instances were specified")
        return ExitCode.Success, dict()

    def get_policy(model_factory, static_atoms, data):

        data = data.to_dict()
        if config.d2l_policy is not None:
            policy = generate_user_provided_policy(config)
            config.d2l_policy = None
            policy = create_action_selection_function_from_transition_policy(config, model_factory, static_atoms, policy)
        elif "d2l_policy" not in data:
            policy = None
        else:
            policy = create_action_selection_function_from_transition_policy(config, model_factory, static_atoms, data["d2l_policy"])
        data = Bunch(data)

        return policy

    # Test that the policy reaches a goal when applied on all test instances
    res = rollout(config, data, get_policy, rng)
    return res, dict()
