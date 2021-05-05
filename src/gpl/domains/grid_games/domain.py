from .grammar.objects import get_domain_objects
from gpl.domain import IDomain
from tarski.fstrips import fstrips, create_fstrips_problem
from .task import Task
import copy
from .grammar.language import *
import importlib
ANCHOR = 'gpl.domains.grid_games'
OBJECTS = None

class Domain(IDomain):
    def __init__(self, params):
        super().__init__(params.domain_name)
        self.params = params
        self.env = importlib.import_module(f'.envs.{params.domain_name}', ANCHOR).Env
        self.action_space = self.env.get_action_space()
        self.type = 'fond'
        self.set_objects()

    def set_objects(self):
        global OBJECTS
        OBJECTS = get_domain_objects(self.get_domain_name())

    # Generate Language
    def generate_language(self):
        """ Generate the Tarski language corresponding to the given domain. """
        return generate_lang(self._domain_name, self.params)

    # Generate Problem
    def generate_problem(self, lang, instance_name):
        """ Generate the Tarski problem corresponding to the given domain and particular layout. """
        return generate_problem(self._domain_name, lang, self.env, instance_name, self.params)

    # Generate Task
    def generate_task(self, instance_name):
        """ Generate a Task object, according to the Interface ITask """
        return Task(self._domain_name, instance_name, self.env, self.params)


def load_general_lang(lang, statics, params):
    """ Return the FOL language corresponding to the Reach for the Star domain,
     plus a set with the names of those predicates / functions that are static. """

    for sort in params.sorts_to_use:
        lang.sort(sort)
        # for o in OBJECTS.general | {OBJECTS.none}:
        for o in OBJECTS.general:
            lang.predicate(f'{sort}-hv-{o}', sort)
        if CELL_S == sort and params.use_adjacency:
            lang.predicate(f'{ADJACENT}_{sort}', sort, sort)
            statics.add(f'{ADJACENT}_{sort}')
        else:
            for d in GRID_DIRECTIONS[sort]:
                lang.predicate(f'{d}_{sort}', sort, sort)
                statics.add(f'{d}_{sort}')

    if params.use_player_as_feature:
        _ = [lang.predicate('player-{}'.format(p),) for p in {OBJECTS.player.w, OBJECTS.player.b}]

    return lang, statics


def load_general_problem(problem, lang, rep, params):
    brd = copy.deepcopy(rep)
    nrows, ncols = rep.shape
    if params.use_player_as_feature:
        problem.init.add(lang.get('player-{}'.format(OBJECTS.player.w)),)

    map_sorts = dict()
    for r in range(-1, nrows + 1):
        for c in range(-1, ncols + 1):
            for sort in params.sorts_to_use:
                try:
                    map_sorts[(r, c, sort)] = lang.constant(CONST[sort](r, c), lang.get(sort))
                except:
                    pass
                if nrows > r >= 0 and ncols > c >= 0:
                    o = brd[r, c]
                else:
                    # Add value for cells outside the grid
                    o = OBJECTS.none
                if o not in {OBJECTS.empty, OBJECTS.none}:
                    problem.init.add(lang.get(f'{sort}-hv-{o}'), lang.get(CONST[sort](r, c)))

    def __add_direction_predicate(problem, lang, direction, sort, const, new_r, new_c):
        if CELL_S == sort and params.use_adjacency:
            problem.init.add(lang.get(f'{ADJACENT}_{sort}'), const, lang.get(CONST[sort](new_r, new_c)))
        else:
            problem.init.add(lang.get(f'{direction}_{sort}'), const, lang.get(CONST[sort](new_r, new_c)))

    for (row, col, sort), const in map_sorts.items():
        if sort in CELL_S and not params.map_cells:
            continue
        if not ROW_S in sort:
            # Right
            if col < ncols:
                __add_direction_predicate(problem, lang, RIGHT, sort, const, row, col + 1)
            # Left
            if col > -1:
                __add_direction_predicate(problem, lang, RIGHT, sort, const, row, col - 1)
                # __add_direction_predicate(problem, lang, LEFT, sort, const, row, col - 1)
        if not COL_S in sort:
            # Down
            if row < nrows:
                __add_direction_predicate(problem, lang, UP, sort, const, row + 1, col)
                # __add_direction_predicate(problem, lang, DOWN, sort, const, row + 1, col)
            # Up
            if row > -1:
                __add_direction_predicate(problem, lang, UP, sort, const, row - 1, col)
        if CELL_S in sort:
            # Right-Down
            if col < ncols and row < nrows:
                __add_direction_predicate(problem, lang, RIGHTDOWN, sort, const, row + 1, col + 1)
            # Right-Up
            if col < ncols and row > -1:
                __add_direction_predicate(problem, lang, RIGHTUP, sort, const, row - 1, col + 1)
            # Left-Down
            if col > -1 and row < nrows:
                __add_direction_predicate(problem, lang, LEFTDOWN, sort, const, row + 1, col - 1)
            # Left-Up
            if col > -1 and row > -1:
                __add_direction_predicate(problem, lang, LEFTUP, sort, const, row - 1, col - 1)

    return problem


def generate_lang(domain_name, params):
    lang, statics = generate_base_lang(domain_name)
    load_general_lang(lang, statics, params)
    return lang, statics


def generate_base_lang(domain_name):
    from tarski.theories import Theory
    lang = fstrips.language(domain_name, theories=[Theory.EQUALITY])
    return lang, set()


def generate_problem(domain_name, lang, env, instance_name, params):
    problem = generate_base_problem(domain_name, lang, instance_name)
    rep = env.get_grid(instance_name)
    load_general_problem(problem, lang, rep, params)
    return problem


def generate_base_problem(domain_name, lang, instance_name):
    problem = create_fstrips_problem(lang, domain_name=domain_name, problem_name=instance_name)
    # problem = tarski.model.create(lang)
    # problem.evaluator = tarski.evaluators.get_entry_point('simple')
    return problem
