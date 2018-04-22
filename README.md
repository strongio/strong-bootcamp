# strong-bootcamp

A Python package that makes it easier to test and compare machine
learning models before they are deployed.

Principle: _If the model makes it through bootcamp, it's fit to be deployed._

## Installation

    git clone https://github.com/strongio/strong-bootcamp.git
    cd strong-bootcamp
    pip install .

## Usage

### Building a Bootcamp

A bootcamp defines a data problem and a model interface that will be
required to solve it.

#### YAML Configuration

See, e.g., `example/bootcamp.yml`.

#### Python Configuration

Provides training and validation subroutines.

### Building Models

Models are simple Python classes that meet the requirements of the bootcamp.

### Preparing Models for Bootcamp

Create a YAML file that specifies the models (e.g. ,`example/models.yml`).
This not only specifies the names and locations of the models, but
also specifies hyper parameters that will be passed to each model's
`__init__()` during testing.

## Usage

bootcamp --config=bootcamp.yml --models=models.yml --results=./results/