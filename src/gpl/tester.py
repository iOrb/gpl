import os
import copy
import logging
import random
from pathlib import Path

from lgp.domains import generate_language, generate_problem
from lgp.utils import unserialize_layout
from sltp.features import InstanceInformation
from sltp.models import FeatureModel, DLModelFactory
from sltp.returncodes import ExitCode
from sltp.separation import generate_user_provided_policy, TransitionClassificationPolicy
from sltp.tester import PolicySearchException
from sltp.util.misc import compute_universe_from_pddl_model, state_as_atoms, types_as_atoms
from tarski.dl import compute_dl_vocabulary

from lgp.task import Task


def apply_policy_on_test_instances(config, create_policy):

    solved_instances, unsolved_instances = list(), list()

    for instance in config.test_instances:
        logging.info(f'Testing policy on instance "{instance}"')

        try:
            """ Run a search on the test instances that follows the given policy """
            lang, static_predicates = generate_language(config.domain)
            vocabulary = compute_dl_vocabulary(lang)

            # We interpret as DL nominals all constants that are defined on the entire domain, i.e. instance-independent
            nominals = lang.constants()
            static_predicates |= {s.name for s in lang.sorts}  # Add unary predicates coming from types!

            instance_name = Path(instance).stem

            # We clone the language so that objects from different instances don't get registered all in the same language;
            # if that happened, we'd be unable to properly compute the universe of each instance.
            pl = copy.deepcopy(lang)
            problem = generate_problem(config.domain, pl, instance_name, unserialize_layout(instance))

            # Compute the universe of each instance: a set with all objects in the universe
            universe = compute_universe_from_pddl_model(problem.language)

            # Compute the set of all static atoms in the instance, including those stemming from types
            static_atoms = {atom for atom in state_as_atoms(problem.init) if atom[0] in static_predicates} |\
                           {atom for atom in types_as_atoms(problem.language)}

            info = InstanceInformation(universe, static_atoms, static_predicates, {}, {})

            # Parse the domain & instance and create a model generator
            model_factory = DLModelFactory(vocabulary, nominals, info)

            # Compute an actual policy object that returns the next action to be applied
            search_policy = create_policy(model_factory, static_atoms)

            # define the Task
            task = Task(config.domain, instance)

            # And now we inject our desired search and heuristic functions
            run_policy_based_search(search_policy, task=task)

            # Add instance to solved instances
            solved_instances.append(os.path.splitext(os.path.basename(instance))[0])

        except PolicySearchException as e:
            logging.warning(f"Testing of policy failed with code: {e.code}")
            unsolved_instances.append(os.path.splitext(os.path.basename(instance))[0])
            continue
            # return e.code
    logging.info("Learnt policy solves the {}% of test instances: {}/{}"
                 .format(round(len(solved_instances)/len(config.test_instances)*100, 2),
                         len(solved_instances), len(config.test_instances)))
    logging.info("Solved instances: {}".format(solved_instances))
    logging.info("Unsolved instances: {}".format(unsolved_instances))
    return ExitCode.Success


def translate_state(task, state, static_atoms):
    """ Translate a pyperplan-like state into a list with the format required by SLTP's concept denotation processor """
    layout, info = state
    translated_state = task.state_to_atoms(layout, info)
    translated_state = translated_state + list(static_atoms)
    return translated_state


def generate_model_from_state(task, model_factory, state, static_atoms):
    translated = translate_state(task, state, static_atoms)
    return FeatureModel(model_factory.create_model(translated))


def run_policy_based_search(search_policy, task):
    expanded = 0  # Some bookkeeping
    initial_state_layout = task.initial_state
    info = {'reward': 0, 'is_goal': 0, 'is_dead_end': 0}
    initial_state_encoded = task.encode_state(initial_state_layout, info) # Assum that initial state is not a goal nor dead_end
    parents = {initial_state_encoded: 'root'}  # We'll use this at the same time as closed list and to keep track of parents
    solution = list()
    node = (initial_state_layout, info)

    while not info['is_goal']:
        # logging.info(f'Expanding: {sorted(node.state)}')
        expanded += 1
        if expanded % 1000 == 0:
            logging.debug(f"Number of expanded states so far in policy-based search: {expanded}")

        # Compute all possible successors:
        successors = task.get_successor_states(node[0])

        # Show the successors to our D2L-type policy to let it pick one
        op = search_policy(task, node, successors)

        succ = task.transition(node[0], op)
        (succ_layout, info) = succ
        succ_encoded = task.encode_state(succ_layout, info)
        solution.append(op)

        if succ_encoded in parents:  # loop detection
            # logging.error(f"Policy incurred in a loop after {expanded} expansions. Repeated node: {succ_layout}")
            # logging.error(f"Trajectory from initial state: {solution}")
            raise PolicySearchException(ExitCode.AbstractPolicyNonTerminatingOnTestInstances)
            # return

        if info['is_dead_end']:

            raise PolicySearchException(ExitCode.DeadEndReached)

        parents[succ_encoded] = node
        node = (succ_layout, info)

    logging.info(f"Goal found after expanding {expanded} nodes")
    logging.info(f"The solution was: {solution}")
    return solution


def create_action_selection_function_from_transition_policy(config, model_factory, static_atoms, policy):
    assert isinstance(policy, TransitionClassificationPolicy)

    def _policy(task, state, successors):
        m0 = generate_model_from_state(task, model_factory, state, static_atoms)

        for op, succs in successors.items():
            labeled_transitions = set()
            for _, succ in succs:
                m1 = generate_model_from_state(task, model_factory, succ, static_atoms)
                labeled_transitions.add(policy.transition_is_good(m0, m1))
            if all(labeled_transitions):
                return op

        # op, succ = random.choice(successors)
        # return [op], [succ]

        # if config.policy_depth == 2:
        #     # Do not surrender!

        # Report the reason why no transition is labeled as good
        # for op, succ in successors:
        #     m1 = generate_model_from_state(task, model_factory, succ, static_atoms)
        #     print(f"\nTransition to state {succ} is bad because:")
        #     policy.explain_why_transition_is_bad(m0, m1)

        raise PolicySearchException(ExitCode.AbstractPolicyNotCompleteOnTestInstances)

    return _policy


def test_d2l_policy_on_gym_env(config, data, rng):
    if not config.test_instances:
        logging.info("No testing instances were specified")
        return ExitCode.Success, dict()

    def create_policy(model_factory, static_atoms):
        if config.d2l_policy is not None:
            policy = generate_user_provided_policy(config)
        else:
            policy = data.d2l_policy

        return create_action_selection_function_from_transition_policy(config, model_factory, static_atoms, policy)

    # Test that the policy reaches a goal when applied on all test instances
    res = apply_policy_on_test_instances(config, create_policy)
    return res, dict()
