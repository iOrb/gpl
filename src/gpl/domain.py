
class IDomain:
    def __init__(self, domain_name,):
        self._domain_name = domain_name

    # Main stateless methods
    def generate_language(self):
        """ Generate the Tarski language corresponding to the given domain. """
        raise NotImplementedError()

    def generate_problem(self, lang, instance_filename):
        """ Generate the Tarski problem corresponding to the given domain and particular layout. """
        raise NotImplementedError()

    def generate_task(self, instance_filename):
        """ Generate a Task object, according to the Interface ITask """
        raise NotImplementedError()

    def expand_state_space(self, instance_filename, teach_policies, output):
        """ Expand state space of an instance """
        raise NotImplementedError()

    def get_domain_name(self):
        return self._domain_name