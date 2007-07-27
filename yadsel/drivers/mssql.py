"""
** not yet documented **
@author Marinho Brandao
@creation 2007-06-11
"""

import re

from yadsel.core import *
from generic import GenericDriver

class MSSQLInspector(SchemaInspector):
    def get_tables_list(self):
        cur = self.connection.cursor()
        cur.execute("\
                SELECT rdb$relation_name as table_name \
                FROM rdb$relations \
                WHERE rdb$system_flag = 0 \
                ")

        result = cur.fetchallmap()
        
        return [r['table_name'].strip() for r in result]

    def get_fields_list(self, table_name):
        ret = []

        cur = self.connection.cursor()
        cur.execute("\
                SELECT \
                 RF.rdb$field_name as field_name, \
                 RF.rdb$default_source as default_source, \
                 F.rdb$field_length as field_length, \
                 F.rdb$field_scale as scale, \
                 F.rdb$field_type as type_code, \
                 T.rdb$type_name as type_name, \
                 RF.rdb$null_flag as required \
                FROM rdb$relation_fields RF \
                JOIN rdb$fields F ON RF.rdb$field_source = F.rdb$field_name \
                JOIN rdb$types T ON F.rdb$field_type = T.rdb$type \
                                AND T.rdb$field_name = 'RDB$FIELD_TYPE' \
                WHERE RF.rdb$relation_name = '%s' \
                ORDER BY RF.rdb$field_id\
                " % table_name)

        result = cur.fetchallmap()
        
        for r in result:
            """
            missing: QUAD, CSTRING, BLOB_ID
            """
            ft = r['type_name'].strip()
            field_name = r['field_name'].strip()

            if ft == 'VARYING':
                col = Varchar(r['field_length'])
            elif ft == 'TEXT':
                col = Char(r['field_length'])
            elif ft == 'LONG':
                col = Integer()
            elif ft == 'DATE':
                col = Date()
            elif ft in ['INT64']:
                col = Decimal(r['field_length'], r['scale'] * -1)
            elif ft == 'SHORT':
                col = SmallInt()
            elif ft == 'TIME':
                col = Time()
            elif ft == 'TIMESTAMP':
                col = Timestamp()
            elif ft == 'FLOAT':
                col = Float()
            elif ft == 'DOUBLE': # to be verified
                col = Float()
            elif ft == 'BLOB':
                col = Text()
            else:
                print "Field type not identified: %s %s" %( r[1], r[2] )
                continue

            col.name = field_name
            col.required = r['required'] == 1

            # Takes the default value
            if r['default_source']:
                reg = re.compile("^(DEFAULT [']{0,1})([^']*).*", re.IGNORECASE)
                m = reg.match(r['default_source'].strip())
                col.default = `m.group(2)`
            
            ret.append(col)

        # Takes primary key information from RDB$INDEX_SEGMENTS and RDB$RELATION_CONSTRAINTS tables
        cur.execute("\
                SELECT I.rdb$field_name as field_name \
                FROM rdb$index_segments I \
                JOIN rdb$relation_constraints RC ON I.rdb$index_name = RC.rdb$index_name \
                WHERE RC.rdb$relation_name = '%s' \
                  AND RC.rdb$constraint_type = 'PRIMARY KEY' \
                " % table_name)
        for f in cur.fetchallmap():
            parseutils.find_field(ret, f['field_name'].strip()).primary_key = True

        return ret

    def get_constraints_list(self, table_name):
        ret = []

        cur = self.connection.cursor()
        cur.execute("\
                SELECT \
                 I.rdb$field_name as field_name, \
                 RC.rdb$constraint_name as constraint_name, \
                 PK.rdb$relation_name as foreign_table \
                FROM rdb$index_segments I \
                JOIN rdb$relation_constraints RC ON I.rdb$index_name = RC.rdb$index_name \
                JOIN rdb$ref_constraints RF ON RC.rdb$constraint_name = RF.rdb$constraint_name \
                JOIN rdb$relation_constraints PK ON RF.rdb$const_name_uq = PK.rdb$constraint_name \
                WHERE RC.rdb$relation_name = '%s' \
                  AND RC.rdb$constraint_type = 'FOREIGN KEY' \
                " % table_name)
        
        for f in cur.fetchallmap():
            ret.append( ForeignKey(f['field_name'].strip(), f['foreign_table'].strip(), 'GUID', f['constraint_name'].strip()) )

        return ret

    def get_indexes_list(self, table_name):
        return []
        #result = self.connection.cursor().execute('PRAGMA index_list(%s)' % table_name)

        #return [r[1] for r in result.fetchall()]

    def get_index_info(self, index_name):
        return None
        #result = self.connection.cursor().execute('PRAGMA index_info(%s)' % index_name)

        #return [r[2] for r in result.fetchall()]

    def get_domains_list(self):
        return []

class MSSQLFieldParser(object):
    field = None
    additional_scripts = []

    def __init__(self, obj):
        self.field = obj
        self.additional_scripts = []

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
        elif fcls == Text:
            ret += " TEXT " #% self.field.length
        elif fcls == Blob:
            ret += " BLOB " #% self.field.length
        elif fcls == Date:
            ret += " DATETIME "
        else:
            ret += " %s " % fcls.__name__.upper()

        if not self.field.default is None:
            if fcls in [Varchar, Char, Date, Time, DateTime, Timestamp, Text]:
                ret += " DEFAULT '%s' " % self.field.default
            else:
                ret += " DEFAULT %s " % self.field.default

        if self.field.required:
            ret += " NOT NULL "

        #if self.field.references and self.field.references.__class__ == ForeignKey:
        #    ret += " REFERENCES '%s' ('%s') " %( self.field.references.table_name, self.field.references.field_name )

        if self.field.primary_key:
            sql = 'ALTER TABLE %%TABLE_NAME%% \
                    ADD CONSTRAINT PK_%%TABLE_NAME%% \
                    PRIMARY KEY (%s);' % self.field.name
            self.additional_scripts += [sql]

        return ret

    def for_alter(self):
        return self.for_create()

    def for_rename(self):
        return self.for_create()

class MSSQLConstraintParser(object):
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

class MSSQLDriver(GenericDriver):
    class Inspector(MSSQLInspector): pass
    class FieldParser(MSSQLFieldParser): pass
    class ConstraintParser(MSSQLConstraintParser): pass

    def __init__(self, connection=None):
        super(MSSQLDriver, self).__init__(connection)

    def execute_command(self, command):
        """
        This method haves a dependency of KInterbasDB extension package, available at:
        http://kinterbasdb.sourceforge.net/
        """
        super(MSSQLDriver, self).execute_command(command)

        if self.connection:
            cur = self.connection.cursor()
            result = cur.execute(command)

            # Verify this ****
            self.connection.commit()

            return result
        else:
            return command

    def generate_script_for_executesql(self, obj):
        if obj.terminator != ';':
            ret  = "SET TERM %s ;\n" % obj.terminator
            ret += "%s%s\n" %( obj.sql, obj.terminator )
            ret += "SET TERM ; %s\n" % obj.terminator
        else:
            ret = obj.sql + obj.terminator

        return ret

