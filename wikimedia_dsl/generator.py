# %%
from textx import metamodel_from_file
from jinja2 import Environment, FileSystemLoader

# Load the DSL grammar
ml_mm = metamodel_from_file('jsl.tx')

# Parse the DSL configuration file
config = ml_mm.model_from_file('classification.jsl')

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
with open('generated_pipeline.py', 'w') as f:
    f.write(generated_code)

print("Generated code saved to 'generated_pipeline.py'")

# %%
