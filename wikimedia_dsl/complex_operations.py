from textx import metamodel_from_str
from jinja2 import Template

# Define the grammar
grammar = """
Calc: assignments*=Assignment;

Assignment: variable=ID '=' expression=Expression ';';

Expression: operands=Term (operators=PlusOrMinus operands=Term)*;

PlusOrMinus: '+' | '-';

Term: operands=Factor (operators=MulOrDiv operands=Factor)*;

MulOrDiv: '*' | '/';

Factor: 
     (sign=PlusOrMinus)? op=Operand
    | '(' op_expr=Expression ')';

Operand: 
    | op_num=NUMBER
    | op_id=ID;
"""

# Create the metamodel
metamodel = metamodel_from_str(grammar)

# Input to parse
input_text = """
len_diff = new_length - old_length;
Celcius = (Fahrenheit - 32) * 5/9;
"""

# Parse the input
model = metamodel.model_from_str(input_text)

# Function to convert parsed expressions to Jinja-compatible strings


def expression_to_jinja(expression):
    result = ""
    for i, term in enumerate(expression.operands):
        if i > 0:
            result += f" {expression.operators[i-1]} "
        result += term_to_jinja(term)
    return result


def term_to_jinja(term):
    result = ""
    for i, factor in enumerate(term.operands):
        if i > 0:
            result += f" {term.operators[i-1]} "
        result += factor_to_jinja(factor)
    return result


def factor_to_jinja(factor):
    if hasattr(factor, 'op_expr'):  # Parenthesized expression
        return f"({expression_to_jinja(factor.op_expr)})"
    else:  # Operand
        op = factor.op
        if hasattr(op, 'op_num'):  # Number
            return str(op.op_num)
        else:  # Variable
            return f"sdf['{op.op_id}']"


# Prepare data for Jinja
assignments = []
for assignment in model.assignments:
    target = assignment.variable
    expression = expression_to_jinja(assignment.expression)
    assignments.append({"target": target, "expression": expression})

# Jinja template
template_str = """
{% for assignment in assignments %}
sdf['{{ assignment.target }}'] = {{ assignment.expression }};
{% endfor %}
"""
template = Template(template_str)

# Render the template
output = template.render(assignments=assignments)

# Output the result
print(output)
