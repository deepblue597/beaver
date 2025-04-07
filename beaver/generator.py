# %%
from textx import metamodel_from_file, TextXSyntaxError, TextXSemanticError
from textx import metamodel_from_file
from jinja2 import Environment, FileSystemLoader
import argparse
import textx.scoping.providers as scoping_providers
from calc import assignment_action, expression_action, factor_action, flatten_nested_list, operand_action, term_action, tester

# %%


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Pipeline generator')

    parser.add_argument('--metamodel', default='general.jsl',
                        help='the file in which your pipeline is configured', type=str)
    parser.add_argument('--generated_file_name', default='generated_pipeline.py',
                        help='Destination file name', type=str)

    return parser.parse_args()


def validate_model(grammar_file, model_file):
    try:
        # Load the grammar
        ml_mm = metamodel_from_file(grammar_file)

        # Parse the model file
        config = ml_mm.model_from_file(model_file)

        print("Model is valid!")
        return config  # Return the parsed model for further use

    except TextXSyntaxError as e:
        print(f"Syntax Error: {e}")
    except TextXSemanticError as e:
        print(f"Semantic Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


# %%


if __name__ == "__main__":
    args = parse_command_line_arguments()
    # metamodel = metamodel_from_file(args.metamodel)
    # metamodel.register_scope_providers({"*.*": scoping_providers.FQN()})
    # Validate the model
    config = validate_model('beaver.tx', args.metamodel)

    if config:
        # Index 1 for the second model
        second_model = config.algorithms.model[1]

        # Access parsed data if the model is valid
        # print(f"Kafka Broker: {config.kafka.broker}")
        print(
            f"Model Type: {config.algorithms.model[1].params[1].value.value.type}")
        print(f"Model Type: {config.preproccessors}")
