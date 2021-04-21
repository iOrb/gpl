from gpl.utils import Bunch

OBJECTS = {0, 1, 2, 'X', 'O', 'none'}

OBJECTS = Bunch({
    'general': set([0, 1, 2,]),
    'player_marks': {"X",
                     "O"},
    'none': "none",
})