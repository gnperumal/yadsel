"""
** not yet documented **
@author Marinho Brandao
@creation 2007-06-01
"""

from yadsel.core import *

AUTO_CONNECT_COMMANDS = [
        'CreateTable',
        'AlterTable',
        'DropTable',
        'CreateIndex',
        'DropIndex',
        'Insert',
        'Update',
        'Delete',
        'ExecuteSQL',
        ]

class GenericFieldParser(object):
    field = None

    def __init__(self, obj):
        self.field = obj

    def for_create(self):
        fcls = self.field.__class__

        if not issubclass(fcls, FieldType):
            return ""

        ret = self.field.name

        if fcls == Varchar:
            ret += " VARCHAR(%d) " % self.field.length
        elif fcls == Char:
            ret += " CHAR(%d) " % self.field.length
        elif fcls == Boolean:
            ret += " TINYINT "
        elif fcls == Decimal or fcls == Numeric:
            ret += " DECIMAL(%d,%d) " % ( self.field.length, self.field.digits )
        else:
            ret += " %s " % fcls.__name__.upper()

        if self.field.required:
            ret += " NOT NULL "

        if not self.field.default is None:
            if fcls in [Varchar, Char, Date, Time, DateTime, Timestamp, Text]:
                ret += " DEFAULT '%s' " % self.field.default
            else:
                ret += " DEFAULT %s " % self.field.default

        if self.field.references and self.field.references.__class__ == ForeignKey:
            ret += " REFERENCES '%s' ('%s') " %( self.field.references.table_name, self.field.references.field_name )

        if self.field.primary_key:
            ret += " PRIMARY KEY "

        return ret

    def for_alter(self):
        return self.for_create()

    def for_rename(self):
        return self.for_create()

class GenericActionParser(object):
    action = None
    class FieldParser: pass

    def __init__(self, obj, field_parser_class=None):
        self.action = obj
        self.FieldParser = field_parser_class or self.FieldParser

    def for_alter(self):
        acls = self.action.__class__

        if acls == Add:
            return "ADD " + self.FieldParser(self.action.object).for_alter()
        elif acls == AlterColumn:
            return "ALTER COLUMN %s" % self.FieldParser(self.action.object).for_alter()
        elif acls == DropColumn:
            return "DROP COLUMN %s" % self.action.name
        elif acls == RenameColumn:
            return "CHANGE COLUMN %s %s" %( self.action.name, self.FieldParser(self.action.object).for_rename() )

class GenericValueParser(object):
    key = None
    value = None

    def __init__(self, key, value):
        self.key, self.value = key, value

    def for_insert(self):
        return "'%s'" % str(self.value)

class GenericClauseParser(object):
    object = None

    def __init__(self, obj):
        self.object = obj

    def parse_clause(self):
        for c in self.object.clauses:
            return self.__class__(c).for_parser()

    def parse_expression(self):
        value1 = self.object.value1
        oper = parseutils.translate_operation(self.object.operation)
        value2 = "\"" + self.object.value2 + "\""

        return " %s %s %s " %( value1, oper, value2 )

    def for_parser(self):
        if issubclass(self.object.__class__, Clause):
            return self.parse_clause()
        elif isinstance(self.object, Expression):
            return self.parse_expression()
        else:
            return ""

    def for_select(self):
        return self.for_parser()

    def for_update(self):
        return self.for_parser()

    def for_delete(self):
        return self.for_parser()

class GenericDriver(Driver):
    auto_connect_commands = AUTO_CONNECT_COMMANDS
    class FieldParser(GenericFieldParser): pass
    class ActionParser(GenericActionParser): pass
    class ValueParser(GenericValueParser): pass
    class ClauseParser(GenericClauseParser): pass

    def __init__(self, connection=None):
        super(GenericDriver, self).__init__(connection)

    def generate_script(self, command):
        class_name = command.__class__.__name__

        if class_name in self.auto_connect_commands:
            f_name = 'generate_script_for_%s' % class_name.lower()

            if hasattr(self, f_name): # verify if func is_calleble ?
                func = getattr(self, f_name)
                return func(command)
            else:
                return ''

    def __replace_macros(self, script, obj):
        ret = script
        
        ret = ret.replace('%TABLE_NAME%', obj.table_name)

        return ret

    def generate_script_for_createtable(self, obj):
        children = ''

        # Fields parsing
        for f in obj.fields:
            inst = self.FieldParser(f)
            children += inst.for_create() + ", "
            self.additional_scripts += [self.__replace_macros(s, obj) for s in inst.additional_scripts]

        # Constraints parsing
        for c in obj.constraints:
            inst = self.ConstraintParser(c)
            self.additional_scripts += [self.__replace_macros(inst.for_create(), obj)]

        children = children[:-2]
        return 'CREATE TABLE %s ( %s )%s' % ( obj.table_name, children, self.terminate_delimiter )

    def generate_script_for_altertable(self, obj):
        children = []

        for a in obj.actions:
            children.append("ALTER TABLE %s %s %s " % ( obj.table_name, self.ActionParser(a, self.FieldParser).for_alter() ), self.terminate_delimiter )

        return children

    def generate_script_for_droptable(self, obj):
        return 'DROP TABLE %s %s' %( obj.table_name, self.terminate_delimiter )

    def generate_script_for_createindex(self, obj):
        return 'CREATE INDEX %s ON %s ( %s )%s' %( obj.index_name, obj.table_name, ''.join([c+", " for c in obj.columns])[:-2], self.terminate_delimiter )

    def generate_script_for_dropindex(self, obj):
        return 'DROP INDEX %s ON %s %s' %( obj.index_name, obj.table_name, self.terminate_delimiter )

    def generate_script_for_insert(self, obj):
        from types import TupleType, DictType

        fields = ''.join([f+", " for f in obj.fields])[:-2]

        ins = 'INSERT INTO %s ( %s ) ' % ( obj.table_name, fields )
        ret = ''

        if obj.select:
            ret = ins + self.generate_script_for_select(obj.select)
        else:
            for item in obj.values:
                if type(item) == TupleType:
                    values = ''.join([self.ValueParser(obj.fields[k], item[k]).for_insert()+", " for k in range(len(item))])[:-2]
                elif type(item) == DictType:
                    values = ''.join([self.ValueParser(k, item[k]).for_insert()+", " for k in item])[:-2]
                ret += '%s VALUES ( %s )%s' %( ins, values, self.terminate_delimiter )

        return ret
        
    def generate_script_for_select(self, obj):
        # Fields
        fields = ''.join([f+", " for f in obj.fields])[:-2]

        # Where
        if obj.where:
            where = " WHERE " + self.ClauseParser(obj.where).for_select()
        else:
            where = ""

        ret = 'SELECT %s FROM %s %s' %( fields, obj.table_name, where )

        return ret

    def generate_script_for_executesql(self, obj):
        return obj.sql + obj.terminator

