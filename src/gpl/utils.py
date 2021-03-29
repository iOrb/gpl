import pickle
import dill

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


def unpack_state(state):
    s_rep = state[0]
    info = state[1]
    goal = state[1]['goal']
    deadend = state[1]['deadend']
    s_encode = state[2]
    return s_rep, goal, deadend, s_encode, info


def save_local_object(local_object, filename):
    with open(filename, 'wb') as f:
        dill.dump(local_object, f)
        f.close()


def load_local_object(filename):
    picklefile = open(filename, 'rb')
    local_object = dill.load(filename)
    picklefile.close()
    return local_object