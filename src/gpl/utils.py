

def _create_exception_msg(step, e):
    return 'Critical error processing step "{}". Error message: {}'. \
        format(step.description(), e)


class Bunch:
    def __init__(self, adict):
        self.__dict__.update(adict)

    def to_dict(self):
        return self.__dict__.copy()

    def update(self, adict):
        self.__dict__.update(adict)


def print_important_message(msg):
    print('------------------------------------------------')
    print(msg)
    print('------------------------------------------------')

