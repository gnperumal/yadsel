"""
** not yet documented **
@author Marinho Brandao
@creation 2007-06-01
"""

from datetime import datetime

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
    additional_scripts = []

    def __init__(self, obj):
        self.field = obj

    def for_create(self):
        fcls = self.field.__class__

        if not issubclass(fcls, FieldType) and not issubclass(fcls, Constraint):
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
        elif fcls == ForeignKey:
            ret = " CONSTRAINT %s FOREIGN KEY ( %s ) REFERENCES %s ( %s ) " %(
                        self.field.name,
                        ''.join(["%s," % f for f in self.field.fields])[:-1],
                        self.field.table_name,
                        ''.join(["%s," % f for f in self.field.foreign_fields])[:-1],
                        )
        else:
            ret += " %s " % fcls.__name__.upper()

        if issubclass(fcls, FieldType):
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
        #ocls = self.action.object.__class__

        if acls == Add:
            return "ADD " + self.FieldParser(self.action.object).for_alter()
        elif acls == AlterColumn:
            return "ALTER COLUMN %s" % self.FieldParser(self.action.object).for_alter()
        elif acls == DropColumn:
            return "DROP %s" % self.action.name
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
        ret = []

        for c in self.object.clauses:
            ret.append(self.__class__(c).for_parser())

        if self.object.__class__ == Or:
            ret = '(%s)' % ' or '.join(ret)
        elif self.object.__class__ == Not:
            ret = 'not (%s)' % ' and '.join(ret)
        elif self.object.__class__ == And:
            ret = '(%s)' % ' and '.join(ret)
        else:
            ret = ' and '.join(ret)

        return ret.strip()

    def parse_expression(self):
        value1 = self.object.value1
        oper = parseutils.translate_operation(self.object.operation)
        value2 = "'%s'" % self.object.value2

        return "%s %s %s" %( value1, oper, value2 )

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

class GenericSetParser(object):
    set = None

    def __init__(self, set):
        self.set = set

    def for_update(self):
        ret = []

        for field_name in self.set.values:
            ret.append("%s = '%s'" %( field_name, self.set.values[field_name] ) )

        return ','.join(ret)


class GenericHistoryControl(object):
    connection = None
    table_name = 'yadsel_history'

    sql_createtable = """
        CREATE TABLE %(t)s (
            version_number INTEGER NOT NULL,
            change_date DATETIME NOT NULL,
            errors INTEGER DEFAULT 0
        );
    """

    sql_createpk = """
        ALTER TABLE %(t)s 
            ADD CONSTRAINT pk_%(t)s
            PRIMARY KEY ( version_number, change_date );
    """

    sql_droptable = """
        DROP TABLE %s;
    """

    sql_registerversion = """
        INSERT INTO %s
         (version_number, change_date, errors)
        VALUES
        ('%s', '%s', %d)
    """

    # 'O': Finished OK, 'E': Finished with Errors
    sql_createerrorsfield = """
        ALTER TABLE %(t)s ADD errors INTEGER DEFAULT 0;
    """

    def __init__(self, connection):
        self.connection = connection or self.connection

    def prepare_database_elements(self):
        sql1 = self.sql_createtable %{ 't': self.table_name }
        sql2 = self.sql_createpk %{ 't': self.table_name }

        cur = self.connection.cursor()
            
        try:
            cur.execute(sql1)
            self.connection.commit()
            
            cur.execute(sql2)
            self.connection.commit()
        except Exception, e:
            # Return 'False' if some error did (like "table already exists")
            return False
        
        return True

    def clear_database_elements(self):
        sql = self.sql_droptable %( self.table_name )

        cur = self.connection.cursor()

        try:
            res = cur.execute(sql)
            self.connection.commit()
        except:
            # Return 'False' if some error occurred
            return False

        return True

    def register_version(self, version_number, change_date=None, errors=0):
        # Determines date/time of version change by default (now)
        change_date = change_date or datetime.now()

        sql = self.sql_registerversion %( self.table_name, version_number, change_date.isoformat(' ')[:19], errors )

        cur = self.connection.cursor()

        def execute(sql):
            cur.execute(sql)
            self.connection.commit()

            #cur.execute('select * from %s' % self.table_name)

        try:
            execute(sql)
        except Exception, e:
            if e.__class__.__name__ == 'ProgrammingError':
                try:
                    # Creates the errors field if does not exists
                    execute(self.sql_createerrorsfield %{'t': self.table_name})

                    # Try again...
                    execute(sql)
                except:
                    return False
            else:
                return False

        return True

    def get_latest_version(self):
        ret = {
            'version_number': None,
            'change_date': None,
            }

        sql = """
            SELECT version_number, change_date
            FROM %s
            ORDER BY change_date DESC
        """ %( self.table_name )

        cur = self.connection.cursor()

        try:
            cur.execute(sql)

            latest = cur.fetchone()

            if latest:
                ret['version_number'], ret['change_date'] = latest
        except Exception, e:
            return None

        return ret


