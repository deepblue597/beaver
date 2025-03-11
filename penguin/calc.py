"""
This is a variant of calc example using object processors for on-the-fly
evaluation.
"""
from textx import metamodel_from_str
from jinja2 import Template

grammar = '''
Calc: assignments*=Assignment ;
Assignment: variable=ID '=' expression=Expression ';';
Expression: operands=Term (operators=PlusOrMinus operands=Term)*;
PlusOrMinus: '+' | '-';
Term: operands=Factor (operators=MulOrDiv operands=Factor)*;
MulOrDiv: '*' | '/' ;
Factor: (sign=PlusOrMinus)?  op=Operand;
Operand: op_num=NUMBER | op_id=ID | ('(' op_expr=Expression ')');
'''


def assignment_action(assignment):
    print('Assignment:', assignment.variable)
    tester.append(assignment.variable)
    tester.append('=')
    tester.append(assignment.expression)
    tester.append(';')
    print(assignment.expression)
    # for operand in assignment.expression:
    #     tester.append(operand)


tester = []


def expression_action(expression):

    ret = [expression.operands[0]]

    for operator, operand in zip(expression.operators,
                                 expression.operands[1:]):
        ret.append(operator)
        ret.append(operand)

    return ret


def term_action(term):
    ret = [term.operands[0]]

    for operator, operand in zip(term.operators,
                                 term.operands[1:]):

        ret.append(operator)
        ret.append(operand)

    return ret


def factor_action(factor):
    value = factor.op
    return -value if factor.sign == '-' else value


def operand_action(operand):
    print(operand.op_num)
    if operand.op_num is not None and operand.op_num != 0:
        return operand.op_num
    elif operand.op_id:
        print(operand.op_id)
        return operand.op_id

    else:

        return operand.op_expr


def flatten_nested_list(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):  # If the item is a list, recursively flatten it
            result.append('(')  # Add opening parenthesis
            result.extend(flatten_nested_list(item))  # Flatten the nested list
            result.append(')')  # Add closing parenthesis
        else:  # If the item is not a list, add it directly
            result.append(item)
    return result


def main(debug=False):

    processors = {
        # 'Calc': calc_action,
        'Assignment': assignment_action,
        'Expression': expression_action,
        'Term': term_action,
        'Factor': factor_action,
        'Operand': operand_action,
        # 'Final': final_action
    }

    calc_mm = metamodel_from_str(grammar, auto_init_attributes=False,
                                 debug=debug)
    calc_mm.register_obj_processors(processors)

    input_expr = '''
        
        len_diff = 2 * new_len + 17;
        c = a + (2 * b +3) ;
    '''
    template_str = """
{% for assignment in assignments %}{{assignment}}{% endfor %}
        """
    calc = calc_mm.model_from_str(input_expr)

    flattened_list = flatten_nested_list(tester)

    output = []
    for item in flattened_list:
        if item == '(' or item == ')':
            output.append(item)
        elif type(item) == int:
            output.append(item)
        elif item == '+' or item == '-' or item == '*' or item == '/' or item == '=':
            output.append(item)
        else:
            output.append(f'sdf["{item}"]')
    print(output)

    template = Template(template_str)

    # Render the template
    output2 = template.render(assignments=output)

    # Output the result
    print(output2)

    # Save the generated code to a file
    with open('calc_result.py', 'w') as f:
        f.write(output2)

    print("Generated code saved to:", 'calc_result.py')


if __name__ == '__main__':
    main()
