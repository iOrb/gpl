import copy
import math
from gpl.utils import Bunch
from gpl.domains.grid_games.grammar.language import CELL_S, COL_S, ROW_S
from gpl.domains.grid_games.grammar.objects import PLAYER1, PLAYER2
from sltp.util.misc import update_dict

from gpl.domains.grid_games.domain import Domain

from gpl.domains.grid_games.envs.space_invaders import LAST_TURN


space_invaders_params = Bunch({
    'domain_name': 'space_invaders',
    'use_player_as_feature': False,
    'map_cells': True,
    'use_diagonals_for_map_cells': False,
    'use_adjacency': {COL_S},
    'use_bidirectional': {},
    'sorts_to_use': {CELL_S, COL_S},
    'unary_predicates': {},
    'predicates_arity_1': {},
    'agent_has_to_shoot': True,
    'adv_can_move_down': True,
    'adv_can_move_up': False,
    'adv_can_kill_agent_going_down': False,
    'adv_can_kill_agent_shooting': False,
    'max_actions': {PLAYER1: 2,
                    PLAYER2: 1},
    'target_columns': True,
})

def experiments():
    base = dict(
        domain=Domain(space_invaders_params),
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

        verbosity=2,
        initial_sample_size=100,
        refinement_batch_size=200,
        maxsat_iter=20,

        allow_bad_states=False,
        decreasing_transitions_must_be_good=False,
        allow_cycles=False,
        use_action_ids=False,
        use_weighted_tx=False,
        use_state_novelty=True,
        distinguish_goals=True,

        sampling_strategy="full",

        # skip_train_steps=[0, 1, 2, 3],
        skip_train_steps=[],
        # rollouts
        # num_episodes=1,
        # num_rollouts=1,
        # rollout_depth=2,
        # train_instances_to_expand=[],
        train_instances_to_expand=list(range(1000)),
        max_states_expanded=math.inf,
    )
    exps = dict()

    # version 1:
    # agent can shoot
    # agent has 2 moves
    # martians can't Kill the Agent
    space_invaders_params_v1 = copy.deepcopy(space_invaders_params)
    space_invaders_params_v1.unary_predicates = {}
    space_invaders_params_v1.use_player_as_feature = True
    space_invaders_params_v1.use_bidirectional = {}
    space_invaders_params_v1.max_actions={PLAYER1: 2, PLAYER2: 1}
    space_invaders_params_v1.target_columns=False
    exps["1"] = update_dict(
        base,
        domain=Domain(space_invaders_params_v1),
        instances=[0, 17, 18],
        test_instances=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18],
    )

    # version 2: the agent can not shoot, but can kill moving into the adv column, has 2 moves
    space_invaders_params_v2 = copy.deepcopy(space_invaders_params)
    space_invaders_params_v2.agent_has_to_shoot = False
    exps["2"] = update_dict(
        exps["1"],
        domain=Domain(space_invaders_params_v2),
        instances=[17],
        # instances=[3, 4],
    )

    # version 3:
    # agent can shoot
    # agent has 3 moves
    # martians can Kill the Agent, shooting, but not going down
    space_invaders_params_v3 = copy.deepcopy(space_invaders_params)
    space_invaders_params_v3.agent_has_to_shoot = True
    space_invaders_params_v3.adv_can_kill_agent_going_down = True
    space_invaders_params_v3.adv_can_kill_agent_shooting = False
    space_invaders_params_v3.use_player_as_feature = True
    space_invaders_params_v3.max_actions={PLAYER1: 3, PLAYER2: 1}
    exps["3"] = update_dict(
        exps["1"],
        domain=Domain(space_invaders_params_v3),
        instances=[0, 11],
        allow_bad_states=True,
        use_weighted_tx=False,  # Good(s, a, s') -> -bad(s')
        max_concept_size=5,
        distance_feature_max_complexity=4,
    )

    # version 4:
    # agent can shoot
    # agent has 3 moves
    # martians can Kill the Agent, shooting, but not going down
    space_invaders_params_v4 = copy.deepcopy(space_invaders_params)
    space_invaders_params_v4.agent_has_to_shoot = True
    space_invaders_params_v4.adv_can_kill_agent_going_down = False
    space_invaders_params_v4.adv_can_kill_agent_shooting = True
    space_invaders_params_v4.use_player_as_feature = False
    space_invaders_params_v4.max_actions={PLAYER1: 5, PLAYER2: 1}
    exps["4"] = update_dict(
        exps["1"],
        domain=Domain(space_invaders_params_v4),
        instances=[0, 16, 17],
        allow_bad_states=False,
        use_weighted_tx=False,  # Good(s, a, s') -> -bad(s')
        max_concept_size=5,
        distance_feature_max_complexity=4,
    )

    return exps
