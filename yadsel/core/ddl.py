"""
** not yet documented **
@author Marinho Brandao
@creation 2007-05-24
"""

import actions, fieldtypes, constraints
from base import Command

# Tables

class CreateTable(Command):
    table_name = None
    fields = []
    constraints = []

    def __init__(self, table_name, *args, **kwargs):
        self.table_name = table_name
        self.fields = []
        self.constraints = []

        # Set fields by args (Ex. Integer(name='id'))
        for k in args:
            if issubclass(k.__class__, fieldtypes.FieldType):
                self.fields.append(k)
            elif issubclass(k.__class__, constraints.Constraint):
                self.constraints.append(k)

        # Set fields by dict args (Ex. id = Integer())
        for k in kwargs:
            if issubclass(kwargs[k].__class__, fieldtypes.FieldType):
                kwargs[k].name = k
                self.fields.append(kwargs[k])
            elif issubclass(kwargs[k].__class__, constraints.Constraint):
                kwargs[k].name = k
                self.constraints.append(kwargs[k])

    def to_script(self, ident_level=2, ident_space="    "):
        """
        Generates a Python script with the sintax to create this object
        
        @author Marinho Brandao
        @creation 2007-06-06
        """
        sp = ident_space * ident_level
        ret = []
        ret.append("%s('%s'," %( self.__class__.__name__, self.table_name ))
        for f in self.fields:
            ret.append("%s%s," %( ident_space, f.to_script() ))
        for c in self.constraints:
            ret.append("%s%s," %( ident_space, c.to_script() ))
        ret.append("%s).append_to(self)" % ident_space)

        return ''.join([sp + row + "\n" for row in ret])

class AlterTable(Command):
    table_name = None
    actions = None
    fields = None
    constraints = None

    def __init__(self, table_name, *args, **kwargs):
        self.table_name = table_name
        self.actions = []
        self.fields = []
        self.constraints = []

        # Parses no named args
        for k in args:
            # Change actions
            if issubclass(k.__class__, actions.Action):
                self.actions.append(k)
            # New fields
            elif issubclass(k.__class__, fieldtypes.FieldType):
                self.fields.append(k)
            # New constraints
            elif issubclass(k.__class__, constraints.Constraint):
                self.constraints.append(k)

        # Parses named args
        for k in kwargs:
            kwargs[k].name = k

            # Change actions
            if issubclass(k.__class__, actions.Action):
                self.actions.append(k)
            # New fields
            elif issubclass(kwargs[k].__class__, fieldtypes.FieldType):
                self.fields.append(kwargs[k])
            # New constraints
            elif issubclass(kwargs[k].__class__, constraints.Constraint):
                self.constraints.append(kwargs[k])

class DropTable(Command):
    table_name = None

    def __init__(self, table_name):
        self.table_name = table_name

class RenameTable(Command):
    table_name = None
    new_name = None

    def __init__(self, table_name, new_name):
        self.table_name, self.new_name = table_name, new_name

# Indexes

class CreateIndex(Command):
    index_name = None
    table_name = None
    columns = []
    type = None # [UNIQUE|FULLTEXT|SPATIAL]
    direction = None # [ASC|DESC]

    def __init__(self, index_name, on, columns, type=None, direction=None):
        self.index_name, self.table_name, self.columns = index_name, on, columns
        self.type = type or self.type
        self.direction = direction or self.direction

class DropIndex(Command):
    index_name = None
    table_name = None

    def __init__(self, index_name, on):
        self.index_name, self.table_name = index_name, on

# Domains

class CreateDomain(Command):
    """
    ** not yet documented **
    @author Marinho Brandao
    @creation 2007-06-05
    """
    domain_name = None
    field_like = None

    def __init__(self, domain_name, field_like):
        self.domain_name, self.field_like = domain_name, field_like

class DropDomain(Command):
    """
    ** not yet documented **
    @author Marinho Brandao
    @creation 2007-06-05
    """
    domain_name = None

    def __init__(self, domain_name):
        self.domain_name = domain_name

class AlterDomain(Command):
    """
    ** not yet documented **
    @author Marinho Brandao
    @creation 2007-06-05
    """
    domain_name = None
    field_like = None

    def __init__(self, domain_name, field_like):
        self.domain_name, self.field_like = domain_name, field_like

class ReplaceDomain(Command):
    """
    ** not yet documented **
    @author Marinho Brandao
    @creation 2007-06-05
    """
    domain_name = None
    new_domain_name = None

    def __init__(self, old_domain_name, new_domain_name):
        self.domain_name, self.new_domain_name = old_domain_name, new_domain_name

