
class IDomain:
    def __init__(self, domain_name,):
        self.__domain_name = domain_name

    # Main stateless methods
    def generate_lang(self):
        """ Generate the Tarski language corresponding to the given domain. """
        raise NotImplementedError()

    def generate_problem(self, instance):
        """ Generate the Tarski problem corresponding to the given domain and particular layout. """
        raise NotImplementedError()
