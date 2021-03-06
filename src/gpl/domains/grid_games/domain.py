from .grammar.objects import get_domain_objects, MARGINS
from gpl.domain import IDomain
from tarski.fstrips import fstrips, create_fstrips_problem
from .task import Task
import copy
from .grammar.language import *
from .utils import identify_margin, in_bottom, in_top, in_left_most, in_right_most
import importlib
ANCHOR = 'gpl.domains.grid_games'
OBJECTS = None

class Domain(IDomain):
    def __init__(self, params):
        super().__init__(params.domain_name)
        self.params = params
        self.env = importlib.import_module(f'.envs.{params.domain_name}', ANCHOR).Env(params)
        self.action_space = self.env.get_action_space()
        self.type = 'adv'
        self.set_objects()

    def set_objects(self):
        global OBJECTS
        OBJECTS = get_domain_objects(self.get_domain_name())

    def get_printable_params(self):
        printable_params = ""
        for p, val in self.params.to_dict().items():
            printable_params += "{}: {}\n".format(p, str(val))
        return printable_params[:-1]

    # Generate Language
    def generate_language(self):
        """ Generate the Tarski language corresponding to the given domain. """
        return generate_lang(self._domain_name, self.env)

    # Generate Problem
    def generate_problem(self, lang, instance_name):
        """ Generate the Tarski problem corresponding to the given domain and particular layout. """
        return generate_problem(self._domain_name, lang, self.env, instance_name)

    # Generate Task
    def generate_task(self, instance_name):
        """ Generate a Task object, according to the Interface ITask """
        return Task(self._domain_name, instance_name, self.env)


def load_general_lang(lang, statics, env):
    """ Return the FOL language corresponding to the Reach for the Star domain,
     plus a set with the names of those predicates / functions that are static. """
    params = env.params
    for sort in params.sorts_to_use:
        lang.sort(sort)
        for o in OBJECTS.general | {OBJECTS.none} | set(MARGINS.values()):
            lang.predicate(CELL_HAS(sort, o), sort)
        if sort in params.use_distance_2:
            lang.predicate(f'{DISTANCE_2}_{sort}', sort, sort)
            statics.add(f'{DISTANCE_2}_{sort}')
        if sort in params.use_distance_more_than_1:
            lang.predicate(f'{DISTANCE_MORE_THAN_1}_{sort}', sort, sort)
            statics.add(f'{DISTANCE_MORE_THAN_1}_{sort}')
        if sort in params.use_adjacency:
            lang.predicate(f'{ADJACENT}_{sort}', sort, sort)
            statics.add(f'{ADJACENT}_{sort}')
        if sort in params.use_bidirectional:
            for d in GRID_DIRECTIONS[sort]:
                lang.predicate(f'{d}_{sort}', sort, sort)
                statics.add(f'{d}_{sort}')

    for u in params.unary_predicates:
        lang.predicate(f'{u}',)

    if params.use_player_as_feature:
        _ = [lang.predicate('player-{}'.format(p),) for p in {OBJECTS.player1, OBJECTS.player2}]

    if params.use_next_player_as_feature:
        _ = [lang.predicate('next_player-{}'.format(p),) for p in {OBJECTS.player1, OBJECTS.player2}]

    # CHECKMATE TACTIC
    from .envs.checkmate_tactic import WHITE_KING, WHITE_TOWER, BLACK_KING, WHITE, BLACK, WHITE_QUEEN
    for pred in {CELL_HAS_COLOR_ATTAKED_BY(WHITE),
                 CELL_HAS_COLOR_ATTAKED_BY(BLACK),
                 CELL_HAS_PIECE_ATTAKED_BY(WHITE_TOWER),
                 CELL_HAS_PIECE_ATTAKED_BY(WHITE_KING),
                 CELL_HAS_PIECE_ATTAKED_BY(BLACK_KING),
                 CELL_HAS_PIECE_ATTAKED_BY(WHITE_QUEEN),
                 CELL_IS_IN(TOP), CELL_IS_IN(RIGHT), CELL_IS_IN(LEFT), CELL_IS_IN(BOTTOM),
                 CELL_IS_IN(BLACK_KING_AVAILABLE_QUADRANT)}:
        lang.predicate(pred, CELL_S)

    return lang, statics


