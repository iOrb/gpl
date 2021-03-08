import sys
import string

from lgp.utils import get_operators

from lgp.grammar.state_to_atoms import state_to_atoms, atom_tuples_to_string

ASCII = string.printable
# ASCII = ''.join(chr(x) for x in range(50, 1000))

class Grammar:
    """
    Wrapper of some grammar utils
    """

    def __init__(self, domain, instance):

        self.domain_name = domain.base_name
        self.objects = domain.objects
        self.actions = get_operators(instance)
        self.object_bytes = self.objects_to_bytes()

    def state_to_atoms(self, state, info):
        return state_to_atoms(self.domain_name, state, info)

    def state_to_atoms_string(self, state, info):
        return atom_tuples_to_string(self.state_to_atoms(state, info))

    def encode_state(self, state, info):
        """ Return a Python bytes object with a byte corresponding to each object type.
        This should have roughly as many bytes as positions in the layout, which will typically be much
        more compact than a numpy array of `object` types for encoding single characters, that uses several bytes per
        position.
        """
        try:
            b = list(self.object_bytes[obj] for obj in state.flatten())
            b = b + [self.object_bytes[1]] if info['reward'] else b + [self.object_bytes[0]]
            b = b + [self.object_bytes[1]] if info['is_goal'] else b + [self.object_bytes[0]]
            b = b + [self.object_bytes[1]] if info['is_dead_end'] else b + [self.object_bytes[0]]
            return bytes(b)
        except:
            for o in state.flatten():
                if o not in self.object_bytes:
                    print('EXCEPTION: Unknown object: {}\n'.format(o))
            sys.exit(1)

    def objects_to_bytes(self):

        object_bytes = dict()
        possible_chars = ASCII

        for obj in self.objects:
            possible_chars, b = possible_chars[1:], possible_chars[0]
            object_bytes[obj] = ord(b)

        for i in range(2):
            possible_chars, b = possible_chars[1:], possible_chars[0]
            object_bytes[i] = ord(b)

        return object_bytes
