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
    field_name = None

    def __init__(self, table_name, field_name, name=None):
        self.table_name, self.field_name, self.name = table_name, field_name, name

    def to_script(self):
        """
        Generates a Python script with the sintax to create this object
        
        @author Marinho Brandao
        @creation 2007-06-06
        """
        return "%s(%s, %s, name=%s)" %( self.__class__.__name__, self.name, self.table_name, self.field_name )

