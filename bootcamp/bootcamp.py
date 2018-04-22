import os
import yaml
import json
import importlib
import inspect
import itertools
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Bootcamp(object):
    def __init__(self, results_path='results/', config_path='bootcamp.yml', model_config_path='models.yml'):
        """
        Initialize a bootcamp.

        :param config_path: Path to the bootcamp's YAML configuration file.
        :param model_path: Path to the model definition YAML configuration file.
        """

        # holds the callable (non-initialized class) for each model:
        self.models = {}

        # holds the initialized class objects for each model permutation:
        self.model_instances = {}

        # holds the bootcamp class object:
        self.bootcamp = None

        # load and validate general configuration:
        with open(config_path, 'r') as config:
            self.config = yaml.load(config)
        self._validate_config()

        # load and validate model configuration:
        with open(model_config_path, 'r') as model_config:
            self.model_config = yaml.load(model_config)
        self._validate_model_config()

        # folder where we will save results
        self.results_path = results_path

    def train_validate(self):
        """
        Train each model and hyperparameter permutation.
        """
        for model_name, model in self.models:
            logger.info("Training one or more permutations of model: {}".format(model_name))

            parameter_iterations = self.model_config[model_name]['parameters']

            for param_iter in self._parameter_iterations(parameter_iterations):
                logger.info("Training model {} with parameters: {}".format(model_name, param_iter))

                # track start time
                iter_start_time = datetime.datetime.now()

                # name this permutation
                model_key = self._model_key(model_name, param_iter)

                # save the model instance and parameters
                self.model_instances[model_key] = {
                    'object': model(*param_iter),
                    'parameters': param_iter
                }

                # initialize and pass to the bootcamp for training
                self.bootcamp.train(model=self.model_instances[model_key]['object'])

                # validate the train model
                logger.info("Validating model...")
                metrics = self.bootcamp.validate(model=self.model_instances[model_key]['object'])

                for metric_name in self.config['validation_metrics']:
                    if metric_name not in metrics:
                        raise Exception("Validation results for {} did not include the {} metric".format(model_name, metric_name))

                # track end time
                iter_end_time = datetime.datetime.now()

                results_json = {
                    'model': model_name,
                    'parameters': param_iter,
                    'metrics': metrics,
                    'timing': {
                        'start': iter_start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'end': iter_end_time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                }

                results_path = os.path.join(self.results_path, "{}.json".format(model_name))
                with open(results_path, 'w') as file:
                    json.dump(results_json, file)

                logger.info("Results saved")

    def _model_key(self, model_name, parameters):
        return "-".join([model_name, "-".join([str(k) + str(v) for k, v in parameters.items()])])

    def _parameter_iterations(self, parameters):
        """
        Iterate through a dictionary of name=>[possible,values].

        :param: parameters: Dictionary like {'epochs': [1,2,3]}
        """
        if not parameters:
            yield {}
        else:
            param_products = itertools.product(*parameters.values())
            param_sets = [{k: param[i] for i, k in enumerate(parameters)} for param in param_products]

            for iteration in param_sets:
                yield iteration

    def _validate_config(self):
        if 'bootcamp' not in self.config:
            raise Exception("Configuration must specify the Python 'bootcamp' class: bootcamp")
        elif 'module' not in self.config['bootcamp']:
            raise Exception("Configuration must specify the module with the Python bootcamp class: bootcamp.module")
        elif 'callable' not in self.config['bootcamp']:
            raise Exception("Configuration must specify the name of the callable class within the Python bootcamp module: bootcamp.callable")
        elif 'results_folder' not in self.config:
            raise Exception("Configuration must specify a folder for validation results: results")
        elif 'model_requirements' not in self.config:
            raise Exception("Configuration must specify the requirements for models: model_requirements")
        elif 'validation_metrics' not in self.config['model_requirements']:
            raise Exception("Models must be assessed with at least one validation metric: model_requirements.validation_metrics")
        elif 'methods' not in self.config['model_requirements']:
            raise Exception("Model requirements must include methods: model_requirements.methods")
        elif 'train' not in self.config['model_requirements']['methods']:
            raise Exception("All Bootcamp-compatible models must have a train() method: model_requirements.methods")
        elif 'validate' not in self.config['model_requirements']['methods']:
            raise Exception("All Bootcamp-compatible models must have a validate() method: model_requirements.methods")

        # load and validate the bootcamp class:
        this_module = importlib.import_module(self.config['bootcamp']['module'])
        self.bootcamp = getattr(this_module, self.config['bootcamp']['callable'])()

        # look for required methods in the bootcamp class:
        required_methods = ['train', 'validate', 'test']
        for method_name in required_methods:
            method_check = getattr(self.bootcamp, method_name)
            if not method_check or not inspect.ismethod(method_check):
                raise Exception("Basecamp class at {}.{} does not have required {}() method.".format(self.config['bootcamp']['module'], self.config['bootcamp']['callable'], method_name))

            # evaluate whether the method can take the required "model" argument:
            this_argspec = inspect.signature(getattr(self.bootcamp, method_name))
            if 'model' not in this_argspec.parameters:
                raise Exception("{}() in the bootcamp class must accept a 'model' as an argument".format(method_name))

    def _validate_model_config(self):
        # validate the configuration file itself:
        if not len(self.model_config['models']):
            raise Exception("One or more models must be submitted to bootcamp: models")

        for model_name, model in self.model_config['models']:
            if 'module' not in model:
                raise Exception("{} is missing the 'module' attribution".format(model_name))
            elif 'callable' not in model:
                raise Exception("{} is missing the 'callable' attribution".format(model_name))

            # try and actually import the model
            try:
                this_module = importlib.import_module(model.module_class)
                self.models[model_name] = getattr(this_module, model.callable)
            except:
                raise Exception("Failed to import module for {}".format(model_name))

            # look for required methods in each model:
            required_methods = ['train', 'validate']
            for method_name in required_methods:
                method_check = getattr(self.models[model], method_name)
                if not method_check or not inspect.ismethod(method_check):
                    raise Exception("{} does not have the required {}() method".format(model_name, method_name))

            # evaluate whether parameters are valid:
            this_argspec = inspect.signature(self.models[model_name].__init__)
            for parameter_name in self.config['model_requirements']['parameters']:
                if parameter_name not in this_argspec:
                    raise Exception("{} argument not found in {}.__init__(), but all models are required to have this.".format(parameter_name, model_name))

            if 'parameters' in model:
                for parameter_name, values in model['parameters']:
                    # do we have potential values?
                    if not len(values):
                        raise Exception("Hyper-parameter values for {} must be a non-zero length list".format(model_name))

                    # can the __init__ take these arguments?
                    if parameter_name not in this_argspec.parameters:
                        raise Exception("{} argument not found in {}.__init__(), but it was specified as a hyper-parameter.".format(parameter_name, model_name))
