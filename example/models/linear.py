class LinearModel(object):
    def __init__(self, n_epochs=10, l1=0):
        """
        Initialize the model.
        :param n_epochs:
        :param l2:
        """
        self.n_epochs = n_epochs

    def train(self, text=[], classes=[]):
        """
        Train the model. No response is required.
        """
        pass

    def validate(self, text=[], classes=[]):
        """
        Validate the model. Requires a response with the metrics defined in bootcamp.yml.
        """
        return {
            'AUC': .66
        }

    def predict(self, text=[]):
        pass

    def save(self, path):
        pass

    def load(self, path):
        pass