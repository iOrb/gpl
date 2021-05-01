from .grammar.objects import OBJECTS
from gpl.domain import IDomain
from tarski.fstrips import fstrips, create_fstrips_problem
from .task import Task
from .utils import identify_margin
from .utils import unserialize_layout
import copy
from .env.chase import ACTION_SPACE
from .config import use_player_as_feature, to_scann, use_margin_as_feature, \
    use_diagonal_directions, use_relaxed_grid_directions, sorts_to_use
from .grammar.state_to_atoms import SORT

class Domain(IDomain):
    def __init__(self, domain_name):
        super().__init__(domain_name)
        self.action_space = ACTION_SPACE
        self.type = 'fond'

    # Generate Language
    def generate_language(self):
        """ Generate the Tarski language corresponding to the given domain. """
        return generate_lang(self._domain_name,)

    # Generate Problem
    def generate_problem(self, lang, instance_name):
        """ Generate the Tarski problem corresponding to the given domain and particular layout. """
        return generate_problem(self._domain_name, lang, instance_name)

    # Generate Task
    def generate_task(self, instance_name, config):
        """ Generate a Task object, according to the Interface ITask """
        return Task(self._domain_name, instance_name, config)


ALL_GRID_DIRECTIONS = ['up', 'rightup', 'right', 'rightdown', 'down', 'leftdown', 'left', 'leftup']
ALL_PERPENDICULAR_GRID_DIRECTIONS = ['up', 'right', 'down', 'left']
ALL_DIAGONAL_GRID_DIRECTIONS = ['rightup', 'rightdown', 'leftdown', 'leftup']

GRID_DIRECTIONS = {'row': {'right', 'left'},
                   'col': {'up', 'down'},
                   'd1': {'leftup', 'rightdown'},
                   'd2': {'leftdown', 'rightup'}}


def generate_lang(domain_name,):
    lang, statics = generate_base_lang(domain_name)
    load_general_lang(lang, statics,)
    return lang, statics


def generate_base_lang(domain_name):
    from tarski.theories import Theory
    lang = fstrips.language(domain_name, theories=[Theory.EQUALITY])
    # lang = tarski.language(theories=[Theory.EQUALITY])
    return lang, set()


def load_general_lang(lang, statics,):
    """ Return the FOL language corresponding to the Reach for the Star domain,
     plus a set with the names of those predicates / functions that are static. """

    for sort in sorts_to_use:
        lang.sort(sort)
        for o in OBJECTS.general:
            lang.predicate(f'{sort}-hv-{o}', sort)

        for d in ALL_GRID_DIRECTIONS:
            lang.predicate(f'{d}_{sort}', sort, sort)
            statics.add(f'{d}_{sort}')

    if 'cell' in sorts_to_use:
        if use_margin_as_feature:
            _ = [lang.predicate(f'{o}', 'cell') for o in OBJECTS.margin.values()]
            _ = [statics.add(f'{o}') for o in OBJECTS.margin.values()]
        else:
            lang.predicate(f'{OBJECTS.none}', 'cell')

        if use_player_as_feature:
            _ = [lang.predicate('player-{}'.format(p),) for p in {OBJECTS.player.w, OBJECTS.player.b}]

        # Scanning ==================================
        for c in to_scann:
            c = 'same_{}'.format(c)
            lang.predicate(c, 'cell', 'cell')
            statics.add(c)
        # ===============================================

        # if not 'cell' in sort:
        #     for d in GRID_DIRECTIONS[sort]:
        #         lang.predicate(f'{d}_{sort}', sort, sort)
        #         statics.add(f'{d}_{sort}')
        # else:
        #     if use_relaxed_grid_directions:
        #         for d in ALL_PERPENDICULAR_GRID_DIRECTIONS:
        #             lang.predicate(f'{d}_relaxed', 'cell', 'cell')
        #             statics.add(f'{d}_relaxed')
        #
        #     if use_margin_as_feature:
        #         _ = [lang.predicate(f'{o}', 'cell') for o in OBJECTS.margin.values()]
        #         _ = [statics.add(f'{o}') for o in OBJECTS.margin.values()]
        #     else:
        #         lang.predicate(f'{OBJECTS.none}', 'cell')
        #
        #     if use_player_as_feature:
        #         _ = [lang.predicate('player-{}'.format(p),) for p in {OBJECTS.player.w, OBJECTS.player.b}]
        #
        #     # Scanning ==================================
        #     for c in to_scann:
        #         c = 'same_{}'.format(c)
        #         lang.predicate(c, 'cell', 'cell')
        #         statics.add(c)
        #     # ===============================================

    return lang, statics


def generate_problem(domain_name, lang, instance_name):
    problem = generate_base_problem(domain_name, lang, instance_name)
    rep = unserialize_layout(instance_name)
    load_general_problem(problem, lang, rep)
    return problem


def generate_base_problem(domain_name, lang, instance_name):
    problem = create_fstrips_problem(lang, domain_name=domain_name, problem_name=instance_name)
    # problem = tarski.model.create(lang)
    # problem.evaluator = tarski.evaluators.get_entry_point('simple')
    return problem