class GenericLogControl(object):
    connection = None
    table_name = 'yadsel_log'

    sql_createtable = """
        CREATE TABLE %(t)s (
            id INTEGER NOT NULL,
            version_number INTEGER NOT NULL,
            log_date DATETIME NOT NULL,
            msg TEXT
        );
    """

    sql_createpk = """
        ALTER TABLE %(t)s 
            ADD CONSTRAINT pk_%(t)s
            PRIMARY KEY ( id );
    """

    sql_droptable = """
        DROP TABLE %s;
    """

    sql_registerlog = """
        INSERT INTO %(t)s
         (id, version_number, log_date, msg)
        VALUES
         ((select case when max(id) is null then 0 else max(id) end + 1 
           from %(t)s), '%(v)s', '%(d)s', '%(m)s')
    """

    def __init__(self, connection):
        self.connection = connection or self.connection

    def prepare_database_elements(self):
        sql1 = self.sql_createtable %{ 't': self.table_name }
        sql2 = self.sql_createpk %{ 't': self.table_name }

        cur = self.connection.cursor()

        try:
            cur.execute(sql1)
            self.connection.commit()
            
            cur.execute(sql2)
            self.connection.commit()
        except Exception, e:
            # Return 'False' if some error did (like "table already exists")
            return False
        
        return True

    def clear_database_elements(self):
        sql = self.sql_droptable %( self.table_name )

        cur = self.connection.cursor()

        try:
            res = cur.execute(sql)
            self.connection.commit()
        except:
            # Return 'False' if some error occurred
            return False

        return True

    def register_log(self, version_number, msg, log_date=None):
        # Determines date/time of version change by default (now)
        log_date = log_date or datetime.now()

        # Remove invalid tokens
        msg = msg.replace('"', "__").replace("'", "__")

        sql = self.sql_registerlog %{ 
                't': self.table_name,
                'v': version_number,
                'd': log_date.isoformat(' ')[:19],
                'm': msg,
                }

        cur = self.connection.cursor()

        try:
            cur.execute(sql)
            self.connection.commit()
        except Exception, e:
            #print sql, "\n\n"
            print sql, "\n"
            raise e
            # Return 'False' if some error occurred
            return False

        return True


class GenericConstraintParser(object):
    constraint = None

    def __init__(self, obj):
        self.constraint = obj

    def get_fields(self):
        ret = ''.join([",%s" % f for f in self.constraint.fields])
        return ret[1:]

    def get_foreign_fields(self):
        ret = ''.join([",%s" % f for f in self.constraint.foreign_fields])
        return ret[1:]

    def for_create(self):
        fcls = self.constraint.__class__

        if issubclass(fcls, ForeignKey):
            ret = 'ALTER TABLE %%TABLE_NAME%% \
                    ADD CONSTRAINT %s \
                    FOREIGN KEY (%s) \
                    REFERENCES %s (%s);' %( self.constraint.name, 
                                            self.get_fields(),
                                            self.constraint.table_name, 
                                            self.get_foreign_fields() )
        else:
            ret = ''

        return ret

    def for_alter(self):
        return self.for_create()

    def for_rename(self):
        return self.for_create()


class GenericDriver(Driver):
    auto_connect_commands = AUTO_CONNECT_COMMANDS
    
    class FieldParser(GenericFieldParser): pass
    class ActionParser(GenericActionParser): pass
    class ValueParser(GenericValueParser): pass
    class ClauseParser(GenericClauseParser): pass
    class ConstraintParser(GenericConstraintParser): pass
    class SetParser(GenericSetParser): pass
    class HistoryControl(GenericHistoryControl): pass
    class LogControl(GenericLogControl): pass

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
            children.append("ALTER TABLE %s %s %s " %( obj.table_name, self.ActionParser(a, self.FieldParser).for_alter(), self.terminate_delimiter ))

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
        ret = []

        if obj.select:
            ret = ins + self.generate_script_for_select(obj.select)
        else:
            for item in obj.values:
                if type(item) == TupleType:
                    values = ''.join([self.ValueParser(obj.fields[k], item[k]).for_insert()+", " for k in range(len(item))])[:-2]
                elif type(item) == DictType:
                    values = ''.join([self.ValueParser(k, item[k]).for_insert()+", " for k in item])[:-2]
                ret += ['%s VALUES ( %s )' %( ins, values )]

        return ret

    def generate_script_for_update(self, obj):
        # Set
        set = self.SetParser(obj.set).for_update()

        # Where
        where = obj.where and " WHERE " + self.ClauseParser(obj.where).for_update() or ""

        ret = 'UPDATE %s SET %s %s' %( obj.table_name, set, where )

        return ret

    def generate_script_for_delete(self, obj):
        # Where
        where = obj.where and " WHERE " + self.ClauseParser(obj.where).for_delete() or ""

        ret = 'DELETE FROM %s %s' %( obj.table_name, where )

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

