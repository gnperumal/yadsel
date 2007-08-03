"""
** not yet documented **
@author Marinho Brandao
@creation 2007-05-24
"""

class Constraint(object):
    name = None

    def __init__(self, **kwargs):
        [setattr(self, k, kwargs[k]) for k in kwargs]

class PrimaryKey(Constraint):
    fields = []

    def __init__(self, *args):
        self.fields = args

class ForeignKey(Constraint):
    table_name = None
    fields = ()
    foreign_fields = ()

    def __init__(self, fields, table_name, foreign_fields, name=None):
        from types import TupleType, ListType
        self.table_name, self.name = table_name, name

        self.fields = type(fields) in (TupleType,ListType) and fields or (fields,)
        self.foreign_fields = type(foreign_fields) in (TupleType,ListType) and foreign_fields or (foreign_fields,)

    def to_script(self):
        """
        Generates a Python script with the sintax to create this object
        
        @author Marinho Brandao
        @creation 2007-06-06
        """
        return "%s = %s((%s), '%s', (%s))" %( self.name,
                                              self.__class__.__name__,
                                              ''.join(["'%s'," % f for f in self.fields]),
                                              self.table_name,
                                              ''.join(["'%s'," % f for f in self.foreign_fields]) )

