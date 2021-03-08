import copy
from collections import namedtuple
from tarski.fstrips import fstrips, create_fstrips_problem

import tarski
from tarski.theories import Theory
import tarski.model
import tarski.evaluators

from generalization_grid_games.envs import two_pile_nim as tpn
from generalization_grid_games.envs import checkmate_tactic as ct
from generalization_grid_games.envs import stop_the_fall as stf
from generalization_grid_games.envs import chase as ec
from generalization_grid_games.envs import reach_for_the_star as rfts
from generalization_grid_games.envs import TwoPileNim
from generalization_grid_games.envs import CheckmateTactic
from generalization_grid_games.envs import StopTheFall
from generalization_grid_games.envs import Chase
from generalization_grid_games.envs import ReachForTheStar

import numpy as np

GRID_DIRECTIONS = ['up', 'rightup', 'right', 'rightdown', 'down', 'leftdown', 'left', 'leftup']

Domain = namedtuple('Domain', 'objects base_name base_class acronym language_generator problem_generator')


def get_domain_data(name):
    _DOMAIN_DATA = dict(
        reach_for_the_star=Domain(
            objects={rfts.EMPTY, rfts.AGENT, rfts.STAR, rfts.DRAWN, rfts.LEFT_ARROW, rfts.RIGHT_ARROW},
            base_name="ReachForTheStar",
            base_class=ReachForTheStar,
            acronym='rfts',
            language_generator=generate_rfts_lang,
            problem_generator=generate_rfts_problem,
        ),

        stop_the_fall=Domain(
            objects={stf.EMPTY, stf.FALLING, stf.RED,
                     stf.STATIC, stf.ADVANCE, stf.DRAWN},
            base_name="StopTheFall",
            base_class=StopTheFall,
            acronym='stf',
            language_generator=generate_stf_lang,
            problem_generator=generate_stf_problem,
        ),

        # Two Player Games

        chase=Domain(
            objects={ec.EMPTY, ec.TARGET, ec.AGENT, ec.WALL, ec.DRAWN,
                     ec.LEFT_ARROW, ec.RIGHT_ARROW, ec.UP_ARROW, ec.DOWN_ARROW},
            base_name="Chase",
            base_class=Chase,
            acronym='ec',
            language_generator=generate_ec_lang,
            problem_generator=generate_ec_problem,
        ),

        checkmate_tactic=Domain(
            objects={ct.EMPTY, ct.HIGHLIGHTED_WHITE_QUEEN, ct.BLACK_KING,
                     ct.HIGHLIGHTED_WHITE_KING, ct.HIGHLIGHTED_BLACK_KING,
                     ct.WHITE_KING, ct.WHITE_QUEEN},
            base_name="CheckmateTactic",
            base_class=CheckmateTactic,
            acronym='ct',
            language_generator=generate_ct_lang,
            problem_generator=generate_ct_problem,
        ),

        two_pile_nim=Domain(
            objects={tpn.EMPTY, tpn.TOKEN},
            base_name="TwoPileNim",
            base_class=TwoPileNim,
            acronym='tpn',
            language_generator=generate_tpn_lang,
            problem_generator=generate_tpn_problem,
        ),
    )
    domain = _DOMAIN_DATA.get(name)
    if domain is None:
        raise RuntimeError(f'Domain "{name}" is not defined in domains.py. Please make sure the name is correct.'
                           f'Defined domains are: {", ".join(_DOMAIN_DATA.keys())}')

    if domain.objects is None:
        raise RuntimeError(f'Domain data for "{name}" does not contain list of objects')
    return domain


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


# Reach for the star (Language & Problem):
def generate_rfts_lang(domain_name):
    lang, statics = generate_base_lang(domain_name)
    objects = get_domain_data(domain_name).objects
    objects.add('none')
    objects.remove(rfts.LEFT_ARROW)
    objects.remove(rfts.RIGHT_ARROW)
    load_general_lang(lang, statics, domain_name, objects)
    return lang, statics


def generate_rfts_problem(domain_name, lang, instance_name, layout):
    problem = generate_base_problem(domain_name, lang, instance_name)
    layout = copy.deepcopy(layout)
    layout = np.delete(layout, [-1], axis=0)
    problem = load_general_problem(problem, domain_name, lang, instance_name, layout)
    return problem


# Two pile nim (Language & Problem):
def generate_tpn_lang(domain_name):
    lang, statics = generate_base_lang(domain_name)
    objects = get_domain_data(domain_name).objects
    objects.add('none')
    lang.predicate('player0',)
    load_general_lang(lang, statics, domain_name, objects)
    return lang, statics


def generate_tpn_problem(domain_name, lang, instance_name, layout):
    problem = generate_base_problem(domain_name, lang, instance_name)
    load_general_problem(problem, domain_name, lang, instance_name, layout)
    return problem


# Checkmate tactic (Language & Problem):
def generate_ct_lang(domain_name):
    lang, statics = generate_base_lang(domain_name)
    objects = get_domain_data(domain_name).objects
    objects.add('none')
    load_general_lang(lang, statics, domain_name, objects)
    return lang, statics


def generate_ct_problem(domain_name, lang, instance_name, layout):
    problem = generate_base_problem(domain_name, lang, instance_name)
    load_general_problem(problem, domain_name, lang, instance_name, layout)
    return problem


