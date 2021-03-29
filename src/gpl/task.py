
class ITask:
    """
    General Task
    """
    def __init__(self, domain_name, objects):
        self._domain_name = domain_name
        self._objects = objects

    def encode_state(self, state, info):
        raise NotImplementedError()

    def state_to_atoms(self, state, info):
        raise NotImplementedError()

    def state_to_atoms_string(self, state, info):
        raise NotImplementedError()

    def get_successor_states(self, state0):
        raise NotImplementedError()

    def transition(self, state0, operator=None):
        raise NotImplementedError()

    def infer_info_from_state(self, state0, operator, state1):
        raise NotImplementedError()

    def get_all_possible_operators(self, state=None):
        raise NotImplementedError()

    def get_applicable_operators(self, state=None):
        raise NotImplementedError()

    def is_operator_applicable(self, state=None, operaror=None):
        raise NotImplementedError()