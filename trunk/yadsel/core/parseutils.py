"""
** not yet documented **
@author Marinho Brandao
@creation 2007-06-01
"""

def translate_operation(oper):
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