def load_general_problem(problem, lang, rep):
    brd = copy.deepcopy(rep)
    nrows, ncols = rep.shape

    if use_player_as_feature:
        problem.init.add(lang.get('player-{}'.format(OBJECTS.player.w)),)

    map_sorts = dict()

    for r in range(-1, nrows + 1):
        for c in range(-1, ncols + 1):
            for sort in sorts_to_use:
                map_cells[(r, c, sort)] = lang.constant(SORT[sort](r, c), lang.get(sort))
                if nrows > r >= 0 and ncols > c >= 0:
                    o = brd[r, c]
                    if o == OBJECTS.empty:
                        continue
                else:
                    # Add value for cells outside the grid
                    o = f'{identify_margin(r, c, nrows, ncols)}' if use_margin_as_feature else f'{OBJECTS.none}'
                problem.init.add(lang.get(f'{sort}-hv-{o}'), lang.get(SORT[sort](r, c)))

    # Let's specify the entire pick_package topology:
    up, rightup, right, rightdown, down, leftdown, left, leftup = [lang.get(d) for d in GRID_DIRECTIONS]

    # The format we use is the following:  an atom at(rightup,x, y) denotes that cell y is to the right and up of
    # cell x, or, in other words, that if you start at x and move right and up, you end up at y.
    for (row, colm, sort), const in map_cells.items():

        # Right
        if col < ncols:
            problem.init.add(right, cell, lang.get(f'c{row}-{col + 1}'))

        # Left
        if col > -1:
            problem.init.add(left, cell, lang.get(f'c{row}-{col - 1}'))

        # Down
        if row < nrows:
            problem.init.add(down, cell, lang.get(f'c{row + 1}-{col}'))

        # Up
        if row > -1:
            problem.init.add(up, cell, lang.get(f'c{row - 1}-{col}'))

        if use_diagonal_directions:
            # Right-Down
            if col < ncols and row < nrows:
                problem.init.add(rightdown, cell, lang.get(f'c{row + 1}-{col + 1}'))

            # Right-Up
            if col < ncols and row > -1:
                problem.init.add(rightup, cell, lang.get(f'c{row - 1}-{col + 1}'))

            # Left-Down
            if col > -1 and row < nrows:
                problem.init.add(leftdown, cell, lang.get(f'c{row + 1}-{col - 1}'))

            # Left-Up
            if col > -1 and row > -1:
                problem.init.add(leftup, cell, lang.get(f'c{row - 1}-{col - 1}'))

        if use_relaxed_grid_directions:
            up_r, right_r, down_r, left_r = [lang.get(d) for d in RELAXED_GRID_DIRECTIONS]

            for (row_0, col_0), cell_0 in map_cells.items():
                for (row_1, col_1), cell_1 in map_cells.items():
                    # Right relaxed
                    if col_0 < col_1:
                        problem.init.add(right_r, cell_0, cell_1)

                    # Left relaxed
                    if col_0 > col_1:
                        problem.init.add(left, cell_0, cell_1)

                    # Down relaxed
                    if row_0 < row_1:
                        problem.init.add(down, cell_0, cell_1)

                    # Up relaxed
                    if row_0 > row_1:
                        problem.init.add(up, cell_0, cell_1)

    return problem


def scan(lang, problem, layout):

    nrows, ncols = layout.shape

    for r in range(-1, nrows + 1):

        row_ = [(r, col) for col in range(ncols)]

        for c in range(-1, ncols + 1):

            # Column cells
            col_ = [(row, c) for row in range(nrows)]

            if 'row' in to_scann:
                # Add the same_row predicate for the current cell
                _ = [problem.init.add(lang.get(f'same_row'), lang.get(f'c{r}-{c}'), lang.get(f'c{r_}-{c_}'))
                     for r_, c_ in row_ if (r_, c_) != (r, c)]

            if 'col' in  to_scann:
                # Add the same_col predicate for the current cell
                _ = [problem.init.add(lang.get(f'same_col'), lang.get(f'c{r}-{c}'), lang.get(f'c{r_}-{c_}'))
                     for r_, c_ in col_ if (r_, c_) != (r, c)]

            if 'd1' in to_scann:
                # left-up
                left_up_ = [(row, col) for row, col in zip(range(r - 1, -1, -1), range(c - 1, -1, -1))]

                # right-down
                right_down_ = [(row, col) for row, col in zip(range(r + 1, nrows), range(c + 1, ncols))]

                # Main diagonal:
                d1_ = left_up_ + right_down_

                # Add the same_d1 predicate for the current cell
                _ = [problem.init.add(lang.get(f'same_d1'), lang.get(f'c{r}-{c}'), lang.get(f'c{r_}-{c_}'))
                     for r_, c_ in d1_ if (r_, c_) != (r, c)]

            if 'd2' in to_scann:
                # left-down
                left_down_ = [(row, col) for row, col in zip(range(r + 1, nrows), range(c - 1, -1, -1))]

                # right-up
                right_up_ = [(row, col) for row, col in zip(range(r - 1, -1, -1), range(c + 1, ncols))]

                # Inverse diagonal:
                d2_ = left_down_ + right_up_

                # Add the same_d2 predicate for the current cell
                _ = [problem.init.add(lang.get(f'same_d2'), lang.get(f'c{r}-{c}'), lang.get(f'c{r_}-{c_}'))
                     for r_, c_ in d2_ if (r_, c_) != (r, c)]

