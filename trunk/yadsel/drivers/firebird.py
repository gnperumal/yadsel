"""
** not yet documented **
@author Marinho Brandao
@creation 2007-06-11
"""

import re

from yadsel.core import *
from generic import GenericDriver

class FirebirdInspector(SchemaInspector):
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
            r = re.compile("^(DEFAULT [']{0,1})([^']*).*")
            m = r.match(r['default_source'].strip())
            col.default = m.group(2)

            # We need take primary key information from RDB$INDEX_SEGMENTS and RDB$RELATION_CONSTRAINTS tables select
            #col.primary_key = r[5] == 1
            
            ret.append(col)

        return ret

    def get_constraints_list(self, table_name):
        ret = []

        #result = self.connection.cursor().execute('PRAGMA foreign_key_list(%s)' % table_name)

        #for r in result.fetchall():
        #    ret.append( ForeignKey(r[1], r[3], r[2]) )

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

class FirebirdFieldParser(object):
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
        elif fcls == Text:
            if hasattr(self.field, 'segment_size'):
                segment_size = self.field.segment_size
            else:
                segment_size = 4096
            
            ret += " BLOB SUB_TYPE 2 SEGMENT SIZE %d " % segment_size
        elif fcls == Blob:
            if hasattr(self.field, 'segment_size'):
                segment_size = self.field.segment_size
            else:
                segment_size = 4096
            
            ret += " BLOB SUB_TYPE 1 SEGMENT SIZE %d " % segment_size
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

class FirebirdDriver(GenericDriver):
    class Inspector(FirebirdInspector): pass
    class FieldParser(FirebirdFieldParser): pass

    def __init__(self, connection=None):
        super(FirebirdDriver, self).__init__(connection)

    def execute_command(self, command):
        """
        This method haves a dependency of KInterbasDB extension package, available at:
        http://kinterbasdb.sourceforge.net/
        """
        super(FirebirdDriver, self).execute_command(command)

        if self.connection:
            cur = self.connection.cursor()
            result = cur.execute(command)

            # Verify this ****
            self.connection.commit()

            return result
        else:
            return command

