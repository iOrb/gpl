from gpl.domain import IDomain
from ..utils import unserialize_layout

from tarski.fstrips import fstrips, create_fstrips_problem

from generalization_grid_games.envs import checkmate_tactic as ct

from .task import Task

from .expand_state_space import expand_state_space


class Domain(IDomain):
    def __init__(self, domain_name):
        super().__init__(domain_name,)

        self.objects = {ct.EMPTY, ct.HIGHLIGHTED_WHITE_QUEEN, ct.BLACK_KING,
                        ct.HIGHLIGHTED_WHITE_KING, ct.HIGHLIGHTED_BLACK_KING,
                        ct.WHITE_KING, ct.WHITE_QUEEN}

    # Main stateless methods
    def generate_language(self):
        """ Generate the Tarski language corresponding to the given domain. """
        return generate_ct_lang(self._domain_name, self.objects)

    def generate_problem(self, lang, instance_filename):
        """ Generate the Tarski problem corresponding to the given domain and particular layout. """
        return generate_ct_problem(self._domain_name, lang, instance_filename)

    def generate_task(self, instance_filename):
        """ Generate a Task object, according to the Interface ITask """
        return Task(self._domain_name, instance_filename, self.objects)

    def expand_state_space(self, instance_filename, teach_policies, output):
        """ Expand state space of an instance """
        return expand_state_space(self.generate_task(instance_filename), teach_policies, output)


GRID_DIRECTIONS = ['up', 'rightup', 'right', 'rightdown', 'down', 'leftdown', 'left', 'leftup']


def generate_ct_lang(domain_name, objects):
    lang, statics = generate_base_lang(domain_name)
    objects.add('none')
    load_general_lang(lang, statics, domain_name, objects)
    return lang, statics


def load_general_lang(lang, statics, domain_name, objects):
    """ Return the FOL language corresponding to the Reach for the Star domain,
     plus a set with the names of those predicates / functions that are static. """

    lang.sort('cell')

    _ = [lang.predicate(d, 'cell', 'cell') for d in GRID_DIRECTIONS]
    statics.update(set(GRID_DIRECTIONS))

    _ = [lang.predicate(f'cell-hv-{o}', 'cell') for o in objects]

    # Scanning ==================================
    lang.predicate('same_row', 'cell', 'cell')
    lang.predicate('same_col', 'cell', 'cell')

    statics.add('same_row')
    statics.add('same_col')
    # ===============================================

    return lang, statics


def generate_base_lang(domain_name):
    from tarski.theories import Theory
    lang = fstrips.language(domain_name, theories=[Theory.EQUALITY])
    # lang = tarski.language(theories=[Theory.EQUALITY])
    return lang, set()


def generate_ct_problem(domain_name, lang, instance_name):
    problem = generate_base_problem(domain_name, lang, instance_name)
    layout = unserialize_layout(instance_name)
    load_general_problem(problem, domain_name, lang, instance_name, layout)
    return problem


def generate_base_problem(domain_name, lang, instance_name):
    problem = create_fstrips_problem(lang, domain_name=domain_name, problem_name=instance_name)
    # problem = tarski.model.create(lang)
    # problem.evaluator = tarski.evaluators.get_entry_point('simple')
    return problem


def load_general_problem(problem, domain_name, lang, instance_name, layout):

    nrows = len(layout)
    assert nrows > 0
    ncols = len(layout[0])

    cell_ = lang.get('cell')

    map_cells = dict()

    for r in range(-1, nrows + 1):

        for c in range(-1, ncols + 1):

            if nrows > r >= 0 and ncols > c >= 0:
                o = layout[r, c]
            else:
                # Add the None value for cells outside the world
                o = 'none'

            cell = lang.constant(f'c{r}-{c}', cell_)

            map_cells[(r, c)] = cell

            # Add the atoms such as hv-drawn(c12,) to the initial state of the problem
            problem.init.add(lang.get(f'cell-hv-{o}'), cell)

    scan(lang, problem, layout)

    # Let's specify the entire grid topology:
    up, rightup, right, rightdown, down, leftdown, left, leftup = [lang.get(d) for d in GRID_DIRECTIONS]

    # The format we use is the following:  an atom at(rightup,x, y) denotes that cell y is to the right and up of
    # cell x, or, in other words, that if you start at x and move right and up, you end up at y.
    for (row, col), cell in map_cells.items():

        # Right
        if col < ncols - 1:
            problem.init.add(right, cell, lang.get(f'c{row}-{col + 1}'))

        # Left
        if col > 0:
            problem.init.add(left, cell, lang.get(f'c{row}-{col - 1}'))

        # Down
        if row < nrows - 1:
            problem.init.add(down, cell, lang.get(f'c{row + 1}-{col}'))

        # Up
        if row > 0:
            problem.init.add(up, cell, lang.get(f'c{row - 1}-{col}'))

        # Right-Down
        if col < ncols - 1 and row < nrows - 1:
            problem.init.add(rightdown, cell, lang.get(f'c{row + 1}-{col + 1}'))

        # Right-Up
        if col < ncols - 1 and row > 0:
            problem.init.add(rightup, cell, lang.get(f'c{row - 1}-{col + 1}'))

        # Left-Down
        if col > 0 and row < nrows - 1:
            problem.init.add(leftdown, cell, lang.get(f'c{row + 1}-{col - 1}'))

        # Left-Up
        if col > 0 and row > 0:
            problem.init.add(leftup, cell, lang.get(f'c{row - 1}-{col - 1}'))

    return problem


def scan(lang, problem, layout):

    nrows, ncols = layout.shape

    for r in range(-1, nrows + 1):

        row_ = [(r, col) for col in range(ncols)]

        for c in range(-1, ncols + 1):

            # Column cells
            col_ = [(row, c) for row in range(nrows)]

            # Add the same_row predicate for the current cell
            _ = [problem.init.add(lang.get(f'same_row'), lang.get(f'c{r}-{c}'), lang.get(f'c{r_}-{c_}'))
                 for r_, c_ in row_ if (r_, c_) != (r, c)]

            # Add the same_col predicate for the current cell
            _ = [problem.init.add(lang.get(f'same_col'), lang.get(f'c{r}-{c}'), lang.get(f'c{r_}-{c_}'))
                 for r_, c_ in col_ if (r_, c_) != (r, c)]

            # # left-up
            # left_up_ = [(row, col) for row, col in zip(range(r - 1, -1, -1), range(c - 1, -1, -1))]
            #
            # # right-down
            # right_down_ = [(row, col) for row, col in zip(range(r + 1, nrows), range(c + 1, ncols))]

            # # Main diagonal:
            # d1_ = left_up_ + right_down_
            #
            # # left-down
            # left_down_ = [(row, col) for row, col in zip(range(r+1, nrows), range(c - 1, -1, -1))]
            #
            # # right-up
            # right_up_ = [(row, col) for row, col in zip(range(r-1, -1, -1), range(c + 1, ncols))]
            #
            # # Inverse diagonal:
            # d2_ = left_down_ + right_up_
            #
            # # Add the same_d1 predicate for the current cell
            # _ = [problem.init.add(lang.get(f'same_d1'), lang.get(f'c{r}-{c}'), lang.get(f'c{r_}-{c_}'))
            #      for r_, c_ in d1_ if (r_, c_) != (r, c)]
            #
            # # Add the same_d2 predicate for the current cell
            # _ = [problem.init.add(lang.get(f'same_d2'), lang.get(f'c{r}-{c}'), lang.get(f'c{r_}-{c_}'))
            #      for r_, c_ in d2_ if (r_, c_) != (r, c)]
