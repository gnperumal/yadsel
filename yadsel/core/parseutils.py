"""
** not yet documented **
@author Marinho Brandao
@creation 2007-06-01
"""

def translate_operation(oper):
    """
    Translate human friendly operations to Standard SQL operators
    @author Marinho Brandao
    @creation 2007-06-01
    """
    if oper == 'notequal':
        return "<>"
    elif oper == 'lt':
        return "<"
    elif oper == 'lte':
        return "<="
    elif oper == 'gt':
        return ">"
    elif oper == 'gte':
        return ">="
    else:
        return oper

def find_field(fields_list, field_name):
    """
    Find a field in the fields_list by its name and returns it
    @author Marinho Brandao
    @creation 2007-06-01
    """
    ret = [f for f in fields_list if f.name == field_name]
    return ret and ret[0] or None

