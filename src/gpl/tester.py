import os
import copy
import logging
import random
from pathlib import Path

from sltp.features import InstanceInformation
from sltp.models import FeatureModel, DLModelFactory
from sltp.returncodes import ExitCode
from sltp.separation import generate_user_provided_policy, TransitionClassificationPolicy, StateActionClassificationPolicy
from sltp.tester import PolicySearchException
from sltp.util.misc import compute_universe_from_pddl_model, state_as_atoms, types_as_atoms
from tarski.dl import compute_dl_vocabulary

from .utils import Bunch, encode_operator

from collections import defaultdict

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


def test_d2l_policy_on_gym_env(config, data, get_policy, rng):

    solved_instances, unsolved_instances = list(), list()

    for instance_name in config.test_instances:
        logging.info(f'Appying rollout in train instance "{instance_name}"')

        try:
            """ Run a search on the test instances that follows the given policy or DFS """
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
            static_atoms = {atom for atom in state_as_atoms(problem.init) if atom[0] in static_predicates} | \
                           {atom for atom in types_as_atoms(problem.language)}

            info = InstanceInformation(universe, static_atoms, static_predicates, {}, {})

            # Parse the domain & instance and create a model generator
            model_factory = DLModelFactory(vocabulary, nominals, info)

            # Compute an actual policy object that returns the next action to be applied
            search_policy = get_policy(model_factory, static_atoms, data)

            # define the Task
            task = config.domain.generate_task(instance_name)

            # And now we inject our desired search and heuristic functions
            run_test(config, search_policy, task, instance_name, rng)

            # Add instance to solved instances
            solved_instances.append(instance_name)

        except PolicySearchException as e:
            logging.warning(f"Testing of policy failed with code: {e.code}")
            unsolved_instances.append(instance_name)
            continue
            # return e.code
    logging.info("Learnt policy solves the {}% of test instances: {}/{}"
                 .format(round(len(solved_instances) / len(config.test_instances) * 100, 2),
                         len(solved_instances), len(config.test_instances)))
    logging.info("Solved instances: {}".format(solved_instances))
    logging.info("Unsolved instances: {}".format(unsolved_instances))
    return ExitCode.Success


def run_test(config, search_policy, task, instance_name, rng):

    s = task.initial_state
    expanded = 0

    sa_pairs = defaultdict(lambda: 0) # We'll use this at the same time as closed list and to keep track of parents
    solution = list()

    while not s[1]['goal']:
        expanded += 1
        if expanded % 1000 == 0:
            logging.debug(f"Number of expanded states so far in policy-based search: {expanded}")

        successors = task.get_successor_states(s)

        if not successors:
            raise PolicySearchException(ExitCode.NotSuccessorsFound)

        exitcode, good_succs = run_policy_based_search(config, search_policy, task, s, successors)
        if exitcode == ExitCode.AbstractPolicyNotCompleteOnTestInstances:
            raise PolicySearchException(ExitCode.AbstractPolicyNotCompleteOnTestInstances)

        for op, _ in good_succs:
            sa_pair_enc = task.encode_sa_pair((s, op))
            if sa_pair_enc in sa_pairs:
                continue
            else:
                break

        sa_pair_enc = task.encode_sa_pair((s, op))
        sp = task.transition(s, op)

        r=s[0][0]
        rp=sp[0][0]

        if sp[1]['deadend']:
            raise PolicySearchException(ExitCode.DeadEndReached)
        if sa_pairs[sa_pair_enc] > 10:
            raise PolicySearchException(ExitCode.AbstractPolicyNonTerminatingOnTestInstances)

        solution.append(encode_operator(s, op, task))
        sa_pairs[sa_pair_enc] += 1
        s = sp

    logging.info(f"Goal found after expanding {expanded} nodes")
    logging.info(f"The solution was: {solution}")
    return solution


def create_action_selection_function_from_transition_policy(config, model_factory, static_atoms, policy):
    # assert isinstance(policy, StateActionClassificationPolicy)
    assert isinstance(policy, TransitionClassificationPolicy)

    def _policy(task, state, successors):
        m0 = generate_model_from_state(task, model_factory, state, static_atoms)
        good_succs = list()
        for op, sp in successors:
            m1 = generate_model_from_state(task, model_factory, sp, static_atoms)
            # if policy.transition_is_good(m0, op):
            if policy.transition_is_good(m0, m1):
                # return ExitCode.Success, op, sp
                good_succs.append((op, sp))
        if not good_succs:
            return ExitCode.AbstractPolicyNotCompleteOnTestInstances, None
        else:
            return ExitCode.Success, good_succs

    return _policy


def run_policy_based_search(config, search_policy, task, state, successors):
    # Show the successors to our D2L-type policy to let it pick one
    return search_policy(task, state, successors)


def translate_state(task, state, static_atoms):
    """ Translate a pyperplan-like state into a list with the format required by SLTP's concept denotation processor """
    translated_state = task.state_to_atoms(state) + list(static_atoms)
    return translated_state


def generate_model_from_state(task, model_factory, state, static_atoms):
    translated = translate_state(task, state, static_atoms)
    return FeatureModel(model_factory.create_model(translated))


def run(config, data, rng):
    if not config.test_instances:
        logging.info("No test instances were specified")
        return ExitCode.NotTestInstancesSpecified, dict()

    if not isinstance(data.d2l_policy, TransitionClassificationPolicy):
    # if not isinstance(data.d2l_policy, StateActionClassificationPolicy):
        return ExitCode.NotPolicySpecified, dict()

    def get_policy(model_factory, static_atoms, data):
        policy = create_action_selection_function_from_transition_policy(config, model_factory, static_atoms,
                                                                             data.d2l_policy)
        return policy

    # Test that the policy reaches a goal when applied on all test instances
    res = test_d2l_policy_on_gym_env(config, data, get_policy, rng)
    return res, dict()
