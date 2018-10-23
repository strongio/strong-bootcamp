import random


class LogLinearModel(object):
    def __init__(self, n_epochs=10, l2=0):
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

    def predict(self, text=[]):
        return [random.choice([True, False]) for _ in range(len(text))]

    def save(self, path):
        pass

    def load(self, path):
        pass
