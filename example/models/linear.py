class LinearModel(object):
    def __init__(self, n_epochs=10, l1=0):
        self.n_epochs = n_epochs

    def train(self):
        pass

    def validate(self):
        return {
            'AUC': .45
        }
