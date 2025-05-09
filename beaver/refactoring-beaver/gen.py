# %%
from textx import metamodel_from_file
from jinja2 import Environment, FileSystemLoader
import argparse


# %%


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Pipeline generator')

    parser.add_argument('--metamodel', default='inheritance.bvr',
                        help='the file in which your pipeline is configured', type=str)
    parser.add_argument('--generated_file_name', default='generated_pipeline.py',
                        help='Destination file name', type=str)

    return parser.parse_args()


# %%
if __name__ == "__main__":

    # processors = {
    #     'Data': data_action,
    #     'Assignment': assignment_action,
    #     'Expression': expression_action,
    #     'Term': term_action,
    #     'Factor': factor_action,
    #     'Operand': operand_action,
    # }

    args = parse_command_line_arguments()

    # Load the DSL grammar
    ml_mm = metamodel_from_file('grammar/processors.tx')

    # ml_mm.register_obj_processors(processors)

    # Parse the DSL configuration file
    config = ml_mm.model_from_file(args.metamodel)

    # %%
    #Load Jinja2 template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/models.jinja')

    # flattened_dict = dict_flatten(outpout)

    generated_code = template.render(
        file=config)

    # Save the generated code to a file
    with open(args.generated_file_name, 'w') as f:
        f.write(generated_code)

    # print("Generated code saved to:", args.generated_file_name)