def load_general_problem(problem, lang, rep, env):
    brd = copy.deepcopy(rep.grid)
    nrows, ncols = brd.shape
    params = env.params
    if params.use_player_as_feature:
        problem.init.add(lang.get('player-{}'.format(rep.player),))
    if params.use_next_player_as_feature:
        problem.init.add(lang.get('next_player-{}'.format(rep.next_player),))

    for u in params.unary_predicates:
        if getattr(rep, u):
            problem.init.add(lang.get(u,))

    map_sorts = dict()
    for r in range(-1, nrows + 1):
        for c in range(-1, ncols + 1):
            for sort in params.sorts_to_use:
                o = brd[r, c] if (nrows > r >= 0 and ncols > c >= 0) else OBJECTS.none
                if o == OBJECTS.none:
                    if params.use_verbose_margin_as_feature:
                        o = identify_margin(r, c, nrows, ncols)
                    elif params.use_margin_as_feature:
                        pass
                    else:
                        continue
                try:
                    map_sorts[(r, c, sort)] = lang.constant(CONST[sort](r, c, nrows, ncols), lang.get(sort))
                except:
                    map_sorts[(r, c, sort)] = lang.get(CONST[sort](r, c, nrows, ncols))
                if o not in {OBJECTS.empty} | params.objects_to_ignore:
                    problem.init.add(lang.get(CELL_HAS(sort, o)), lang.get(CONST[sort](r, c, nrows, ncols)))

    # CHECKMATE TACTIC
    if params.domain_name == 'checkmate_tactic':
        from .envs.checkmate_tactic import get_attacking_mask_from_piece, get_attacking_mask, WHITE, BLACK, WHITE_KING, \
            WHITE_TOWER, BLACK_KING, CHECKMATE, WHITE_QUEEN
        mask_white = get_attacking_mask(brd, WHITE)
        mask_black = get_attacking_mask(brd, BLACK)
        mask_bk = get_attacking_mask_from_piece(brd, BLACK_KING)
        mask_wk = get_attacking_mask_from_piece(brd, WHITE_KING)
        # mask_wr = get_attacking_mask_from_piece(brd, WHITE_TOWER)
        mask_wq = get_attacking_mask_from_piece(brd, WHITE_QUEEN)
        # mask_quadrant_bk = get_mask_quadrant_black_king(brd)
        for r in range(nrows):
            for c in range(ncols):
                cell = lang.get(CONST[CELL_S](r, c, nrows, ncols))
                if mask_wk[r, c]:
                    problem.init.add(lang.get(CELL_HAS_PIECE_ATTAKED_BY(WHITE_KING)), cell)
                # if mask_wr[r, c]:
                #     problem.init.add(lang.get(CELL_HAS_PIECE_ATTAKED_BY(WHITE_TOWER)), cell)
                if mask_bk[r, c]:
                    problem.init.add(lang.get(CELL_HAS_PIECE_ATTAKED_BY(BLACK_KING)), cell)
                if mask_wq[r, c]:
                    problem.init.add(lang.get(CELL_HAS_PIECE_ATTAKED_BY(WHITE_QUEEN)), cell)
                if mask_white[r, c]:
                    problem.init.add(lang.get(CELL_HAS_COLOR_ATTAKED_BY(WHITE)), cell)
                if mask_black[r, c]:
                    problem.init.add(lang.get(CELL_HAS_COLOR_ATTAKED_BY(BLACK)), cell)
                # if mask_quadrant_bk[r, c] and not mask_white[r, c] and not getattr(rep, CHECKMATE):
                #     problem.init.add(lang.get(CELL_IS_IN(BLACK_KING_AVAILABLE_QUADRANT)), cell)
                if in_top(r, c, nrows, ncols):
                    problem.init.add(lang.get(CELL_IS_IN(TOP)), cell)
                if in_bottom(r, c, nrows, ncols):
                    problem.init.add(lang.get(CELL_IS_IN(BOTTOM)), cell)
                if in_left_most(r, c, nrows, ncols):
                    problem.init.add(lang.get(CELL_IS_IN(LEFT)), cell)
                if in_right_most(r, c, nrows, ncols):
                    problem.init.add(lang.get(CELL_IS_IN(RIGHT)), cell)

    # WUMPUS
    # from .envs.wumpus import AT_WUMPUS, AT_PIT, AGENT, WUMPUS
    # if AGENT not in brd and getattr(rep, AT_WUMPUS):
    #     r, c = np.argwhere(brd == WUMPUS)[0]
    #     sort = CELL_S
    #     o = AGENT
    #     problem.init.add(lang.get(f'{sort}-has-{o}'), lang.get(CONST[sort](r, c, nrows, ncols)))
    # if AGENT not in brd and getattr(rep, AT_PIT) is not None:
    #     r, c = getattr(rep, AT_PIT)
    #     sort = CELL_S
    #     o = AGENT
    #     atoms.append((f'{sort}-has-{o}', CONST[sort](r, c, nrows, ncols)))

    # DELIVERY
    # from .envs.delivery import AT_DESTINATION, HOLDING_PACKAGE, DESTINY, PACKAGE
    # if getattr(rep, AT_DESTINATION):
    #     r, c = np.argwhere(brd==AGENT)[0]
    #     sort = CELL_S
    #     o=DESTINY
    #     problem.init.add(lang.get(f'{sort}-has-{o}'), lang.get(CONST[sort](r, c, nrows, ncols)))
    # if not PACKAGE in rep.grid:
    #     r, c = np.argwhere(brd==AGENT)[0]
    #     sort = CELL_S
    #     o=PACKAGE
    #     problem.init.add(lang.get(f'{sort}-has-{o}'), lang.get(CONST[sort](r, c, nrows, ncols)))

    def __add_direction_predicate(problem, lang, direction, sort, const, new_r, new_c):
        if (new_r<0 or new_c<0 or ncols==new_c or nrows==new_r) and not params.use_margin_as_feature:
            return
        if sort in params.use_adjacency:
            problem.init.add(lang.get(f'{ADJACENT}_{sort}'), const, lang.get(CONST[sort](new_r, new_c, nrows, ncols)))
        if sort in params.use_bidirectional:
            problem.init.add(lang.get(f'{direction}_{sort}'), const, lang.get(CONST[sort](new_r, new_c, nrows, ncols)))

    for (row, col, sort), const in map_sorts.items():
        if sort in CELL_S and not params.map_cells:
            continue
        if sort in {CELL_S, COL_S, D1_S, D2_S}:
            # Right
            if col < ncols:
                __add_direction_predicate(problem, lang, RIGHT, sort, const, row, col + 1)
            # Left
            if col > -1:
                __add_direction_predicate(problem, lang, LEFT, sort, const, row, col - 1)
        if sort in {CELL_S, ROW_S}:
            # Down
            if row < nrows:
                __add_direction_predicate(problem, lang, DOWN, sort, const, row + 1, col)
            # Up
            if row > -1:
                __add_direction_predicate(problem, lang, UP, sort, const, row - 1, col)
        if sort in {CELL_S}:
            # Right-Down
            if col < ncols and row < nrows:
                __add_direction_predicate(problem, lang, RIGHTDOWN, sort, const, row + 1, col + 1)
            # Left-Up
            if col > -1 and row > -1:
                __add_direction_predicate(problem, lang, LEFTUP, sort, const, row - 1, col - 1)
        if sort in {CELL_S}:
            # Right-Up
            if col < ncols and row > -1:
                __add_direction_predicate(problem, lang, RIGHTUP, sort, const, row - 1, col + 1)
            # Left-Down
            if col > -1 and row < nrows:
                __add_direction_predicate(problem, lang, LEFTDOWN, sort, const, row + 1, col - 1)

    # add distance 2 predicates
    DISTANCE_2_DIRECTIONS = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
                             (-1, -2),                             (-1, 2),
                             (0, -2),                              (0, 2),
                             (1, -2),                              (1, 2),
                             (2, -2),  (2, -1),  (2, 0),  (2, 1),  (2, 2),
    ]
    from .utils import in_grid
    for (row, col, sort), const in map_sorts.items():
        if sort not in params.use_distance_2:
            continue
        for dr, dc in DISTANCE_2_DIRECTIONS:
            new_r, new_c = row + dr, col + dc
            in_grid_ = in_grid(new_r, new_c, nrows, ncols, use_margins=params.use_margin_as_feature)
            if in_grid_:
                problem.init.add(lang.get(f'{DISTANCE_2}_{sort}'), const, lang.get(CONST[sort](new_r, new_c, nrows, ncols)))

    # add distance more than 1 predicates
    ALL_DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for (row, col, sort), const in map_sorts.items():
        if sort not in params.use_distance_more_than_1:
            continue
        for dr, dc in ALL_DIRECTIONS:
            new_r, new_c  = row, col
            while True:
                new_r += dr
                new_c += dc
                in_grid_ = in_grid(new_r, new_c, nrows, ncols, use_margins=params.use_margin_as_feature)
                if in_grid_:
                    problem.init.add(lang.get(f'{DISTANCE_2}_{sort}'), const,
                                     lang.get(CONST[sort](new_r, new_c, nrows, ncols)))
                else:
                    break
    return problem


def generate_base_lang(domain_name):
    from tarski.theories import Theory
    lang = fstrips.language(domain_name, theories=[Theory.EQUALITY])
    return lang, set()


def generate_lang(domain_name, env):
    lang, statics = generate_base_lang(domain_name)
    load_general_lang(lang, statics, env)
    return lang, statics


def generate_base_problem(domain_name, lang, instance_name):
    problem = create_fstrips_problem(lang, domain_name=domain_name, problem_name=instance_name)
    # problem = tarski.model.create(lang)
    # problem.evaluator = tarski.evaluators.get_entry_point('simple')
    return problem


def generate_problem(domain_name, lang, env, instance_name):
    problem = generate_base_problem(domain_name, lang, instance_name)
    rep = env.init_instance(instance_name)
    load_general_problem(problem, lang, rep, env)
    return problem