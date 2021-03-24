
class GPLModel:
    def __init__(self, parameters):
        self.parametes = parameters

        self.train_mode = False
        self.eval_mode = False

    def step(self):
        if self.train_mode:
            # run episode
            pass

    def train(self):
        if self.eval_mode:
            self.eval_mode = False
        self.train_mode = True

    def eval(self):
        if self.train_mode:
            self.train_mode = False
        self.eval_mode = True