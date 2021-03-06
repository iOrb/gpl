import os
import copy
import logging
import random
from pathlib import Path

from sltp.features import InstanceInformation
from sltp.models import FeatureModel, DLModelFactory
from sltp.returncodes import ExitCode
from sltp.separation import generate_user_provided_policy, TransitionClassificationPolicy, TransitionActionClassificationPolicy, StateActionClassificationPolicy
from sltp.tester import PolicySearchException
from sltp.util.misc import compute_universe_from_pddl_model, state_as_atoms, types_as_atoms
from tarski.dl import compute_dl_vocabulary

from .utils import Bunch, encode_operator

from collections import defaultdict


def test_d2l_policy_on_gym_env(config, data, get_policy, rng):

    solved_instances, unsolved_instances = list(), list()

    count_instances = 0

    for instance_name in config.test_instances:

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
            try:
                problem = config.domain.generate_problem(pl, instance_name)
            except:
                break

            count_instances += 1

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

            # init inteactive screen
            task.init_interacive_screen(task.initial_state)

            # And now we inject our desired search and heuristic functions
            exitcode, solution, path, expanded = run_test(config, search_policy, task, instance_name, rng)

            if config.verbosity > 0:
                task.print_path(path)

            if exitcode == ExitCode.Success:
                # Add instance to solved instances
                solved_instances.append(instance_name)
                logging.info(f"Goal found after expanding {expanded} nodes")
                logging.info(f"The solution was: {solution}")
            else:
                logging.warnieng(f"Testing of policy failed with code: {exitcode}")
                unsolved_instances.append(instance_name)
                continue

        except PolicySearchException as e:
            logging.warning(f"Testing of policy failed with code: {e.code}")
            return e.code

    logging.info("Learnt policy solves the {}% of test instances: {}/{}"
                 .format(round(len(solved_instances) / count_instances * 100, 2),
                         len(solved_instances), count_instances))
    logging.info("Solved instances: {}".format(solved_instances))
    logging.info("Unsolved instances: {}".format(unsolved_instances))
    return ExitCode.Success


def run_test(config, search_policy, task, instance_name, rng):

    logging.info(f'Testing policy in instance: {task.get_domain_name()} - {instance_name}')

    s = task.initial_state
    expanded = 0
    visited_sp = defaultdict(lambda: 0)
    # visited_sp = defaultdict(lambda: 0)
    solution = list()
    path = list()
    path.append(s[0])

    while not s[0].goal:
        expanded += 1
        if expanded % 1000 == 0:
            logging.debug(f"Number of expanded states so far in policy-based search: {expanded}")

        successors = task.get_successor_states(s, just_sp=True)

        if not successors:
            raise PolicySearchException(ExitCode.NotSuccessorsFound)

        exitcode, goods = run_policy_based_search(config, search_policy, task, s, successors)
        if exitcode == ExitCode.AbstractPolicyNotCompleteOnTestInstances:
            if (config.verbosity > 2):
                logging.info("WARNING: Policy not complete in state:\n{}".format(task.get_printable_rep(s[0])))
            exitcode = ExitCode.AbstractPolicyNotCompleteOnTestInstances
            break
            # if config.allow_bad_states:
            #     # we know we are not complete
            #     # TODO: take bad states into account
            #     goods = successors
            # else:
            #     exitcode = ExitCode.AbstractPolicyNotCompleteOnTestInstances
            #     break

        not_novelty_sp = dict()
        for op, sp in goods:
            enc_op = encode_operator(s, op, task)
            if config.use_state_novelty:
                times_seen = visited_sp[sp[1]]
                if times_seen > 0:
                    not_novelty_sp[(enc_op, sp[1])] = times_seen
                    continue
                else:
                    break
            break
        else:
            exitcode = ExitCode.AbstractPolicyNotCompleteOnTestInstances
            break
            # op, _ = min(not_novelty_sp, key=not_novelty_sp.get)
            # if config.verbosity>2:
            #     print("WARNING: not novel transition found")
                # print("WARNING: not novel transition for state:\n{}".format(task.get_printable_rep(s[0])))
            # exitcode = ExitCode.AbstractPolicyNonTerminatingOnTestInstances
            # break

        # Execute the selected action
        # sa_pair_enc = task.encode_sa_pair((s, op))
        visited_sp[sp[1]] += 1
        path.append(sp[0])

        spp = task.transition_env(sp, interactive=True)

        if spp[1] != sp[1]:
            path.append(spp[0])

        if spp[0].deadend:
            exitcode = ExitCode.DeadEndReached
            break

        if visited_sp[sp[1]] > 3:
            exitcode = ExitCode.AbstractPolicyNonTerminatingOnTestInstances
            break

        op = encode_operator(s, op, task) if not isinstance(op, str) else op
        solution.append(op)
        s = spp

    return exitcode, solution, path, expanded


def create_action_selection_function_from_transition_policy(config, model_factory, static_atoms, policy):

    def _policy(task, state, successors):
        m0 = generate_model_from_state(task, model_factory, state, static_atoms)
        goods = list()
        for op, sp in successors:
            # if sp[0].goal:
            #     goods = [(op, sp)]
            #     break
            m1 = generate_model_from_state(task, model_factory, sp, static_atoms)
            # if policy.transition_is_good(m0, op):
            tx = (m0, m1, op) if config.use_action_ids else (m0, m1)
            if policy.transition_is_good(*tx):
                goods.append((op, sp))
        if not goods:
            return ExitCode.AbstractPolicyNotCompleteOnTestInstances, None
        else:
            return ExitCode.Success, goods

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

    if config.d2l_policy is not None:
        data.d2l_policy = generate_user_provided_policy(config)
    if data.d2l_policy is None:
        return ExitCode.NotPolicySpecified, dict()
    else:
        # data.d2l_policy.minimize()
        if config.use_action_ids:
            print("Policy (with actions):")
            data.d2l_policy.print()
        else:
            print("\nPOLICY:")
            data.d2l_policy.print_aaai20()
        print("")

    def get_policy(model_factory, static_atoms, data):
        policy = create_action_selection_function_from_transition_policy(config,
                                                                         model_factory,
                                                                         static_atoms,
                                                                         data.d2l_policy)
        return policy

    # Test that the policy reaches a goal when applied on all test instances
    res = test_d2l_policy_on_gym_env(config, data, get_policy, rng)
    return res, dict()
