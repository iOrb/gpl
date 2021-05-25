import string
import sys

from .state_to_atoms import state_to_atoms, atom_tuples_to_string
from .objects import get_domain_objects

# ASCII = string.printable
MAX_NUM = 1000
ASCII = ''.join(chr(x) for x in range(5000))


class Grammar:
    """
    Wrapper of some grammar utils
    """

    def __init__(self, domain_name, params):

        self.domain_name = domain_name
        self.params = params
        self.object_bytes = self.objects_to_bytes()

    def state_to_atoms(self, state):
        return state_to_atoms(self.domain_name, state, self.params)

    def state_to_atoms_string(self, state,):
        return atom_tuples_to_string(self.state_to_atoms(state,))

    def encode_state(self, r):
        """ Return a Python bytes object with a byte corresponding to each object type.
        This should have roughly as many bytes as positions in the layout, which will typically be much
        more compact than a numpy array of `object` types for encoding single characters, that uses several bytes per
        position.
        """
        try:
            b = list(self.object_bytes[obj] for obj in r.grid.flatten())
            if self.params.use_player_as_feature:
                b = b + [self.object_bytes[r.player]]
            if self.params.use_next_player_as_feature:
                b = b + [self.object_bytes[r.next_player]]
            for u in self.params.unary_predicates:
                b = b + [self.object_bytes['true']] if getattr(r, u) else b + [self.object_bytes['false']]
            # b = b + [self.object_bytes[r.nmoves]]
            # b = b + [self.object_bytes['true']] if info['reward'] else b + [self.object_bytes['false']]
            # b = b + [self.object_bytes['true']] if info['goal'] else b + [self.object_bytes['false']]
            # b = b + [self.object_bytes['true']] if info['deadend'] else b + [self.object_bytes['false']]
            return bytes(b)
        except:
            for o in r.grid.flatten():
                if o not in self.object_bytes:
                    print('EXCEPTION: Unknown object: {}'.format(o))

    def objects_to_bytes(self):
        OBJECTS = get_domain_objects(self.domain_name)

        object_bytes = dict()
        possible_chars = ASCII
        numbers = list(range(MAX_NUM))

        for obj in OBJECTS.general | {OBJECTS.empty}:
            possible_chars, b = possible_chars[1:], possible_chars[0]
            object_bytes[obj] = ord(b)

        for obj in {OBJECTS.player1, OBJECTS.player2}:
            possible_chars, b = possible_chars[1:], possible_chars[0]
            object_bytes[obj] = ord(b)

        for i in ['true', 'false']:
            possible_chars, b = possible_chars[1:], possible_chars[0]
            object_bytes[i] = ord(b)

        for i in numbers:
            possible_chars, b = possible_chars[1:], possible_chars[0]
            object_bytes[i] = ord(b)

        return object_bytes




