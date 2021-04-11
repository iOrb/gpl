import string
import sys

from domains.chess_.grammar.state_to_atoms import state_to_atoms, atom_tuples_to_string
from domains.chess_.grammar.objects import OBJECTS

ASCII = string.printable
# ASCII = ''.join(chr(x) for x in range(50, 1000))


class Grammar:
    """
    Wrapper of some grammar utils
    """

    def __init__(self, domain_name,):

        self.domain_name = domain_name
        self.object_bytes = self.objects_to_bytes()

    def state_to_atoms(self, state,):
        return state_to_atoms(self.domain_name, state,)

    def state_to_atoms_string(self, state,):
        return atom_tuples_to_string(self.state_to_atoms(state,))

    def encode_state(self, r, info):
        """ Return a Python bytes object with a byte corresponding to each object type.
        This should have roughly as many bytes as positions in the layout, which will typically be much
        more compact than a numpy array of `object` types for encoding single characters, that uses several bytes per
        position.
        """
        try:
            b = list(self.object_bytes[obj] for obj in r.flatten())
            b = b + [self.object_bytes[1]] if info['reward'] else b + [self.object_bytes[0]]
            b = b + [self.object_bytes[1]] if info['goal'] else b + [self.object_bytes[0]]
            b = b + [self.object_bytes[1]] if info['deadend'] else b + [self.object_bytes[0]]
            return bytes(b)
        except:
            for o in r.flatten():
                if o not in self.object_bytes:
                    print('EXCEPTION: Unknown object: {}\n'.format(o))
            sys.exit(1)

    def objects_to_bytes(self):

        object_bytes = dict()
        possible_chars = ASCII

        for obj in OBJECTS.general:
            possible_chars, b = possible_chars[1:], possible_chars[0]
            object_bytes[obj] = ord(b)

        for obj in OBJECTS.player_marks.values():
            possible_chars, b = possible_chars[1:], possible_chars[0]
            object_bytes[obj] = ord(b)

        for i in ['true', 'false']:
            possible_chars, b = possible_chars[1:], possible_chars[0]
            object_bytes[i] = ord(b)

        return object_bytes




