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


def assignment_action(assignment):
    # tester.append(assignment.variable)
    # print('the assignment', assignment.variable)
    namespace[assignment.variable] = assignment.expression
    tester.append('=')
    tester.append(assignment.variable)


# def calc_action(calc):
#     return calc.expression


tester = []


def expression_action(expression):

    ret = [expression.operands[0]]
    # print(ret)
    # tester.append(ret)
    print(expression.operands)
    print(expression.operators)
    for operator, operand in zip(expression.operators,
                                 expression.operands[1:]):
        ret.append(operator)
        ret.append(operand)
        # tester.append(operator)
        # tester.append(operand)
        # if operator == '+':
        #     ret += operand
        # else:
        #     ret -= operand
        pass
    # print(tester)
    tester.extend(ret)
    return ret


def final_action(expression):
    namespace[expression.variable] = expression.expression


def term_action(term):
    ret = [term.operands[0]]
    print(term.operands)
    print(term.operators)
    # tester.append(ret)
    for operator, operand in zip(term.operators,
                                 term.operands[1:]):

        ret.append(operator)
        ret.append(operand)
        # print(operator)
        # tester.append(operator)
        # print(operand)
        # tester.append(operand)
        # if operator == '*':
        #     ret *= operand
        # else:
        #     ret /= operand
        pass
    return ret


def factor_action(factor):
    value = factor.op
    return -value if factor.sign == '-' else value


def operand_action(operand):

    if operand.op_num is not None:
        # print('operand is ', operand.op_num)
        # tester.append(operand.op_num)
        return operand.op_num
    elif operand.op_id:
        # print('variable is ', operand.op_id)
        # tester.append(f'sdf[{operand.op_id}]')
        return operand.op_id
        # if operand.op_id in namespace:
        #     return namespace[operand.op_id]
        # else:
        #     raise Exception(f'Unknown variable "{operand.op_id}" '
        #                     f'at position {operand._tx_position}')
    else:

        return operand.op_expr


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
        
        b = 2 * a + 17;
        c = a + (2 * b +3) ;
    '''

    calc = calc_mm.model_from_str(input_expr)
    results = calc.assignments

    # assert (result - 6.93805555) < 0.0001
    for result in results:
        print('result is ',  result.variable)
    print(tester[::-1])
    # print(namespace)


if __name__ == '__main__':
    main()
