import pickle
import sys

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


def save_local_object(local_object, filename):
    with open(filename, 'wb') as f:
        dill.dump(local_object, f)
        f.close()


def load_local_object(filename):
    picklefile = open(filename, 'rb')
    local_object = dill.load(filename)
    picklefile.close()
    return local_object


def encode_operator(s, op, task):
    if callable(getattr(task, "encode_op", None)):
        o = task.encode_op(s, op)
    else:
        o = op
    return o

def get_sampling_class(config):
    from .sampling.adv import TransitionSampleADV
    sampling_class = {
        'adv': TransitionSampleADV(),
    }[config.domain.type]
    if config.use_action_ids:
        sampling_class.set_operators(config.domain.action_space)
    return sampling_class