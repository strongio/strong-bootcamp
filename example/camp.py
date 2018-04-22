from collections import namedtuple

# define an example data structure that will be used
text = namedtuple('text', ['string'])


class Camp(object):
    def __init__(self):
        super().__init__()

        # pre-load data for use in training and testing
        self.training = [
            text(string='test1'),
            text(string='test2')
        ]
        self.training_classes = [True, False]

        self.validation = [
            text(string='test3'),
            text(string='test4')
        ]

    def train(self, model):
        """
        Receive an untrained model and pass it whatever is required to train it.
        """
        model.train(text=self.training, classes=self.training_classes)

    def validate(self, model):
        """
        Receive a trained model and pass it whatever is required to validate it. Return
        the validation dictionary it returns.
        """

        # before doing statistical validation, we can do some miscellaneous unit tests
        if type(model).__name__ == 'random':
            raise Exception("Models can't be named random. It sends a bad message to the client.")

        # run the validation and return the results
        return model.validate(text=self.validation, classes=self.training_classes)
