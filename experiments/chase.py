import math

from sltp.util.misc import update_dict
from gpl.domains.grid_games.domain import Domain
from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import CELL_S, COL_S, ROW_S
from gpl.domains.grid_games.grammar.objects import PLAYER1, PLAYER2
from gpl.domains.grid_games.envs.chase import RIGHTUP, RIGHTDOWN, LEFTDOWN, LEFTUP, UP, DOWN, RIGHT, LEFT

chase_params = Bunch({
    'domain_name': 'chase',
    'use_player_as_feature': False,
    'use_player_to_encode': False,
    'use_next_player_as_feature': False,
    'use_next_player_to_encode': False,
    'use_margin_as_feature': False,
    'objects_to_ignore': set(),
    'map_cells': True,
    'use_diagonals_for_map_cells': True,
    'use_adjacency': {COL_S, ROW_S, CELL_S},
    'use_bidirectional': {},
    'sorts_to_use': {COL_S, ROW_S, CELL_S},
    'unary_predicates': {},
    'can_build_walls': False,
    'use_distance_2': {},
    'use_distance_more_than_1': {},
    'use_verbose_margin_as_feature': False,
    'ava_actions': {
        PLAYER1: {RIGHTUP, RIGHTDOWN, LEFTDOWN, LEFTUP},
        # PLAYER1: {UP, DOWN, RIGHT, LEFT},
        PLAYER2: {UP, DOWN, RIGHT, LEFT}},
    'max_actions': {PLAYER1: 1,
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

        verbosity=3,
        initial_sample_size=20,
        refinement_batch_size=50,
        maxsat_iter=10,

        allow_bad_states=False,
        decreasing_transitions_must_be_good=False,
        allow_cycles=False,
        use_action_ids=False,
        use_weighted_tx=True,
        distinguish_goals=False,

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
        instances=[0],
        # instances=[0, 15],
        skip_train_steps=[],
        # skip_train_steps=[0, 1, 2, 3],
        test_instances=[12],
        # test_instances=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],

    )

    # version 2:
    # Agent move Ortogonal, Adv Ortogonal
    # Agent has 2 moves, Adv has 1
    # chase_params.agent_has_to_shoot = True
    # chase_params.max_actions = {PLAYER1: 2, PLAYER2: 1}
    # chase_params.ava_actions={
    #     PLAYER1: {UP, DOWN, RIGHT, LEFT},
    #     PLAYER2: {UP, DOWN, RIGHT, LEFT}}
    exps["2"] = update_dict(
        exps["1"],
        instances=[0],
        domain=Domain(chase_params),
    )

    return exps



