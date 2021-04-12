
class ITask:
    """
    General Task
    """
    def __init__(self, domain_name, instance_name):
        self.__domain_name = domain_name
        self.__instance_name = instance_name

    def get_instance_name(self):
        return self.__instance_name

    def get_domain_name(self):
        return self.__domain_name