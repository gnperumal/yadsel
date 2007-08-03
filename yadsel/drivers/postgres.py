"""
** not yet documented **
@author Marinho Brandao
@creation 2007-08-02
"""

import re

from yadsel.core import *
from generic import GenericDriver, GenericHistoryControl

class PostgresInspector(SchemaInspector):
    def get_tables_list(self):
        cur = self.connection.cursor()
        cur.execute("\
                select relname as table_name \
                from pg_class \
                where relkind = 'r' \
                  and relname not like 'pg_%' \
                  and relname not like 'sql_%' \
                ")

        result = cur.fetchallmap()
        
        return [r['table_name'].strip() for r in result]

    def get_fields_list(self, table_name):
        ret = []

        cur = self.connection.cursor()
        cur.execute("\
                select \
                 c.relname, \
                 a.attname as field_name, \
                 a.atthasdef as has_default, \
                 a.attnotnull as required, \
                 d.adsrc as default_source, \
                 case when t.typname = 'varchar' then a.atttypmod - 4 \
                      when t.typname = 'numeric' then a.atttypmod / 65536 \
                      else a.attlen end as field_length, \
                 case when t.typname = 'numeric' then a.atttypmod - (a.atttypmod / 65536) * 65536 - 4 \
                      else 0 end as scale, \
                 a.atttypid as type_code, \
                 t.typname as type_name \
                from pg_attribute a join pg_class c on a.attrelid = c.oid \
                                    join pg_type t on a.atttypid = t.oid \
                               left join pg_attrdef d on a.attrelid = d.adrelid \
                                                     and a.attnum = d.adnum \
                where c.relkind = 'r' \
                  and a.attnum > 0 \
                  and c.relname = '%s' \
                order by c.relname, a.attnum \
                " % table_name)

        # IMPLEMENTED UNTIL HERE (2007-08-02)

        result = cur.fetchallmap()
        
        for r in result:
            """
            to be implemented...
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

class PostgresFieldParser(object):
    field = None
    additional_scripts = []

    def __init__(self, obj):
        self.field = obj
        self.additional_scripts = []

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
        elif fcls == Text:
            if hasattr(self.field, 'segment_size'):
                segment_size = self.field.segment_size or 4096
            else:
                segment_size = 4096
            
            ret += " BLOB SUB_TYPE 2 SEGMENT SIZE %d " % segment_size
        elif fcls == Blob:
            if hasattr(self.field, 'segment_size'):
                segment_size = self.field.segment_size or 4096
            else:
                segment_size = 4096
            
            ret += " BLOB SUB_TYPE 1 SEGMENT SIZE %d " % segment_size
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
            if not self.field.default is None:
                if fcls in [Varchar, Char, Date, Time, DateTime, Timestamp, Text] and self.field.default.lower() not in ['current_date', 'current_time', 'current_datetime']:
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

class PostgresConstraintParser(object):
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

class PostgresHistoryControl(GenericHistoryControl):
    sql_createtable = """
        CREATE TABLE %(t)s (
            version_number INTEGER NOT NULL,
            change_date TIMESTAMP NOT NULL
        );
    """

class PostgresDriver(GenericDriver):
    class Inspector(PostgresInspector): pass
    class FieldParser(PostgresFieldParser): pass
    class ConstraintParser(PostgresConstraintParser): pass
    class HistoryControl(PostgresHistoryControl): pass

    def __init__(self, connection=None):
        super(PostgresDriver, self).__init__(connection)

    def execute_command(self, command):
        """
        This method haves a dependency of KInterbasDB extension package, available at:
        http://kinterbasdb.sourceforge.net/
        """
        super(PostgresDriver, self).execute_command(command)

        if self.connection:
            cur = self.connection.cursor()
            result = cur.execute(command)

            # Verify this ****
            self.connection.commit()

            return result
        else:
            return command

    def generate_script_for_executesql(self, obj):
        return obj.sql

