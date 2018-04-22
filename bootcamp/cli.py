import argparse
from bootcamp.bootcamp import Bootcamp

# parse arguments from CLI
parser = argparse.ArgumentParser()
parser.add_argument("--config", required=True)
parser.add_argument("--models", required=True)
parser.add_argument("--results", required=True)
parser.add_argument("--model")
_args = parser.parse_args()


def main(args=None):
    args = _args if not args else args

    # initialize the Bootcamp
    selected_models = [args.model] if args.model else None
    camp = Bootcamp(config_path=args.config,
                    model_config_path=args.models,
                    results_path=args.results,
                    models=selected_models)

    # train, test, and validate each model
    camp.train_test_validate()


if __name__ == "__main__":
    main()
