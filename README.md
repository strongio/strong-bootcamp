# strong-bootcamp

A Python package that makes it easier to test and compare machine
learning models before they are deployed.

The guiding principle: _If the model makes it through bootcamp, it's fit to be deployed._

## Why use Bootcamp?

1. You can ensure that each model faces the same rigorous tests before deployment, encouraging
more confident, rapid iteration.
2. You inherit a straightforward means of hyperparameter testing and evaluation for free.
3. You maintain total control over _what_ is tested.
4. You maintain total control over _where_ these tests occur (e.g., you can test models
within a larger application or in a standalone experiment).

## Installation

    git clone https://github.com/strongio/strong-bootcamp.git
    pip install strong-bootcamp

## Usage

### Build a Bootcamp

A bootcamp is made up of three, simple components:

* **Bootcamp Configuration**: A YAML file defining the requirements for models that will
be tested on this problem.
* **Model Configuration(s)**: One or more YAML files defining models that will be
evaluated in the bootcamp. For each model, we specify where it can be found
as well as a number of (optional) hyperparameters to test.
* **Bootcamp Class**: A simple Python class that oversees each model's _training_ and
_validation_ in the bootcamp.

#### Bootcamp Configuration (YAML)

Bootcamp configuration files lay the basic ground rules for this modeling problem, outlining:

* the basic requirements for all models that will be evaluated.
* the requirements for model interfaces — i.e., the methods
that they are required to have and the arguments those methods are required to take.
* the metrics that must be return by the model during validation.

Example Bootcamp configuration file:

```
bootcamp:
 module: example.camp
 callable: Camp
model_requirements:
  parameters:
    - n_epochs
  methods:
    - train: [text, classes]
    - validate: [text, classes]
    - save: [path]
    - load: [path]
    - predict: [text]
  validation_metrics:
    - AUC
```

In this example, we stipulate:

* that the Bootcamp class can be imported like `from example.camp import Camp`
* that each model must include `n_epochs` as an `__init__()` argument (akaa model parameter)
* that each model must have `train()` and `validate()` methods that accept `text` and `classes` arguments,
`save()` and `load()` methods with `path` arguments, and a `predict` method accepts a `text` argument.
* that each model must return an `AUC` metric during validation.

#### Model Configuration (YAML)

Model configuration files specify the models that will be evaluated in the bootcamp.

For each model, we provide a name and two simple bits of info:

* where the model can be found
* what hyperparameters can be passed as parameters to `__init__()`, and testable variations of each

Example model configuration file:

```
models:
  linear:
    module: example.models.linear
    callable: LinearModel
    parameters:
      l1: [.1, .5, .9]
  loglinear:
    module: example.models.loglinear
    callable: LogLinearModel
    parameters:
      l2: [.1, .2, .3]
```

Here, we define two models with slightly different parameterizations.

When we run the bootcamp, we will test the `LinearModel` model with 3 `l1` parameters, and
the `LogLinearModel` with 3 `l2` parameters.

#### Bootcamp Class (Python)

Finally, the Bootcamp class provides a dynamic declaration of the bootcamp training
and validation procedure. By specifying it in code, rather than as a YAML file,
we give the experimenter complete control over the testing environment.

This class has just two required methods:

* `train(model)`: Receives an untrained model (initialized with a specific hyperparameter
variation) and trains it. Because models' methods and their arguments are validated
upon bootcamp initialization, you can be confident that models have the interface
required for testing.
* `validate(model)`: Receives a trained model, tests it in as many arbitrary ways
as you would like (or not at all), and finally returns the model's validation results.
In our example, the bootcamp trusts each model to perform its own validation
and retrieve the required metric. (If a required metric is not returned, the bootcamp
will throw an error). In other cases, the Bootcamp class itself could retrieve
the predictions from each model and validate them in some other way. As long as a dictionary
of the required metrics is returned from this method, all is well.

### Starting Bootcamp!

Once the three components of a Bootcamp are defined (see above), you can call a simple
CLI to run models through the bootcamp.

Example command:

    bootcamp --config=bootcamp.yml --models=models.yml --results=./results/

Command line arguments:

* `config`: The location of the Bootcamp YAML configuration file.
* `models`: The location of the models YAML configuration file.
* `results`: Path to a folder in which to save the results of each model test.
* `model` (optional): A single model (defined in the models configuration file) to test, as opposed to testing them all.

### Evaluating Your Results

The most important results are received right way: Each model is tested for
adherence to the requirements of the current bootcamp.

Assuming all models pass validation, each hyperparameter variation will be tested
and a JSON file containing the results of that test will be saved into the
results folder specified in the CLI.

Example results file for a single model test:

    {
        "model": "linear",
        "parameters": {
            "l1": 0.5
        },
        "metrics": {
            "AUC": 0.66
        },
        "timing": {
            "start": "2018-04-21 19:49:52",
            "end": "2018-04-21 19:49:52"
        }
    }

Each model results file is saved with a unique filename that indicates its parameterization,
e.g., `linear-l1_0.1.json`, `linear-l1_0.5.json`, and `linear-l1_0.9.json` in the current
example.
