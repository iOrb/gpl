import math

from sltp.util.misc import update_dict
from gpl.domains.grid_games.domain import Domain
from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import CELL_S, COL_S, ROW_S
from gpl.domains.grid_games.envs.wumpus import RIGHTUP, RIGHTDOWN, LEFTDOWN, LEFTUP, UP, DOWN, RIGHT, LEFT
from gpl.domains.grid_games.grammar.objects import PLAYER1, PLAYER2

chase_params = Bunch({
    'domain_name': 'wumpus',
    'use_player_as_feature': False,
    'use_next_player_as_feature': False,
    'map_cells': True,
    'use_diagonals_for_map_cells': True,
    'use_adjacency': {CELL_S},
    'use_bidirectional': {},
    'sorts_to_use': {CELL_S},
    'unary_predicates': {},
    'can_build_walls': False,
    'wumpus_active': False,
    'ava_actions': {
        # PLAYER1: {RIGHTUP, RIGHTDOWN, LEFTDOWN, LEFTUP},
        PLAYER1: {UP, DOWN, RIGHT, LEFT, RIGHTUP, RIGHTDOWN, LEFTDOWN, LEFTUP},
        PLAYER2: {UP, DOWN, RIGHT, LEFT, RIGHTUP, RIGHTDOWN, LEFTDOWN, LEFTUP}},
    'max_actions': {PLAYER1: 3te,
                    PLAYER2: 1},
})

def experiments():
    base = dict(
        domain=Domain(chase_params),
        maxsat_encoding="d2l",
        num_states="all",
        concept_generator=None,
        parameter_generator=None,
        v_slack=2,
        acyclicity='topological',
        discrete_action_space=False,
        use_incremental_refinement=False,

        max_concept_size=5,
        distance_feature_max_complexity=4,
        concept_generation_timeout=15000,
        cond_feature_max_complexity=0,
        comparison_features=False,
        generate_goal_concepts=False,
        print_denotations=True,
        print_hstar_in_feature_matrix=False,

        verbosity=1,
        initial_sample_size=20,
        refinement_batch_size=50,
        maxsat_iter=10,

        allow_bad_states=False,
        decreasing_transitions_must_be_good=False,
        allow_cycles=False,
        use_action_ids=False,
        use_weighted_tx=False,
        distinguish_goals=True,

        sampling_strategy="full",

        # skip_train_steps=[0, 1, 2],  # do not generate features twice!
        skip_train_steps=[],

        # rollouts
        # num_episodes=1,
        # num_rollouts=1,
        # rollout_depth=2,
        # train_instances_to_expand=[],
        train_instances_to_expand=list(range(1000)),
        max_states_expanded=math.inf,
        use_state_novelty=True,
    )

    # version 1:
    # Agent move diagonal, Adv Ortogonal
    # Agent has 1 move, Adv has 1
    exps = dict()
    exps["1"] = update_dict(
        base,
        instances=[1, 6],
        test_instances=[0, 1, 2, 3, 4, 5, 6],
        allow_bad_states=True,
    )

    return exps



