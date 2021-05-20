import math

from sltp.util.misc import update_dict

from gpl.domains.grid_games.domain import Domain

from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import CELL_S, COL_S, ROW_S, D1_S, D2_S
from gpl.domains.grid_games.envs.shoot import RIGHTUP, RIGHTDOWN, LEFTDOWN, LEFTUP, UP, DOWN, RIGHT, LEFT
from gpl.domains.grid_games.grammar.objects import PLAYER1, PLAYER2

shoot_params = Bunch({
    'domain_name': 'shoot',
    'use_player_as_feature': True,
    'map_cells': True,
    'use_diagonals_for_map_cells': True,
    'use_adjacency': {COL_S, ROW_S},
    'use_bidirectional': {},
    'sorts_to_use': {COL_S, ROW_S, D1_S, D2_S},
    'player_can_shoot': {},
    'player_can_check': {PLAYER1},
    'max_actions': {PLAYER1: 1, PLAYER2: 1},
    'unary_predicates': {},
    'attaking_mask': {UP, DOWN, RIGHT, LEFT},
    # 'attaking_mask': {RIGHTUP, RIGHTDOWN, LEFTDOWN, LEFTUP, UP, DOWN, RIGHT, LEFT},
})

def experiments():
    base = dict(
        domain=Domain(shoot_params),
        maxsat_encoding="d2l",
        num_states="all",
        concept_generator=None,
        parameter_generator=None,
        v_slack=2,
        acyclicity='topological',
        use_incremental_refinement=False,
    )

    exps = dict()
    exps["1"] = update_dict(
        base,
        instances=[0],
        # instances=[0, 1],
        test_instances=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        max_concept_size=5,
        distance_feature_max_complexity=4,
        concept_generation_timeout=15000,
        cond_feature_max_complexity=0,
        comparison_features=False,
        generate_goal_concepts=False,
        print_denotations=True,
        print_hstar_in_feature_matrix=False,

        verbosity=1,
        initial_sample_size=50,
        refinement_batch_size=10,
        maxsat_iter=3,

        sampling_strategy='full',

        allow_bad_states=False,
        decreasing_transitions_must_be_good=False,
        allow_cycles=False,
        use_action_ids=False,
        use_weighted_tx=True,
        use_state_novelty=True,
        distinguish_goals=True,

        # skip_train_steps=[0, 1, 2],  # do not generate features twice!
        skip_train_steps=[],
        # rollouts
        # num_episodes=1,
        # num_rollouts=1,
        # rollout_depth=2,
        # train_instances_to_expand=[],
        train_instances_to_expand=list(range(1000)),
        max_states_expanded=math.inf,
    )

    exps["2"] = update_dict(
        exps["1"],
        use_weighted_tx=False,
    )

    return exps