# Stop the fall (Language & Problem):
def generate_stf_lang(domain_name):
    lang, statics = generate_base_lang(domain_name)
    objects = get_domain_data(domain_name).objects
    objects.add('none')
    load_general_lang(lang, statics, domain_name, objects)
    return lang, statics


def generate_stf_problem(domain_name, lang, instance_name, layout):
    problem = generate_base_problem(domain_name, lang, instance_name)
    load_general_problem(problem, domain_name, lang, instance_name, layout)
    return problem


# Chase (Language & Problem):
def generate_ec_lang(domain_name):
    lang, statics = generate_base_lang(domain_name)
    objects = get_domain_data(domain_name).objects
    objects.add('none')
    objects.remove(ec.LEFT_ARROW)
    objects.remove(ec.RIGHT_ARROW)
    objects.remove(ec.DOWN_ARROW)
    objects.remove(ec.UP_ARROW)
    objects.remove(ec.WALL)
    statics = set()

    lang.sort('cell')
    lang.sort('row')
    lang.sort('col')

    _ = [lang.predicate(d, 'cell', 'cell') for d in GRID_DIRECTIONS]
    statics.update(set(GRID_DIRECTIONS))

    lang.predicate(f'vertical_row', 'row', 'row')
    statics.add(f'vertical_row')

    lang.predicate(f'horizontal_col', 'col', 'col')
    statics.add(f'horizontal_col')

    _ = [lang.predicate(f'cell-hv-{o}', 'cell') for o in objects]
    _ = [lang.predicate(f'row-hv-{o}', 'row') for o in objects]
    _ = [lang.predicate(f'col-hv-{o}', 'col') for o in objects]

    return lang, statics


def generate_ec_problem(domain_name, lang, instance_name, layout):
    problem = generate_base_problem(domain_name, lang, instance_name)

    layout = copy.deepcopy(layout)
    la, _ = np.argwhere(layout == ec.LEFT_ARROW)[0]
    ra, _ = np.argwhere(layout == ec.RIGHT_ARROW)[0]
    da, _ = np.argwhere(layout == ec.DOWN_ARROW)[0]
    ua, _ = np.argwhere(layout == ec.UP_ARROW)[0]
    layout = np.delete(layout, [la, ra, da, ua], axis=0)

    nrows, ncols = layout.shape
    layout = layout.flatten()
    layout = np.delete(layout, np.argwhere(layout == ec.WALL)).reshape(nrows - 2, ncols - 2)
    nrows, ncols = layout.shape

    assert nrows > 0

    cell_ = lang.get('cell')

    # Rows and Columns =========================================================
    _ = [lang.constant(f'row-{i}', lang.get('row')) for i in range(-1, nrows + 1)]
    _ = [lang.constant(f'col-{i}', lang.get('col')) for i in range(-1, ncols + 1)]

    vertical_row = lang.get('vertical_row')
    for i in range(-1, nrows):
        problem.init.add(vertical_row, lang.get(f'row-{i}'), lang.get(f'row-{i + 1}'))
        problem.init.add(vertical_row, lang.get(f'row-{i + 1}'), lang.get(f'row-{i}'))

    horizonal_col = lang.get('horizontal_col')
    for i in range(-1, ncols):
        problem.init.add(horizonal_col, lang.get(f'col-{i}'), lang.get(f'col-{i + 1}'))
        problem.init.add(horizonal_col, lang.get(f'col-{i + 1}'), lang.get(f'col-{i}'))
    # ==========================================================================

    map_cells = dict()

    for r in range(-1, nrows + 1):

        for c in range(-1, ncols + 1):

            if nrows > r >= 0 and ncols > c >= 0:
                o = layout[r, c]
            else:
                # Add the None value for cells outside the world
                o = 'none'

            cell = lang.constant(f'c{r}-{c}', cell_)
            row = lang.get(f'row-{r}')
            col = lang.get(f'col-{c}')

            map_cells[(r, c)] = cell

            # Add the atoms such as hv-drawn(c12,) to the initial state of the problem
            problem.init.add(lang.get(f'cell-hv-{o}'), cell)
            problem.init.add(lang.get(f'row-hv-{o}'), row)
            problem.init.add(lang.get(f'col-hv-{o}'), col)

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


# Init Language & Problem:
def generate_base_lang(domain_name):
    lang = fstrips.language(domain_name, theories=[Theory.EQUALITY])
    # lang = tarski.language(theories=[Theory.EQUALITY])
    return lang, set()


def generate_base_problem(domain_name, lang, instance_name):
    problem = create_fstrips_problem(lang, domain_name=domain_name, problem_name=instance_name)
    # problem = tarski.model.create(lang)
    # problem.evaluator = tarski.evaluators.get_entry_point('simple')
    return problem


def generate_language(domain):
    """ Generate the Tarski language corresponding to the given grid domain. """
    return get_domain_data(domain).language_generator(domain)


def generate_problem(domain, lang, instance_name, layout):
    """ Generate the Tarski problem corresponding to the given grid domain and particular layout. """
    return get_domain_data(domain).problem_generator(domain, lang, instance_name, layout)
