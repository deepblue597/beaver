"""
This is a variant of calc example using object processors for on-the-fly
evaluation.
"""
from textx import metamodel_from_str

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

# Global variable namespace
namespace = {}
tester = []


def assignment_action(assignment):
    result = f"sdf['{assignment.variable}'] = "
    result += ''.join(expression_action(assignment.expression))
    print(result)
    tester.append(result)


def expression_action(expression):
    ret = [operand_action(expression.operands[0])]
    for operator, operand in zip(expression.operators, expression.operands[1:]):
        ret.append(operator)
        ret.append(operand_action(operand))
    return ret


def term_action(term):
    ret = [operand_action(term.operands[0])]
    for operator, operand in zip(term.operators, term.operands[1:]):
        ret.append(operator)
        ret.append(operand_action(operand))
    return ret


def factor_action(factor):
    value = operand_action(factor.op)
    return f"-{value}" if factor.sign == '-' else value


def operand_action(operand):
    if isinstance(operand, str):
        return operand
    if operand.op_num is not None:
        return str(operand.op_num)
    elif operand.op_id:
        return f"sdf['{operand.op_id}']"
    else:
        return f"({''.join(expression_action(operand.op_expr))})"


def main(debug=False):
    processors = {
        'Assignment': assignment_action,
        'Expression': expression_action,
        'Term': term_action,
        'Factor': factor_action,
        'Operand': operand_action,
    }

    calc_mm = metamodel_from_str(
        grammar, auto_init_attributes=False, debug=debug)
    calc_mm.register_obj_processors(processors)

    input_expr = '''
        b = 2 * a + 17;
        c = a + (2 * b + 3);
    '''

    calc = calc_mm.model_from_str(input_expr)
    results = calc.assignments

    flattened_list = flatten_nested_list(tester)
    print(flattened_list)


if __name__ == '__main__':
    main()
