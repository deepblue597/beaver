

__all__ = ["data_action",
           "assignment_action", "expression_action", "term_action",
           "factor_action", "operand_action", "flatten_nested_list","tester","name"]

tester = []
name = [] 

def data_action(data):
    name.append(data.name)


def assignment_action(assignment):

    tester.append(assignment.variable)
    tester.append('=')
    tester.append(assignment.expression)
    tester.append(';')

    # for operand in assignment.expression:
    #     tester.append(operand)


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
    if operand.op_num is not None and operand.op_num != 0:
        return operand.op_num
    elif operand.op_id:

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
