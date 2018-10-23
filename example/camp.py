from collections import namedtuple

# define an example data structure that will be used
text = namedtuple('text', ['string'])


class Camp(object):
    def __init__(self):
        super().__init__()
        # pre-load data for use in training and testing
        self.training_data = [
            text(string='I am a nice string'),
            text(string='I am also a very average string')
        ]

        self.training_classes = [True, False]

        self.validation_data = [
            text(string='I am a new string'),
            text(string='I am another new string')
        ]

        self.validation_classes = [False, False]

    def train(self, model):
        """
        Receive an untrained model and pass it whatever is required to train it.
        """
        model.train(text=self.training_data, classes=self.training_classes)

    def validate(self, model):
        """
        Receive a trained model and pass it whatever is required to validate it. Return
        the validation dictionary it returns.
        """

        # before doing statistical validation, we can do some miscellaneous validations
        if type(model).__name__ == 'random':
            raise Exception("Models can't be named random. It scares the marketing team.")

        # run the validation and return the results
        predictions = model.predict(text=self.validation_data)

        return {
            'accuracy': sum([1 if p == self.validation_classes[i] else 0 for i, p in enumerate(predictions)]) / float(len(predictions))
        }
