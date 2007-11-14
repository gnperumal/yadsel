"""
** not yet documented **
@author Marinho Brandao
@creation 2007-05-24
"""

from base import Command

OPERATION_DELIMITER = '__' # Ex. name__like="A%"

# Fixtures

class Expression(object):
    value1 = None
    operation = None
    value2 = None

    def __init__(self, value1, operation, value2):
        self.value1, self.operation, self.value2 = value1, operation, value2

class Clause(object):
    clauses = []
    
    def __init__(self, *args, **kwargs):
        self.clauses = [c for c in args if issubclass(c.__class__, Expression) or issubclass(c.__class__, Clause)]

        for k, v in kwargs.items():
            if issubclass(v.__class__, Clause):
                self.clauses.append(v)
            else:
                if k.count(OPERATION_DELIMITER):
                    value1, oper = k.split(OPERATION_DELIMITER)
                else:
                    value1, oper = k, '='
                
                value2 = v #kwargs[k]
            
                self.clauses.append(Expression(value1, oper, value2))

class Not(Clause): pass

class And(Clause): pass

class Or(Clause): pass

class Where(Clause): pass

class Set(object):
    values = {}

    def __init__(self, **kwargs):
        self.values = kwargs

class Insert(Command):
    table_name = None
    fields = []
    values = {}
    select = None
    
    def __init__(self, table_name, *args, **values):
        from types import TupleType

        self.table_name = table_name

        if len(args) and isinstance(args[0], Select):
            self.select = args[0]
            self.fields = self.select.fields.keys()
        elif len(args) == 2 and isinstance(args[0], TupleType) and isinstance(args[1], TupleType):
            self.fields = args[0]
            self.values = args[1]
        else:
            self.fields = values.keys()
            self.values = values and (values,) or ()

class Update(Command):
    table_name = None
    set = None
    where = None
    
    def __init__(self, table_name, set, where=None):
        self.table_name = table_name
        self.set_set(set)
        self.set_where(where)

    def set_set(self, set):
        self.set = set

    def set_where(self, where):
        self.where = where

class Delete(Command):
    table_name = None
    where = None
    
    def __init__(self, table_name, where=None):
        self.table_name = table_name
        self.set_where(where)

    def set_where(self, where):
        self.where = where

class Select(Command):
    table_name = None
    fields = {}
    where = None
    
    def __init__(self, table_name, fields, where=None):
        self.table_name = table_name
        self.fields = fields
        self.set_where(where)

    def set_where(self, where):
        self.where = where

class Merge(Command):
    table_name = None
    # Not yet implemented

class ClearAllData(Command):
    pass
    # Not yet implemented

class DropAllObjects(Command):
    pass
    # Not yet implemented

class ExecuteSQL(Command):
    """This class abstract any other SQL command does not supported by the API"""
    sql = ''
    terminator = None
    
    def __init__(self, sql, terminator=';'):
        self.sql, self.terminator = sql, terminator

