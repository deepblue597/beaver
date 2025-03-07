# %%
from textx import metamodel_from_file
from jinja2 import Environment, FileSystemLoader
import argparse

# %%


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Pipeline generator')

    parser.add_argument('--metamodel', default='general.jsl',
                        help='metamodel text', type=str)
    parser.add_argument('--generated_file_name', default='generated_pipeline.py',
                        help='Destination file name', type=str)

    return parser.parse_args()


# %%
if __name__ == "__main__":

    args = parse_command_line_arguments()

    # Load the DSL grammar
    ml_mm = metamodel_from_file('jsl.tx')

    # Parse the DSL configuration file
    config = ml_mm.model_from_file(args.metamodel)

    # Access parsed data
    print(f"Pipeline Name: {config.name}")
    print(f"Kafka Broker: {config.kafka.broker}")
    print(f"Model Type: {config.model.name}")
    print(f"Features: {config.features.features}")
    print(f"Target: {config.target.name}")

    # %%
    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('python.template')

    # Render template with parsed configuration
    generated_code = template.render(pipeline=config)

    # Save the generated code to a file
    with open(args.generated_file_name, 'w') as f:
        f.write(generated_code)

    print("Generated code saved to:", args.generated_file_name)

# %%
