

__all__ = ["data_action",
           "assignment_action", "expression_action", "term_action",
           "factor_action", "operand_action", "flatten_nested_list", "outpout", "dict_flatten"]


outpout = {}


def data_action(data):

    if len(data.features) > 0:
        outpout[data.name] = data.features[0].assignments


def assignment_action(assignment):
    functionvar = []
    functionvar.append(assignment.variable)
    functionvar.append('=')
    functionvar.append(assignment.expression)
    functionvar.append(';')
    return functionvar


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


def dict_flatten(dict_list: dict):
    result_dict = {}
    for key, item in dict_list.items():

        result_dict[key] = flatten_nested_list(item)
    return result_dict


def flatten_nested_list(nested_list, depth=0):
    result = []
    for item in nested_list:
        if isinstance(item, list):  # If the item is a list, recursively flatten it
            if depth >= 3:  # Add parentheses only if depth is greater than 3
                result.append('(')  # Add opening parenthesis
            result.extend(flatten_nested_list(
                item, depth + 1))  # Increase depth
            if depth >= 3:  # Add closing parenthesis only if depth is greater than 3
                result.append(')')
        else:  # If the item is not a list, add it directly
            result.append(item)

    return result
